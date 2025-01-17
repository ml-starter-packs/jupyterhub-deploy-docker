c.LatexConfig.latex_command = 'pdflatex'

# Jupyterlab icons can be created here to launch apps
# that are included in the user's image.
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
