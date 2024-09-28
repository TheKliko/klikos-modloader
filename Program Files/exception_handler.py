from modules.interface import Color


def run(exception: Exception) -> None:
    if type(exception) == SystemExit:
        return
    
    print(Color.ERROR+"ERROR: "+type(exception).__name__+"!")
    print(Color.WARNING+str(exception))
    print(Color.RESET)
    input("Press ENTER to exit . . .")