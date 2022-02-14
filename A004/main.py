from sqlalchemy import create_engine

engine = create_engine(
    'postgresql+psycopg2://root:root@localhost/db_test'
)