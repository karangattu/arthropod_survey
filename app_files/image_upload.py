import requests


def upload_image_to_imgur(image_path):
    client_id = "<insert_your_client_id_here>"
    # Set Imgur API endpoint
    api_url = "https://api.imgur.com/3/upload"

    # Set headers with client ID
    headers = {
        "Authorization": f"Client-ID {client_id}",
    }

    # Open and read the image file
    with open(image_path, "rb") as file:
        # Prepare the payload
        files = {"image": file}
        data = {"type": "file"}

        # Make the API request
        response = requests.post(api_url, headers=headers, files=files, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["data"]["link"]
