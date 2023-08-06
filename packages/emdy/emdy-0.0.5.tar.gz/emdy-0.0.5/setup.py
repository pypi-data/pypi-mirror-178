# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['emdy']

package_data = \
{'': ['*'],
 'emdy': ['licenses/*',
          'licenses/Creative-Commons-Markdown/*',
          'licenses/Creative-Commons-Markdown/.github/workflows/*',
          'licenses/Creative-Commons-Markdown/1.0/*',
          'licenses/Creative-Commons-Markdown/2.0/*',
          'licenses/Creative-Commons-Markdown/2.5/*',
          'licenses/Creative-Commons-Markdown/3.0/*',
          'licenses/Creative-Commons-Markdown/4.0/*',
          'licenses/markdown-licenses/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'inflect>=6.0.2,<7.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['emdy = emdy.emdy:cli']}

setup_kwargs = {
    'name': 'emdy',
    'version': '0.0.5',
    'description': 'Generate open source and Creative Commons licenses from your command line',
    'long_description': "# Emdy\n\nEmdy generates Markdown-formattted open source and Creative Commons licenses from your command line.\n\n## Installation\n\n### pipx (recommended)\n\nThe recommended, cross-platform way of installing Emdy is via [pipx](https://pypa.github.io/pipx/).\n\n```bash\npipx install emdy\n```\n\n### Homebrew (macOS and Linux)\n\nA [Homebrew](https://brew.sh) formula for Emdy is available from\nthe [Houkago Tea Tap](https://github.com/celsiusnarhwal/homebrew-htt).\n\n```bash\nbrew tap celsiusnarhwal/htt\nbrew install emdy\n```\n\n### pip (not recommended)\n\nEmdy can be installed via pip like any other Python package, but unless you're going to create a virtual environment\nfor it yourself, you're strongly recommeded to use pipx or Homebrew.\n\n```bash\npip install emdy\n```\n\n## Usage\n\nSimply invoke Emdy from the command line:\n\n```bash\nemdy\n```\n\nThat's it. Emdy will interactively guide you through the rest.\n\nSee it in action below.\n\n## Acknowledgements\n\nEmdy sources its Markdown-formatted licenses\nfrom [IQAndreas/markdown-licenses](https://github.com/IQAndreas/markdown-licenses)\nand [idleberg/Creative-Commons-Markdown](https://github.com/idleberg/Creative-Commons-Markdown).\n\n## Disclaimer\n\nLicenses produced by Emdy have been modified from their original forms. I'm not responsible for any legal issues\narising from inconsistencies between Emdy's licenses and those they were derived from.\n\n## License\n\nEmdy is licensed under the [MIT License](https://github.com/celsiusnarhwal/emdy/blob/HEAD/LICENSE.md).",
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/emdy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
