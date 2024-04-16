import os
import subprocess



path = os.path.join('Program Files', 'main.py')
launch_arguments = 'setup'
command: str = f'python "{path}" -{launch_arguments}'



def main():
    try:
        subprocess.run(command)
    except Exception as e:
        print(f'An unexpected {type(e).__name__} occured: {str(e)}')
        input()

if __name__ == '__main__':
    main()