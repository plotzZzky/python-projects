from urllib3 import request
from pathlib import Path
import json


class WebdroidBuild:
    """
        Script usado para gerar um json simplificado do fdroid para o webdroid em pt-br

        Steps:
            - Busca na web o index.json do webdroid
            - Pega apenas os campos necessários (preferêncialmente em pt-br)
            - Salva os campos escolidos em um novo json muito mais leve

    """
    API_URL = "https://f-droid.org/repo/index-v2.json"
    fdroid_json = "fdroid.json"
    result_json = "result.json"
    result_json_path = f"{result_json}"

    apps_json = []

    def __init__(self):
        self.check_if_fdroid_json_exists()

    def check_if_fdroid_json_exists(self):
        json_path = Path(self.fdroid_json)

        if json_path.exists():
            self.open_json_file(json_path)

        else:
            self.get_json_from_web()

    def get_json_from_web(self):
        result = request(url=self.API_URL, method="GET")

        with open(self.fdroid_json, "w") as file:
            json.dump(result.json(), file, indent=4)

    def open_json_file(self, json_path: Path):
        if json_path:
            with json_path.open() as file:
                json_file = json.loads(file.read())

                for item in json_file["packages"]:
                    item_json = json_file['packages'][item]
                    self.create_data_for_app(item_json)

                self.save_result_json()

    def save_result_json(self):
        with open(self.result_json_path, "w") as file:
            file.write(json.dumps(self.apps_json, indent=4))

    def create_data_for_app(self, item_json: dict):
        metadata = item_json["metadata"]

        name = self.return_app_data(metadata, "name")
        description = self.return_app_data(metadata, "description")
        categories = self.return_app_data(metadata, "categories")
        app_license = self.return_app_data(metadata, "license")
        source_code = self.return_app_data(metadata, "source_code")
        website = self.return_app_data(metadata, "website")
        icon = self.return_app_icon(metadata)
        apk, apk_hash, version_number = self.return_apk_name_and_version(item_json)

        self.apps_json.append(
            {
                "name": name,
                "description": description,
                "categories": categories,
                "icon": (icon if icon else None),
                "license": app_license,
                "source_code": source_code,
                "website": website,
                "version": version_number,
                "apk": apk,
                "hash": apk_hash,
            }
        )

    def return_app_icon(self, metadata: dict):
        """ Retorna o icone se existir, se não, retorna nulo """
        try:
            icon = self.return_app_data(metadata["icon"]["en-US"], "name")
            return icon

        except KeyError:
            return ""

    def return_apk_name_and_version(self, item_json: dict):
        """ Retorna o path do apk e versão do app """
        versions = item_json["versions"] # Lista com todas as versões
        first_key = list(versions.keys())[0]
        latest_version = versions[first_key]

        apk = self.return_app_data(latest_version["file"], "name")
        apk_hash = self.return_app_data(latest_version["file"], "sha256")
        version_number = self.return_app_data(latest_version["manifest"],"versionName")
        return apk, apk_hash, version_number

    @staticmethod
    def return_app_data(app_dict, key_name):
        try:
            data = (
                app_dict.get(key_name, {}).get("pt-BR")
                or app_dict.get(key_name, {}).get("en-US")
                or ""
            )
            return data

        except AttributeError:
            return app_dict[key_name]


if __name__ == "__main__":
    WebdroidBuild()
