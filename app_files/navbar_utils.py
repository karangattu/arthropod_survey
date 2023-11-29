from shiny import App, Inputs, Outputs, Session, reactive, render, ui, req


def record_observation():
    return ui.nav(
        "Record observation",
        ui.layout_column_wrap(
            ui.card(
                ui.input_date("survey_date", label="Survey Date"),
                ui.input_selectize(
                    "location",
                    label="Select the location",
                    choices=["Eden Landing", "Bair Island", "Alviso Marina"],
                ),
                ui.input_checkbox_group(
                    "surveyors",
                    "Choose Surveyor(s)*:",
                    {
                        "Cole": "Cole",
                        "Eric": "Eric",
                        "Hop": "Hop",
                        "Kaili": "Kaili",
                        "Karan": "Karan",
                        "Sirena": "Sirena",
                    },
                ),
                ui.input_selectize(
                    "plot",
                    label="Select the plot",
                    choices=["P1", "P2", "P3", "P4"],
                ),
                ui.input_selectize(
                    "survey_point",
                    label="Select the survey point",
                    choices=["PTF1", "PTF2", "PTF3", "PTF4"],
                ),
                ui.input_selectize(
                    "survey_side",
                    label="Select the side",
                    choices=["Slough side", "Pond side"],
                ),
                ui.input_selectize("specimen", label="Specimen", choices={}),
                ui.input_slider(
                    "count", label="Count observed", min=1, max=100, value=1
                ),
                ui.input_text("notes", label="Notes"),
                ui.input_file(
                    "file1",
                    "Upload Image File (optional)",
                    accept=[".jpg", ".png", ".jpeg"],
                    multiple=False,
                ),
                ui.input_action_button(
                    "submit", "Record observation", class_="btn btn-outline-success"
                ),
                fill=False,
            ),
            ui.output_ui("notes"),
            width=1 / 2,
        ),
    )


def verify_observation():
    return ui.nav(
        "Verify observation",
        ui.output_data_frame("observations_data_frame"),
        ui.page_fluid(
            ui.input_action_button(
                "reset", "Clear selected observation", class_="btn btn-outline-info"
            ),
            ui.br(),
            ui.br(),
            ui.input_action_button(
                "sync", "Sync all observations", class_="btn btn-outline-danger"
            ),
        ),
    )


def dichotomous_key():
    return ui.nav(
        "Dichotomous Key for Arthropods (WIP)",
        ui.layout_column_wrap(
            ui.card(
                ui.input_radio_buttons(
                    "legs",
                    "Choose number of legs in specimen",
                    ["8 legs", "6 legs", "More than 8 legs"],
                    selected=None,
                ),
                ui.panel_conditional(
                    "input.legs === 'More than 8 legs'",
                    ui.input_radio_buttons(
                        "is_isopod",
                        "Does it have seven pairs of tiny legs?",
                        ["Yes", "No"],
                    ),
                    ui.panel_conditional(
                        "input.legs === 'More than 8 legs' && input.is_isopod === 'Yes'",
                        ui.code("It is an isopod"),
                        ui.br(),
                        ui.br(),
                        ui.tags.img(
                            src="https://upload.wikimedia.org/wikipedia/commons/7/7f/Oniscus_asellus_-_male_side_2_%28aka%29.jpg",
                            width="100%",
                            height="100%",
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === 'More than 8 legs' && input.is_isopod === 'No'",
                        ui.input_radio_buttons(
                            "pair_of_legs",
                            "How many pairs of legs does the specimen have in each body segment?",
                            ["1", "2"],
                        ),
                        ui.panel_conditional(
                            "input.legs === 'More than 8 legs' && input.pair_of_legs === '2'",
                            ui.code("It is a millipede"),
                            ui.br(),
                            ui.br(),
                            ui.tags.img(
                                src="https://upload.wikimedia.org/wikipedia/commons/b/bb/Millipede_collage.jpg",
                                width="100%",
                                height="100%",
                            ),
                        ),
                        ui.panel_conditional(
                            "input.legs === 'More than 8 legs' && input.pair_of_legs === '1'",
                            ui.code("It is a centipede"),
                            ui.br(),
                            ui.br(),
                            ui.tags.img(
                                src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Chilopoda_collage.png",
                                width="100%",
                                height="100%",
                            ),
                        ),
                    ),
                ),
                ui.panel_conditional(
                    "input.legs === '6 legs'",
                    ui.code("It is an insect"),
                    ui.br(),
                    ui.br(),
                    ui.tags.img(
                        src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Insecta_Diversity.jpg",
                        width="100%",
                        height="100%",
                    ),
                ),
                ui.panel_conditional(
                    "input.legs === '8 legs'",
                    ui.input_radio_buttons(
                        "distinct",
                        "Is the body separated into a cephalothorax and abdomen?",
                        ["Yes", "No"],
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'Yes'",
                        ui.code("It is a spider"),
                        ui.br(),
                        ui.br(),
                        ui.tags.img(
                            src="https://upload.wikimedia.org/wikipedia/commons/f/f9/Spiders_Diversity.jpg",
                            width="100%",
                            height="100%",
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'No'",
                        ui.input_radio_buttons(
                            "body_shape",
                            "Does it have stilt-like legs?",
                            ["Yes", "No"],
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'No' && input.body_shape === 'Yes'",
                        ui.code("It is a harvestman"),
                        ui.br(),
                        ui.br(),
                        ui.tags.img(
                            src="https://upload.wikimedia.org/wikipedia/commons/9/90/Opiliones_harvestman.jpg",
                            width="100%",
                            height="100%",
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'No' && input.body_shape === 'No'",
                        ui.input_radio_buttons(
                            "arachnid_size",
                            "Is it barely noticeable using the naked eye?",
                            ["Yes", "No"],
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'No' && input.body_shape === 'No' && input.arachnid_size === 'Yes'",
                        ui.code("It is a mite"),
                        ui.br(),
                        ui.br(),
                        ui.tags.img(
                            src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Trombidium_holosericeum_%28aka%29.jpg",
                            width="100%",
                            height="100%",
                        ),
                    ),
                    ui.panel_conditional(
                        "input.legs === '8 legs' && input.distinct === 'No' && input.body_shape === 'No' && input.arachnid_size === 'No'",
                        ui.code("It is a tick"),
                        ui.br(),
                        ui.br(),
                        ui.tags.img(
                            src="https://upload.wikimedia.org/wikipedia/commons/3/34/Adult_deer_tick.jpg",
                            width="100%",
                            height="100%",
                        ),
                    ),
                ),
            ),
            ui.output_ui("possible_candidates"),
        ),
    )


def release_notes():
    return ui.nav(
        "What's new",
        ui.layout_column_wrap(
            ui.card(
                ui.markdown(
                    """
        # Release notes
        1. Added **database link** in the verify & sync observations tab _(Nov 27, 2023)_
        1. Show user a preview of uploaded image and add **location** dropdown. _(Nov 24, 2023)_
        1. Allow users to **upload images** of unknown specimens _(Nov 23, 2023)_
        1. Use specimen name field only with search functionality. Plus specimen resets after each submission. 
        **Date** field now shown in **Verify observation** tab _(Nov 22, 2023)_
        1. Survey side should reset after syncing data _(Nov 20, 2023)_

        """
                ),
            ),
            width=1 / 2,
        ),
    )
