
# -*- coding: utf-8 -*-
from setuptools import setup

import codecs

with codecs.open('README.md', encoding="utf-8") as fp:
    long_description = fp.read()
INSTALL_REQUIRES = [
    'aiohttp>=3.8.3',
    'nonebot-adapter-onebot>=2.1.3',
    'nonebot2>=2.0.0b4',
    'aiofiles>=22.1.0',
    'pillow>=9.2.0',
]

setup_kwargs = {
    'name': 'nonebot-plugin-novelai',
    'version': '0.5.7',
    'description': '基于nonebot2的novelai绘图插件',
    'long_description': long_description,
    'license': 'MIT',
    'author': '',
    'author_email': 'sena-nana <851183156@qq.com>',
    'maintainer': None,
    'maintainer_email': None,
    'url': "https://github.com/sena-nana/nonebot-plugin-novelai",
    'packages': [
        'nonebot_plugin_novelai',
        'nonebot_plugin_novelai.backend',
        'nonebot_plugin_novelai.locales',
        'nonebot_plugin_novelai.utils',
        "nonebot_plugin_novelai.extension",
        "nonebot_plugin_novelai.amusement",
        "nonebot_plugin_novelai.outofdate"
    ],
    'package_data': {'': ['*']},
    'long_description_content_type': 'text/markdown',
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.8',

}


setup(**setup_kwargs)
