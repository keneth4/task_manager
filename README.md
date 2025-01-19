# Task Management API

## Description
A simple task management API to allow users to create, update, delete, and retrieve tasks. Users can also filter tasks by status or due date. Developed using FastAPI and SQLModel.

---

## Features
- **CRUD Operations**: Create, retrieve, update, and delete tasks.
- **Filtering**: Filter tasks by status or due date.
- **Task Attributes**:
  - `id`: Auto-generated unique identifier (UUID).
  - `title`: String, required, max length 100.
  - `description`: String, optional.
  - `status`: Enum (`"pending"`, `"in-progress"`, `"completed"`), default is `"pending"`.
  - `due_date`: Datetime, optional.
  - `created_at`: Auto-generated timestamp.
  - `updated_at`: Auto-generated timestamp.

---

## API Endpoints

### Tasks
- **Create a Task**: `POST /tasks/`  
    Request Body:
    ```json
    {
        "title": "Task Title",
        "description": "Optional description",
        "status": "in-progress", // Optional
        "due_date": "YYYY-MM-DD" // Optional
    }
    ```
    *NOTE: All optionals must have the required format.*

    **Response:** Created task details.

- **Retrieve All Tasks**: `GET /tasks/`

    **Response:** List of all tasks.

- **Retrieve a Specific Task:** `GET /tasks/{uuid}/`

    **Response:** Details of the task with the specified ID.

- **Update a Task:** `PUT /tasks/{uuid}/`  
    Request Body:
    ```json
    {
        "title": "Updated Title",
        "description": "Updated description",
        "status": "completed",
        "due_date": "YYYY-MM-DD"
    }
    ```
    *NOTE: All are optional but must have the required format.*

    **Response:** Updated task details.

- **Delete a Task:** `DELETE /tasks/{id}/`

    **Response:** Confirmation of deletion.

### Filters

- **Filter by Status:** `GET /tasks/?status=pending`

    **Response:** List of tasks with the specified status.

- **Filter by Due Date:** `GET /tasks/?due_date=YYYY-MM-DD`

    **Response:** List of tasks due on the specified date.

- **Filter by both Status and Due Date:** `GET /tasks/?status=pending&due_date=YYYY-MM-DD`

    *NOTE: Filters can be combined to improve the query's scope.*

---

## Setup and Run Instructions

### Prerequisites
- Docker

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/keneth4/task_manager.git
    ```

2. **Move into project directory:**
    ```bash
    cd task_manager
    ```

3. **Give execution permission to the `run` script:**
    ```bash
    chmod +x ./run.sh
    ```

4. **Start API service:**
    ```bash
    ./run.sh
    ```

---

## Assumptions
- Validation for fields (e.g., title length, valid status).
- Basic error handling for invalid requests and non-existent resources.
- SQLite is used as the default database for simplicity.
- Containerization with Docker to simplify deployment.
- Project and package manager to keep track of every dependency.
- Basic CI pipeline (Github Actions) for Linting, to improve code quality, and Container Build, to verify a correct deployment.

---

## Future Enhancements

1. **CI Testing:**
   - Create a CI testing pipeline when requesting a PR to the main branch.

2. **Authentication and Authorization:**
   - Add user authentication (e.g., JWT-based).
   - Allow only authorized users to access or modify their tasks.

3. **Enhanced Validation:**
   - Validate `due_date` is not in the past.
   - Restrict `status` transitions (e.g., cannot move from `completed` to `pending`).

4. **Database Improvements:**
   - Use PostgreSQL for production readiness.

5. **Logging and Monitoring:**
   - Improve logging for debugging and audit trails.
   - Set up monitoring and alerts.

6. **Scalability:**
   - Add support for deploying to cloud platforms (AWS, Azure, GCP).
   - Implement load balancing and database replication.

7. **UI Integration:**
   - Build a frontend interface for user interaction.

---

## Testing
- Automated tests are included in the `tests/` directory.
- To run tests:
    ```bash
    ./run.sh -test
    ```
