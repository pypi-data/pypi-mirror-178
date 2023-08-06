import os
from .settings import config

for k in config:
    if k.endswith('_path') or k.endswith('_cache'):
        if not os.path.isdir(config[k]):
            os.makedirs(config[k])

f = os.path.join(config['home'], '.huggingface/token')
if os.path.exists(f):
    token = open(f).read()
else:
    token = 'please run python -m axiom set_huggingface add token to '+f

server_file = os.path.join(config['axiom_path'], 'server')
if not os.path.exists(server_file):
    open(server_file, 'w').write('local')



local_server_folders = ['obj', 'info', 'sha256_info']
local_server_folders = [os.path.join(config['local_server_path'], x) for x in local_server_folders]
for local_server_folder in local_server_folders:
    if not os.path.isdir(local_server_folder):
        os.makedirs(local_server_folder)

