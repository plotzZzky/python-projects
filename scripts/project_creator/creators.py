from pathlib import Path
import os


class CreatorBase:
    """ Classe base do criador dos projetos com as funções genericas """
    project_name: str = ""

    # Generics functions
    @staticmethod
    def get_project_name() -> str:
        option: str = input("Digite o nome do projeto: \n")
        return option

    def create_project_folder(self) -> bool:
        folder: bool = Path(self.project_name).exists()
        if not folder:
            Path(self.project_name).mkdir()
            return True
        else:
            return False

    def create_readme(self):
        file_path: str = f"{self.project_name}/readme.md"
        content: str = f"### {self.project_name}"

        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def get_requirements():
        options: str = input("Digite os requirements do projeto separados apenas com espaços: \n")
        return options

    def create_generic_contents(self):
        self.project_name: str = self.get_project_name()
        self.create_project_folder()
        self.create_readme()

    def create_main_file(self, filename: str, content: str):
        file_path: str = f"{self.project_name}/{filename}"
        with open(file_path, 'w') as file:
            file.write(content)


class PythonCreator(CreatorBase):
    """ Classe para criar a estrutura do projeto python"""
    def create_python_project(self):
        self.create_generic_contents()
        self.create_main_file("main.py", "# New main file")
        self.create_python_requirements()
        self.create_venv()

    def create_python_requirements(self):
        options: str = self.get_requirements()
        file_path: str = f"{self.project_name}/requirements.txt"

        with open(file_path, 'w') as file:
            for item in options.split(" "):
                file.write(item)

    def create_venv(self):
        if os.name == 'nt':
            cmd = "venv/Scripts/activate.bat"
        else:
            cmd = "source venv/bin/activate"

        os.system(f"cd {self.project_name}; python -m venv venv; {cmd}; pip install -r requirements.txt")


class JsCreator(CreatorBase):
    """ Classe para criar a estrutura do projeto js """
    def create_js_project(self):
        self.create_generic_contents()
        self.create_main_file("main.js", "// New main file")
        self.create_npm_folder()
        self.install_js_requirements()

    def create_npm_folder(self):
        os.system(f"cd {self.project_name}; npm init")

    def install_js_requirements(self):
        options: str = self.get_requirements()

        for item in options.split(" "):
            os.system(f"cd {self.project_name}; npm install {item}")
