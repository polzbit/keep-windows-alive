from KeepAlive.core.db._model import DBModel

class Projects(DBModel):
    def __init__(self):
        model = {
            'name': 'projects', 
            'keys':[
                ('id','INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL'), 
                ('name', 'VARCHAR(140)'),
                ]
            }
        super().__init__(model) 

    def getProjects(self):
        return self.get()

    def getProjectIdByName(self, name: str):
        return self.get(keys=['id'],where=[('name',name)])[0][0]
    
    def createProject(self, name:str):
        self.create(keys=[('name', name)])
    