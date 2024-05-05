from materia.domain.entities.materia import Materia
from pymongo import MongoClient

class MongoDBMateriaRepository:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db['materias']

    def save(self, materia):
        materia_data = {
            'name': materia.name,
            'quarter': materia.quarter
        }
        result = self.collection.insert_one(materia_data)

    def find_by_name(self, name):
        query = {"name": name}
        materia_data = self.collection.find_one(query)
        if materia_data:
            return Materia(name=materia_data['name'], quarter=materia_data['quarter'])
        else:
            return None