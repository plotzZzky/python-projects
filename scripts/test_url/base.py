from urllib3 import request
import os


class TestUrl:
    """
        Ferramenta para fazer solicitações http (GET, POST, DELETE, PUT e PATCH) para url espeficas
        Possui muitas funções builtin que facilitam o processo
    """
    URL: str = ""

    # Full functions
    def get_and_get_list_request_url(self, url: str = None, object_id: int = 1):
        """
            Faz uma solicitação GET and GET list

            Args:
                url (str) - Url para fazer as solicitações
                object_id (int) - Id do objeto solicitado
        """
        self.get_list_request_url(url)
        self.get_request_url(f"{url}/{object_id}")

    # Simple functions
    def get_list_request_url(self, url: str = None):
        """
            Faz a solicitação Get para receber uma lista de objetos /get

            Args:
                url (str) - Url para fazer a soliciatção
        """
        self.generic_request("GET", url)

    def get_request_url(self, url: str | int = 1):
        """
            Faz a solicitação Get para receber um objeto /get/{id}

            Steps:
                - Recebe a url ou object_id
                - Se for o object_id cria a url (self.URL + object_id)
                - Faz a solicitação

            Args:
                url (str | int) - Url para fazer a soliciatção ou o object_id
        """
        try:
            # Verifica se foi passado o id ou a url
            object_id: int = int(url)
            url: str = f"{self.URL}/{object_id}"

        except TypeError:
            pass

        self.generic_request("GET", url)

    def post_request_url(self, data: dict, url: str = None):
        """
            Faz a solicitação POST para criar um objeto

            Args:
                data (dict) - As do objeto a ser criado
                url (str) - Url para fazer a soliciatação
        """
        self.generic_request("POST", url, data=data)

    def delete_request_url(self, url: str | int = 1):
        """
            Faz uma solicitação DELETE para remover um objeto

            - Recebe a url ou object_id
            - Se for o object_id cria a url (self.URL + object_id)
            - Faz a solicitação

            Args:
                url (str) - Url para fazer a soliciatção ou object_id
        """
        try:
            # Verifica se foi passado o id ou a url
            object_id: int = int(url)
            url: str = f"{self.URL}/{object_id}"

        except TypeError:
            pass

        self.generic_request("DELETE", url)

    def patch_or_put_request_url(self, method: str, data: dict, url: str | int = 1):
        """
            Faz uma solicitação PUT para atualizar um objeto

            - Recebe a url ou object_id
            - Se for o object_id cria a url (self.URL + object_id)
            - Faz a solicitação

            Args:
                method (str) - Metodo http usado na solicitação
                data (dict) - As iformações a serem atualizadas
                url (str) - Url para fazer a solicitação ou o object_id
        """
        try:
            # Verifica se foi passado o id ou a url
            object_id: int = int(url)
            url: str = f"{self.URL}/{object_id}"

        except TypeError:
            pass

        self.generic_request(method, url, data)


    # Base functions
    def generic_request(self, method: str, url: str, data: dict = None):
        """
            Funçao generica para as solicitações

            Args:
                method (str) - Metodo http para a solicitação
                url (str) - Url para fazer a soliciatção
                data (dict) - Formulario para as solicitações que precisam (POST, PUT, PATCH)

            Steps:
                - Se nao receber uma url, usa o self.URL
                - faz a solicitação com os dados passados pelo usuario

            Return:
                response - a resposta da solicitação
        """
        if not url:
            url = self.URL

        response = request(method, url, fields=data)
        self.show_result(response, method, url)

    def show_result(self, result, method, url):
        """
            Exibe os resultados
        """
        size: int = self.receive_terminal_width()
        print(f"{'_' * size}")
        print(f"--> {method} in {url} - status {result.status}\n")
        print(f"Response --> {result.data}")
        print(f"{'_' * size}")

    @staticmethod
    def receive_terminal_width() -> int:
        """
            Calcula a largura do terminal e a retorna
        """
        size = os.get_terminal_size()
        width: int = size.columns - 2
        return width
