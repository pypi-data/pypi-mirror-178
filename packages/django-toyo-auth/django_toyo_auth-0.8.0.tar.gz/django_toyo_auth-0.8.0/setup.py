# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_toyo_auth',
 'django_toyo_auth.providers',
 'django_toyo_auth.providers.iniad',
 'django_toyo_auth.providers.toyo']

package_data = \
{'': ['*']}

install_requires = \
['Django', 'django-allauth']

setup_kwargs = {
    'name': 'django-toyo-auth',
    'version': '0.8.0',
    'description': 'It offers providers of Toyo University and INIAD Accounts for django-allauth',
    'long_description': '# Django Toyo Auth\n\n"Django Toyo Auth" offers providers of Toyo University Accounts(@toyo.jp) and INIAD Accounts(@iniad.org) for [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html)\n\n## Installation\n\n### Install Package\n\n```bash\npip install django-toyo-auth\n```\n\n### settings.py\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'django.contrib.auth\',\n    \'django.contrib.messages\',\n    \'django.contrib.sites\',\n    \'allauth\',\n    \'allauth.account\',\n    \'allauth.socialaccount\',\n    \'django_toyo_auth\',\n    \'django_toyo_auth.providers.iniad\', # INIAD Account\n    \'django_toyo_auth.providers.toyo\', # Toyo Account\n    ...\n]\n\nSITE_ID = 1\n\n# Provider specific settings\nSOCIALACCOUNT_PROVIDERS = {\n    \'iniad\': { # for INIAD Account\n        \'SCOPE\': [\n            \'profile\',\n            \'email\',\n        ],\n        \'AUTH_PARAMS\': {\n            \'access_type\': \'online\',\n        },\n    },\n    \'toyo\': { # for Toyo Account\n        \'SCOPE\': [\n            \'profile\',\n            \'email\',\n        ],\n        \'AUTH_PARAMS\': {\n            \'access_type\': \'online\',\n        },\n    },\n}\n```\n\n### urls.py\n\n```python\nurlpatterns = [\n    ...\n    path(\'accounts/\', include(\'allauth.urls\')),\n    ...\n]\n```\n\n## Classes\n\n### django_toyo_auth.models.AbstractUser\n\nUser class with student_id, entry_year, is_student, is_toyo_member, is_iniad_member\n\n#### Attributes\n\n- student_id\n- entry_year\n- is_student\n- is_toyo_member\n- is_iniad_member\n- grade\n\n### django_toyo_auth.models.UUIDAbstractUser\n\nInherits all attributes and methods from [AbstractUser](#django_toyo_auth.models.AbstractUser),\nbut also primary_key is UUID\n\n#### Attributes\n\n- uuid\n\n### django_toyo_auth.admin.ToyoUserAdmin\n\nModelAdmin class for [AbstractUser](#django_toyo_auth.models.AbstractUser).\nIt offers user-friendly admin pages.\n\n### django_toyo_auth.admin.UUIDToyoUserAdmin\n\nModelAdmin class for [UUIDAbstractUser](#django_toyo_auth.models.UUIDAbstractUser).\nIt offers user-friendly admin pages.\n\n## Details\n\nIt offers only providers and custom models for django-allauth.\nPlease see [django-allauth documents](https://django-allauth.readthedocs.io/en/latest/index.html) for detail\n\n## Requirements\n\n- [Django](https://docs.djangoproject.com/)\n- [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html)\n\n## License\n\nMIT\n',
    'author': 'ayame.space',
    'author_email': 'ayame.space@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/ayame-q/django-toyo-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
