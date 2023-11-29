import requests
import pandas as pd


def get_species_image(genus, species, image_number):
    """
    Retrieves the image URL for a given species.

    Args:
        genus (str): The genus of the species.
        species (str): The species name.
        image_number (int): The number of the image to retrieve. The first image is 0, the second is 1, etc.

    Returns:
        str: The URL of the species image, or a default image URL if no image is found.
    """
    base_url = "https://api.inaturalist.org/v1/taxa/autocomplete"
    params = {
        "q": f"{genus} {species}",
        "limit": 1,  # Limit to the first result
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["results"] and data["results"][0]["id"]:
            taxon_id = data["results"][0]["id"]
            photo_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}?locale=en"
            photo_response = requests.get(photo_url)
            if photo_response.status_code == 200:
                photo_data = photo_response.json()
                if (
                    photo_data["results"]
                    and photo_data["results"][0]["taxon_photos"]
                    and len(photo_data["results"][0]["taxon_photos"]) > 1
                ):
                    if (
                        "large_url"
                        in photo_data["results"][0]["taxon_photos"][1]["photo"]
                    ):
                        image_url = photo_data["results"][0]["taxon_photos"][
                            image_number
                        ]["photo"]["large_url"]
                        return image_url

    return "https://i.ibb.co/m6YDp69/sorry.jpg"


def get_airtable_data():
    return {
        "api_key": "<api_key>",
        "base_id": "<base_id",
        "data_table_name": "<data_table_name>",
        "observation_table_name": "<observation_table_name>",
    }


def get_headers(api_key):
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def get_url(base_id, table_name):
    return f"https://airtable.com/v0/{base_id}/{table_name}"
