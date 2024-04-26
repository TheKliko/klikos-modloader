import os
import subprocess
import sys



# path = os.path.join('Program Files', 'main.py')
# launch_arguments = 'launcher'
# command: str = f'python "{path}" -{launch_arguments}'



def main():
    try:
        # Retrieve launch arguments from command-line arguments
        launch_arguments = ' '.join(sys.argv[1:])  # Join all arguments except the first (which is the script name)
        if not launch_arguments:
            launch_arguments = '-menu'
        
        # Path to main.py
        path = os.path.join('Program Files', 'main.py')
        
        # Construct the command with launch arguments
        command = f'python "{path}" {launch_arguments}'
        
        # Run the command
        subprocess.run(command)
    except Exception as e:
        print(f'An unexpected {type(e).__name__} occured: {str(e)}')
        input()

if __name__ == '__main__':
    main()