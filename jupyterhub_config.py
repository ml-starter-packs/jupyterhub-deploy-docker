# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Major edits by MathematicalMichael(.com) 02-2019

# Configuration file for JupyterHub
import os
import sys
from subprocess import check_call
pwd = os.path.dirname(__file__)
c = get_config()


### Helper scripts
def create_group_map(filename='userlist') -> 'Dict[str, List[str]]':
    """
    Parses text file to assign users to groups and creates
    a dictionary where keys are usernames and values are the list
    of group names to which they belong.

    You can use group membership to define policies for shared volumes
    or use an `admin` group to determine which users get root permissions.

    Note that updates to the userlist require restarts for the jupyerhub to
    take effect. This can be inconvenient as an interruption to existing users.
    
    For this reason, we suggest not using `userlist` to manage
    shared volumes but rather setting up an external filesystem on the network
    and managing access through that (give users instructions on how to mount them
    as folders inside their containerized environments), or perhaps opt for
    object storage like s3 and distribute user-keys / credentials and rely on
    CLI or programmatic file access.
    """
    group_map = {}
    # TODO: check if file exists and return empty dictionary if it does not.
    with open(os.path.join(pwd, filename)) as f:
        for line in f:
            if not line:
                continue
            # each line of file is user: group_1 group_2 ...
            parts = line.split()
            # in case of newline at the end of userlist file
            if len(parts) == 0:
                continue
            user_name = parts[0]
            group_map[user_name] = []

            for i in range(1,len(parts)):
                group_name = parts.pop()
                group_map[user_name].append(group_name)
    return group_map


def create_volume_mount(group_id='group', mode='ro', nb_user='jovyan') -> 'Dict[str, Dict[str, str]]':
    volumes = {}
    volume_name = f'shared-{group_id}'
    volume_config = {
        'bind': f'/home/{nb_user}/{volume_name}',
        'mode': mode,
    }
    volumes[volume_name] = volume_config
    return volumes



# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.
HUB_NAME = os.environ['HUB_NAME']
DEFAULT_IMAGE = f'{HUB_NAME}-user'
GROUP_MAP = create_group_map('userlist')

# Allow admin users to log into other single-user servers (e.g. for debugging, testing)?  As a courtesy, you should make sure your users know if admin_access is enabled.
c.JupyterHub.admin_access = True

## Allow named single-user servers per user
c.JupyterHub.allow_named_servers = True

# Allow admin to access other users' containers
c.NotebookApp.allow_remote_access = True

# Optional list of images
ENABLE_DROPDOWN = True
IMAGE_WHITELIST= {
    'default': f"{HUB_NAME}-user",
    'gpu': f"{HUB_NAME}-gpu-user",
    'rstudio+shiny': "r-image",
    'scipy-notebook': "jupyter/scipy-notebook", 
    'tensorflow-notebook': "jupyter/tensorflow-notebook",
    'r-notebook': 'jupyter/r-notebook',
    'base-notebook': "jupyter/base-notebook",
}


