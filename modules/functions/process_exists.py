import subprocess


# https://stackoverflow.com/a/29275361
def process_exists(process: str) -> bool:
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process
    output = subprocess.check_output(call, creationflags=subprocess.CREATE_NO_WINDOW).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process.lower())