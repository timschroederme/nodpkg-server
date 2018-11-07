import sqlite3


sql_create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
                                   id integer PRIMARY KEY,
                                   name text NOT NULL,
                                   site text,
                                   url text,
                                   xpath text,
                                   version text,
                                   last_update text,
                                   last_release text
                                   ); """

sql_insert_row =  """INSERT INTO projects (
                        name, 
                        site,
                        url,
                        xpath,
                        version,
                        last_update,
                        last_release) 
        VALUES(?, ?, ?, ?, ?, ?, ?);"""

sql_select_tables = """SELECT name FROM sqlite_master WHERE type='table';"""

sql_select_all = """SELECT * FROM projects;"""

sql_update_row =  """ UPDATE projects
              SET version = ? ,
                  last_update = ? ,
                  last_release = ?
              WHERE id = ?"""


class DBConnector:

    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.count = 0
        self.projects = []
        if not self.table_exists():
            self.create_table()

    def start_iteration(self):
        cursor = self.cursor()
        self.projects = cursor.execute(sql_select_all).fetchall()
        self.count = 0

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def get_next_project(self):
        if self.count < len(self.projects):
            data = self.projects[self.count]
            project={
                'id': data[0],
                'name': data[1],
                'site': data[2],
                'url': data[3],
                'xpath': data[4],
                'version': data[5],
                'last_update': data[6],
                'last_release': data[7]
            }
            self.count += 1
            return project
        else:
            return False

    def table_exists(self):
        cursor = self.cursor()
        cursor.execute(sql_select_tables)
        if len(cursor.fetchall()) == 0:
            return False
        return True

    def create_table(self):
        cursor = self.cursor()
        cursor.execute(sql_create_projects_table)
        self.commit()

    def insert_project(self, name,
                       site=None,
                       url=None,
                       xpath=None,
                       version=None,
                       last_update=None,
                       last_release=None):
        data = (name, site, url, xpath, version, last_update, last_release)
        cursor = self.cursor()
        cursor.execute(sql_insert_row, data)
        self.commit()

    def update_project(self, project):
        data = (project['version'],
                project['last_update'],
                project['last_release'],
                project['id'])
        cursor = self.cursor()
        cursor.execute(sql_update_row, data)
        self.commit()
