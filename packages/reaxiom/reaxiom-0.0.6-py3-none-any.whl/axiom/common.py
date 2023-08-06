import os
import glob
import json
import yaml
import shutil
import hashlib
import huggingface_hub as hh
from .settings import config

init_folders = ['obj', 'info', 'huggingface_cache', 'bypy_cache']
for f in init_folders:
    folder = os.path.join(config['axiom_path'], f)
    if not os.path.isdir(folder):
        os.makedirs(folder)

f = os.path.join(config['home'], '.huggingface/token')
if os.path.exists(f):
    token = open(f).read()
else:
    token = 'please run python -m axiom set_huggingface add token to '+f

def upload_to_server(md5, given_name):
    setting_file = os.path.join(config['home'], '.huggingface', 'setting.json')
    hh_setting = json.load(open(setting_file)) # huggingface setting
    obj_file = os.path.join(config['axiom_path'], 'obj', md5)
    info_file = os.path.join(config['axiom_path'], 'info', 'local', given_name, md5+'.yaml')
    hh.upload_file(
        path_or_fileobj=obj_file,
        path_in_repo=md5,
        repo_id=hh_setting['user_name']+'/'+hh_setting['obj_db'],
        repo_type="dataset",
        token=token
    )
    hh.upload_file(
        path_or_fileobj=info_file,
        path_in_repo=given_name+'/'+md5+'.yaml',
        repo_id=hh_setting['user_name']+'/'+hh_setting['info_db'],
        repo_type="dataset",
        token=token
    )


def get_sha256_from_server_by_given_name(given_name):
    setting_file = os.path.join(config['home'], '.huggingface', 'setting.json')
    hh_setting = json.load(open(setting_file)) # huggingface setting
    cache_dir = config['huggingface_cache']
    repo_id_info = hh_setting['user_name']+'/'+hh_setting['info_db']
    sha = hh.dataset_info(repo_id_info).sha
    info_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id_info.replace('/','--'), 'snapshots', sha)
    full_info_folder = os.path.join(info_folder, given_name)
    if not os.path.isdir(full_info_folder):
        hh.snapshot_download(repo_id_info, repo_type='dataset', cache_dir=cache_dir, token=True)
    if not os.path.isdir(full_info_folder):
        return None
    info_files = os.listdir(full_info_folder)
    if len(info_files) > 1:
        print('multiple sha256 files share the same given name', info_files, given_name)
    info_file = os.path.join(full_info_folder, info_files[0])
    
    ya = yaml.safe_load(open(info_file))
    sha256 = ya['sha256']
    target_info_folder = os.path.join(config['axiom_path'], 'info', 'local', given_name)
    if not os.path.isdir(target_info_folder):
        os.makedirs(target_info_folder)
    target_info_file = os.path.join(target_info_folder, sha256+'.yaml')
    yaml.safe_dump(ya, open(target_info_file,'w'))
    cache_info_folder = os.path.join(config['axiom_cache'], sha256)
    if not os.path.isdir(cache_info_folder):
        os.mkdir(cache_info_folder)
    cache_info_file = os.path.join(cache_info_folder, 'info.yaml')
    yaml.safe_dump(ya, open(target_info_file,'w'))
    yaml.safe_dump(ya, open(cache_info_file,'w'))
    return ya['sha256']


def download_obj_from_server(sha256):
    setting_file = os.path.join(config['home'], '.huggingface', 'setting.json')
    hh_setting = json.load(open(setting_file)) # huggingface setting
    cache_dir = config['huggingface_cache']
    repo_id = hh_setting['user_name']+'/'+hh_setting['obj_db']

    hh.hf_hub_download(
        repo_id=repo_id,
        filename=sha256,
        repo_type="dataset",
        cache_dir=cache_dir,
        token=token
    )
    sha = hh.dataset_info(repo_id).sha
    obj_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id.replace('/','--'), 'snapshots', sha)
    extract_folder = os.path.join(config['axiom_cache'], sha256, 'obj')
    if not os.path.isdir(extract_folder):
        os.makedirs(extract_folder)
        md5_full_path = os.path.join(obj_folder, sha256)
        cmd = 'tar zxf %s -C %s' % (md5_full_path, extract_folder)
        print(cmd)
        os.system(cmd)
    return extract_folder
        
    

