from flask import Blueprint
from alumno.infrastructure.controllers.get_materias_controller import get_materias_blueprint, initialize_endpoints as get_materias_endpoints
from alumno.infrastructure.controllers.create_alumno_controller import create_student_blueprint, initialize_endpoints as create_student_endpoints
from alumno.infrastructure.controllers.get_alumno_controller import get_alumno_blueprint, initialize_endpoints as get_alumno_endpoints
from alumno.infrastructure.controllers.assign_materias_controller import assign_materias_blueprint, initialize_endpoints as assign_materias_endpoints
from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository
from materia.infrastructure.repositories.materia_repository import MongoDBMateriaRepository

alumno_router = Blueprint('alumno_router', __name__)

def initialize_endpoints(student_repository, materia_repository):
    create_student_endpoints(student_repository)
    get_alumno_endpoints(student_repository)
    assign_materias_endpoints(student_repository, materia_repository)
    get_materias_endpoints(student_repository)

initialize_endpoints(
    MongoDBStudentRepository(connection_string='mongodb://localhost:27017/', database_name='APIdiagnostico'),
    MongoDBMateriaRepository(connection_string='mongodb://localhost:27017/', database_name='APIdiagnostico')
)

alumno_router.register_blueprint(create_student_blueprint, url_prefix='/api/alumnos')
alumno_router.register_blueprint(get_alumno_blueprint, url_prefix='/api/alumnos')
alumno_router.register_blueprint(assign_materias_blueprint, url_prefix='/api/alumnos')
alumno_router.register_blueprint(get_materias_blueprint, url_prefix='/api/alumnos')
