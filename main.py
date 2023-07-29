from controller import Controller
from view import ViewCLI

def main():
    view = ViewCLI()
    while True:
        controller = Controller()
        controller.translate_the_folder()

        if view.user_request_stop():
            break

if __name__ == "__main__":
    main()
