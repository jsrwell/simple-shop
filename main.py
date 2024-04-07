"""
Simple Shop - Django application with PyQt GUI.
"""
import os
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from django.core.management import execute_from_command_line
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')


def open_window():
    """
    Open a PyQt window with a web view of the Django application.

    This function creates a PyQt application and window, loads the Django
    application's URL
    in a web view, and sets up an event handler to terminate the Django server
      when the window
    is closed.

    If an instance of QApplication already exists, this function does nothing.

    Returns:
        None
    """
    if not QApplication.instance():
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.showMaximized()
        view = QWebEngineView()
        view.load(QUrl('http://127.0.0.1:8000/'))
        window.setCentralWidget(view)

        def close_event_handler(event):
            """
            Handle the window close event.

            This function is called when the PyQt window is closed. It
            terminates the Django
            server process by sending a kill command.

            Args:
                event: The close event.

            Returns:
                None
            """
            print("Fechando janela... Encerrando o servidor Django.")
            os.system("taskkill /f /im python.exe")
            print("Servidor Django encerrado.")

        window.closeEvent = close_event_handler
        print("Executando loop de eventos do PyQt...")
        sys.exit(app.exec_())


def start_django_server():
    """
    Start the Django server.

    This function starts the Django server by calling the 'manage.py runserver'
      command.

    Returns:
        None
    """
    print("Iniciando o servidor Django...")
    execute_from_command_line(['manage.py', 'runserver'])


def main():
    """
    Main function to start the application.

    This function checks if a PyQt application instance exists. If not, it
    starts a new instance
    in a separate thread and then starts the Django server.

    Returns:
        None
    """
    if not QApplication.instance():
        gui_thread = threading.Thread(target=open_window)
        gui_thread.start()
    start_django_server()


if __name__ == "__main__":
    main()
