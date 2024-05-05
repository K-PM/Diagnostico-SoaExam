from flask import Blueprint, request, jsonify
from alumno.application.usecases.assign_materias import AssignMaterias
from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository
from materia.infrastructure.repositories.materia_repository import MongoDBMateriaRepository

assign_materias_blueprint = Blueprint('assign_materias', __name__)

def initialize_endpoints(student_repository, materia_repository):
    assign_materias_usecase = AssignMaterias(student_repository, materia_repository)

    @assign_materias_blueprint.route('/<enrollment>/materias', methods=['POST'])
    def assign_materias(enrollment):
        data = request.get_json()

        # Validar la existencia de datos y de la lista de materias en el cuerpo de la solicitud
        if not data or 'materias' not in data:
            return jsonify({"error": "Materias are required"}), 400

        materias = data.get('materias', [])

        try:
            # Ejecutar caso de uso para asignar materias al alumno
            assign_materias_usecase.execute(enrollment, materias)
            return jsonify({"message": "Materias assigned successfully"}), 200
        except ValueError as e:
            # Manejar error si ocurre al asignar las materias
            return jsonify({"error": str(e)}), 400