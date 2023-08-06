execute python code using string, PyPI test. Instruct how to build a PyPI.
# Python打包上传PyPI
## 注册 PyPI
在[PyPI](https://pypi.org/)注册帐号
## 准备含有 setup.py 的Python 项目
[项目地址](https://github.com/dulingkang/exeu)
目录结构：
![目录结构](./pic/exeu_code_struct.png)

### exeu 目录
exeu 目录为源码目录，一般一个项目下，需要有一个源码目录

### core.py
具体实现文件

core.py 
```python
def ev(s: str):
    return eval(s)
```
实现 eval 的功能。

### init 文件
源码目录下的__init__文件需要引入需要暴露的接口，以及 version 定义。
__init__.py 文件
```python
__version__ = "0.0.1"

from .core import *
```

### setup.py 文件
打包成 PyPI 的配置文件
```python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages
from setuptools import setup

# version
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'exeu', '__init__.py'), 'r') as f:
  init_py = f.read()
version = re.search('__version__ = "(.*)"', init_py).groups()[0]

# obtain long description from README
with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
  README = f.read()

# installation packages
packages = find_packages()

# setup
setup(
  name='exeu',
  version=version,
  description='execute python code using string',
  long_description=README,
  long_description_content_type="text/markdown",
  author='dulingkang',
  author_email='dulingkang@163.com',
  packages=packages,
  python_requires='>=3.7',
  install_requires=[],
  url='https://github.com/dulingkang/exeu',
  project_urls={
    "Bug Tracker": "https://github.com/dulingkang/exeu/issues",
    "Documentation": "https://github.com/dulingkang/exeu",
    "Source Code": "https://github.com/dulingkang/exeu",
  },
  keywords=('exeucate eval, '
            'pipy test, '
            'python instruction, '),
  classifiers=[
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Software Development :: Libraries',
  ],
  license='Apache-2.0 license',
)
```
上述主要参数解析:
- name：库名
- version：版本号
- author：作者
- author_email：作者邮箱（如：发现 bug，可以联系邮箱处理）
- description：简要描述
- long_description：详细描述（一般会写在README.md中）
- long_description_content_type：README.md中描述的语法（一般为markdown)
- install_requires: 依赖的其它 Python 包
- url：库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
- packages：使用setuptools.find_packages()即可，这个是方便以后我们给库拓展新功能的（详情请看官方文档）
- classifiers：指定该库依赖的Python版本、license、操作系统之类的
- license: 使用协议名称

## 安装 PyPI 工具包
install `setuptools` 和 `wheel` 和 `twine`
```
python3 -m pip install --user --upgrade setuptools wheel twine
```

## 打包
打包前，需要先 check setup.py 中有没有错误：
```
python3 setup.py check
```

确认无误后，执行打包：
```
python3 setup.py sdist bdist_wheel
```
完成后，会生成 `dist` 文件夹

## 上传
使用 `twine` 将打好的包上传到 `PyPI`

使用如下命令上传：
```
TWINE_PASSWORD=your_password TWINE_USERNAME=your_name twine upload dist/*
```
`your_name`, `your_password`, 输入第一步在 PyPI注册的用户名和密码。
