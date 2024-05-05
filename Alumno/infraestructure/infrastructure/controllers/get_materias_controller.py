from flask import Blueprint, jsonify, request
from alumno.application.usecases.get_materias import GetMaterias
from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository

get_materias_blueprint = Blueprint('get_materias', __name__)

def initialize_endpoints(repository):
    get_materias_usecase = GetMaterias(student_repository=repository)
    
    @get_materias_blueprint.route('/<enrollment>/materias', methods=['GET'])
    def get_materias(enrollment):
        try:
            materias = get_materias_usecase.execute(enrollment)
            return jsonify({"materias": materias}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
