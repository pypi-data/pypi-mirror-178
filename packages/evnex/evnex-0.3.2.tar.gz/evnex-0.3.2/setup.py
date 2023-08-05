# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evnex', 'evnex.schema', 'evnex.schema.v3']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<0.24',
 'pycognito>=2022.11,<2023.0',
 'pydantic>=1.10,<2.0',
 'tenacity>=8.1,<9.0']

setup_kwargs = {
    'name': 'evnex',
    'version': '0.3.2',
    'description': 'A Python wrapper for the EVNEX Cloud API',
    'long_description': '# python-evnex\n\nPython client for the Evnex API.\n\nAuthor not affiliated with Evnex.\n\n## Features \n\n- Talks to your Evnex charger via Cloud API\n- Automatic retries with exponential backoff\n- Automatic re-authentication\n- Optionally pass in a `httpx` client\n- Optionally pass in tokens to resume existing session\n\n## Installation\n\n```\npip install evnex\n```\n\n\n## Usage\n\n```python\nimport asyncio\nfrom pydantic import BaseSettings, SecretStr\nfrom evnex.api import Evnex\n\n\nclass EvnexAuthDetails(BaseSettings):\n    EVNEX_CLIENT_USERNAME: str\n    EVNEX_CLIENT_PASSWORD: SecretStr\n\n\nasync def main():\n    creds = EvnexAuthDetails()\n    evnex = Evnex(username=creds.EVNEX_CLIENT_USERNAME,\n                  password=creds.EVNEX_CLIENT_PASSWORD.get_secret_value())\n\n    user_data = await evnex.get_user_detail()\n\n    for org in user_data.organisations:\n        print("Getting 7 day insight for", org.name, "User:", user_data.name)\n        insights = await evnex.get_org_insight(days=7, org_id=org.id)\n\n        for segment in insights:\n            print(segment)\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n## Examples\n\n`python-evnex` is intended as a library, but a few example scripts are provided in the `examples` folder.\n\nProviding authentication for the examples is via environment variables, e.g. on nix systems:\n\n```\nexport EVNEX_CLIENT_USERNAME=you@example.com\nexport EVNEX_CLIENT_PASSWORD=<your password>\n\npython -m examples.get_charge_point_detail\n```\n\n## Developer Notes\n\n### Making a new release\n\nWhat ends up on PyPi is what really matters. \n\nUpdate the version in `pyproject.toml`, build and publish with poetry:\n\n```shell\npoetry build\npoetry publish\n```\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@hardbyte.nz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hardbyte/python-evnex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
