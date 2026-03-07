from FastapiForge.forges.forgebase import ForgeBase
from pathlib import Path
import subprocess
import shutil


class ForgeFront(ForgeBase):

    def __init__(self, project_name: str, app_path: Path):
        super().__init__()
        self.project_name = project_name
        self.APP_PATH: Path = app_path

        self.front_path: str = ""

        self.create_paths()

    def create_paths(self):
        self.project_path: Path = Path(f"{self.APP_PATH}/{self.project_name}")
        self.front_path: Path = Path(f"{self.project_path}/front")

    def create_js_project(self):
        cmds: str = (
            f"cd {self.project_path} && "
            "npx create-next-app@latest front --js --eslint --app --no-tailwind --yes"
        )
        try:
            subprocess.run(cmds, shell=True, check=True, stderr=True)
            self.create_home_folder_on_front()
        except subprocess.CalledProcessError as e:
            print(e.cmd)

    def create_home_folder_on_front(self):
        # Cria as pastas do back
        path: Path = Path(f"{self.front_path}/app/(home)")
        path.mkdir(parents=True, exist_ok=True)

        self.create_home_files()

    def create_home_files(self):
        path: str = f"{self.front_path}/app/(home)"
        self.generic_copy_file("page.jsx", path)
        self.generic_create_file(f"{path}/page.css", "")

        self.create_auth_folder_on_front()

    def create_auth_folder_on_front(self):
        path: Path = Path(f"{self.front_path}/app/(auth)")
        path.mkdir(parents=True, exist_ok=True)

        self.create_auth_files()

    def create_auth_files(self):
        path: str = f"{self.front_path}/app/(auth)"
        self.generic_copy_file("page.jsx", path)
        self.generic_create_file(f"{path}/page.css", "")

        self.create_comps_folder_on_front()

    def create_comps_folder_on_front(self):
        path: Path = Path(f"{self.front_path}/app/comps")
        path.mkdir(parents=True, exist_ok=True)

        self.create_dotenv_file()

    def create_dotenv_file(self):
        # Cria o arquivo .env
        self.generic_create_file(f"{self.front_path}/.env", "")
        self.remove_front_files()

    def remove_front_files(self):
        # Remove os arquivos desnecessarios do front
        files: list = [
            "app/page.js",
            "app/page.module.css",
            "app/favicon.ico",
            "README.md"
        ]

        for file in files:
            file = Path(f"{self.front_path}/{file}")
            if file.exists():
                file.unlink(missing_ok=True)

        self.delete_home_public_folder()

    def delete_home_public_folder(self):
        # Deleta a pasta public com seu conteudo
        path: Path = Path(f"{self.front_path}/public")
        if path.exists():
            shutil.rmtree(path)

        self.create_new_public_folder()

    def create_new_public_folder(self):
        # Cria uma nova pasta public
        path: Path = Path(f"{self.front_path}/public")
        path.mkdir(exist_ok=True)
