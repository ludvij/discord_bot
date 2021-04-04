
#! Wip, just a placeholder
#TODO: make this a proper thing

def confirm(msg, tablevel=0):
	tabs = get_tabs(tablevel)
	print(f"{tabs}{logcolors.OKGREEN}[CONFIRM]: {msg}{logcolors.ENDC}")

def notice(msg, tablevel=0):
	tabs = get_tabs(tablevel)
	print(f"{tabs}{logcolors.OKCYAN}[NOTICE]: {msg}{logcolors.ENDC}")

def warn(msg, tablevel=0):
	tabs = get_tabs(tablevel)
	print(f"{tabs}{logcolors.WARNING}[WARNING]: {msg}{logcolors.ENDC}")

def error(msg, tablevel=0):
	tabs = get_tabs(tablevel)
	print(f"{tabs}{logcolors.FAIL}[ERROR]: {msg}{logcolors.ENDC}")

def log(msg, tablevel=1):
	tabs = get_tabs(tablevel)
	print(f"{tabs}[LOG]: {msg}")

def internal(msg, tablevel=1):
	tabs = get_tabs(tablevel)
	print(f'{tabs}{logcolors.OKBLUE}[INTERNAL]: {msg}{logcolors.ENDC}')


def get_tabs(n : int):
	return '\t' * n
	
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