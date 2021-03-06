import pymysql


class DataBase:
    def __init__(self, database, host, user, password):
        self.database = database
        self.host = host
        self.user = user
        self.password = password

    def get_connection(self):
        return pymysql.connect(user=self.user, password=self.password,  host=self.host,
                               database=self.database, charset='utf8', autocommit=True)

    def close_connection(self, connection):
        connection.close()

    def execute_select(self, sql):
        with self.get_connection() as cursor:
            cursor.execute(sql)

            attributes = cursor.description
            fetch = cursor.fetchall()

            answer = [{} for _ in range(len(fetch))]
            for indexOfItem in range(len(fetch)):
                for indexOfAttr in range(len(attributes)):
                    answer[indexOfItem][attributes[indexOfAttr][0]] = \
                        fetch[indexOfItem][indexOfAttr]
            return answer

    def execute_update_and_create(self, sql):
        with self.get_connection() as cursor:
            answer = True
            try:
                cursor.execute(sql)
            except pymysql.err.Error:
                answer = False
            return answer

    @staticmethod
    def execute_select_with_connection(sql, connection):
        cursor = connection.cursor()
        cursor.execute(sql)

        attributes = cursor.description
        fetch = cursor.fetchall()

        answer = [{} for _ in range(len(fetch))]
        for indexOfItem in range(len(fetch)):
            for indexOfAttr in range(len(attributes)):
                answer[indexOfItem][attributes[indexOfAttr][0]] = \
                    fetch[indexOfItem][indexOfAttr]
        return answer

    @staticmethod
    def execute_update_and_create_with_connection(sql, connection):
        cursor = connection.cursor()
        answer = True
        try:
            cursor.execute(sql)
            connection.commit()
        except pymysql.err.Error:
            answer = False
        return answer

