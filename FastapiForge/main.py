from BoilerPlate.boilerplate import CliBoilerplate
from FastapiForge.forges.forgeback import ForgeBack
from FastapiForge.forges.forgefront import ForgeFront
from pathlib import Path


class FastapiForge(CliBoilerplate):
    project_name: str = ""
    CLI_DESC: str = "Ferramenta para criar a estrutura de um projeto fastapi"
    CLI_NAME_SPACE: int = 6

    HOME_PATH: Path = Path.home()
    APP_PATH: Path = Path(f"{HOME_PATH}/Dev/Next") # ALTERAR ESSE PATH!!!!

    def __init__(self):
        super().__init__()
        self.back = ForgeBack(self.project_name, self.APP_PATH)
        self.front = ForgeFront(self.project_name, self.APP_PATH)

        self.menu_options = [
            self.create_api_only,
            self.create_app,
            self.create_front_only,
        ]

    def create_api_only(self):
        print("\nCriando uma api sem front\n")
        self.get_project_name()
        self.back = ForgeBack(self.project_name, self.APP_PATH)

        self.back.create_project_folder() # Cria a pasta do projeto
        self.back.create_back_folders()  # Cria o back

    def create_app(self):
        print("\nCriando um app (back + front)\n")
        self.get_project_name()
        self.back = ForgeBack(self.project_name, self.APP_PATH)

        self.back.create_project_folder() # Cria a pasta do projeto
        self.back.create_back_folders()  # Cria o back

        self.front = ForgeFront(self.project_name, self.APP_PATH)
        self.front.create_js_project()  # Cria o front

    def create_front_only(self):
        # cria apenas o front
        print("\nCriando apenas o front\n")
        self.get_project_name()
        self.front = ForgeFront(self.project_name, self.APP_PATH)

        self.front.create_project_folder()
        self.front.create_js_project()

    def get_project_name(self):
        # Recebe o nome do projeto
        try:
            self.project_name: str = input("Digite um nome para a o app:\n")

        except KeyboardInterrupt:
            print("Bye...")


fastapi_forge = FastapiForge()

if __name__ == "__main__":
    fastapi_forge.main_loop()