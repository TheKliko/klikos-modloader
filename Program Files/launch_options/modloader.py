import os
import subprocess
import sys


def main():  # 
    try:  # Retrieve launch arguments from command-line arguments
        path = os.path.join('Program Files', 'main.py')  # Path to main.py
        launch_arguments = ' '.join(sys.argv[1:])  # Join all arguments except the first (which is the script name)
        command = f'python "{path}" {launch_arguments}'
        if not launch_arguments:
            command = f'python "{path}"'
        subprocess.run(command)  # Run the command


    except Exception as e:
        print(f'An unexpected {type(e).__name__} occured: {str(e)}')
        input('Press ENTER to exit . . .')


if __name__ == '__main__':
    main()