# < telefone >

<!-- [//]: # (Links to examples)
[text formatting]: https://github.com/telefone-org/framework/blob/main/examples/high_level/formatting_example.py
[middleware]: https://github.com/telefone-org/framework/blob/main/examples/high_level/setup_middleware.py
[file uploading]: https://github.com/telefone-org/framework/blob/main/examples/high_level/file_upload_example.py
[blueprints]: https://github.com/telefone-org/framework/blob/main/examples/high_level/load_blueprints.py
[FSM]: https://github.com/telefone-org/framework/blob/main/examples/high_level/use_state_dispenser.py -->

![Version](https://img.shields.io/pypi/v/telefone?label=version&style=flat-square)
![Package downloads](https://img.shields.io/pypi/dw/telefone?label=downloads&style=flat-square)
![Supported Python versions](https://img.shields.io/pypi/pyversions/telefone?label=supported%20python%20versions&style=flat-square)

## > why

`telefone` empowers you to build powerful bots using simple tools while not sacrifing performance and extensibility. It has all batteries included: text formatting, file uploading, blueprints, middleware and FSM are available to use right away.

## > examples

It's easy to build an echo bot with `telefone` — it's ready in *six* lines of code. And expanding it further is a piece of cake too.

```python
from telefone import Bot

bot = Bot("your-token")


@bot.on.message()
async def handler(_) -> str:
    return "Hello world!"

bot.run_forever()
```

Isn't it beautiful how little code is needed to achieve something this big? To get started on `telefone`, check out our awesome examples.

## > license

This project is MIT licensed. Special thanks to maintainers and contributors of [vkbottle/vkbottle](https://github.com/vkbottle/vkbottle) upon which it is built!

© **timoniq** (2019-2021); **feeeek** (2022); **exthrempty** (2022)
