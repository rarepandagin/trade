import psycopg2

from traceback import format_exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker





class BeatsDbClass:
    def __init__(self) -> None:

        self.host = "localhost"

        self.dbname="beats"
        self.user="postgres"
        self.password="f4I8H2C0U40X104jwVUSKW38F4X23894j2938429jz"

        self.connection_string = f'postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}'

        self.engine = create_engine(self.connection_string)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()





    def run_sql_command(self, sql_command, commit=False):
        
        database_connection = None
        return_dict = []

        try:

            database_connection = psycopg2.connect(
                                                    dbname=self.dbname,
                                                    user=self.user,
                                                    password=self.password,
                                                    host=self.host
                                                )


            cursor_obj = database_connection.cursor()

            cursor_obj.execute(sql_command)

            try:

                result = cursor_obj.fetchall()

                if cursor_obj.description is not None:
                    columns = [description[0] for description in cursor_obj.description]
                    return_dict = []
                    for row in result:
                        return_dict.append(dict(zip(columns, row)))

            except:
                pass

            if commit:
                database_connection.commit()
        
            cursor_obj.close()

        except :
            tk.logger.error(format_exc())
            return_dict = None
        
        finally:
        
            if database_connection:
                database_connection.close()

            return return_dict



    def obtain_db_record(self, table_name):
        
        sql = f"""
            SELECT * from {table_name} 
        """
        records = self.run_sql_command(sql)

        return records

