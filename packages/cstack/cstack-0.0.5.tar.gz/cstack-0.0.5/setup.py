# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cstack',
 'cstack._internal',
 'cstack.cli',
 'cstack.cli.generators',
 'cstack.core']

package_data = \
{'': ['*'], 'cstack': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'fastapi>=0.87.0,<0.88.0',
 'pydantic[dotenv]>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'tortoise-orm>=0.19.2,<0.20.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['cstack = cstack.cli.app:app']}

setup_kwargs = {
    'name': 'cstack',
    'version': '0.0.5',
    'description': 'Fullstack Python Framework. Built on Python, Vite, and Vue.',
    'long_description': "# 🐍 Cstack - Python made Easy\nAn Opinionated Full Stack Framework for Web Development. Built on Python, Vite, and Vue. \n\nThis stack can be used to create a fullstack application that can be deployed on Deta, or another python hosting.\nIt includes:\n- Monadic Error Handling\n- ORM\n- Testing Library\n- CLI Generator\n- Type Safety\n\n## Project Structure\n```\napp/\n | api/                  -- Python Project\n    | app.py             -- API Entrypoint\n    | models/            -- Database ORM Models\n    | config/            -- Pydantic Configuration\n       | db.py           -- Database Configuration\n       | env.py          -- Environment Variables\n       | settings.py     -- Application Settings\n    | features/          -- Feature Libraries\n    | shared/            -- Shared Code\n    | tests/             -- Pytest Tests\n | view/                 -- Vue Project\n __init__.py             -- Application File\n.env                     -- Env File\ncstack                   -- CLI Tool\npyproject.toml           -- Poetry File\n```\n\n\n### Features\n\nThis is the lifeblood of a Cstack project.\nCstack is feature-driven, rather than layered.\nThe reason is feature code is co-located, rather than spread across directories.\nA feature includes:\n- `__init__.py`\n- `router.py`\n- `services/`\n- `repositories/`\n- `repositories/mocks/`\n- `DTOs/`\n\n#### `router.py`\n\nThis is the fastapi router.\nAll endpoints for this function should be defined here.\n\n#### `services/`\n\nThis is collection of services.\nThese services can be defined as a either a class or as a collection of functions.\nThey should be pure operations, and contain most of the business logic.\nThe reason for purity is testability and portability.\nIf for a reason you move away from Cstack, the code is easily usable again.\nIt also means that the feature logic could be shared if needed.\n\nA service can be generated as well, these are injected into routes through FastAPI's dependency injection.\nA service includes:\n- `{{service_name}}.py`\n- `test_{{service_name}}.py`\n\n#### `repositories/`\n\nA repository communicates with the database. The reason for both repositories and an ORM is it allows the business logic\nto be completely decoupled from the database pattern. This is also means the services are easily testable.\nA repository includes:\n- `{{repository_name}}.py`\n- `mocks/{{repository_name}}.py`\n\nThe mocks folder contains dummy implementations of the repo, for use in testing.\n\n#### `DTOs/`\n\nThis a collection of Pydantic Objects.\nThese are used for communicating data for the given feature.\n\n> ORM Models ARE NOT DTOs. Use a Pydantic Model. Leave ORM code in the Repositories.\n\n### `config/db.py`\n\nAll the database setup code is contained here.\nIt is exposed to the user if the need arises to modify it.\nAll models should import the declared Database base.\n\n### `config/settings.py`\n\nThis includes versioning info, as well as other global settings used in the project.\nThis is instantiated as a singleton, and should only be used through that singleton.\n\n### `config/env.py`\n\nThis is influenced by T3-stack's env folder, where they define a runtime schema for Environment Variables.\nThese variables are defined here, and parsed through Pydantic.\nThis is instantiated as a singleton and should only be used through that singleton.",
    'author': 'Ian Kollipara',
    'author_email': 'ian.kollipara@cune.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
