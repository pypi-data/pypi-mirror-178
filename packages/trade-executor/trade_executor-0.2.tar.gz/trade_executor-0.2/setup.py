# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradeexecutor',
 'tradeexecutor.analysis',
 'tradeexecutor.backtest',
 'tradeexecutor.cli',
 'tradeexecutor.ethereum',
 'tradeexecutor.monkeypatch',
 'tradeexecutor.state',
 'tradeexecutor.statistics',
 'tradeexecutor.strategy',
 'tradeexecutor.strategy.pandas_trader',
 'tradeexecutor.strategy.qstrader',
 'tradeexecutor.testing',
 'tradeexecutor.utils',
 'tradeexecutor.visual',
 'tradeexecutor.webhook']

package_data = \
{'': ['*'], 'tradeexecutor.ethereum': ['abi/uniswap/*']}

install_requires = \
['ipywidgets>=7.0,<8.0',
 'jupyterlab>=3.5.0,<4.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'pandas-ta>=0.3.14-beta.0,<0.4.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm-loggable>=0.1.1,<0.2.0',
 'tqdm>=4.64.1,<5.0.0',
 'trading-strategy==0.8.5',
 'web3-ethereum-defi>=0.11.1,<0.12.0',
 'web3>=5.26.0,<6.0.0']

extras_require = \
{'execution': ['typer>=0.4.0,<0.5.0',
               'colorama>=0.4.4,<0.5.0',
               'coloredlogs>=15.0.1,<16.0.0',
               'prompt-toolkit>=3.0.31,<4.0.0',
               'APScheduler>=3.9.1,<4.0.0',
               'python-logstash-tradingstrategy>=0.5.0,<0.6.0',
               'python-logging-discord-handler>=0.1.3,<0.2.0',
               'python-dotenv>=0.21.0,<0.22.0'],
 'qstrader': ['trading-strategy-qstrader>=0.5,<0.6'],
 'web-server': ['pyramid>=2.0,<3.0',
                'pyramid-openapi3>=0.13,<0.14',
                'waitress>=2.0.0,<3.0.0',
                'WebTest>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['get-latest-release = '
                     'tradeexecutor.cli.latest_release:main',
                     'prepare-docker-env = '
                     'tradeexecutor.cli.prepare_docker_env:main',
                     'trade-executor = tradeexecutor.cli.main:app']}

setup_kwargs = {
    'name': 'trade-executor',
    'version': '0.2',
    'description': 'Trading strategy execution and backtesting',
    'long_description': '[![.github/workflows/tests.yml](https://github.com/tradingstrategy-ai/trade-executor/actions/workflows/tests.yml/badge.svg)](https://github.com/tradingstrategy-ai/trade-executor/actions/workflows/tests.yml)\n\n# Trade Executor\n\nTrade Executor is a Python framework for executing algorithmic trading strategies on decentralised exchanges. \n\n**Note**: This is early alpha software. Please pop in to the Discord for any questions. \n\n## Features\n\n- [High quality documentation](https://tradingstrategy.ai/docs/)\n- Support [decentralised markets like Uniswap, PancakeSwap](https://tradingstrategy.ai/docs/overview/supported-markets.html) \n- [Live trading](https://tradingstrategy.ai/docs/running/live-trading.html) and [backtesting](https://tradingstrategy.ai/docs/running/backtesting.html)  \n- [Webhook web serverPlain](https://tradingstrategy.ai/docs/running/webhook.html) for web and JavaScript integration\n- Run the strategy execution as [Python application or Docker container](https://tradingstrategy.ai/docs/running/cli.html)\n\n## More information\n\n- [Read documentation on running and backtesting strategies](https://tradingstrategy.ai/docs/running/index.html)\n- Visit [Trading Strategy website to learn about algorithmic trading on decentralised exchanges](https://tradingstrategy.ai)\n- [Join the Discord for any questions](https://tradingstrategy.ai/community)\n\n## Installation\n\n```shell\ngit clone git@github.com:tradingstrategy-ai/trade-executor.git\ncd trade-executor\ngit submodule update --init --recursive\npoetry install -E web-server -E execution\n```\n\n## Architecture overview\n\n![Archiecture overview](docs/deployment-overview.drawio.svg)\n\n## Development\n\nSee [docs](./docs).\n\n## Community\n\n* [Trading Strategy website](https://tradingstrategy.ai)\n\n* [Blog](https://tradingstrategy.ai/blog)\n\n* [Twitter](https://twitter.com/TradingProtocol)\n\n* [Discord](https://tradingstrategy.ai/community#discord) \n\n* [Telegram channel](https://t.me/trading_protocol)\n\n## License \n\n- AGPL\n',
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@tradingstrategy.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://tradingstrategy.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
