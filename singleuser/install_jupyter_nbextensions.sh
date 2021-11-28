
python3 -m pip install jupyter_contrib_nbextensions && \
	jupyter contrib nbextension install --user --symlink && \
	jupyter nbextension enable snippets_menu/main && \
	jupyter nbextension enable codefolding/main && \
	jupyter nbextension enable codefolding/edit && \
	jupyter nbextension enable execute_time/ExecuteTime && \
	jupyter nbextension enable notify/notify && \
	jupyter nbextension enable rubberband/main && \
	jupyter nbextension enable varInspector/main && \
	jupyter nbextension enable latex_envs/latex_envs && \
	jupyter nbextension enable load_tex_macros/main && \
	jupyter nbextension enable toc2/main