def get_uuid_by_given_name_in_folder(folder, given_name):
    fs = glob.glob(os.path.join(folder, given_name, '*.yaml'))
    ys = [yaml.safe_load(open(f).read()) for f in fs]
    idx = [i for i in range(len(fs)) if ys[i]['given_name'] == given_name]
    if len(idx) >= 1:
        return os.path.split(fs[idx[0]])[-1][:-5]
    else:
        return None

'''
def get_uuid_by_given_name_from_server(given_name):
    cache_dir = config['huggingface_cache']
    repo_id = 'reaxiom/info'
    cache_dir = config['huggingface_cache']
    hh.snapshot_download(repo_id, repo_type='dataset', cache_dir=cache_dir, token=True)
    sha = hh.dataset_info(repo_id).sha
    info_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id.replace('/','--'), 'snapshots', sha)
    md5, info_file = get_uuid_by_given_name_in_folder(info_folder, given_name)
    print('md5', md5, 'found at:', info_folder)
    axiom_cache_info_folder = os.path.join(config['axiom_cache'], md5)
    if not os.path.isdir(axiom_cache_info_folder):
        os.mkdir(axiom_cache_info_folder)
    axiom_cache_info_file = os.path.join(axiom_cache_info_folder, 'info.yaml')
    remote_cache_info_file = os.path.join(info_folder, md5+'.yaml')
    axiom_info_file = os.path.join(config['axiom_path'], 'info', md5+'.yaml')
    info_content = open(remote_cache_info_file).read()
    open(axiom_cache_info_file, 'w').write(info_content)
    open(axiom_info_file, 'w').write(info_content)
    return md5, info_file
'''


def get_uuid_by_given_name(given_name):
    axiom_path = config['axiom_path']
    md5 = get_uuid_by_given_name_in_folder(os.path.join(axiom_path, 'info', 'local'), given_name)
    if md5 is not None:
        return md5
    print('not found in local path: %s, checking with huggingface' % axiom_path)
    md5 = get_sha256_from_server_by_given_name(given_name)
    if md5 is None:
        print('get_uuid_by_given_name return None')
    return md5

def get_folder_fs(folder):
    fs = []
    for subdir, _, files in os.walk(folder):
        fs += [os.path.join(subdir, f) for f in files]
    return fs

def get_folder_md5(folder):
    md5 = hashlib.sha256()
    size_ = 0
    for subdir, _, files in os.walk(folder):
        for f in files:
            full_name = os.path.join(subdir, f)
            size_ += os.stat(full_name).st_size
            with open(full_name, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
    return md5.hexdigest(), size_



def add_obj_common(folder, to_move=True): # folder with all data but not info.yaml
    # to copy if not to_move,
    # when added form __import the folder is already at axiom cache
    uuid_folder = os.path.split(folder)[0]
    info_file = os.path.join(uuid_folder, 'info.yaml')
    info_yaml = yaml.safe_load(open(info_file))
    if not os.path.exists(info_file):
        if info_file == 'info.yaml':
            info_file = os.path.join('.', info_file)
        print("make sure %s exists" % info_file)
        return None
    obj_folder = os.path.split(folder)[-1]
    cmd = 'cd '+folder+'&& tar zfc ../'+obj_folder+'.tar.gz ./'
    print(cmd)
    os.system(cmd)
    md5, folder_size = get_folder_md5(folder)
    gz_size = os.stat(folder+'.tar.gz').st_size
    info_yaml['original_size'] = folder_size
    info_yaml['compressed_size'] = gz_size
    info_yaml['sha256'] = md5
    shutil.move(folder+'.tar.gz', os.path.join(config['axiom_path'], 'obj', md5))

    if to_move:
        md5_folder = os.path.join(config['axiom_cache'], md5)
        shutil.move(uuid_folder, md5_folder)
    else:
        target_folder = os.path.join(config['axiom_cache'], md5)
        if not os.path.isdir(target_folder):
            shutil.copytree(uuid_folder, target_folder)
    given_name = info_yaml['given_name']
    target_info_path = os.path.join(config['axiom_path'], 'info', 'local', given_name)
    if not os.path.isdir(target_info_path):
        os.makedirs(target_info_path)
    f = os.path.join(target_info_path, md5+'.yaml')
    yaml.safe_dump(info_yaml, open(f,'w'))
    upload_to_server(md5, info_yaml['given_name'])
    print(md5, 'added')


