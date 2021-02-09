
def confirm(msg):
	print(f"{logcolors.OKGREEN}[NOTICE]: {msg}{logcolors.ENDC}")

def notice(msg):
	print(f"{logcolors.OKCYAN}[NOTICE]: {msg}{logcolors.ENDC}")

def warn(msg):
	print(f"{logcolors.WARNING}[WARNING]: {msg}{logcolors.ENDC}")

def error(msg):
	print(f"{logcolors.FAIL}[ERROR]: {msg}{logcolors.ENDC}")

def log(msg):
	print(f"\t[LOG]: {msg}")
	
class logcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'