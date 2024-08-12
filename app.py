from flask import Flask, request, jsonify
from models.task import Task



# __name__ == __main__
app = Flask(__name__)

# CRUD
# Create, Read, Update and Delete
# Tabela : Tarefa

# Função responsável por iterar sobre a lista em busca do id
def find_task_by_id(task_id):
    return next((task for task in tasks if task.id == task_id), None)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({'message': 'Nova tarefa criada com sucesso'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = find_task_by_id(id)
    
    if task is None:
        return jsonify({'message': 'Não foi possível encontrar a atividade'}), 404
    
    return jsonify(task.to_dict())

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = find_task_by_id(id)
    
    if task is None:
        return jsonify({'message': 'Não foi possível encontrar a atividade'}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    return jsonify({'message': 'Tarefa atualizada com sucesso'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = find_task_by_id(id)
    
    if task is None:
        return jsonify({'message': 'Não foi possível encontrar a atividade'}), 404
    
    tasks.remove(task)
    return jsonify({'message': 'Tarefa deletada com sucesso'})


if __name__ == "__main__":
    app.run(debug=True)