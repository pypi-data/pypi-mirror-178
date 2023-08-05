import os
import sys
import uuid
import yaml
import json
import glob
import shutil
import pandas as pd
import axiom.common
from itertools import chain

from axiom.settings import config

def main(sys_argv):
    if len(sys_argv) == 1:
        lines = open(__file__).read().split('\n')
        lines = [line for line in lines if line.find('if sys_argv[1]') > 0][1:]
        cmds = [line.split("'")[1].split("'")[0] for line in lines]
        comments = [line.split("#")[-1] for line in lines]
        usages = [cmds[i]+': '+comments[i] for i in range(len(cmds))]
        print('\n'.join(usages))
        sys.exit()

    if sys_argv[1] == 'info': # show basic info of the project
        print('my file name', __file__)
        print('config', config)

    def compile(txt):
        from axiom.settings import config
        folder = str(uuid.uuid4())
        os.makedirs(os.path.join(folder, 'obj'))
        me, code_txt = txt.split('##__AXIOM_INFO_END__\n')
        code_txt = code_txt.split('##__AXIOM_FUNCTION_END__')[0]
        print('me'.center(50,'='))
        print(me)
        print('code'.center(50,'='))
        print(code_txt)
        open(os.path.join(folder, 'obj', 'main.py'),'w').write(code_txt)
        info_file = os.path.join(folder, 'info.yaml')

        me = me[me.find('=')+1:]
        yaml.safe_dump(json.loads(me), open(info_file, 'w'))
        print('info_file', info_file)
        axiom.common.add_obj_common(os.path.join(folder, 'obj'))

    if sys_argv[1] == 'compile':
        txt = open(sys_argv[2]).read()
        blocks = txt.split('##__AXIOM_BLOCK_BEGIN__')[1:]
        blocks = [b.split('##__AXIOM_BLOCK_END__')[0] for b in blocks]
        for b in blocks:
            compile(b)

    if sys_argv[1] == 'what': # show what can we show
        fs = glob.glob(os.path.join(config['axiom_path'], 'info', '*'))
        yamls = [yaml.safe_load(open(f).read()) for f in fs]
        if len(sys_argv) == 2:
            keys = [list(y.keys()) for y in yamls]
            print(list(set(list(chain.from_iterable(keys)))))
        if len(sys_argv) == 3:
            obj_properties = []
            for y in yamls:
                x = y[sys_argv[2]]
                if isinstance(x, list):
                    obj_properties += x
                else:
                    obj_properties.append(x)

            obj_properties = sorted(list(set(obj_properties)))
            print('\n'.join(obj_properties))

    if sys_argv[1] == 'template': # axiom template report_matrix, add a function template at the current folder
        func_name = sys_argv[2]
        os.mkdir(func_name)
        open(os.path.join(func_name, '__main.py'), 'w').write(template_main)
        open(os.path.join(func_name, 'info.yaml'), 'w').write(template_info)
        open(os.path.join(func_name, '__INCLUDE__'), 'w').write('external folder')
        open(os.path.join(func_name, 'config.yaml'), 'w').write('{}')

    def list_axiom(axiom_path):
        print('------------', 'axiom_path')
        print(axiom_path)
        fs = glob.glob(os.path.join(axiom_path, '*.yaml'))
        ys = [yaml.safe_load(open(f).read()) for f in fs]
        md5s = [os.path.split(f)[-1][:-5] for f in fs]
        columns = ['given_name', 'type', 'description']
        d = {}
        for i in range(len(fs)):
            d[md5s[i]] = [ys[i]['given_name'], ys[i]['type'], ys[i]['description']]
        df = pd.DataFrame.from_dict(d, orient='index', columns=columns)
        print(df)

    if sys_argv[1] == 'ls': # show the axiom.obj
        if len(sys_argv) == 3:
            axiom_path = sys_argv[2]
        else:
            axiom_path = config['axiom_path']
        list_axiom(os.path.join(axiom_path, 'info'))

    if sys_argv[1] == 'lsb': # list all the objects at huggingface axiom/info
        list_axiom(axiom.common.config['bypy_cache'])

    if sys_argv[1] == 'add': # add the current folder as the obj
        axiom.common.add_obj_common(sys_argv[2], to_move=False)

    if sys_argv[1] == 'rm': # remove a md5 obj
        md5 = sys_argv[2]
        os.remove(os.path.join(config['axiom_path'], 'obj', md5))
        os.remove(os.path.join(config['axiom_path'], 'info', md5+'.yaml'))
        shutil.rmtree(os.path.join(config['axiom_cache'], md5))

    if sys_argv[1] == 'extract': # exting an object to the corrent folder
        md5 = sys_argv[2]
        f = os.path.join(config['axiom_path'], 'obj', md5)
        cmd = 'cp %s ./&& tar zfx %s&&rm %s' % (f, md5, md5)
        print(cmd)
        os.system(cmd)


    if sys_argv[1] == 'commit': # upload an md5 to bypy
        md5 = sys_argv[2]
        axiom.common.upload_to_server(md5)

    def run_python_block(txt):
        file_name = str(uuid.uuid4())
        open(file_name, 'w').write(txt)
        os.system('python '+file_name)
        os.remove(file_name)

    if sys_argv[1] == 't': # test a file with __AXIOM__BLOCK__BEGIN__ block, with test
        txt = open(sys_argv[2]).read()
        blocks = txt.split('##__AXIOM_BLOCK_BEGIN__')[1:]
        blocks = [b.split('##__AXIOM_BLOCK_END__')[0] for b in blocks]
        for b in blocks:
            run_python_block(b)

    if sys_argv[1] == 'aaa':
        import huggingface_hub as hh
        cache_dir = config['huggingface_cache']
        repo_id = 'reaxiom/info'
        hh.snapshot_download(repo_id, repo_type='dataset', cache_dir=cache_dir, token=True)
        sha = hh.dataset_info(repo_id).sha
        info_folder = os.path.join(config['huggingface_cache'], 'datasets--'+repo_id.replace('/','--'), 'snapshots', sha)
        fs = glob.glob(os.path.join(info_folder, '*.yaml'))
        print('info_folder'.center(50, '-'))
        print(info_folder)
        print('\n'.join(fs))

if __name__ == '__main__':
#    main(['a', 'compile', '/Users/test/axiom/master/code/site-package/axiom/example/add_one_func.py'])
    main(sys.argv)
