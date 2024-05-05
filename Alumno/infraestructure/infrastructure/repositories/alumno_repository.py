from pymongo import MongoClient
from alumno.domain.entities.alumno import Student

class MongoDBStudentRepository:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db['alumnos']

    def get_last_enrollment_number(self, year, status_code):
        query = {
            "enrollment": {"$regex": f"^{year}{status_code}"},
        }
        projection = {"enrollment": 1, "_id": 0}
        result = self.collection.find(query, projection).sort("enrollment", -1).limit(1)
        last_enrollment = result[0]['enrollment'] if self.collection.count_documents(query) > 0 else f"{year}{status_code}000"
        return last_enrollment

    def save(self, student: Student):
        student_data = {
            'name': student.name,
            'career': student.career,
            'enrollment': student.enrollment,
            'initial_status': student.initial_status
        }
        self.collection.insert_one(student_data)

    def find_all(self):
        alumnos_data = self.collection.find({})
        alumnos = [Student(
            name=alumno['name'],
            career=alumno['career'],
            enrollment=alumno['enrollment'],
            initial_status=alumno['initial_status']
        ) for alumno in alumnos_data]
        return alumnos

    def find_by_name(self, name):
        query = {"name": name}
        student_data = self.collection.find_one(query)
        if student_data:
            return Student(name=student_data['name'], career=student_data['career'], enrollment=student_data['enrollment'], initial_status=student_data['initial_status'])
        else:
            return None
    
    def find_by_enrollment(self, enrollment):
        query = {"enrollment": enrollment}
        student_data = self.collection.find_one(query)
        if student_data:
            return Student(name=student_data['name'], career=student_data['career'], enrollment=student_data['enrollment'], initial_status=student_data['initial_status'])
        else:
            return None
        
    def assign_materias(self, alumno, materias):
        if not self.collection.find_one({"enrollment": alumno.enrollment}):
            raise ValueError("El alumno no está registrado")

        for materia in materias:
            if not self.db['materias'].find_one({"name": materia}):
                raise ValueError(f"La materia '{materia}' no existe")

        self.collection.update_one(
            {"enrollment": alumno.enrollment},
            {"$addToSet": {"materias": {"$each": materias}}}
        )
    
    def get_materias(self, enrollment):
        query = {"enrollment": enrollment}
        projection = {"_id": 0, "materias": 1}
        result = self.collection.find_one(query, projection)
        return result.get("materias", []) if result else []