from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080, debug=True)

