# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pylint_blocking_calls']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.15.6,<3.0.0']

setup_kwargs = {
    'name': 'pylint-blocking-calls',
    'version': '0.1.0',
    'description': 'Pylint plugin to detect blocking calls in async functions',
    'long_description': '# Pylint Blocking Calls Checker\n\nThis is a pylint plugin that checks for blocking calls in your async python code.\n\n## Installation\n\nThe best way to install the plugin is to use pip as follows:\n```bash\npip install pylint-blocking-calls\n```\n\n## Usage\n\nLet\'s start with an example:\n\n```python\nimport asyncio\nimport time\n\n\ndef blocking_function():\n    time.sleep(5)  # an example of a IO-bound operation\n\n\nasync def async_function():\n    blocking_function()  # <- This call blocks the event loop!\n\n\ndef some_another_function():\n    blocking_function()\n\n\nasync def async_function2():\n    some_another_function()  # <- This call also implicitly blocks the event loop.\n\n\nasync def main():\n    time_before = time.time()\n    await asyncio.gather(async_function(), async_function2())\n    time_after = time.time()\n\n    # This can take 5 seconds but actually takes 10, because both async functions block the event loop\n    print(f"Time elapsed: {(time_after - time_before):.0f} seconds")\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nSave the file with the name "example.py" and run the following command:\n\n```bash\nBLOCKING_FUNCTION_NAMES="^blocking_function$" pylint --load-plugins=pylint_blocking_calls example.py\n```\n\nThis should provide the following output:\n```bash\n************* Module example\nexample.py:9:4: W0002: blocking_function (blocking-call)\nexample.py:17:4: W0002: some_another_function -> blocking_function (blocking-call)\n```\n\n## Plugin configuration\n\nPlugin supports configuration via the following environment variables:\n```bash\n# required\nexport BLOCKING_FUNCTION_NAMES="" # comma-separated list of regexps that match blocking function names in your project\n\n# optional\nexport SKIP_FUNCTIONS="" # comma-separated list of regexps that match function names that should be skipped\nexport SKIP_MODULES=""  # comma-separated list of regexps that match module names that should be skipped\nexport SKIP_DECORATED="" # comma-separated list of regexps that match decorator names that should be skipped\n```\n\nSee the [tests/test_blocking_calls.py](https://github.com/Edge-Center/pylint-blocking-calls/tests/test_blocking_calls.py) file for a real configuration example.\n\n## Production setup\n\nThe plugin is designed to be used in a CI/CD pipeline.\n\n> **_NOTE:_**  When running on a multiple files, you must run pylint with the single process mode (`--jobs=1`), otherwise there could be a race condition and the plugin may be not working correctly.\n\nConsider the following workaround in production:\n```bash\n# ... as a part of your CI/CD pipeline\nexport BLOCKING_FUNCTION_NAMES="...."\nexport SKIP_FUNCTIONS="...."\nexport SKIP_MODULES="...."\nexport SKIP_DECORATED="...."\n# run pylint with multiple cores for better performance\npylint --disable=blocking-call $(REPO_DIR)/src\n# run pylint with a single core to check for blocking calls\npylint -j 1 --disable=all --enable=blocking-call $(REPO_DIR)/src\n```\n\n## Motivation\n\nThis plugin was created to help us find blocking calls in our async code. \n\nWe use it in our CI pipeline to prevent blocking calls from being merged into the master branch.\n\nPlease share your feedback and ideas in the issues section.\n\n## External links\n\nView the plugin page on [PyPi](https://pypi.org/project/pylint-blocking-calls/).\n',
    'author': 'Aleksei Marashov',
    'author_email': 'marashov-aleksey@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Edge-Center/pylint-blocking-calls',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
