# Arthropod Survey Shiny App

The shiny app allows users to look up identification information for arthropods, and enter survey data for [SFBBO](https://www.sfbbo.org/). The app is designed to be used on a tablet/smartphone in the field, but can also be used on a desktop computer.
There is a tab that allows for user to use the dichotomous key to find different kinds of arthropods. In addition, it allows users to upload unknown specimens to an image hosting site like `imgur` and use `Airtable` for syncing over the observations.

### Installation

User needs to install all python packages the code uses by running
```bash
pip install -r requirements.txt
```

### Image uploading to Imgur
The app uses Imgur to host images. To use this feature, you will need to register for an Imgur account and register an application.
Once you have an account, you can register an application at https://api.imgur.com/oauth2/addclient
You will select the option without a callback url and then you will need to copy the client ID and replace it in the app_files/image_upload.py file

```python
def upload_image_to_imgur(image_path):
    client_id = "<insert_your_client_id_here>"
    # Set Imgur API endpoint
    api_url = "https://api.imgur.com/3/upload"
```
to 
```python
def upload_image_to_imgur(image_path):
    client_id = "1d0995815dbb"
    # Set Imgur API endpoint
    api_url = "https://api.imgur.com/3/upload"

```


### Using Airtable for uploading survey data
1. Create a free Airtable account by navigating to this [link](https://airtable.com/signup)
2. A free account provides the following benefits
```
- Unlimited bases
- 1,000 records per base
- 1 GB of attachments per base
- 100 automation runs per month
- 1000 API calls per workspace per month
- the Web API has a rate limit of 5 requests per second, per base
```
3. Once the account is created, create a Personal access token by following [these instructions](https://airtable.com/developers/web/guides/personal-access-tokens)
4. Replace the existing code with all the relevant information to make it work with your base in Airtable
```
def get_airtable_data():
    return {
        "api_key": "<api_key>",
        "base_id": "<base_id",
        "data_table_name": "<data_table_name>",
        "observation_table_name": "<observation_table_name>",
    }
```
