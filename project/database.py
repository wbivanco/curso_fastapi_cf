from peewee import PostgresqlDatabase, Model, CharField

database = PostgresqlDatabase('curso_fastapi_cf', 
                              user='postgres', 
                              password='12345678',
                              host='localhost',
                              port=5432)