import psycopg2
from psycopg2 import Error

class Database:

    def __connect__(self):
        try:
            self.con = psycopg2.connect(host='localhost', user='postgres', password='', database='post_jobs')
            self.cursor = self.con.cursor()
            self.cursor.execute("SELECT version();")
            # Fetch result
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
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
            print("__connect__", ex)
        finally:
            self.__disconnect__()
            if error:
                raise Exception(error)
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
            result = self.cursor.fetchall()
            if result and len(result)> 0:
                col_names = []
                for elt in self.cursor.description:
                    col_names.append(elt[0])
                return result.insert(0, tuple(col_names))
            return result
        except (Exception, Error) as ex:
            print("select_all!", ex)
            error = ex
        finally:
            self.__disconnect__()
            if error:
                raise Exception(error)
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
            if error:
                raise Exception(error)
            return result


if __name__ == "__main__":
    Database().__connect__()
