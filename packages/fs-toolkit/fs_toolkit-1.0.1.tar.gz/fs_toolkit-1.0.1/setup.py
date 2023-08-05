# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fs_toolkit',
 'fs_toolkit.fstab',
 'fs_toolkit.fstab.platform',
 'fs_toolkit.mounts',
 'fs_toolkit.mounts.platform']

package_data = \
{'': ['*']}

install_requires = \
['sys-toolkit>=2.2,<3.0']

setup_kwargs = {
    'name': 'fs-toolkit',
    'version': '1.0.1',
    'description': 'Classes for filesystem usage utilities',
    'long_description': "![Unit Tests](https://github.com/hile/fs-toolkit/actions/workflows/unittest.yml/badge.svg)\n![Style Checks](https://github.com/hile/fs-toolkit/actions/workflows/lint.yml/badge.svg)\n\n# Filesystem information tools\n\nThis module contains utilities to query local filesystem information as python objects,\nincluding mount points, disk usage and fstab contents.\n\n## Installing\n\n```bash\npip install fs-toolkit\n```\n\n## Basic examples\n\nSome usage examples\n\nFstab:\n\n```bash\nfrom fs_toolkit.fstab import Fstab\nfstab = Fstab()\nfstab.get_by_mountpoint('/var/my-secrets').uuid\n```\n\nMounts and df (linked together):\n\n```bash\nfrom fs_toolkit.mounts import Mountpoints\nprint('\\n'.join(f'{mp.usage.used:10} {mp.mountpoint}' for mp in Mountpoints()))\n```\n",
    'author': 'Ilkka Tuohela',
    'author_email': 'hile@iki.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
