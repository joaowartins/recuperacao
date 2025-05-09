# Importa as bibliotecas necessárias do Flask para criar a aplicação web
from flask import Flask, render_template, request, redirect, url_for
import csv  # Biblioteca para manipulação de arquivos CSV
import os  # Biblioteca para interagir com o sistema de arquivos
import uuid  # Biblioteca para gerar IDs únicos

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Funções para manipulação de CSV
def load_projects():
    """Carrega a lista de projetos a partir do arquivo projetos.csv, se existir."""
    projects = []
    if os.path.exists('projetos.csv'):  # Verifica se o arquivo existe
        with open('projetos.csv', newline='') as csvfile:  # Abre o arquivo em modo leitura
            reader = csv.DictReader(csvfile)  # Lê o CSV como dicionário
            for row in reader:
                projects.append(row)  # Adiciona cada linha à lista de projetos
    return projects

def save_projects(projects):
    """Salva a lista de projetos no arquivo projetos.csv, sobrescrevendo o conteúdo."""
    with open('projetos.csv', 'w', newline='') as csvfile:  # Abre o arquivo em modo escrita
        fieldnames = ['id', 'name', 'description', 'created_at']  # Define os cabeçalhos do CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Cria um escritor de CSV
        writer.writeheader()  # Escreve os cabeçalhos
        for project in projects:
            writer.writerow(project)  # Escreve cada projeto como uma linha

def load_tasks():
    """Carrega a lista de tarefas a partir do arquivo tarefas.csv, se existir."""
    tasks = []
    if os.path.exists('tarefas.csv'):  # Verifica se o arquivo existe
        with open('tarefas.csv', newline='') as csvfile:  # Abre o arquivo em modo leitura
            reader = csv.DictReader(csvfile)  # Lê o CSV como dicionário
            for row in reader:
                tasks.append(row)  # Adiciona cada linha à lista de tarefas
    return tasks

def save_tasks(tasks):
    """Salva a lista de tarefas no arquivo tarefas.csv, sobrescrevendo o conteúdo."""
    with open('tarefas.csv', 'w', newline='') as csvfile:  # Abre o arquivo em modo escrita
        fieldnames = ['id', 'project_id', 'title', 'description', 'status']  # Define os cabeçalhos do CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Cria um escritor de CSV
        writer.writeheader()  # Escreve os cabeçalhos
        for task in tasks:
            writer.writerow(task)  # Escreve cada tarefa como uma linha

# Rotas
@app.route('/')
def dashboard():
    """Rota principal que exibe o dashboard com a lista de projetos."""
    projects = load_projects()  # Carrega os projetos
    return render_template('index.html', projects=projects)  # Renderiza o template com os projetos

@app.route('/novo_projeto', methods=['GET', 'POST'])
def novo_projeto():
    """Rota para criar um novo projeto.
    GET: Exibe o formulário de criação.
    POST: Salva o novo projeto e redireciona para o dashboard."""
    if request.method == 'POST':
        projects = load_projects()  # Carrega os projetos existentes
        project_id = str(uuid.uuid4())  # Gera um ID único
        project = {
            'id': project_id,
            'name': request.form['name'],  # Obtém o nome do formulário
            'description': request.form['description'],  # Obtém a descrição do formulário
            'created_at': '2025-05-09'  # Define a data de criação fixa
        }
        projects.append(project)  # Adiciona o novo projeto à lista
        save_projects(projects)  # Salva a lista atualizada
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard
    return render_template('editar_projeto.html', project={'id': '', 'name': '', 'description': '', 'created_at': ''})  # Exibe o formulário vazio

@app.route('/salvar_novo_projeto', methods=['POST'])
def salvar_novo_projeto():
    """Rota alternativa para salvar um novo projeto via POST."""
    projects = load_projects()  # Carrega os projetos existentes
    project_id = str(uuid.uuid4())  # Gera um ID único
    project = {
        'id': project_id,
        'name': request.form['name'],  # Obtém o nome do formulário
        'description': request.form['description'],  # Obtém a descrição do formulário
        'created_at': '2025-05-09'  # Define a data de criação fixa
    }
    projects.append(project)  # Adiciona o novo projeto à lista
    save_projects(projects)  # Salva a lista atualizada
    return redirect(url_for('dashboard'))  # Redireciona para o dashboard

