# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telefone',
 'telefone.api',
 'telefone.api.request_validator',
 'telefone.api.response_validator',
 'telefone.api.utils',
 'telefone.bot',
 'telefone.bot.blueprint',
 'telefone.bot.dispatch',
 'telefone.bot.dispatch.handlers',
 'telefone.bot.dispatch.labelers',
 'telefone.bot.dispatch.middlewares',
 'telefone.bot.dispatch.return_manager',
 'telefone.bot.dispatch.router',
 'telefone.bot.dispatch.view',
 'telefone.bot.polling',
 'telefone.bot.rules',
 'telefone.bot.states',
 'telefone.bot.states.dispenser',
 'telefone.bot.updates',
 'telefone.contrib',
 'telefone.contrib.rules',
 'telefone.contrib.storage',
 'telefone.errors',
 'telefone.errors.error_handler',
 'telefone.errors.swear_handler',
 'telefone.http',
 'telefone.tools',
 'telefone.tools.keyboard',
 'telefone.tools.storage',
 'telefone.tools.text',
 'telefone.tools.text.formatting',
 'telefone.types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'certifi>=2022.6.15,<2023.0.0',
 'choicelib>=0.1.5,<0.2.0',
 'pydantic>=1.9.0,<2.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{'auto-reload': ['watchfiles>=0.16.0,<0.17.0'],
 'better-performance': ['orjson>=3.7.11,<4.0.0', 'uvloop>=0.16.0,<0.17.0'],
 'file-uploading': ['aiofiles>=22.1.0,<23.0.0'],
 'text-formatting': ['telegram-text>=0.1.0,<0.2.0']}

setup_kwargs = {
    'name': 'telefone',
    'version': '6.3.0',
    'description': 'Asynchronous, feature-rich, high performant Telegram Bot API framework for building stunning bots',
    'long_description': '# < telefone >\n\n<!-- [//]: # (Links to examples)\n[text formatting]: https://github.com/telefone-org/framework/blob/main/examples/high_level/formatting_example.py\n[middleware]: https://github.com/telefone-org/framework/blob/main/examples/high_level/setup_middleware.py\n[file uploading]: https://github.com/telefone-org/framework/blob/main/examples/high_level/file_upload_example.py\n[blueprints]: https://github.com/telefone-org/framework/blob/main/examples/high_level/load_blueprints.py\n[FSM]: https://github.com/telefone-org/framework/blob/main/examples/high_level/use_state_dispenser.py -->\n\n![Version](https://img.shields.io/pypi/v/telefone?label=version&style=flat-square)\n![Package downloads](https://img.shields.io/pypi/dw/telefone?label=downloads&style=flat-square)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/telefone?label=supported%20python%20versions&style=flat-square)\n\n## > why\n\n`telefone` empowers you to build powerful bots using simple tools while not sacrifing performance and extensibility. It has all batteries included: text formatting, file uploading, blueprints, middleware and FSM are available to use right away.\n\n## > examples\n\nIt\'s easy to build an echo bot with `telefone` — it\'s ready in *six* lines of code. And expanding it further is a piece of cake too.\n\n```python\nfrom telefone import Bot\n\nbot = Bot("your-token")\n\n\n@bot.on.message()\nasync def handler(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n```\n\nIsn\'t it beautiful how little code is needed to achieve something this big? To get started on `telefone`, check out our awesome examples.\n\n## > license\n\nThis project is MIT licensed. Special thanks to maintainers and contributors of [vkbottle/vkbottle](https://github.com/vkbottle/vkbottle) upon which it is built!\n\n© **timoniq** (2019-2021); **feeeek** (2022); **exthrempty** (2022)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/telefone/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
