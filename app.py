from app import create_app

app = create_app()

if __name__ == '__main__':
    # For deployment
    # app.run(debug=True, host = "0.0.0.0")
    
    # For demo
    app.run(debug = True, ssl_context =('cert.pem','key.pem'))
    