import requests
from ibm_cloud_sdk_core import IAMTokenManager


def get_access_token(api_key):
    return IAMTokenManager(
        apikey=api_key,
        url="https://iam.cloud.ibm.com/identity/token"
    ).get_token()


class Prompt:
    def __init__(self, access_token, project_id):
        self.access_token = access_token
        self.project_id = project_id

    def generate(self, prompt_input, model_id, parameters):
        wml_url = "https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-28"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "model_id": model_id,
            "input": prompt_input,
            "parameters": parameters,
            "project_id": self.project_id
        }
        response = requests.post(wml_url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["results"][0]
        else:
            return response.text
