"""
If you want only pip package installed, run `get_pip` and it is fast to
generate.
If you need '~/scripts/pip.exe' etc., run `get_pip_scripts`. Note that `get_pip_
scripts` can only generate pip scripts, no package being installed; you may
need also to run `get_pip` after that.

References:
    ~/docs/depsland-venv-setup.md
    
FIXME:
    All static links in this script should be replaced with source-selectable
    links.
"""
import os
import shutil
from os.path import dirname
from os.path import exists

from lk_utils import find_dirs
from lk_utils import find_files
from lk_utils import run_cmd_shell

from .downloader import download
from .downloader import extract
from .path_model import assets_model
from .pyversion import PyVersion

""" Notice of Extracting whl/tar Files

Example:
    ~/assets/pip_suits/python3
    |
    |
    |- pip-21.3.1-py3-none-any.whl  # 1.1. download whl file
    |= pip  # 1.2. extract whl file (notice there're two dirs)
        |= pip
        |= pip-21.3.1.dist-info
    |
    |
    |- pip-21.3.1.tar.gz  # 2.1. download tar file
    |= pip_src  # 2.2. extract tar file
        |= pip-21.3.1  # 2.3. we will rename it to 'pip'. see `download_pip_src`
            |- setup.py
            |- ...
        |- @PaxHeader
    |
    |
    |- setuptools-58.0.4-py3-none-any.whl  # 3.1
    |= setuptools  # 3.2 (notice there're four dirs and one file)
        |= _distutils_hack
        |= pkg_resources
        |= setuptools
        |= setuptools-58.0.4.dist-info
        |- distutils-precedence.pth
    |
    |
    |- urllib3-1.25.9-py2.py3-none-any.whl  # 4.1
    |= urllib3  # 4.2
        |= urllib3
        |= urllib3-1.25.9.dist-info
"""


def download_setuptools(pyversion: PyVersion):
    """ Download and extract setuptools.
    """
    if pyversion.major == 2:
        name = 'setuptools-45.0.0-py2.py3-none-any.whl'
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/af/e7/02db816dc88c' \
               '598281bacebbb7ccf2c9f1a6164942e88f1a0fded8643659/setuptools-4' \
               '5.0.0-py2.py3-none-any.whl'
    elif pyversion.major == 3:
        name = 'setuptools-58.0.4-py3-none-any.whl'  # 2021-09-09
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/c4/c1/aed7dfedb18e' \
               'a73d7713bf6ca034ab001a6425be49ffa7e79bbd5999f677/setuptools-5' \
               '8.0.4-py3-none-any.whl'
    else:
        raise Exception(pyversion)
    
    file = download(
        link, dirname(assets_model.setuptools_in_pip_suits) + '/' + name)
    dir_ = extract(file, assets_model.setuptools_in_pip_suits)
    return f'{dir_}/setuptools'


def download_pip_src(pyversion: PyVersion):
    if pyversion.major == 2:
        name = 'pip-20.3.4.tar.gz'
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/53/7f/55721ad0501a' \
               '9076dbc354cc8c63ffc2d6f1ef360f49ad0fbcce19d68538/pip-20.3.4.t' \
               'ar.gz'
    elif pyversion.major == 3:
        name = 'pip-21.3.1.tar.gz'  # updated 2021-10-25
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/da/f6/c83229dcc363' \
               '5cdeb51874184241a9508ada15d8baa337a41093fab58011/pip-21.3.1.t' \
               'ar.gz'
    else:
        raise Exception(pyversion)
    
    file = download(
        link, dirname(assets_model.pip_src_in_pip_suits) + '/' + name)
    dir_ = extract(file, assets_model.pip_src_in_pip_suits, type_='tar')
    
    sole_sub_dir_before = f'{dir_}/{name.replace(".tar.gz", "")}'
    sole_sub_dir_after = f'{dir_}/pip'
    if exists(sole_sub_dir_before):
        os.rename(sole_sub_dir_before, sole_sub_dir_after)
    return sole_sub_dir_after


