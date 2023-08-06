import os

__version__ = "1.5.6"

USERNAME = os.environ.get("USERNAME", 'root')
HOME = os.environ.get('HOME', f'/home/{USERNAME}' if USERNAME != 'root' else '/root')
ASSISTANT_PATH = f"{HOME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

REPO_PROTOCOL = "https"
REPO_HOST = "gitlab.com"
REPO_BASE_GROUP = "waser-technologies"
REPO_BASE_URL = f"{REPO_PROTOCOL}://{REPO_HOST}/{REPO_BASE_GROUP}"
REPO_DOMAINS = f"{REPO_BASE_URL}/data/nlu" # Where are the domains located
REPO_BASE_DOMAIN_NAME = "smalltalk" # Single base domain name across languages
REPO_MODELS = f"{REPO_BASE_URL}/models" # Where are pre-trained models located
REPO_BASE_MODELS_NAME = "nlu" # Single base models name across languages
REPO_COOKIECUTTERS = "https://gitlab.com/waser-technologies/cookiecutters" # Where are cookiecutter templates located
REPO_BASE_COOKIECUTTER_NAME = "nlu-domain-template" # Single base template name across languages
REPO_BASE_COOKIECUTTER_URL = f"{REPO_COOKIECUTTERS}/{REPO_BASE_COOKIECUTTER_NAME}"
