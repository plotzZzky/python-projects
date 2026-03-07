from pathlib import Path
from shutil import copyfile


class ForgeBase:
    ex_path: str = "FastapiForge/examples"
    project_name: str = ""
    project_path: str = ""

    def create_project_folder(self):
        # Cria a pasta do projeto
        path: Path = Path(self.project_path)
        path.mkdir(parents=True, exist_ok=True)
        self.create_readme_file()

    def create_readme_file(self):
        # Cria o readme do projeto
        content: str = f"# {self.project_name}"
        self.generic_create_file(f"{self.project_path}/readme.md", content)

    @staticmethod
    def generic_create_file(file_path: str, content: str):
        """
            Funçao generica para criar novos arquivos

            parameters:
                file_path (str) : caminho final do arquivo
                content (str) : conteudo do arquivo
        """
        path: Path = Path(file_path)
        path.touch(exist_ok=True)

        if content:
            path.write_text(content)

    def generic_copy_file(self, filename: str, new_path: str):
        """
            Copia um arquivo da pasta examples para a pasta final

            parameters:
                filename (str) : nome do arquivo a ser copiado
                new_path (str) : local para salvar o novo arquivo
        """
        try:
            file_path: Path = Path(f"{self.ex_path}/{filename}")

            if file_path.exists():
                new_path: Path = Path(f"{new_path}/{filename}")
                copyfile(file_path, new_path)

            else:
                raise FileNotFoundError

        except FileNotFoundError:
            print(f"{filename} nao existe!")
