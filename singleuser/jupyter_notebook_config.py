import os

c.LatexConfig.latex_command = 'pdflatex'
c.NotebookApp.default_url = '/lab'
if os.environ.get("VSCODE", None):
  c.NotebookApp.default_url = '/vscode'
if os.environ.get("RSTUDIO", None):
  c.NotebookApp.default_url = '/rstudio'

# Jupyterlab icons can be created here to launch apps
# that are included in the user's image.
if os.environ.get("VSCODE", None):
  c.ServerProxy.servers = {
    'vscode': {
      'command': [
  		'code-server',
  		'--auth', 'none',
  		'--bind-addr', '0.0.0.0',
  		'--port', '5000'
  	],
      'port': 5000,
      'absolute_url': False,
      'new_browser_tab': True,
      'launcher_entry': {
          'title': 'VSCode',
          },
    }
  }
