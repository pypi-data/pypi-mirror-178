import requests
import logging
import json

logger = logging.getLogger(__name__)

headers = {"content-type": "application/json"}


class BindService:
    @staticmethod
    def login(username: str, password: str, bind_endpoint: str) -> str:
        logger.info(f"username: {username} | password:{password}")

        url = f"{bind_endpoint}/login/jwt"

        payload = json.dumps({"username": f"{username}", "password": f"{password}"})

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

    @staticmethod
    def bancked_cuit(
        cuit: str,
        bind_credential: str,
        bind_endpoint: str,
        obp_document_type: str = "cuit",
    ) -> dict:
        url = f"{bind_endpoint}/persons/{cuit}/banks"
        headers["Authorization"] = f"JWT :{bind_credential}"
        headers["obp_document_type"] = obp_document_type

        response = requests.request("GET", url, headers=headers)

        return response.json()
