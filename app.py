from typing import List
import pandas as pd
from app_files.image_upload import upload_image_to_imgur
from app_files.airtable_utils import (
    get_species_image,
    get_airtable_data,
    get_url,
    get_headers,
)
from app_files.navbar_utils import (
    record_observation,
    verify_observation,
    dichotomous_key,
    release_notes,
)
import requests
from shiny import App, Inputs, Outputs, Session, reactive, render, ui, req
from shiny.types import ImgData

from shiny.types import NavSetArg


# read data from csv file
df = pd.read_csv("data.csv", keep_default_na=False)


def nav_controls() -> List[NavSetArg]:
    return [
        record_observation(),
        verify_observation(),
        dichotomous_key(),
        release_notes(),
    ]


app_ui = ui.page_navbar(
    title="SFBBO Arthropod Survey",
    *nav_controls(),
    id="navbar_id",
)


def server(input, output, session):
    """
    This function is the main server function that handles the logic of the invertebrate survey app. It takes three arguments:

    The function creates a new dataframe and sets it as a reactive value.
    It then defines several reactive effects that update the UI based on user input.
    The function also defines several reactive events that handle user actions such as submitting and syncing data.
    Finally, the function defines an output that displays the observations data frame in a data grid.

    """
    new_df = pd.DataFrame(
        [],
        columns=[
            "Date observed",
            "Location",
            "Plot",
            "Surveyors",
            "Survey Point",
            "Side",
            "Class",
            "Order",
            "Family",
            "Common Name",
            "Genus",
            "Species",
            "Count",
            "Notes",
        ],
    )
    val = reactive.Value(new_df)

    notes_val = reactive.Value(None)

    @reactive.Effect
    def _show():
        """
        This function displays information and images related to a selected arthropod specimen.

        It retrieves the input specimen, finds the corresponding image URL, ID notes, genus, and species from a dataframe.
        If the image URL is not available or the genus and species are unknown, a default image URL is used.
        The function then creates a UI card with the specimen name, image, ID notes, and an additional image (if available).
        The card is stored in the 'notes_val' variable.

        Returns:
            None
        """
        notes_val.set(None)
        req(input.specimen())
        x = str(input.specimen())
        id_notes = df.loc[df["Common Name"] == x, "ID notes"].values[0]
        genus = df.loc[df["Common Name"] == x, "Genus"].values[0]
        species = df.loc[df["Common Name"] == x, "Species"].values[0]
        image_url = get_species_image(genus, species, 0)
        if genus != "Unknown" and species != "Unknown":
            image_url_2 = get_species_image(genus, species, 1)
        else:
            image_url, image_url_2 = "https://i.ibb.co/m6YDp69/sorry.jpg"
        m = ui.card(
            ui.h3(f"{x} ID notes"),
            ui.tags.img(src=image_url, height="100%", width="100%"),
            id_notes,
            ui.tags.img(src=image_url_2, height="100%", width="100%"),
        )
        notes_val.set(m)

    @render.ui
    def notes():
        return notes_val.get()

    @reactive.Effect
    def _specimen():
        ui.update_selectize(
            "specimen",
            label="Specimen",
            choices=list(df["Common Name"].sort_values(ascending=True)),
            selected="None",
        )

    @reactive.Effect
    @reactive.event(input.reset)
    def _reset():
        df = val.get()
        if not df.empty:
            index_to_delete = list(input.observations_data_frame_selected_rows())
            if index_to_delete and index_to_delete[0] in df.index:
                df.drop(index_to_delete[0], inplace=True)
                df = pd.DataFrame(df)
                # Reindex the DataFrame
                df.reset_index(drop=True, inplace=True)
                val.set(df)
                m = ui.modal(
                    "Your observation have been cleared",
                    easy_close=True,
                    footer=None,
                )
                ui.modal_show(m)

    @reactive.Effect
    @reactive.event(input.sync)
    def _sync():
        api_key = get_airtable_data()["api_key"]
        base_id = get_airtable_data()["base_id"]
        observation_table_name = get_airtable_data()["observation_table_name"]
        url = get_url(base_id, observation_table_name)
        df = val.get()
        if not df.empty:
            data = df.to_dict("records")
            for record in data:
                response = requests.post(
                    url, json={"fields": record}, headers=get_headers(api_key)
                )
                if response.status_code == 200:
                    print("Data successfully submitted to Airtable")
                else:
                    print(response.text)
            df = val.get()
            # Clear the DataFrame by creating a new empty one
            df = pd.DataFrame(columns=df.columns)
            val.set(df)
            ui.update_selectize(
                "survey_side",
                label="Select the side",
                choices=["Slough side", "Pond side"],
            )
            m = ui.modal(
                "Your observations have been synced",
                easy_close=True,
                footer=None,
            )
            ui.modal_show(m)

    @reactive.Effect
    @reactive.event(input.submit)
    def _submit():
        """
        This function is triggered when the submit button is clicked.
        It handles the submission of the arthropod survey form and records the observation.
        """
        req(input.surveyors())
        if input.file1() and input.file1() is not None:
            path = input.file1()[0]["datapath"]
            url = upload_image_to_imgur(path)
            input.file1().clear()
            m = ui.modal(
                "This is your uploaded image",
                ui.br(),
                ui.br(),
                ui.tags.img(src=url, height="100%", width="100%"),
                easy_close=True,
                footer=None,
            )
            ui.modal_show(m)
            ui.remove_ui(selector="div:has(> #file1-label)")
            ui.insert_ui(
                ui.input_file(
                    "file1",
                    "Upload Image File (optional)",
                    accept=[".jpg", ".png", ".jpeg"],
                    multiple=False,
                ),
                selector="#submit",
                where="beforeBegin",
            )
        else:
            url = ""
        data = {
            "fields": {
                "Date observed": str(input.survey_date()),
                "Location": str(input.location()),
                "Plot": str(input.plot()),
                "Survey Point": str(input.survey_point()),
                "Side": str(input.survey_side()),
                "Class": df.loc[
                    df["Common Name"] == str(input.specimen()), "Order"
                ].values[0],
                "Order": df.loc[
                    df["Common Name"] == str(input.specimen()), "Order"
                ].values[0],
                "Family": df.loc[
                    df["Common Name"] == str(input.specimen()), "Family"
                ].values[0],
                "Common Name": str(input.specimen()),
                "Genus": df.loc[
                    df["Common Name"] == str(input.specimen()), "Genus"
                ].values[0],
                "Species": df.loc[
                    df["Common Name"] == str(input.specimen()), "Species"
                ].values[0],
                "Count": int(input.count()),
                "Notes": str(input.notes()),
                "Surveyors": str(", ".join(input.surveyors())),
                "Url": url,
                "Image attachment": [{"url": url}],
            }
        }

        newValue = val.get()
        newValue = newValue._append(data["fields"], ignore_index=True)
        val.set(newValue)
        ui.notification_show("Your observation has been recorded.", duration=2)
        ui.update_selectize(
            "specimen",
            label="Specimen",
            choices=list(df["Common Name"].sort_values(ascending=True)),
            selected="None",
        )
        ui.update_slider("count", label="Count observed", min=1, max=100, value=1)
        ui.update_text("notes", label="Notes", value="")

    @output
    @render.data_frame
    def observations_data_frame():
        return render.DataGrid(
            val.get()[
                [
                    "Date observed",
                    "Plot",
                    "Survey Point",
                    "Side",
                    "Common Name",
                    "Count",
                    "Notes",
                ]
            ],
            row_selection_mode="single",
        )


app = App(app_ui, server)
()
