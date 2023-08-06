import time

from _responses import make_response
from ._sessions import Session


class Drive:
    def __init__(
            self,
            token: str,
            collection: str,
            region: str,
            base_url: str = "https://connect.huddu.io",
    ):
        self.session = Session(collection, token, region, base_url)
        self.session.set_type("drive")

    def upload(self, name: str, data: str = None, path: str = None):
        n = int(1e7)  # 10 MB in bytes

        if path:
            f = open(path, "r")
            data = f.read()

        chunks = [data[i: i + n] for i in range(0, len(data), n)]

        documents = []
        for i in chunks:
            documents.append({"id": f"{chunks.index(i) + 1}_{name}", "data": str(i)})

        for i in documents:
            self.session.create_documents([i])
            time.sleep(1)

    def get(self, name: str):
        run = 1
        while True:
            try:
                document = self.session.list_documents([f"{run}_{name}"])
                yield make_response([document["data"][0]])[0]
                run += 1
            except:
                break

    def delete(self, name: str):
        run = 1
        while True:
            try:
                self.session.delete_documents([f"{run}_{name}"])
                run += 1
            except:
                break
