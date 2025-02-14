import sys
import os

print("PYTHONPATH:")
print("\n".join(sys.path))
print("\nChecking imports...")

try:
    import flask_socketio
    print("flask_socketio: OK")
except ImportError as e:
    print(f"flask_socketio: FAILED - {e}")

try:
    from flaskapp.socketio_app import start_background_task
    print("flaskapp.socketio_app: OK")
except ImportError as e:
    print(f"flaskapp.socketio_app: FAILED - {e}")
