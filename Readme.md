# Mediphore Task Management API

This project is a Django REST API for managing projects, tasks, resources, and skills. It is designed to help teams assign resources to tasks based on required skills and track project progress.

## Features

- **Projects**: Create and manage projects with descriptions, due dates, status, and timelines.
- **Tasks**: Assign tasks to projects, specify required skills, and track assignment and status.
- **Resources**: Manage team members/resources, their skills, and availability.
- **Skills**: Define and assign skills to resources and tasks.
- **Assignment Logic**: Assign resources to tasks only if they have the required skill.

## Models

### Project
- `name`: Project name
- `description`: Project description
- `duedate`: Optional due date
- `status`: Project status (`not started`, `in progress`, `completed`)
- `start_date`, `end_date`: Project timeline

### Task
- `title`: Task title
- `description`: Task details
- `status`: Task status (`not started`, `in progress`, `completed`)
- `start_date`, `end_date`: Task timeline
- `skill`: Required skill for the task
- `project`: Associated project
- `assigned_resource`: Resource assigned to the task (optional)

### Resource
- `name`: Resource name
- `short_description`: Optional description
- `skills`: Skills possessed by the resource (many-to-many)
- `current_status`: Availability (`avalible`, `unavailable`, `busy`)

### Skill
- `name`: Skill name

## API Endpoints

See [app/urls.py](app/urls.py) for the full list of endpoints, including:
- `/projects`
- `/tasks`
- `/tasks/<int:task_id>`
- `/task/<int:task_id>/assign`
- `/resources`
- `/resources/search`
- `/skills`

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
2. Run migrations:
    ```sh
    python manage.py migrate
    ```
3. Start the server:
    ```sh
    python manage.py runserver
    ```

## License

MIT