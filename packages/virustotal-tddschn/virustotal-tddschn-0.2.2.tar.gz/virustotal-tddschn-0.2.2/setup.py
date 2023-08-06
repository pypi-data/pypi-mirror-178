# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virustotal_tddschn']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['vtpy = virustotal_tddschn.virustotal_sum_search:main']}

setup_kwargs = {
    'name': 'virustotal-tddschn',
    'version': '0.2.2',
    'description': 'VirusTotal Utility Scripts',
    'long_description': "# VirusTotal Utility Library and Command Line Tools\n\n- [VirusTotal Utility Library and Command Line Tools](#virustotal-utility-library-and-command-line-tools)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Utilities](#utilities)\n    - [vtpy](#vtpy)\n      - [Features](#features)\n        - [Homebrew integration](#homebrew-integration)\n        - [macOS specific features](#macos-specific-features)\n      - [Usage](#usage)\n  - [Develop](#develop)\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install virustotal-tddschn\n```\n\n### [pip](https://pypi.org/project/virustotal-tddschn/)\n\n```\n$ pip install virustotal-tddschn\n```\n\n## Utilities\n\n### vtpy\n\n\n#### Features\n\n##### Homebrew integration\n- `--brew` & `--cask`: Parsing Homebrew's DSL `formula` and `cask` files, extracting the package checksum with matching CPU arch\n\n    <details>\n    <summary>Click to expand example</summary>\n\n    ```\n    $ vtpy -w inkscape -B\n    \n    File path:       /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/inkscape.rb\n    SHA256 checksum: 8117d5d864358c9f626ce574d07d2f121ad96fc96a535cc3fddaba3c74bd3279\n    VirusTotal URL:  https://www.virustotal.com/gui/search/8117d5d864358c9f626ce574d07d2f121ad96fc96a535cc3fddaba3c74bd3279\n    ```\n    <!-- Two important rules:\n    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.\n    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->\n    </details>\n\n\n- `--brew-cache`: Locating the `brew`-downloaded package in `brew`'s cache\n\n    <details>\n    <summary>Click to expand example</summary>\n\n    ```\n    $ vtpy -c google-chrome -b firefox -B\n    \n    File path:       /Users/tscp/Library/Caches/Homebrew/downloads/88881e66883c4776fff9b3019b48a26795020439a33ddbedd3bd4620283aecd2--googlechrome.dmg\n    SHA256 checksum: 201739d3cf941d33daf605351160f22bdd5877070267e2b42f37efa661378772\n    VirusTotal URL:  https://www.virustotal.com/gui/search/201739d3cf941d33daf605351160f22bdd5877070267e2b42f37efa661378772\n    ```\n    <!-- Two important rules:\n    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.\n    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->\n    </details>\n\n\n##### macOS specific features\n- `--mac`: Locating binaries inside macOS app bundles (the `.app` directories).\n\n    <details>\n    <summary>Click to expand example</summary>\n\n    ```\n    $ vtpy -m /Applications/kitty.app -B\n    \n    File path:       /Applications/kitty.app/Contents/MacOS/kitty\n    SHA256 checksum: ca6aabac5bd9cd9dde7e3c713eae2031aabec08129218817aecbccb5408b3b0b\n    VirusTotal URL:  https://www.virustotal.com/gui/search/ca6aabac5bd9cd9dde7e3c713eae2031aabec08129218817aecbccb5408b3b0b\n    ```\n    <!-- Two important rules:\n    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.\n    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->\n    </details>\n\n\n#### Usage\n\n```\n$ vtpy --help\n\nusage: vtpy [-h] [--hash HASH] [-f FILE] [-b browser] [-B] [-ldl] [-w BREW] [-C] [-c BREW] [-m APP] [-F PATH] [-V]\n\nSearch file or Homebrew package checksum on VirusTotal\n\noptions:\n  -h, --help            show this help message and exit\n  --hash HASH           The hash to search (default: None)\n  -f FILE, --file FILE  The file to hash and check (default: None)\n  -b browser, --browser browser\n                        Browser to open URLs (default: chrome)\n  -B, --no-browser      Do not open URLs in a browser (default: False)\n  -ldl, --latest-download\n                        Use the latest downloaded file (default: False)\n  -w BREW, --brew BREW  Use the checksum in Homebrew formula or cask file (default: None)\n  -C, --cask            Use cask (default: None)\n  -c BREW, --brew-cache BREW\n                        Use brew downloaded cache (default: None)\n  -m APP, --mac APP     Path to app bundle (default: None)\n  -F PATH, --brew-file PATH\n                        Use the checksum in the brew formula or cask file (default: None)\n  -V, --version         show program's version number and exit\n```\n\n\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/virustotal-tddschn.git\n$ cd virustotal-tddschn\n$ poetry install\n```",
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/virustotal-tddschn',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
