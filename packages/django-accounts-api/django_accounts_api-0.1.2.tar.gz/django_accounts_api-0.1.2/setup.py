# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_accounts_api', 'django_accounts_api.migrations']

package_data = \
{'': ['*'], 'django_accounts_api': ['templates/django_accounts_api/*']}

install_requires = \
['django>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'django-accounts-api',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Django Api Tools\n\nA collection of apps that support basic django functionality over api\n\nCaveat enptor, very early days, still being tested in it's first project\n\n# Use\n\n- `pip install ...`\n- add `'django_accounts_api',` to INSTALLED_APPS\n- add `path('/accounts_api/', include('django_accounts_api.urls'))` to your urls\n\n## Features\n\n### API endpoints\n\nScenario to support is a compiled javascript capable frontend needing to provide authentication features over api\nFrontend should be able to:\n\nOptionally get api endpoints from api.\n\n| Task | How |\n|-----|-----|\n| find api endpoints | GET `/manifest` |\n| Detect auth | GET `/login-check` |\n| show user name | json parse GET `/login-check` response |\n| render a login form | GET `/login` body returns partial HTML |\n| submit a login form | wrap partial form above in a form, `new FormData(...)` it and POST to `/login |\n| render form errors | render partial HTML returned from POST `/login` |\n| login | POST `/login` returns 201 |\n| logout | POST `/logout` |\n\n\n## Development\n1. Install Poetry https://python-poetry.org/docs/#installation\n\n2. Use a virtual environment https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment\n\n3. `poetry install --with test,dev --no-root`\n\n4. `pytest`\n",
    'author': 'PeteCoward',
    'author_email': 'peter@catalpa.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
