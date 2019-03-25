import oauth


app = oauth.create_app()

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

