from pathlib import Path
import pandas as pd
import yt_dlp
import art


class YtMusicDownloader:
    """
        Script para baixar musicas em mp3 do youtube music.

        Steps:
        - Crie uma tabela csv com o nome da musica (Title) e banda (Artists) ou export de seu player de musica favorito
        - O arquivo musicas.csv deve estar na raiz do projeto
        - O script baixa e salva as músicas na past musicas/
    """
    app_desc: str = 'Script para baixar musicas em mp3 do youtube music.'

    musics_table_path: Path = Path('musicas.csv')
    folder_path: Path = Path('musicas')
    records: list = []

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'outtmpl': 'Musics/%(title)s.%(ext)s',
    }

    def welcome(self):
        art.tprint(self.__class__.__name__)
        print(self.app_desc)

        self.check_if_folder_exists()

    def check_if_folder_exists(self):
        folder_opath: Path = Path(self.folder_path)

        if not folder_opath.exists(): # Se a pasta para download não existir cria ela
            folder_opath.mkdir()

        self.open_musics_table()

    def open_musics_table(self):
        try:
            df = pd.read_csv(self.musics_table_path)
            self.records = df.to_dict(orient='records') # Converte cada linha em um dict

            self.select_any_music_from_list()

        except FileNotFoundError:
            print("Lista de músicas não encontrada!")

    def select_any_music_from_list(self):
        for record in self.records:
            self.create_query_to_download(record)

    def create_query_to_download(self, record):
        band: str = record['Artists']
        music_name: str = record['Title']
        filename: str = f"{band} - {music_name}"

        self.download_mp3_from_yt(filename)

    def download_mp3_from_yt(self, filename):
        self.ydl_opts['outtmpl'] = f'Musics/{filename}.%(ext)s' # Nome para salvar
        query: str = f"ytsearch1:{filename}" # Query para buscar no youtube e retorna o primeiro resultado

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([query])


app = YtMusicDownloader()

if __name__ == '__main__':
    app.welcome()
