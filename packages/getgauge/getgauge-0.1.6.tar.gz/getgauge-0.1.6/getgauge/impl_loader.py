import importlib
import json
import os
import py_compile
import shutil
import sys
import traceback
from os import path

PROJECT_ROOT_ENV = 'GAUGE_PROJECT_ROOT'
STEP_IMPL_DIR = 'step_impl'

project_root = os.path.abspath(os.environ[PROJECT_ROOT_ENV])
impl_dir = os.path.join(project_root, STEP_IMPL_DIR)
env_dir = os.path.join(project_root, 'env', 'default')
requirements_file = os.path.join(project_root, 'requirements.txt')
sys.path.append(project_root)
PLUGIN_JSON = 'python.json'
VERSION = 'version'
PYTHON_PROPERTIES = 'python.properties'
SKEL = 'skel'


def load_impls(step_impl_dir=impl_dir):
    os.chdir(project_root)
    for f in os.listdir(step_impl_dir):
        file_path = os.path.join(step_impl_dir, f)
        if f.endswith('.py'):
            import_file(file_path)
        elif path.isdir(file_path):
            load_impls(file_path)


def import_file(file_path):
    rel_path = os.path.normpath(file_path.replace(project_root + os.path.sep, ''))
    try:
        py_compile.compile(file_path)
        importlib.import_module(os.path.splitext(rel_path.replace(os.path.sep, '.'))[0])
    except:
        print('Exception occurred while loading step implementations from file: {}.'.format(rel_path))
        traceback.print_exc()


def copy_skel_files():
    try:
        print('Initialising Gauge Python project')
        print('create  {}'.format(env_dir))
        os.makedirs(env_dir)
        print('create  {}'.format(impl_dir))
        shutil.copytree(os.path.join(SKEL, STEP_IMPL_DIR), impl_dir)
        print('create  {}'.format(os.path.join(env_dir, PYTHON_PROPERTIES)))
        shutil.copy(os.path.join(SKEL, PYTHON_PROPERTIES), env_dir)
        open(requirements_file, 'w').write('getgauge==' + get_version())
    except Exception as e:
        print('Cannot copy skel files, Reason: {}.'.format(e))


def get_version():
    json_data = open(PLUGIN_JSON).read()
    data = json.loads(json_data)
    return data[VERSION]
