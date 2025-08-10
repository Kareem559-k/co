# Medical AI Assistant - Deployment Guide

This guide provides comprehensive instructions for deploying the Medical AI Assistant web application to a production environment. The application consists of a Flask backend API and a React frontend, designed to work together as a full-stack application.

## 1. Overview of the Application Architecture

The Medical AI Assistant is built with a clear separation of concerns, allowing for flexible deployment options. It comprises:

*   **Flask Backend**: Developed using Python and Flask, this serves as the core API for symptom analysis, image analysis (future), user authentication, and data management. It also serves the static React frontend files.
*   **React Frontend**: A modern single-page application (SPA) built with React, Vite, Tailwind CSS, and shadcn/ui. This provides the user interface for interacting with the backend services.

### Key Technologies Used:

*   **Backend**: Python 3.11, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, SQLite (for development/small scale), Gunicorn (for production serving).
*   **Frontend**: React 18, Vite, pnpm, Tailwind CSS, shadcn/ui, Lucide React.
*   **Database**: SQLite (development), PostgreSQL/MySQL (recommended for production).

## 2. Prerequisites

Before you begin the deployment process, ensure you have the following installed on your server or local machine:

*   **Python 3.11 or higher**: For the Flask backend.
    ```bash
    sudo apt update
    sudo apt install python3.11 python3.11-venv
    ```
*   **Node.js (LTS version) and pnpm**: For the React frontend. pnpm is recommended for faster and more efficient package management.
    ```bash
    curl -fsSL https://get.pnpm.io/install.sh | sh
    # Follow instructions to add pnpm to your PATH
    ```
*   **Git**: To clone the repository.
    ```bash
    sudo apt install git
    ```
*   **Web Server (e.g., Nginx, Apache)**: To act as a reverse proxy for the Flask application and serve static files.
*   **Database System (e.g., PostgreSQL, MySQL)**: For production environments. SQLite is used by default for simplicity in development but is not recommended for production.

## 3. Deployment Steps

Follow these steps to deploy the Medical AI Assistant:

### Step 3.1: Clone the Repository

First, clone the project repository to your server:

```bash
cd /path/to/your/deployment/directory
git clone <repository_url> # Replace with your actual repository URL
cd medical-ai-assistant
```

### Step 3.2: Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd medical-ai-backend
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Database (Production Recommendation):**
    For production, it's highly recommended to use a robust database like PostgreSQL or MySQL instead of SQLite. Update your `medical-ai-backend/src/main.py` to connect to your production database. You will need to install the appropriate database connector (e.g., `psycopg2-binary` for PostgreSQL, `mysqlclient` for MySQL) and configure the `SQLALCHEMY_DATABASE_URI`.

    Example for PostgreSQL:
    ```python
    # medical-ai-backend/src/main.py
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@host:port/database_name"
    ```

5.  **Initialize the database:**
    ```bash
    flask db upgrade # If using Flask-Migrate
    # Or manually create tables if not using migrations
    # from src.main import app, db
    # with app.app_context():
    #     db.create_all()
    ```

6.  **Run the backend with a production-ready WSGI server (e.g., Gunicorn):**
    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
    ```
    (This command runs Gunicorn with 4 worker processes, binding to all network interfaces on port 5000. You can adjust the number of workers based on your server's CPU cores.)

### Step 3.3: Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../medical-ai-frontend
    ```

2.  **Install frontend dependencies:**
    ```bash
    pnpm install
    ```

3.  **Build the frontend for production:**
    ```bash
    pnpm run build
    ```
    This will create a `dist` directory containing the optimized static files for your React application.

4.  **Copy built frontend to backend's static folder:**
    The Flask backend is configured to serve the React frontend's static files. Copy the contents of the `dist` folder into the `medical-ai-backend/src/static` directory.
    ```bash
    cp -r dist/* ../medical-ai-backend/src/static/
    ```

### Step 3.4: Web Server Configuration (Nginx Example)

Configure a web server like Nginx to act as a reverse proxy for your Flask application and serve the static files. This provides better performance, security, and allows you to run your application on standard HTTP/HTTPS ports.

1.  **Install Nginx (if not already installed):**
    ```bash
    sudo apt install nginx
    ```

2.  **Create a new Nginx configuration file** (e.g., `/etc/nginx/sites-available/medical_ai_assistant`):
    ```nginx
    server {
        listen 80;
        server_name your_domain.com www.your_domain.com; # Replace with your domain

        location / {
            proxy_pass http://127.0.0.1:5000; # Proxy requests to Gunicorn
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Optional: Serve static files directly from Nginx for better performance
        # This assumes your Flask app serves them from /static
        # location /static/ {
        #     alias /path/to/your/deployment/directory/medical-ai-backend/src/static/;
        #     expires 30d;
        #     add_header Cache-Control "public, no-transform";
        # }
    }
    ```

3.  **Create a symbolic link to enable the configuration:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/medical_ai_assistant /etc/nginx/sites-enabled
    ```

4.  **Test Nginx configuration and restart:**
    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

### Step 3.5: Secure with HTTPS (Recommended)

For production, it's crucial to secure your application with HTTPS using Let's Encrypt and Certbot.

1.  **Install Certbot and its Nginx plugin:**
    ```bash
    sudo apt install certbot python3-certbot-nginx
    ```

2.  **Obtain and install SSL certificates:**
    ```bash
    sudo certbot --nginx -d your_domain.com -d www.your_domain.com
    ```
    Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

## 4. Running the Application

After completing the deployment steps, ensure your Gunicorn process is running (e.g., using `systemd` for process management) and Nginx is active. Your application should now be accessible via your configured domain name over HTTPS.

## 5. Maintenance and Updates

*   **Updating Code**: Pull the latest changes from your Git repository, rebuild the frontend, and restart the Gunicorn process.
*   **Database Backups**: Regularly back up your production database.
*   **Monitoring**: Set up monitoring tools to track application performance and errors.
*   **Security Updates**: Keep all dependencies and server software updated.

This guide provides a robust foundation for deploying your Medical AI Assistant. For more advanced deployments (e.g., Docker, Kubernetes, cloud platforms), further configuration and tools would be required.

---

**Author**: Manus AI
**Date**: August 10, 2025



