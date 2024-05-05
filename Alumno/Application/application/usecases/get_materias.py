from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository

class GetMaterias:
    def __init__(self, student_repository: MongoDBStudentRepository):
        self.student_repository = student_repository

    def execute(self, enrollment):
        return self.student_repository.get_materias(enrollment)
