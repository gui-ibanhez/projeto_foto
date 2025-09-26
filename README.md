# Loja Fotos - Gallery Project

This project is a simple Django-based photo gallery. This guide contains instructions for setting up the development environment on Linux and deploying the application on a Windows machine for a private LAN.

---

## 1. Development Setup (Linux)

These instructions are for setting up a local development environment on Arch Linux.

### Requirements
- Python 3.10+
- `pip` and `venv`
- ImageMagick library (`imagemagick` package on Arch)

### Installation
1.  **Create and activate a virtual environment:**
    ```fish
    python -m venv .venv
    source .venv/bin/activate.fish
    ```

2.  **Install dependencies:**
    The development requirements include `wand` for image processing, which uses the system's ImageMagick library.
    ```fish
    python -m pip install -U pip
    python -m pip install -r requirements-dev.txt
    ```

3.  **Configure environment:**
    Copy the example `.env` file. For development, the default settings are fine.
    ```fish
    cp .env.example .env
    ```

4.  **Setup database:**
    Run the migrations to create the SQLite database and necessary tables.
    ```fish
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```fish
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---

## 2. Production Deployment (Windows)

These instructions are for deploying the application on a Windows machine for access within a private LAN. This setup uses the `waitress` pure-Python web server and does not require ImageMagick.

### Requirements
- Python 3.10+ (ensure it's added to your PATH during installation)

### Setup
1.  **Copy Project Files:**
    Transfer the entire project folder to your Windows machine.

2.  **Open PowerShell or Command Prompt:**
    Navigate into the project directory.
    ```powershell
    cd path\\to\\projeto_foto
    ```

3.  **Create Virtual Environment and Install Dependencies:**
    ```powershell
    # Create and activate the virtual environment
    python -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1

    # Install production dependencies
    python -m pip install -U pip
    python -m pip install -r requirements.txt
    ```

4.  **Configure `.env` for Production:**
    Create a copy of the environment configuration file and edit it for your network.
    ```powershell
    copy .env.example .env
    ```
    Open the `.env` file in a text editor and make the following changes:
    - `DEBUG`: Set to `False`.
    - `SECRET_KEY`: **Change this to a new, long, random string.**
    - `ALLOWED_HOSTS`: Set to the IP address of your Windows server (e.g., `192.168.1.50`) or `*` if your LAN is secure.

5.  **Prepare Database and Static Files:**
    - **Run Migrations:** Create the production SQLite database.
      ```powershell
      python manage.py migrate --noinput
      ```
    - **Collect Static Files:** Gather all static files for `whitenoise` to serve.
      ```powershell
      python manage.py collectstatic --noinput
      ```

6.  **Run the Production Server:**
    Use `waitress` to serve the application.
    ```powershell
    waitress-serve --host 0.0.0.0 --port 8000 loja_fotos.wsgi:application
    ```
    The application will now be accessible from other computers on the same network via `http://<windows-server-ip>:8000`.
