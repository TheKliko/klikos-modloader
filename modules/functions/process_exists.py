# https://stackoverflow.com/a/29275361
# import subprocess
# def process_exists(process: str) -> bool:
#     call = 'TASKLIST', '/FI', 'imagename eq %s' % process
#     output = subprocess.check_output(call, creationflags=subprocess.CREATE_NO_WINDOW).decode()
#     last_line = output.strip().split('\r\n')[-1]
#     return last_line.lower().startswith(process.lower())


# New method to prevent UnicodeDecodeError
import psutil
def process_exists(process: str) -> bool:
    processes = list(p.name() for p in psutil.process_iter())
    count = processes.count(process)
    return count >= 1