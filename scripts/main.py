import argparse
from controller import Controller
from view import ViewCLI

def main():
    parser = argparse.ArgumentParser(description="Translate documents in a folder.")
    parser.add_argument('-l', '--languages', nargs='*', help="List of destination languages", default=[])
    parser.add_argument('-o', '--origin', help="Original language", default='')
    parser.add_argument('-s', '--subfolder', help="Subfolder to translate in 'inputs/'", default='')

    args = parser.parse_args()

    print(args.languages)
    print(args.origin)
    print(args.subfolder)

    view = ViewCLI([])
    if args.languages and args.origin and args.subfolder:
        controller = Controller(args.languages, args.origin, args.subfolder)
        controller.translate_the_folder()
    else:
        while True:
            controller = Controller()
            controller.translate_the_folder()
            if view.user_request_stop():
                break


if __name__ == "__main__":
    main()
