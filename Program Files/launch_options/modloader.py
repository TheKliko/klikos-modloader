import os
import subprocess
import sys


def main():
    try:
        path = os.path.join(os.path.dirname(sys.executable), 'Program Files', 'main.py')
        launch_arguments = ' '.join(sys.argv[1:])
        command = f'python "{path}" {launch_arguments}'
        if not launch_arguments:
            command = f'python "{path}"'
        subprocess.run(command)


    except Exception as e:
        print(f'An unexpected {type(e).__name__} occured: {str(e)}')
        input('Press ENTER to exit . . .')


if __name__ == '__main__':
    main()