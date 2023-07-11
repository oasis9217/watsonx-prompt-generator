import streamlit as st
from ibm_cloud_sdk_core import IAMTokenManager


def get_access_token():
    return IAMTokenManager(
        apikey=st.secrets["IBM_CLOUD_API_KEY"],
        url="https://iam.cloud.ibm.com/identity/token"
    ).get_token()

