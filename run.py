from collection import create_app, socketio

# Create the app instance via the factory
app = create_app()

if __name__ == '__main__':
    # Use socketio.run instead of app.run
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)