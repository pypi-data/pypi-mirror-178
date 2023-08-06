# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['github_storage', 'github_storage.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2.16,<=4.1.3']

extras_require = \
{':python_version >= "3.8" and python_full_version <= "3.11.0"': ['requests>=2']}

setup_kwargs = {
    'name': 'django-github-storages',
    'version': '0.3.0',
    'description': 'A Django file storage backend that leverages GitHub.',
    'long_description': '# django-github-storage\n\n![GitHub](https://img.shields.io/github/license/arunim-io/django-github-storage?style=flat-square)\n![GitHub issues](https://img.shields.io/github/issues/arunim-io/django-github-storage?style=flat-square)\n\n> A Django file storage backend that leverages GitHub.\n\n**Note**: It currently works only for media files. Support for static files will soon be added.\n\n## Requirements\n\n- Python 3.6+\n- Django 3.2, 4.0, 4.1\n\nIt is highly recommended to use the latest versions of Python and Django if possible.\n\n## Installation\n\n1. Install the package in 2 ways.\n\n   - Using poetry:\n\n   ```console\n   poetry add django-github-storage\n   ```\n\n   - Using pip:\n\n   ```console\n   pip install django-github-storage\n   ```\n\n2. Include the package in the `INSTALLED_APPS` dict in your `<project-dir>/settings.py`.\n\n```python\nINSTALLED_APPS = [\n    # other apps...\n    \'github_storages\',\n]\n\n```\n\n3. Set the following settings:\n\n```python\nDEFAULT_FILE_STORAGE = "github_storages.backend.BackendStorages"\n\nGITHUB_USERNAME = ""\nGITHUB_ACCESS_TOKEN = ""\nGITHUB_REPO_NAME = ""\nGITHUB_MEDIA_DIRECTORY = ""\n\n```\n\n## Reference\n\n| Settings               | Description                                                                                                                      | Required | Example                  |\n| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------ |\n| GITHUB_USERNAME        | Your GitHub Username                                                                                                             | ✅       | \'arunim-io\'              |\n| GITHUB_ACCESS_TOKEN    | Your GitHub access token (Used for accessing the files). [Click here to get one](#getting-a-access-token-from-github).           | ✅       | \'\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\' |\n| GITHUB_REPO_NAME       | The name of the repository that will be used for storing.(**Warning**: it must be public or else GitHub won\'t accept any files.) | ✅       | \'backend-files\'          |\n| GITHUB_MEDIA_DIRECTORY | The directory inside the repo                                                                                                    | ❌       | \'media\'                  |\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n## 📝 License\n\nCopyright © 2022 [Mugdha Arunim Ahmed](https://github.com/arunim-io).<br />\nThis project is [BSD-3-Clause](https://github.com/arunim-io/django-github-storage/blob/main/LICENSE) licensed.\n',
    'author': 'Mugdha Arunim Ahmed',
    'author_email': 'mugdhaarunimahmed2017@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arunim-io/django-github-storage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<=3.11',
}


setup(**setup_kwargs)
