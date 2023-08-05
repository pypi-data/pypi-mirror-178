# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keepluggable',
 'keepluggable.storage_file',
 'keepluggable.storage_metadata',
 'keepluggable.web',
 'keepluggable.web.pyramid']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0',
 'bag>=5.0.0',
 'colander>=1.0.0,<2.0.0',
 'kerno>=0.7.0',
 'pillow-heif>=0.8.0',
 'sqlalchemy']

extras_require = \
{'aws': ['awscli>=1.22.0,<1.23.0', 'boto3>=1.20.0,<1.21.0']}

setup_kwargs = {
    'name': 'keepluggable',
    'version': '0.11.1',
    'description': 'Manage storage of images and other files, with metadata.',
    'long_description': '=======================================\nkeepluggable, the reusable file storage\n=======================================\n\n\nScope\n=====\n\n`keepluggable <https://pypi.python.org/pypi/keepluggable>`_ is an open source,\n`(MIT licensed) <http://docs.nando.audio/keepluggable/latest/LICENSE.html>`_,\nhighly configurable Python library to **manage storage of images and\nother documents** (any kind of file, really), with metadata.\n\nThe documentation is at http://docs.nando.audio/keepluggable/latest/\n\nThe file **metadata** can be stored in a different place than the file payload.\nThis is recommended because many operations, such as listing files,\ndo not involve actual file content, so you should avoid loading it.\nAlso, payloads should be optimized for serving and metadata should be\noptimized for querying.\n\nFor file payloads, we currently have implemented one backend that stores\nthem in Amazon S3. There is also a very simple backend that stores\nfiles in the local filesystem (useful during development).\n\nFor (optionally) storing the metadata we currently provide a base SQLAlchemy\nbackend for you to subclass.\n\nIn both cases, you can easily write other storage backends.\n\nUsing this library you can more easily have your user upload images\n(or any kind of file) and enter metadata about them, such as name,\ndescription, date, place, alt text, title attribute etc.\n\nSome of the metadata is automatically found, such as file size, mime type,\nimage size, aspect ratio, MD5 checksum etc.\n\nThe code is highly decoupled so you can tweak the behaviour easily.\n\nThe business rules are implemented in a separate layer\n(isolated from any of the storage strategies and any UI),\ncalled an "action" layer. (This is commonly known as a "service" layer,\nbut we call it "action".) This makes it possible for us to have any\nstorage backends and use any web frameworks or other UI frameworks.\n\nEach application has its own business rules, therefore it is likely that\nyou will subclass the provided action layer to tweak the workflow for\nyour purposes.\n\nOne such "action" is the pluggable policy for uploaded image treatment.\nFor instance, the default policy converts the original uploaded image\nto the JPEG format (so it will never store an unecessarily large BMP),\noptionally stores the original image in whatever size it is, then\ncreates configurable smaller versions of it.\n\nSome cameras do not rotate the photo, they just add orientation metadata to the\nimage file, so keepluggable rotates it for you, before creating the thumbnails.\n\n`Get started with keepluggable! <http://docs.nando.audio/keepluggable/latest/getting_started.html>`_\n\nThere exists a similar library called\n`filedepot <https://pypi.org/project/filedepot/>`_.\n\n\nCollaboration\n=============\n\nWe want your help. We are open to feature requests, suggestions,\n`bug reports <https://github.com/nandoflorestan/keepluggable/issues>`_\nand\n`pull requests <https://github.com/nandoflorestan/keepluggable>`_,\nin reverse order of openness.\n\n\nMigration to keepluggable 0.8\n=============================\n\nkeepluggable 0.8 changes the way files are stored. How?\n\n- It separates namespaces using the "/" character rather than "-". This\n  creates a better user experience in the S3 Management console.\n- Now you can use only one bucket per environment if you wish to.\n  Multiple keepluggable integrations (in a single app) can use the\n  same bucket, because each keepluggable integration can use its\n  own directories.\n- Between the bucket name and the file name you can create your own\n  directory scheme (e. g. "/users/42/avatars/angry_mode/"). I am calling\n  this a "middle path". See the function ``get_middle_path()`` in the\n  *orchestrator.py* file.\n\nA migration function is provided so you can update your old storages\nto keepluggable 0.8. See the method ``migrate_bucket()`` in the file\n*amazon_s3.py*.\n\nThe names of the configuration settings also changed in 0.8.\n',
    'author': 'Nando Florestan',
    'author_email': 'nandoflorestan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nandoflorestan/keepluggable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
