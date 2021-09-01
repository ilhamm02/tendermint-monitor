import time, os, sys, argparse
from datetime import datetime

args = argparse.ArgumentParser(description='Available Command')
args.add_argument('start', nargs='?', help='run realtime bot monitoring')
args.add_argument('install', nargs='?', help='install this awesome tool')
args.add_argument('--cmd', default='3030', required=True, help='snarkos rpc port (default: 3030)')
args.add_argument('--port', default='127.0.0.1', required=True, type=int, help='snarkos ip (default: 127.0.0.1) ONLY ON STATUS ARGUMENT')
args = args.parse_args()

if arg.start == "install":
  try:
    import requests, colorama
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} There's nothing to do. You have already installed this tool.")
  except ModuleNotFoundError:
    print("Installing dependencies...")
    os.system('pip install colorama requests > /dev/null 2>&1')
    print("Installed! Now you are ready to use this tool.")
elif args.start == "start":
  from colorama import Fore, Style
  if args.cmd and args.port:
    import requests
    block = 0
    attempt = 0
    status = ""
    sleeping = 8
    info = 0
    lastStatus = ""
    endpoint = "http://localhost:"+str(args.port)+"/status"
    while True:
        try:
          get = requests.get(endpoint)
          get = get.json()
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if block < int(get["result"]["sync_info"]["latest_block_height"]):
            lastStatus = "SYNC"
            block = int(get["result"]["sync_info"]["latest_block_height"])
            attempt = 0
            if get["result"]["sync_info"]["catching_up"]:
              print(f"{Fore.YELLOW}[CATCHUP]{Style.RESET_ALL} Highest={block} {now}")
            else :
              print(f"{Fore.GREEN}[SYNCED!]{Style.RESET_ALL} Highest={block} {now}")
          else :
            if lastStatus == "WARNING" :
              attempt += 1
            else :
              attempt = 0
            lastStatus = "WARNING"
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Highest={block} Attempt={attempt} {now}")
          if attempt > 2 :
            os.system("pkill -9 "+args.cmd)
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Highest={block} Attempt={attempt} {now}")
            attempt = 0
          time.sleep(sleeping)
        except KeyboardInterrupt:
          sys.exit(0)
        except requests.exceptions.HTTPError as errh:
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if lastStatus == "TRY":
            attempt +=1
            sys.stdout.write("\033[F")
          else :
            attempt = 0
          lastStatus = "TRY"
          print(f"{Fore.YELLOW}[ RETRY ]{Style.RESET_ALL} Trying to get node status Attempt={attempt} {now}")
          if attempt > 60:
            os.system("pkilll -9 "+args.cmd)
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Tendermint-RPC didn't responding Attempt={attempt} {now}")
            attempt = 0
          time.sleep(1)
        except requests.exceptions.ConnectionError as errc:
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if lastStatus == "TRY":
            attempt +=1
            sys.stdout.write("\033[F")
          else :
            attempt = 0
          lastStatus = "TRY"
          print(f"{Fore.YELLOW}[CONNERR]{Style.RESET_ALL} Trying to get node status Attempt={attempt} {now}")
          if attempt > 60:
            os.system("pkilll -9 "+args.cmd)
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Tendermint-RPC didn't responding Attempt={attempt} {now}")
            attempt = 0
          time.sleep(1)
        except requests.exceptions.Timeout as errt:
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if lastStatus == "TRY":
            attempt +=1
            sys.stdout.write("\033[F")
          else :
            attempt = 0
          lastStatus = "TRY"
          print(f"{Fore.YELLOW}[TIMEOUT]{Style.RESET_ALL} Trying to get node status Attempt={attempt} {now}")
          if attempt > 60:
            os.system("pkilll -9 "+args.cmd)
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Tendermint-RPC didn't responding Attempt={attempt} {now}")
            attempt = 0
          time.sleep(1)
        except requests.exceptions.RequestException as err:
          nowdate = datetime.now()
          now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
          if lastStatus == "TRY":
            attempt +=1
            sys.stdout.write("\033[F")
          else :
            attempt = 0
          lastStatus = "TRY"
          print(f"{Fore.YELLOW}[{err}]{Style.RESET_ALL} Trying to get node status Attempt={attempt} {now}")
          if attempt > 60:
            os.system("pkilll -9 "+args.cmd)
            print(f"{Fore.RED}[RESTART]{Style.RESET_ALL} Tendermint-RPC didn't responding Attempt={attempt} {now}")
            attempt = 0
          time.sleep(1)
  else:
    nowdate = datetime.now()
    now = nowdate.strftime("%H:%M:%S %a %d, %B %Y")
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Please set start,--cmd and --port args {now}")
