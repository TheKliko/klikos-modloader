RESET_COLOR: str = "\033[0m"
ERROR_COLOR: str = "\033[38;2;255;107;104m"
WARNING_COLOR: str = "\033[38;2;241;176;12m"


def run(exception: Exception) -> None:
    if type(exception) == SystemExit:
        return
    
    print(ERROR_COLOR+"ERROR: "+type(exception).__name__+"!")
    print(WARNING_COLOR+str(exception))
    print(RESET_COLOR)
    input("Press ENTER to exit . . .")