# SECDEV_Project

Instructions on how to run the project. (Make sure python is installed) 
1) Open CLI, and do "pip install virtualenv"
2) After the installation run the virtual environment by entering in the CLI ".venv/Scripts/activate" (Assuming you're using Windows)
3) Create a .env file in the base folder. Create a variable name, "DATABASE_URL" inside the .env file and enter your credentials that can be found on the ElephantSQL website with the format: "postgresql://username:password@hostname/databasename".
4) Add .env file to .gitignore to protect your credentials 
5) Run the Flask web app by entering the command "python app.py"

**Notes:**
**Tutorial how to connect ElephantSQL in pgAdmin4**: https://www.elephantsql.com/docs/pgadmin.html
**Development Website URL**: http://127.0.0.1:5000/
