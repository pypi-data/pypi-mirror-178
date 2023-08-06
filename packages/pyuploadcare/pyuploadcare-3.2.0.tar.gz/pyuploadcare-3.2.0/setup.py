# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyuploadcare',
 'pyuploadcare.api',
 'pyuploadcare.dj',
 'pyuploadcare.resources',
 'pyuploadcare.transformations',
 'pyuploadcare.ucare_cli',
 'pyuploadcare.ucare_cli.commands']

package_data = \
{'': ['*'], 'pyuploadcare.dj': ['static/uploadcare/*']}

install_requires = \
['pydantic[email]>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.4,<2023.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['httpx>=0.18.2,<0.19.0',
                                                         'typing-extensions>=3.10.0,<4.0.0'],
 ':python_version >= "3.7" and python_version < "4.0"': ['httpx==0.23.0',
                                                         'typing-extensions>=4.3.0,<5.0.0'],
 'django': ['Django>=1.11']}

entry_points = \
{'console_scripts': ['ucare = pyuploadcare.ucare_cli.main:main']}

setup_kwargs = {
    'name': 'pyuploadcare',
    'version': '3.2.0',
    'description': 'Python library for Uploadcare.com',
    'long_description': '\n<table>\n    <tr style="border: none;">\n        <td style="border: none;">\n            <img src="https://ucarecdn.com/2f4864b7-ed0e-4411-965b-8148623aa680/-/inline/yes/uploadcare-logo-mark.svg" target="" width="64" height="64">\n        </td>\n        <th style="vertical-align: center; border: none;">\n            <h1>PyUploadcare: a Python library for Uploadcare</h1>\n        </th>\n    </tr>\n</table>\n\n<p>\n  <img src="https://badge.fury.io/py/pyuploadcare.svg" height="25" />\n  <img src="https://github.com/uploadcare/pyuploadcare/actions/workflows/test.yml/badge.svg" height="25" /> \n  <img src="https://readthedocs.org/projects/pyuploadcare/badge/?version=latest" height="25" />\n  <img src="https://coveralls.io/repos/github/uploadcare/pyuploadcare/badge.svg?branch=master" height="25" />\n  <img src="https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat" height="25" />\n</p>\n\nUploadcare Python & Django integrations handle uploads and further operations\nwith files by wrapping Upload and REST APIs.\n\nSimple file uploads for the web are of most importance for us. Today, everyone\nis used to the routine of allowing users to upload their pics or attach resumes.\nThe routine covers it all: installing image processing libraries, adjusting\npermissions, ensuring servers never go down, and enabling CDN.\n\nThis library consists of the Uploadcare API interface and a couple of Django\ngoodies.\n\nSimple as that, Uploadcare ``ImageField`` can be added to an\nexisting Django project in just a couple of [simple steps](https://pyuploadcare.readthedocs.org/en/latest/quickstart.html).\nThis will enable your users to see the upload progress, pick files\nfrom Google Drive or Instagram, and edit a form while files are\nbeing uploaded asynchronously.\n\nYou can find an example project [here](<https://github.com/uploadcare/pyuploadcare-example>)`.\n\n[id]: http://b.org/ "title"\n\n```python\n\n    from django import forms\n    from django.db import models\n\n    from pyuploadcare.dj.models import ImageField\n    from pyuploadcare.dj.forms import FileWidget, ImageField as ImageFormField\n\n\n    class Candidate(models.Model):\n        photo = ImageField(blank=True, manual_crop="")\n\n\n    # optional. provide advanced widget options: https://uploadcare.com/docs/uploads/widget/config/#options\n    class CandidateForm(forms.Form):\n        photo = ImageFormField(widget=FileWidget(attrs={\n            \'data-cdn-base\': \'https://cdn.super-candidates.com\',\n            \'data-image-shrink\': \'1024x1024\',\n        }))\n\n```\n\n![](https://ucarecdn.com/dbb4021e-b20e-40fa-907b-3da0a4f8ed70/-/resize/800/manual_crop.png)\n\n## Documentation\n\nDetailed documentation is available [on RTD](<https://pyuploadcare.readthedocs.io/en/latest/>).\n\n\n## Feedback\n\n\nIssues and PRs are welcome. You can provide your feedback or drop us a support\nrequest at [hello@uploadcare.com](hello@uploadcare.com).\n',
    'author': 'Uploadcare Inc',
    'author_email': 'hello@uploadcare.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://uploadcare.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
