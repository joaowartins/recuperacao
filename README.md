## Visão Geral

Este é um sistema web de gerenciamento de projetos desenvolvido com Flask, projetado para permitir o cadastro, edição, visualização e exclusão de projetos e tarefas. Os dados são armazenados em arquivos CSV, e a interface utiliza HTML com Tailwind CSS para estilização.

## Requisitos Funcionais

- **Cadastrar Projetos**: Criar novos projetos com nome, descrição e data de criação.
- **Listar Projetos**: Exibir todos os projetos no dashboard.
- **Editar Projetos**: Modificar nome e descrição de projetos existentes.
- **Remover Projetos**: Excluir projetos, removendo também suas tarefas associadas.
- **Adicionar Tarefas**: Vincular tarefas a projetos com título, descrição e status (Pendente, Em andamento, Concluída).
- **Editar e Remover Tarefas**: Modificar ou excluir tarefas individualmente.
- **Visualizar Tarefas**: Exibir todas as tarefas de um projeto específico.

## Requisitos Técnicos

- **Backend**: Flask (Python).
- **Armazenamento**: Arquivos CSV (projetos.csv e tarefas.csv).
- **Frontend**: HTML com Tailwind CSS.
- **Dependências**: flask.

## Estrutura de Pastas

```
recuperacao/
├── static/
│   └── img/ (pasta para imagens, opcional e não utilizada atualmente)
├── templates/
│   ├── base.html
│   ├── editar_projeto.html
│   ├── editar_tarefa.html
│   ├── index.html
│   ├── nova_tarefa.html
│   └── projeto.html
├── app.py
├── projetos.csv
└── tarefas.csv
```

## Instalação e Execução

1. **Pré-requisitos**:
    - Python 3.x instalado.
    - Pip (gerenciador de pacotes Python).
2. **Instalação das Dependências**:
    - Execute o comando: pip install flask werkzeug.
3. **Configuração**:
    - Crie a estrutura de pastas conforme descrito.
    - Copie os arquivos fornecidos para os locais correspondentes.
    - Certifique-se de que projetos.csv e tarefas.csv contenham os cabeçalhos corretos:
        - projetos.csv: id,name,description,created_at
        - tarefas.csv: id,project_id,title,description,status
4. **Execução**:
    - No terminal, navegue até o diretório do projeto.
    - Execute: python app.py.
    - Acesse o aplicativo em http://127.0.0.1:5000/ no navegador.

## Funcionalidades

- **Dashboard (/)**: Lista todos os projetos com opções de visualização, edição e exclusão.
- **Novo Projeto (/novo_projeto)**: Formulário para criar um novo projeto.
- **Editar Projeto (/editar_projeto/<project_id>)**: Formulário para modificar um projeto existente.
- **Deletar Projeto (/deletar_projeto/<project_id>)**: Remove um projeto e suas tarefas.
- **Visualizar Projeto (/projeto/<project_id>)**: Exibe detalhes de um projeto e suas tarefas.
- **Nova Tarefa (/nova_tarefa/<project_id>)**: Adiciona uma nova tarefa a um projeto.
- **Editar Tarefa (/editar_tarefa/<project_id>/<task_id>)**: Modifica uma tarefa existente.
- **Deletar Tarefa (/deletar_tarefa/<project_id>/<task_id>)**: Remove uma tarefa.

## Estilização

- Fundo em tom escuro (#2d1b1b).
- Elementos em vermelho (#ff0000) com hover em (#cc0000).
- Bordas vermelhas nos blocos do dashboard.
- Campos de entrada com fundo escuro (#3d2b2b) e texto vermelho.

## Limitações

- Armazenamento em CSV pode não ser escalável para grandes volumes de dados.
- Sem autenticação de usuários.
- Sem validação avançada de entrada de dados.

## Melhorias Futuras

- Migração para banco de dados (ex.: MySQL).
- Adição de autenticação de usuários.
- Filtros por status de tarefas.
- Barra de progresso baseada em tarefas concluídas.

IMAGENS:

![image.png](attachment:105a1c5a-1fb6-4945-984f-54c26f361dd9:image.png)

Adicionar novo projeto:

![image.png](attachment:b2bef1bb-2e37-4f38-9b23-214ba92a85ad:image.png)

Visualização do projeto adicionado:

![image.png](attachment:ae86278f-1548-439b-b636-6ca73df191b0:image.png)

Adicionar subtarefas no projeto:

![image.png](attachment:620b38fe-e7ab-4a38-aa30-2d3e4d619897:image.png)