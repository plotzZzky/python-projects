from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = "sqlite:///os.getenv("DB_URL")"

# Criando o engine para conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Função para criar a sessão com o banco de dados
def get_session():
    with Session(engine) as session:
        yield session

# Função para criar as tabelas no banco de dados
def create_db():
    SQLModel.metadata.create_all(bind=engine)