# Spawn single-user servers as Docker containers
from dockerspawner import DockerSpawner
class MyDockerSpawner(DockerSpawner):
    def start(self):
        group_list = GROUP_MAP.get(self.user.name, [])
        self.update_volumes(group_list)
        # if 'admin' in group_list:
        #     self.mount_config_files()
        #     self.grant_sudo()
        # self.limit_resources()
        self.update_image_name()
        self.grant_sudo()  # grants sudo to all users!!!
        self.grant_gpu()
        # self.enable_lab()
        return super().start()


    def update_image_name(self):
        """
        Updates the image name from dropdown list (if exists).
        This is required because the `self.start()` method
        updates it but we need access to the variable `self.image`
        prior to startup in order to set extra_host_config (for gpus).
        NOTE: If the check was based on username rather than image name,
        this would not be required (but then GPUs are attached per-user)
        """
        image = self.user_options.get('image')
        if image:
            allowed_images = self._get_allowed_images()
            if allowed_images:
                if image not in allowed_images:
                    raise web.HTTPError(
                        400,
                        "Image %s not in allowed list: %s" % (image, ', '.join(allowed_images)),
                    )
                else:
                    image = allowed_images[image]

        self.image = image

        if self.image in (f"{HUB_NAME}-user", f"{HUB_NAME}-gpu-user"):
            self.environment["VSCODE"] = "1"

        if self.image == "r-image":
            self.environment["RSTUDIO"] = "1"

    def grant_sudo(self):
        """
        Grants sudo permission to current user being spawned.
        """
        self.environment['GRANT_SUDO'] = "1"
        self.extra_create_kwargs.update({"user": "root"})

    def grant_gpu(self):
        if "gpu" in self.image:
            import docker
            self.extra_host_config.update({
                "device_requests": [
                    docker.types.DeviceRequest(
                    count=-1,
                    capabilities=[["gpu"]],
                    driver="nvidia",
                    options={"--gpus":"all"}
                    )],
            })

    def enable_lab(self):
        """
        Sets Jupyterlab as the default environment which users see.
        WARNING: Will not work if ~/.jupyter/jupyter_notebook_config.py exists.
        """
        self.environment['JUPYTER_ENABLE_LAB'] = 'yes'
        self.default_url = '/lab'
        # self.notebook_dir = '/home/jovyan/work'

    def update_volumes(self, group_list):
        for group_id in group_list:
            mode = 'rw' if 'admin' in group_list else 'ro'
            volume = create_volume_mount(group_id, mode, 'jovyan') 
            self.volumes.update(volume)

    def limit_resources(self, mem_limit='8G', cpu_limit=1.0):
        self.mem_limit = mem_limit
        self.cpu_limit = cpu_limit

    def mount_config_files(self, username='jovyan'):
        """
        Allows editing of `jupyterhub_config.py` + `userlist` from
        within the container but relies on using `Shut Down` from
        the admin panel + docker automatically restarting the hub
        in order for changes to take effect. If you make a mistake,
        your hub will become unavailable and you will need to edit
        it by logging into the server hosting the jupyterhub app.
        """
        self.volumes['%s/userlist'%(os.environ['HUB_LOC'])] = \
            { 'bind': f'/home/{username}/userlist', 'mode': 'rw' }
        self.volumes['%s/jupyterhub_config.py'%(os.environ['HUB_LOC'])] = \
            { 'bind': f'/home/{username}/jupyterhub_config.py', 'mode': 'rw' }

c.JupyterHub.spawner_class = MyDockerSpawner

c.DockerSpawner.image = '%s-user'%HUB_NAME
c.DockerSpawner.name_template = '%s-{username}-{servername}-{imagename}'%HUB_NAME
if ENABLE_DROPDOWN:
    c.DockerSpawner.allowed_images = IMAGE_WHITELIST

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = '%s-network'%HUB_NAME
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
# c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'hub-user-{username}': notebook_dir }

# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = HUB_NAME
# The hub will be hosted at example.com/HUB_NAME/ 
# c.JupyterHub.base_url = u'/%s/'%HUB_NAME
c.JupyterHub.base_url = u'/'
#c.JupyterHub.hub_port = 8001

## Authentication 
# Whitlelist users and admins
c.Authenticator.allowed_users = whitelist = set()
c.Authenticator.admin_users = admin = set()

# add default user so that first-time log in is easy.
admin.add('hub-admin')
for name in GROUP_MAP:
    if 'admin' in GROUP_MAP[name]:
        admin.add(name)
    else:
        whitelist.add(name)

# Authenticate users with GitHub OAuth
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Authenticate with thedataincubator/jupyterhub-hashauthenticator
# c.JupyterHub.authenticator_class = 'hashauthenticator.HashAuthenticator'
# You can generate a good "secret key" by running `openssl rand -hex 32` in terminal.
# it is recommended to do this from time-to-time to change passwords (including changing their length)
# c.HashAuthenticator.secret_key = os.environ['HASH_SECRET_KEY']  # Defaults to ''
# c.HashAuthenticator.password_length = int(os.environ['PASSWORD_LENGTH'])          # Defaults to 6
# Can find your password by looking at `hashauthpw --length 10 [username] [key]`
# If the `show_logins` option is set to `True`, a CSV file containing 
# login names and passwords will be served (to admins only) at `/hub/login_list`. 
# c.HashAuthenticator.show_logins = True            # Optional, defaults to False

# TLS config
#c.JupyterHub.port = 8000
#c.JupyterHub.ssl_key = os.environ['SSL_KEY']
#c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

### Database Interaction - cookies, db for jupyterhub
# Persist hub data on volume mounted inside container
data_dir = '/data' # DATA_VOLUME_CONTAINER

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=HUB_NAME,
)


# https://github.com/jupyterhub/jupyterhub-idle-culler
if os.environ['CULL_IDLE'] == "true":
    c.JupyterHub.services = [
        {
            "name": "jupyterhub-idle-culler-service",
            "command": [
                sys.executable,
                "-m", "jupyterhub_idle_culler",
                "--timeout=3600",
            ],
            "admin": True,
        }
    ]
