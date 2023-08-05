# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['peakrdl_markdown']

package_data = \
{'': ['*']}

install_requires = \
['py-markdown-table>=0.3.3,<0.4.0', 'systemrdl-compiler>=1.25.0,<2.0.0']

extras_require = \
{'cli': ['peakrdl>=0.3.0,<0.4.0']}

entry_points = \
{'peakrdl.exporters': ['markdown = peakrdl_markdown.__peakrdl__:Exporter']}

setup_kwargs = {
    'name': 'peakrdl-markdown',
    'version': '0.1.0',
    'description': 'Export Markdown description from the systemrdl-compiler register model',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/peakrdl-markdown/badge/?version=latest)](http://peakrdl-markdown.readthedocs.io)\n[![build](https://github.com/MarekPikula/PeakRDL-Markdown/workflows/build/badge.svg)](https://github.com/MarekPikula/PeakRDL-Markdown/actions?query=workflow%3Abuild+branch%3Amain)\n[![Coverage Status](https://coveralls.io/repos/github/MarekPikula/PeakRDL-Markdown/badge.svg?branch=main)](https://coveralls.io/github/MarekPikula/PeakRDL-Markdown?branch=main)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peakrdl-markdown.svg)](https://pypi.org/project/peakrdl-markdown)\n\n# PeakRDL-Markdown\n\nThis package implements Markdown exporter for the PeakRDL toolchain.\n\n- **Export:** Convert compiled SystemRDL input into Markdown description.\n\nFor the command line tool, see the [PeakRDL\nproject](https://peakrdl.readthedocs.io).\n\n## Usage\n\nPeakRDL project provides a standard CLI interface. It can be installed directly\nvia pip or by installing this package with `cli` extra:\n\n    $ pip install peakrdl-markdown[cli]\n\nThen this package can be used with the following command:\n\n    $ peakrdl markdown input_file.rdl -o output_file.md\n\n## Documentation\n\nSee the [PeakRDL-Markdown\nDocumentation](http://peakrdl-markdown.readthedocs.io) for more details.\n',
    'author': 'Marek Pikuła',
    'author_email': 'marek.pikula@embevity.com',
    'maintainer': 'Marek Pikuła',
    'maintainer_email': 'marek.pikula@embevity.com',
    'url': 'https://github.com/MarekPikula/PeakRDL-Markdown',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
