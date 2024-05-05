from materia.domain.entities.materia import Materia
from materia.infrastructure.repositories.materia_repository import MongoDBMateriaRepository

class RegisterMateria:
    def __init__(self, materia_repository: MongoDBMateriaRepository):
        self.materia_repository = materia_repository

    def execute(self, name, quarter):
        self._validate_quarter(quarter)
        self._validate_unique_name(name)
        materia = Materia(name, quarter)
        self.materia_repository.save(materia)

    def _validate_quarter(self, quarter):
        if not isinstance(quarter, int):
            raise ValueError("El cuatrimestre debe de ser un número")

    def _validate_unique_name(self, name):
        existing_materia = self.materia_repository.find_by_name(name)
        if existing_materia:
            raise ValueError("Ya existe una materia con ese nombre")