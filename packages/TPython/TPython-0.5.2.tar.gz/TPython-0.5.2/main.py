# Import libs
import sys, subprocess
from os import system, name, get_terminal_size
from traceback import format_exc
try:
    from colorama import init as cinit, Fore
    cinit(autoreset=True)
except ModuleNotFoundError:
    sys.exit('module not found: colorama')
try:
    from requests import get, ConnectionError
except ModuleNotFoundError:
    sys.exit('module not found: requests')

# Vars
n = 1
err = False
a = False
namespace = {}
VERSION = '0.5.2'

# Updater
try:
    pypi_json = get('https://pypi.org/pypi/TPython/json')
    pypi_json = pypi_json.json()
    pypi_version = None
    for i in pypi_json['releases']:
        pypi_version = i
    if pypi_version != VERSION:
        print(f'{Fore.LIGHTCYAN_EX}Newer version of TPython is available: {Fore.LIGHTGREEN_EX}{pypi_version}')
        CHOICE = input(f'{Fore.LIGHTCYAN_EX}Do you want to install {Fore.LIGHTGREEN_EX}{pypi_version}{Fore.LIGHTCYAN_EX} Y/n: {Fore.RESET}').lower().strip()
        if CHOICE in ('y', 'yes', ''):
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'TPython'])
            sys.exit()
except KeyboardInterrupt:
    print(f'\n{Fore.LIGHTYELLOW_EX}KeyboardInterrupt')
    sys.exit()
except ConnectionError:
    pass

# Main Function
def main():
    global n, err, a

    # exit function
    def ext(crash=False):
        cl = get_terminal_size().columns
        m = 'Crashed' if crash else 'Process Completed Successfully'
        for i in range((cl-len(m))//2):
            m = f'-{m}-'
        if len(m) != cl:
            m += '-'
        sys.exit(f'{Fore.LIGHTYELLOW_EX}{"-"*cl}\n{m}\n{"-"*cl}' if crash else f'{Fore.LIGHTCYAN_EX}{m}')

    try:
        # execute function
        def execute(inp):
            global err, n
            run = False
            try:
                print(repr(eval(inp, namespace)))
            except:
                run = True
            if run:
                try:
                    exec(inp, namespace)
                    err = False
                except Exception:
                    print(f'{Fore.LIGHTRED_EX}{format_exc()}')
                    err = True
            n += 1

        # Welcome message
        cl = get_terminal_size().columns
        m = 'Welcome to TPython'
        cl -= 18
        for i in range(cl//2):
            m = f'-{m}-'
        print(f'{Fore.LIGHTCYAN_EX}{m}')

        # Input
        while True:
            try:
                inp = input(f'{Fore.LIGHTGREEN_EX}[{Fore.LIGHTRED_EX if err else Fore.RESET}{n}{Fore.LIGHTGREEN_EX}]-{Fore.LIGHTCYAN_EX}> {Fore.RESET}')
                if not (inp.isspace() or inp == ''):
                    inp = inp.strip()
                    # Exit command
                    if inp in ('exit', 'quit', 'close'):
                        ext()
                    elif inp in ('clear', 'cls'):
                        system('cls' if name == 'nt' else 'clear')
                        err = False
                    # Version command
                    elif inp == 'version':
                        print(f'{Fore.LIGHTCYAN_EX}{VERSION}')
                    else:
                        # Statements that require indents eg: def, if
                        if inp.endswith(':'):
                            while True:
                                ig = input(f'{Fore.LIGHTGREEN_EX}[{Fore.LIGHTYELLOW_EX}{":"*len(str(n))}{Fore.LIGHTGREEN_EX}]-{Fore.LIGHTYELLOW_EX}> {Fore.RESET}')
                                if ig.strip() == '':
                                    if not a:
                                        a = True
                                    else:
                                        break
                                else:
                                    inp += f'\n\t{ig}' if repr(inp).startswith('\t') else f'\n\t{ig}'
                            print(inp)
                            execute(inp)
                            a = False
                        else:
                            execute(inp)
            except KeyboardInterrupt:
                print(f'\n{Fore.LIGHTYELLOW_EX}KeyboardInterrupt')
                err = True
    except Exception:
        print(f'\n{Fore.LIGHTRED_EX}{format_exc()}')
        ext(True)