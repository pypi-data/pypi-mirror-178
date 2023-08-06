import json

import requests

from ._exceptions import APIException


class Session:
    def __init__(
            self,
            collection: str,
            token: str,
            region: str,
            base_url: str = "https://connect.huddu.io",
    ):
        self.collection = collection
        self.token = token
        self.region = region
        self.base_url = base_url

    def _request(self, method, params: dict = None, data: dict = None):
        headers = {
            "Authorization": f"Token {self.token}",
            "Collection": self.collection,
            "Region": self.region,
        }

        if data:
            res = requests.request(
                method,
                f"{self.base_url}/documents",
                data=json.dumps(data),
                headers=headers,
            )
        else:
            res = requests.request(
                method, f"{self.base_url}/documents", params=params, headers=headers
            )

        if res.status_code > 299 or res.json().get("error"):
            raise APIException(res.json())
        return res.json()

    def create_documents(self, items: list):
        for i in items:

            if type(i["data"]) == dict or type(i["data"]) == list:
                i["data"] = json.dumps(i["data"])
            else:
                i["data"] = str(i["data"])

        return self._request("POST", data={"items": items})

    def list_documents(
            self,
            ids: list = None,
            limit: int = 25,
            skip: int = 0,
            start: int = 0,
            end: int = 0,
    ):
        params = {}

        if ids:
            params["ids"] = ",".join(ids)
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
        if skip:
            params["skip"] = skip

        return self._request("GET", params=params)

    def delete_documents(self, ids: list):
        return self._request("DELETE", data={"ids": ids})

    def set_type(self, type):
        type_document = None
        try:
            type_document = self.list_documents(["_type"])["data"][0]
        except:
            self.create_documents(
                [{
                    "id": "_type",
                    "data": type
                }]
            )
        if type_document:
            if not type_document["data"] == type:
                raise APIException("Collection is already used for " + type_document["data"])
