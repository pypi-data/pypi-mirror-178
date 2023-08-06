from .protector import Protector
from dotenv import load_dotenv
import os

""" Settings """
api_key = None
default_client = None

load_dotenv()

if "API_KEY" in os.environ:
    api_key = os.getenv("API_KEY")

def auth_check(*args):
  print(*args)
  self = args[0]
  if not hasattr(self, 'api_key') or not self.api_key:
      raise TypeError('Failed to authenticate API key')
  print('DECORATOR SUCCESSFUL AUTH')


def config(*args, **kwargs):
  _proxy('config', *args, **kwargs)

def upload_dataset(*args, **kwargs):
  _proxy('upload_dataset', *args, **kwargs)

def upload_model(*args, **kwargs):
  _proxy('upload_model', *args, **kwargs)

def get_entries(*args, **kwargs):
  _proxy('get_entries', *args, **kwargs)

def get_orgs_and_projects(*args, **kwargs):
  _proxy('get_orgs_and_projects', *args, **kwargs)

def report(*args, **kwargs):
  _proxy('report', *args, **kwargs)

def get_report_status(*args, **kwargs):
  _proxy('get_report_status', *args, **kwargs)

def _proxy(method, *args, **kwargs):
    """Create an analytics client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
      default_client = Protector(api_key)

    fn = getattr(default_client, method)
    fn(*args, **kwargs)
