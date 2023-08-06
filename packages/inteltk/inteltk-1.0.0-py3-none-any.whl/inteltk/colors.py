RESET = '\033[0m'
BLACK = "\033[90;1m"
RED = "\033[91;1m"
GREEN = "\033[92;1m"
YELLOW = "\033[93;1m"
BLUE = "\033[94;1m"
MAGENTA = "\033[95;1m"
CYAN = "\033[96;1m"
WHITE = "\033[97;1m"


def printcolor(string: str, color: str = RESET, end: str = "\n"):
    print(color + string.replace(RESET, color) + RESET, end=end)


def inputcolor(string: str, color: str = RESET):
    return input(color + string.replace(RESET, color) + RESET)
