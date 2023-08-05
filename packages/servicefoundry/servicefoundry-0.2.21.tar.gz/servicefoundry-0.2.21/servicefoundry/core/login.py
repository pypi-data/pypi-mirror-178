from servicefoundry.core.notebook.notebook_util import get_default_callback
from servicefoundry.lib.session import login as session_login


def login(api_key=None, relogin=False):
    session_login(api_key=api_key, relogin=relogin, output_hook=get_default_callback())
