from flask import Blueprint, request, jsonify
from alumno.application.usecases.register_alumno import RegisterStudent
from alumno.infrastructure.repositories.alumno_repository import MongoDBStudentRepository

create_student_blueprint = Blueprint('create_student', __name__)

def initialize_endpoints(repository):
    register_student_usecase = RegisterStudent(student_repository=repository)
    
    @create_student_blueprint.route('', methods=['POST'])
    def register_student():
        data = request.get_json()

        # Validar la existencia de datos y los campos obligatorios en el cuerpo de la solicitud
        if not data or not all(key in data for key in ['name', 'career', 'initial_status']):
            return jsonify({"error": "Nombre, carrera y estatus de inicio son necesarios"}), 400

        name = data.get('name')
        career = data.get('career')
        initial_status = data.get('initial_status')

        try:
            # Ejecutar caso de uso para registrar un alumno
            register_student_usecase.execute(name, career, initial_status)
            return jsonify({"message": "Alumno registrado exitosamente"}), 201
        except ValueError as e:
            # Manejar error si ocurre al registrar el alumno
            return jsonify({"error": str(e)}), 400
