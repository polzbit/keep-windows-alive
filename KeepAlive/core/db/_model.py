from PyQt5.QtSql import QSqlQuery

class DBModel:
    def __init__(self, model: dict[str, str|tuple[str, str]]):
        self.model = model
        self.createTable()
    
    def createTable(self):
        query = QSqlQuery()
        table_keys = ''
        for (key, type) in self.model['keys']:
            table_keys += f'{key} {type},'
        table_keys = table_keys[:-1]
        query.exec(
            f"""
            CREATE TABLE IF NOT EXISTS {self.model['name']} ({table_keys})
            """
        )
        query.finish()

    def get(self, keys: list[str] = [], where: list[tuple[str,str|int]] = []):
        query = QSqlQuery()
        table_keys = ''
        table_where = ''
        for key in keys:
            table_keys += f'{key},'
        table_keys = table_keys[:-1]
        for (key, value) in where:
            key_type = type(value)
            if key_type == int:
                table_where += f"{key} = {value} AND "
            else:
                table_where += f"{key} = '{value}' AND "
        table_where = table_where[:-4]
        keyRange = len(keys)
        if not table_keys:
            table_keys = '*'
            keyRange = len(self.model['keys'])
        if len(where):
            # print(f"SELECT {table_keys} FROM {self.model['name']} WHERE {table_where}")
            query.exec(f"SELECT {table_keys} FROM {self.model['name']} WHERE {table_where}")
        else:
            query.exec(f"SELECT {table_keys} FROM {self.model['name']}")
        data = []
    
        while query.next():
            row = []
            for key in range(keyRange):
                row.append(query.value(key))
            data.append(row)
        query.finish()
        return data
    
    def create(self, keys: list[tuple[str,str|int]]):
        query = QSqlQuery()
        table_values = ''
        table_keys = ''
        for (key, value) in keys:
            key_type = type(value)
            table_keys += f"{key},"
            if key_type == int:
                table_values += f"{value},"
            else:
                table_values += f"'{value}',"
        table_values = table_values[:-1]
        table_keys = table_keys[:-1]
        query.exec(
                f"""INSERT INTO {self.model['name']} ({table_keys})
                VALUES ({table_values})"""
            )
        query.finish()

    def update(self, keys: list[tuple[str,str|int]], where: list[tuple[str,str|int]] = []):
        query = QSqlQuery()
        table_keys = ''
        table_where = ''
        for (key, value) in keys:
            key_type = type(value)
            if key_type == int:
                table_keys += f"{key} = {value},"
            else:
                table_keys += f"{key} = '{value}',"
        table_keys = table_keys[:-1]
        for (key, value) in where:
            key_type = type(value)
            if key_type == int:
                table_where += f"{key} = {value} AND "
            else:
                table_where += f"{key} = '{value}' AND "
        table_where = table_where[:-4]
        if len(where):
            query.exec_(
                    f"""UPDATE {self.model['name']} SET {table_keys} WHERE {table_where}"""
                )
        else:
            query.exec_(
                    f"""UPDATE {self.model['name']} SET {table_keys}"""
                )
        query.finish()

    def delete(self, where: list[tuple[str,str|int]] = []):
        query = QSqlQuery()
        table_where = ''
        for (key, value) in where:
            key_type = type(value)
            if key_type == int:
                table_where += f"{key} = {value} AND "
            else:
                table_where += f"{key} = '{value}' AND "
        table_where = table_where[:-4]
        if len(where):
            query.exec(f'delete from {self.model["name"]} WHERE {table_where}')
        else:
            query.exec(f'delete from {self.model["name"]}')
        query.finish()