def download_pip(pyversion: PyVersion):
    if pyversion.major == 2:
        name = 'pip-20.3.4-py2.py3-none-any.whl'
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/27/79/8a850fe34964' \
               '46ff0d584327ae44e7500daf6764ca1a382d2d02789accf7/pip-20.3.4-p' \
               'y2.py3-none-any.whl'
    elif pyversion.major == 3:
        name = 'pip-21.3.1-py3-none-any.whl'  # updated 2021-10-25
        link = 'https://pypi.tuna.tsinghua.edu.cn/packages/a4/6d/6463d49a933f' \
               '547439d6b5b98b46af8742cc03ae83543e4d7688c2420f8b/pip-21.3.1-p' \
               'y3-none-any.whl'
    else:
        raise Exception(pyversion)
    
    file = download(
        link, dirname(assets_model.pip_in_pip_suits) + '/' + name)
    dir_ = extract(file, assets_model.pip_in_pip_suits)
    return f'{dir_}/pip'


def download_urllib3_compatible(pyversion: PyVersion):
    """
    References:
        https://blog.csdn.net/shizheng_Li/article/details/115838420
    """
    if pyversion.major == 2:
        print(':v2', 'no need to download urllib3 compatible version')
        return
    
    name = 'urllib3-1.25.9-py2.py3-none-any.whl'
    link = 'https://pypi.tuna.tsinghua.edu.cn/packages/e1/e5/df302e8017440f11' \
           '1c11cc41a6b432838672f5a70aa29227bf58149dc72f/urllib3-1.25.9-py2.p' \
           'y3-none-any.whl'
    file = download(
        link, dirname(assets_model.urllib3_in_pip_suits) + '/' + name)
    dir_ = extract(file, assets_model.urllib3_in_pip_suits)
    return f'{dir_}/urllib3'


# ------------------------------------------------------------------------------

def get_setuptools():
    return copy_resources(
        assets_model.setuptools_in_pip_suits,
        assets_model.site_packages,
    )


def get_pip_scripts():
    run_cmd_shell('cd "{pip_src_dir}" & "{python}" setup.py install'.format(
        pip_src_dir=assets_model.pip_src_in_pip_suits + '/' + 'pip',
        python=assets_model.python,
    ).replace('/', '\\'))
    
    assert exists(assets_model.pip_script)
    
    # find and remove pip egg dir in site-packages
    for d in find_dirs(assets_model.site_packages):
        if d.name.startswith('pip-') and d.name.endswith('.egg'):
            shutil.rmtree(d.path)
            break
    
    return assets_model.pip_script


def get_pip():
    return copy_resources(
        assets_model.pip_in_pip_suits,
        assets_model.site_packages,
    )


def replace_urllib3():
    if exists(x := assets_model.urllib3 + '_bak'):
        print(':v3', '"urllib3_bak" dir already exists. you need to delete the '
                     'then try again.')
        return x
    os.rename(
        assets_model.urllib3,
        assets_model.urllib3 + '_bak'
    )
    return copy_resources(
        assets_model.urllib3_in_pip_suits,
        assets_model.pip_vendor,
        exclusions=('urllib3-1.25.11.dist-info',)
    )


def copy_resources(parent_dir_i, parent_dir_o, exclusions=()):
    out = []
    
    for d in find_dirs(parent_dir_i):
        if d.name in exclusions:
            continue
        dp_i, dp_o = d.path, f'{parent_dir_o}/{d.name}'
        shutil.copytree(dp_i, dp_o)
        out.append(dp_o)
    
    for f in find_files(parent_dir_i):
        if f.name in exclusions:
            continue
        fp_i, fp_o = f.path, f'{parent_dir_o}/{f.name}'
        shutil.copyfile(fp_i, fp_o)
        out.append(fp_o)
    
    return out
