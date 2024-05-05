from flask import Blueprint, jsonify
from alumno.application.usecases.get_alumnos import GetAlumnos
from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository

get_alumno_blueprint = Blueprint('get_alumno', __name__)

def initialize_endpoints(repository):
    get_alumnos_usecase = GetAlumnos(student_repository=repository)
    
    @get_alumno_blueprint.route('/', methods=['GET'])
    def get_alumnos():
        alumnos = get_alumnos_usecase.execute()
        alumnos_list = [{
            "name": alumno.name,
            "career": alumno.career,
            "enrollment": alumno.enrollment,
            "initial_status": alumno.initial_status
        } for alumno in alumnos]
        return jsonify({"alumnos": alumnos_list}), 200
