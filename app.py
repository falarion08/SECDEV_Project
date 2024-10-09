from src import create_app

app = create_app()

if __name__ == '__main__':
    # Default and for deployment
    app.run(debug=True, host = "0.0.0.0")

    # You can use this if you have a cert.pem and key.pem file in the root.
    # app.run(debug = True, ssl_context =('cert.pem','key.pem'))
    