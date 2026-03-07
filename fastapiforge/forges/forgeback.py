from FastapiForge.forges.forgebase import ForgeBase
from pathlib import Path
import subprocess


class ForgeBack(ForgeBase):
    """ Classe para criar o backend usando o fastapi"""

    def __init__(self, project_name: str, app_path: Path):
        super().__init__()
        self.project_name = project_name
        self.APP_PATH: Path = app_path

        self.back_path: str = ""
        self.src_path: str = ""
        self.routes_path: str = ""

        self.create_paths()

    def create_paths(self):
        """ Cria os paths mais usados pela aplicaçao """
        self.project_path: str = f"{self.APP_PATH}/{self.project_name}"
        self.back_path: str = f"{self.project_path}/back"
        self.src_path: str = f"{self.back_path}/src"
        self.routes_path: str = f"{self.src_path}/routes"

    def create_back_folders(self):
        # Cria a pasta do back
        path: Path = Path(self.routes_path)
        path.mkdir(parents=True, exist_ok=True)

        self.create_dotenv_file()

    def create_dotenv_file(self):
        # Cria o arquivo .env
        self.generic_create_file(f"{self.back_path}/.env", 'DB_URL=""')
        self.create_gitignore_file()

    def create_gitignore_file(self):
        # Cria o .gitignore
        self.generic_copy_file(".gitignore", self.back_path)
        self.create_requirements_file()

    def create_requirements_file(self):
        # Cria o requirements.txt
        self.generic_copy_file("requirements.txt", self.back_path)
        self.create_venv()

    def create_venv(self):
        # Executa o comando para criar o ambienre virtual e instala os requisitos do projeto
        cmds: str = (
            f"python -m venv {self.back_path}/.venv && "
            f"source {self.back_path}/.venv/bin/activate && "
            f"pip install -r {self.back_path}/requirements.txt"
        )
        try:
            subprocess.run(cmds, shell=True, check=True, stderr=True)
        except subprocess.CalledProcessError as e:
            print(e.cmd)

        self.create_fastapi_files()

    def create_fastapi_files(self):
        # Cria os arquivos do projeto
        self.generic_create_file(f"{self.src_path}/__init__.py", "pass")
        self.generic_create_file(f"{self.src_path}/models.py", "pass")
        self.generic_create_file(f"{self.src_path}/schemas.py", "pass")
        self.generic_copy_file("app.py", self.src_path)
        self.generic_copy_file("db.py", self.src_path)

        self.create_routers_files()

    def create_routers_files(self):
        # Cria os arquivos das rotas
        self.generic_create_file(f"{self.routes_path}/__init__.py", "")
        self.generic_create_file(f"{self.routes_path}/auth.py", "")
        self.generic_create_file(f"{self.routes_path}/routes.py", "")
