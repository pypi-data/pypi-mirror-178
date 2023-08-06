import os, sys
import requests

from requests.exceptions import ConnectionError

from .tools import HOME

def checkIfServiceIsOK(host="localhost", port="5005"):
	try:
		r = requests.get(f'http://{host}:{port}')
		return r.ok
	except (ConnectionError, Exception) as e:
		return False

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/user/dmt.service"):
        print("Missing DMT Service")
        print("To download it, type: ")
        print("     wget https://gitlab.com/waser-technologies/technologies/dmt/-/raw/main/dmt.service.example")
        print("     mv dmt.service.example /usr/lib/systemd/user/dmt.service")
        sys.exit(1)
    if not any([
        os.path.exists(f"{HOME}/.config/systemd/user/default.target.wants/assistant.service"),
        os.path.exists("/usr/lib/systemd/user/default.target.wants/assistant.service"),
        checkIfServiceIsOK()
    ]):
        print("DMT Service is disabled")
        print("To enable it, type: ")
        print("     systemctl --user enable --now dmt.service")
        sys.exit(1)
