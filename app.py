from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import uuid

app = Flask(__name__)

# Funções para manipulação de CSV
def load_projects():
    projects = []
    if os.path.exists('projetos.csv'):
        with open('projetos.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                projects.append(row)
    return projects

def save_projects(projects):
    with open('projetos.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'description', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for project in projects:
            writer.writerow(project)

def load_tasks():
    tasks = []
    if os.path.exists('tarefas.csv'):
        with open('tarefas.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tasks.append(row)
    return tasks

def save_tasks(tasks):
    with open('tarefas.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'project_id', 'title', 'description', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)

# Rotas
@app.route('/')
def dashboard():
    projects = load_projects()
    return render_template('index.html', projects=projects)

@app.route('/novo_projeto', methods=['GET', 'POST'])
def novo_projeto():
    if request.method == 'POST':
        projects = load_projects()
        project_id = str(uuid.uuid4())
        project = {
            'id': project_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'created_at': '2025-05-09'
        }
        projects.append(project)
        save_projects(projects)
        return redirect(url_for('dashboard'))
    return render_template('editar_projeto.html', project={'id': '', 'name': '', 'description': '', 'created_at': ''})

@app.route('/salvar_novo_projeto', methods=['POST'])
def salvar_novo_projeto():
    projects = load_projects()
    project_id = str(uuid.uuid4())
    project = {
        'id': project_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'created_at': '2025-05-09'
    }
    projects.append(project)
    save_projects(projects)
    return redirect(url_for('dashboard'))

@app.route('/editar_projeto/<project_id>', methods=['GET', 'POST'])
def editar_projeto(project_id):
    projects = load_projects()
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        project['name'] = request.form['name']
        project['description'] = request.form['description']
        save_projects(projects)
        return redirect(url_for('dashboard'))
    return render_template('editar_projeto.html', project=project)

@app.route('/deletar_projeto/<project_id>')
def deletar_projeto(project_id):
    projects = load_projects()
    projects = [p for p in projects if p['id'] != project_id]
    save_projects(projects)
    tasks = load_tasks()
    tasks = [t for t in tasks if t['project_id'] != project_id]
    save_tasks(tasks)
    return redirect(url_for('dashboard'))

@app.route('/projeto/<project_id>')
def ver_projeto(project_id):
    projects = load_projects()
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return redirect(url_for('dashboard'))
    tasks = load_tasks()
    project_tasks = [t for t in tasks if t['project_id'] == project_id]
    return render_template('projeto.html', project=project, tasks=project_tasks)

@app.route('/nova_tarefa/<project_id>', methods=['GET', 'POST'])
def nova_tarefa(project_id):
    if request.method == 'POST':
        tasks = load_tasks()
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'project_id': project_id,
            'title': request.form['title'],
            'description': request.form['description'],
            'status': request.form['status']
        }
        tasks.append(task)
        save_tasks(tasks)
        return redirect(url_for('ver_projeto', project_id=project_id))
    return render_template('nova_tarefa.html', project_id=project_id)

@app.route('/editar_tarefa/<project_id>/<task_id>', methods=['GET', 'POST'])
def editar_tarefa(project_id, task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return redirect(url_for('ver_projeto', project_id=project_id))
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['status'] = request.form['status']
        save_tasks(tasks)
        return redirect(url_for('ver_projeto', project_id=project_id))
    return render_template('editar_tarefa.html', project_id=project_id, task=task)

@app.route('/deletar_tarefa/<project_id>/<task_id>')
def deletar_tarefa(project_id, task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('ver_projeto', project_id=project_id))

if __name__ == '__main__':
    app.run(debug=True)