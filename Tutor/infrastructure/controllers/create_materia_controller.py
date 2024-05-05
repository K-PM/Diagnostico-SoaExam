from flask import Blueprint, request, jsonify
from materia.application.usecases.register_materia import RegisterMateria
from materia.infrastructure.repositories.materia_repository import MongoDBMateriaRepository

create_materia_blueprint = Blueprint('create_materia', __name__)

def initialize_endpoints(repository):
    register_materia_usecase = RegisterMateria(materia_repository=repository)
    
    @create_materia_blueprint.route('', methods=['POST'])
    def register_materia():
        data = request.get_json()

        if not data or not all(key in data for key in ['name', 'quarter']):
            return jsonify({"error": "Name and quarter are required"}), 400

        name = data.get('name')
        quarter = data.get('quarter')

        try:
            register_materia_usecase.execute(name, quarter)
            return jsonify({"message": "Materia registered successfully"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
