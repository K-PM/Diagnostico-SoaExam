from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository

class GetAlumnos:
    def __init__(self, student_repository: MongoDBStudentRepository):
        self.student_repository = student_repository

    def execute(self):
        return self.student_repository.find_all()