@app.route('/editar_projeto/<project_id>', methods=['GET', 'POST'])
def editar_projeto(project_id):
    """Rota para editar um projeto existente.
    GET: Exibe o formulário com os dados do projeto.
    POST: Atualiza os dados do projeto e redireciona."""
    projects = load_projects()  # Carrega os projetos
    project = next((p for p in projects if p['id'] == project_id), None)  # Busca o projeto pelo ID
    if not project:
        return redirect(url_for('dashboard'))  # Redireciona se o projeto não for encontrado
    if request.method == 'POST':
        project['name'] = request.form['name']  # Atualiza o nome
        project['description'] = request.form['description']  # Atualiza a descrição
        save_projects(projects)  # Salva a lista atualizada
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard
    return render_template('editar_projeto.html', project=project)  # Exibe o formulário com os dados

@app.route('/deletar_projeto/<project_id>')
def deletar_projeto(project_id):
    """Rota para deletar um projeto e suas tarefas associadas."""
    projects = load_projects()  # Carrega os projetos
    projects = [p for p in projects if p['id'] != project_id]  # Remove o projeto da lista
    save_projects(projects)  # Salva a lista atualizada
    tasks = load_tasks()  # Carrega as tarefas
    tasks = [t for t in tasks if t['project_id'] != project_id]  # Remove as tarefas associadas
    save_tasks(tasks)  # Salva a lista de tarefas atualizada
    return redirect(url_for('dashboard'))  # Redireciona para o dashboard

@app.route('/projeto/<project_id>')
def ver_projeto(project_id):
    """Rota para visualizar os detalhes de um projeto e suas tarefas."""
    projects = load_projects()  # Carrega os projetos
    project = next((p for p in projects if p['id'] == project_id), None)  # Busca o projeto pelo ID
    if not project:
        return redirect(url_for('dashboard'))  # Redireciona se o projeto não for encontrado
    tasks = load_tasks()  # Carrega as tarefas
    project_tasks = [t for t in tasks if t['project_id'] == project_id]  # Filtra as tarefas do projeto
    return render_template('projeto.html', project=project, tasks=project_tasks)  # Renderiza o template

@app.route('/nova_tarefa/<project_id>', methods=['GET', 'POST'])
def nova_tarefa(project_id):
    """Rota para adicionar uma nova tarefa a um projeto.
    GET: Exibe o formulário de criação.
    POST: Salva a nova tarefa e redireciona."""
    if request.method == 'POST':
        tasks = load_tasks()  # Carrega as tarefas
        task_id = str(uuid.uuid4())  # Gera um ID único
        task = {
            'id': task_id,
            'project_id': project_id,  # Associa ao projeto
            'title': request.form['title'],  # Obtém o título do formulário
            'description': request.form['description'],  # Obtém a descrição do formulário
            'status': request.form['status']  # Obtém o status do formulário
        }
        tasks.append(task)  # Adiciona a nova tarefa
        save_tasks(tasks)  # Salva a lista atualizada
        return redirect(url_for('ver_projeto', project_id=project_id))  # Redireciona para a página do projeto
    return render_template('nova_tarefa.html', project_id=project_id)  # Exibe o formulário

@app.route('/editar_tarefa/<project_id>/<task_id>', methods=['GET', 'POST'])
def editar_tarefa(project_id, task_id):
    """Rota para editar uma tarefa existente.
    GET: Exibe o formulário com os dados da tarefa.
    POST: Atualiza os dados da tarefa e redireciona."""
    tasks = load_tasks()  # Carrega as tarefas
    task = next((t for t in tasks if t['id'] == task_id), None)  # Busca a tarefa pelo ID
    if not task:
        return redirect(url_for('ver_projeto', project_id=project_id))  # Redireciona se a tarefa não for encontrada
    if request.method == 'POST':
        task['title'] = request.form['title']  # Atualiza o título
        task['description'] = request.form['description']  # Atualiza a descrição
        task['status'] = request.form['status']  # Atualiza o status
        save_tasks(tasks)  # Salva a lista atualizada
        return redirect(url_for('ver_projeto', project_id=project_id))  # Redireciona para a página do projeto
    return render_template('editar_tarefa.html', project_id=project_id, task=task)  # Exibe o formulário

@app.route('/deletar_tarefa/<project_id>/<task_id>')
def deletar_tarefa(project_id, task_id):
    """Rota para deletar uma tarefa específica."""
    tasks = load_tasks()  # Carrega as tarefas
    tasks = [t for t in tasks if t['id'] != task_id]  # Remove a tarefa da lista
    save_tasks(tasks)  # Salva a lista atualizada
    return redirect(url_for('ver_projeto', project_id=project_id))  # Redireciona para a página do projeto

if __name__ == '__main__':
    # Inicia o servidor Flask em modo de depuração
    app.run(debug=True)