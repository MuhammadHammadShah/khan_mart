from sqlmodel import  create_engine 
from khan_mart.core.settings import settings

# from sqlalchemy import Engine

# connection_STr=settings.DATABASE_URL.replace(
#     "postgresql", "postgresql+psycopg"
# )

# print("STR  CONNECITONBDNBJNG",connection_STr)

# engine = create_engine(
#     connection_STr,connect_args={} ,pool_recycle=300
# )



connectionSTR=settings.DATABASE_URL
print(connectionSTR)

engine = create_engine(connectionSTR,echo=True , pool_recycle=300)

# def createTable(engine:)