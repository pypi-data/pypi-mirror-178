# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['np_logging']

package_data = \
{'': ['*']}

install_requires = \
['kazoo>=2.8.0,<3.0.0', 'pyyaml>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'np-logging',
    'version': '0.1.3',
    'description': 'Pre-configured file, web and email logging for neuropixels projects, repackaging code from mpeconfig.',
    'long_description': "```\nimport np_config\n```\n\n`np_config.setup()` will run automatically on import using a default logging config.\n\n- user configs can be specified according to the [`logging` library dict schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)\n\n- the default config is fetched from the\nZooKeeper server `eng-mindscope:2181`\n- configs can be added via ZooNavigator webview:\n  [http://eng-mindscope:8081](http://eng-mindscope:8081)\n- or more conveniently, via an extension for VSCode such as [gaoliang.visual-zookeeper](https://marketplace.visualstudio.com/items?itemName=gaoliang.visual-zookeeper)\n\nZooKeeper configs can be fetched via their path:\n```\ntest_config: dict = np_config.fetch_zk_config(\n    '/projects/np_logging_test/defaults/logging'\n)\n```\n\nOnce a logging config dict has been modified as necessary...\n```\ntest_config['handlers']['email_handler']['toaddrs'] = username@alleninstitute.org\n```\nre-run the logging setup with the new config dict:\n```\nnp_config.setup(\n    config: dict = test_config,\n    project_name = 'test',\n)\n```\n\n- `project_name` must be supplied to use the web logger\n- web log can be viewed at [http://eng-mindscope:8080](http://eng-mindscope:8080)\n\nThe default config provides the loggers `web` and `email`, in addition to the default\n`root` which includes file handlers\nfor info and debug logging levels, plus console logging:\n```\nlogging.getLogger('web').info('test message')\nlogging.getLogger('email').info('test message')\nlogging.debug('test message to files and console')\n```\n\n\nOther parameters to `np_config.setup()`:\n- `log_at_exit` (default `True`)\n\n    - If `True`, a message is logged when the program terminates, reporting total\n      elapsed time.\n\n- `email_at_exit` (default `False`)\n\n    - If `True`, an email is sent when the program terminates, reporting the\n      elapsed time and cause of termination. If an exception was raised, the\n      traceback is included.\n      \n    - If `logging.error`, the email is only sent if the program terminates via an exception.\n\n",
    'author': 'Ben hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'Ben hardcastle',
    'maintainer_email': 'ben.hardcastle@alleninstitute.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
