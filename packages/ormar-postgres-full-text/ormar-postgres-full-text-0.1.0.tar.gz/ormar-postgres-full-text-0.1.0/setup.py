# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ormar_postgres_full_text']

package_data = \
{'': ['*']}

install_requires = \
['ormar[postgresql]==0.11.3']

setup_kwargs = {
    'name': 'ormar-postgres-full-text',
    'version': '0.1.0',
    'description': 'Extension to use full text search from postgresql in ormar ORM.',
    'long_description': '# ormar-postgres-full-text\nExtension to use full text search from postgresql in ormar ORM.\n\n## Install\n\n```shell\npip install ormar-postgres-full-text\n```\n\n## Usage\n\nFor usage example refer to `examples/basic_example/main.py`\n\n## Caveat\n\nTSVector is not a textual data type.\nAlthough you pass a string as the value, postgres would transform it internally and represent it as bag of words, so when retrieving a model containing TSVector, the value will be different than the one you provided initially.\n```\n>>> await FulltextModel.objects.create(text="hello world")\n>>> (await FulltextModel.objects.filter(text__match="hello").first()).text\n"\'hello\' \'world\'"\n```\n',
    'author': 'Jegor Kitskerkin',
    'author_email': 'jegor.kitskerkin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
