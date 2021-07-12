import psycopg2
from psycopg2 import Error

class Database:

    def __connect__(self):
        try:
            self.con = psycopg2.connect(host='localhost', user='postgres', password='', database='post_jobs')
            self.cursor = self.con.cursor()
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
            raise Exception(error)

    def __disconnect__(self):
        if self.con:
            self.cursor.close()
            self.con.close()

    def __manipulate_data__(self, query, params=None):
        self.__connect__()
        error = None
        row_count = 0
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            self.con.commit()
            row_count = self.cursor.rowcount
        except (Exception, Error) as ex:
            print("__manipulate_data__", ex)
            error = str(ex)
        finally:
            self.__disconnect__()
            if error and len(error) > 0:
                raise Exception(error)
            else:
                return row_count

    def insert(self, query, params=None):
        return self.__manipulate_data__(query, params)

    def update(self, query, params=None):
        return self.__manipulate_data__(query, params)

    def delete(self, query, params=None):
        return self.__manipulate_data__(query, params)

    def select_all(self, query, params=None):
        error = None
        self.__connect__()
        result = []
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            result = [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in self.cursor.fetchall()]
            # result = self.cursor.fetchall()
            # if result and len(result)> 0:
            #     col_names = []
            #     for elt in self.cursor.description:
            #         col_names.append(elt[0])
            #     return result.insert(0, tuple(col_names))
            return result
        except (Exception, Error) as ex:
            print("select_all!", ex)
            error = ex
        finally:
            self.__disconnect__()
            if error and len(error) > 0:
                raise Exception(error)
            else:
                return result

    def select_one(self, query, params=None):
        self.__connect__()
        error = None
        result = None
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.__disconnect__()
        except (Exception, Error) as ex:
            print("select_one!", ex)
        finally:
            self.__disconnect__()
            if error and len(error) > 0:
                raise Exception(error)
            else:
                return result


if __name__ == "__main__":
    Database().__connect__()
    # Tables Dump command CMD
    #  C:\Users\Tariq>pg_dump -U postgres -p 5432 -d post_jobs -W -f  C:\Users\Tariq\source\repos\Python\TODO_App\database\jobs.sql