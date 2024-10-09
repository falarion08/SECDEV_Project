# Workbox

A **simple project management web application** designed to streamline workspace and task management, built with Flask PostgreSQL, Jinja2, and TailwindCSS. Workbox prioritizes security by aligning with the OWASP Top 10 security guidelines.

## Table Of Contents

- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Notes](#notes)

## Project Structure

This project is structured as a monorepo and includes three main directories:

- **`src/`**: Contains the source code and logic for the application such as app configs, controllers, models, routes, utils, and the flask app initializer factory.
- **`static/`**: Contains the static assets of the application such as the Tailwind CSS build output, static images used throughout the site, and a storage directory for files uploaded by users.
- **`templates/`**: Contains the HTML pages built with Jinja2 and styled with Tailwind CSS. Each template provides the front-end layout and structure for various views to render dynamic content based on user interaction and roles. <br> <br>

├── src/ <br>
│   ├── configs/ ──── Configuration settings and environment-specific configs <br>
│   ├── controllers/ ──── Business logic, handling requests and responses <br>
│   ├── db_seed/ ──── Database seeding scripts and initial data <br>
│   ├── models/ ──── Database models and schema definitions (SQLAlchemy) <br>
│   ├── routes/ ──── Route handlers, connecting endpoints to controllers <br>
│   ├── utils/ ──── Utility functions (helpers, validation, security) <br>
│   ├── __init__.py ──── Factory for initializing the Flask app <br>
│   └── styles.css ──── # Input file for Tailwind CSS styles <br>
├── static/ <br>
│   ├── css/ ──── # Compiled Tailwind CSS output for styling <br>
│   ├── images/ ──── # Static images for the site <br>
│   └── upload/ ──── # Directory for user-uploaded files <br>
├── templates/ ──── # Jinja2 templates for HTML pages, styled with TailwindCSS <br>
│   ├── (...).html <br>
│   └── base.html ──── # Base layout template for consistent site structure <br>
├── README.md <br>
├── requirements.txt ──── # List of Python dependencies <br>
├── package.json <br>
├── vercel.json ──── # Configuration file for Vercel deployment <br>
└── .env <br>

## Tech Stack

- **Flask**: Serves as the core framework for building the web application, managing HTTP requests, routing, and integrating extensions for security and form validation. Key libraries include Talisman for security headers, Principal for role-based access control, and WTForms for form management.
- **PostgreSQL**: A powerful, open-source relational database used to store and manage data securely and efficiently. Integrated with Flask using SQLAlchemy, it allows for seamless data handling and structured querying across application components.
- **Jinja2**: A templating engine for Python, used with Flask to generate dynamic HTML content. Jinja2 enables separation of the application’s logic from its presentation, making it easy to render data-driven views for users.
- **Tailwind CSS**: A utility-first CSS framework that provides flexibility and ease of use in designing responsive and modern user interfaces. Tailwind CSS is used in conjunction with Jinja2 to create consistent, responsive, and visually appealing layouts across the application.

## Installation

### Prerequisites

Make sure you have the following installed:
- **Python (v3.11 or higher)**
- **Node.js (LTS)**

### Clone the Repository
```bash
git clone https://github.com/falarion08/Workbox.git
cd Workbox
```

### Install Dependencies

In Python, without a virtual environment, the dependencies will be installed globally into your machine. To avoid this, open CLI, and install the virtualenv package to create a virtual environment.
```
pip install virtualenv
python -m virtualenv .venv
```

After creating a virtual environment, we can access it via CLI again by running the .venv activate script and then we can install the dependencies in the virtual environment by running the following commands:
```
.venv/Scripts/activate
pip install -r requirements.txt
```

Now that you have the Python dependencies installed, in a separate terminal, we can install the npm dependencies for Tailwind CSS by running this command:
```
npm install
```

### Environment Variables

Before proceeding with starting the application, the application uses .env to store URLs, secret keys, and other variables. The required variables in your .env file are as follows:
```
DATABASE_URL = your_postgresql_db_url
MAX_IMAGE_SIZE = your_preferred_max_image_size
MAX_FILE_UPLOAD_SIZE = your_preferred_max_upload_size
FOLDER_UPLOAD = "static/upload/"
RECAPTCHA_PRIVATE_KEY = your_google_recaptcha_private_key
RECAPTCHA_PUBLIC_KEY = your_google_recaptcha_public_key
SECRET_KEY = your_secure_secret_key
```

### Running the Application

Before running the application, ensure that you have a .env file with the environment variables from the previous section. If you do, you can start the application by running the following commands in the two terminals from earlier:

On the terminal that isn't using the virtual environment:
```
npm run build
```

On the terminal using the virtual environment:
```
python app.py
```

Alternatively, if you've already built the Tailwind CSS output file, and don't plan on changing any styles, then you do not need to build it with a separate terminal and can just use the virtual environment terminal to run the application directly.

## Notes

**Development Website URL**: http://localhost:5000/

**The website is live on:** https://workbox-revamped.vercel.app/ (deployed from a forked repo)
