A backend API for a blog application built with FastAPI.

## Key Features

* User Authentication (Signup, Login)
* Post Management (Create, Read, Update, Delete)
* PostgreSQL Database Integration

## Project Status & Development Notes

* **API Endpoints:** Verified and functional via Swagger UI.
* **Database:** Successfully connected to PostgreSQL. Tables initialized and verified.
* **Initial Challenges:** Encountered significant compatibility issues with Python 3.13.x and `pydantic-core`. Resolved by downgrading to Python 3.12.x.
* **Commit History Insight:** An initial commit of non-functional code. Subsequent late-night efforts to troubleshoot and fix Python compatibility issues, leading to a functional application.

## Setup & Running

**Prerequisites:**

* Python 3.12.x
* Poetry (recommended) or pip
* PostgreSQL database instance

**Installation:**

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```
2.  Create and activate a virtual environment (e.g., `venv312`):
    ```bash
    python -m venv venv312
    # On Windows:
    .\venv312\Scripts\activate
    # On macOS/Linux:
    source venv312/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Configuration:**

1.  Create a `.env` file in the project root based on `config.py` example (or directly modify `app/config.py` for local development).
2.  Configure your PostgreSQL database connection string:
    ```
    # Example .env content
    DATABASE_URL="postgresql://user:password@localhost:5432/your_database_name"
    SECRET_KEY="your-super-secret-key-change-in-production"
    # ... other settings as needed
    ```

**Database Initialization:**

1.  Ensure your PostgreSQL database server is running.
2.  Create database tables:
    ```bash
    python create_db_tables.py
    ```

**Running the Application:**

```bash
uvicorn app.main:app --reload
