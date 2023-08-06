# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tesh', 'tesh.tests']

package_data = \
{'': ['*'],
 'tesh.tests': ['fixtures/*', 'fixtures/empty_folder/*', 'fixtures/folder/*']}

install_requires = \
['click', 'pexpect']

entry_points = \
{'console_scripts': ['tesh = tesh:tesh']}

setup_kwargs = {
    'name': 'tesh',
    'version': '0.1.1',
    'description': 'TEstable SHell sessions in Markdown',
    'long_description': '<p align="center">\n  <a href="https://circleci.com/gh/OceanSprint/tesh">\n    <img alt="CircleCI for tesh (main branch)"\n         src="https://circleci.com/gh/OceanSprint/tesh.svg?style=shield">\n  </a>\n  <img alt="Test coverage (main branch)"\n       src="https://img.shields.io/badge/tests_coverage-100%25-brightgreen.svg">\n  <img alt="Test coverage (main branch)"\n       src="https://img.shields.io/badge/types_coverage-100%25-brightgreen.svg">\n  <a href="https://pypi.org/project/tesh/">\n    <img alt="latest version of tesh on PyPI"\n         src="https://img.shields.io/pypi/v/tesh.svg">\n  </a>\n  <a href="https://pypi.org/project/tesh/">\n    <img alt="Supported Python versions"\n         src="https://img.shields.io/pypi/pyversions/tesh.svg">\n  </a>\n  <a href="https://github.com/OceanSprint/tesh/blob/main/LICENSE">\n    <img alt="License: MIT"\n         src="https://img.shields.io/badge/License-MIT-yellow.svg">\n  </a>\n  <a href="https://github.com/OceanSprint/tesh/graphs/contributors">\n    <img alt="Built by these great folks!"\n         src="https://img.shields.io/github/contributors/OceanSprint/tesh.svg">\n  </a>\n</p>\n\n# tesh [[tɛʃ]](http://ipa-reader.xyz/?text=t%C9%9B%CA%83&voice=Joanna) - TEstable SHell sessions in Markdown\n\nShowing shell interactions how to run a tool is useful for teaching and explaining.\n\nMaking sure that example still works over the years is painfully hard.\n\nNot anymore.\n\n```shell-session\n$ tesh demo/\n📄 Checking demo/happy.md\n  ✨ Running foo  ✅ Passed\n  ✨ Running bar  ✅ Passed\n📄 Checking demo/sad.md\n  ✨ Running foo  ❌ Failed\n\n         Expected:\nsad panda\n         Got:\nfoo\n\nTaking you into the shell ...\n\n$\n```\n\n## Syntax\n\nTo mark a code block as testable, append `tesh-session="NAME"` to the header line.\n\nYou can use any syntax highlighting directives like `shell-session` or `console`.\n\n~~~\n```shell-session tesh-session="hello"\n$ echo "Hello World!"\nHello World!\n```\n~~~\n\n### Linking multiple code blocks into a single shell session\n\nBesides marking a code block as testable, `tesh-session` is a unique identifier that allows for multiple code blocks to share the same session.\n\n~~~\n```shell-session tesh-session="multiple_blocks"\n$ export NAME=Earth\n\n```\n~~~\n\n~~~\n```shell-session tesh-session="multiple_blocks"\n$ echo "Hello $NAME!"\nHello Earth!\n```\n~~~\n\n### Ignoring parts of the output\n\nParts of the inline output can be ignored with `...`:\n\n~~~\n```shell-session tesh-session="ignore"\n$ echo "Hello from Space!"\nHello ... Space!\n```\n~~~\n\nThe same can be done for multiple lines of output. Note that trailing whitespace in every line is trimmed.\n\n~~~\n```shell-session tesh-session="ignore"\n$ printf "Hello \\nthere \\nfrom \\nSpace!"\nHello\n...\nSpace!\n```\n~~~\n\n## Advanced directives\n\nYou can set a few other optional directives in the header line:\n\n- `tesh-exitcodes`: a list of exit codes in the order of commands executed inside the code block,\n- `tesh-setup`: a filename of a script to run before running the commands in the code block,\n- `tesh-ps1`: allow an additional PS1 prompt besides the default `$`,\n- `tesh-platform`: specify on which platforms this session block should be tested (`linux`, `darwin`, `windows`),\n- `tesh-fixture`: a filename to save the current snippet.\n\nLet\'s look at all of these through examples\n\n### Testing exit codes\n\n`tesh-exitcodes` accepts a list of integers, which represent the exit code for every command in the block.\n\n~~~\n```shell-session tesh-session="exitcodes" tesh-exitcodes="1 0"\n$ false\n\n$ true\n\n```\n~~~\n\n\n### Test setup\n\nSometimes you need to do some test setup before running the examples in your code blocks. Put those [in a file](./readme.sh) and point to it with the `tesh-setup` directive.\n\n~~~\n```shell-session tesh-session="setup" tesh-setup="readme.sh"\n$ echo "Hello $NAME!"\nHello Gaea!\n```\n~~~\n\n\n### Custom prompts\n\nSometimes you need to drop into a virtualenv or similar shell that changes the prompt. `tesh` supports this via `test-ps1` directive.\n\n~~~\n```shell-session tesh-session="prompt" tesh-ps1="(foo) $"\n$ PS1="(foo) $ "\n\n\n(foo) $ echo "hello"\nhello\n```\n~~~\n\n### Only run on certain platforms\n\nSome examples should only run on certain platforms, use `tesh-platform` to declare them as such.\n\n~~~\n```shell-session tesh-session="platform" tesh-platform="linux"\n$ uname\n...Linux...\n```\n~~~\n\n~~~\n```shell-session tesh-session="platform" tesh-platform="darwin"\n$ uname\n...Darwin...\n```\n~~~\n\n\n## Design decisions\n\n- Supports Linux / macOS.\n- Not tied to a specific markdown flavor or tooling.\n- Renders reasonably well on GitHub.\n\n\n## Comparison with other tools\n\n| | tesh | [mdsh](https://github.com/zimbatm/mdsh) | [pandoc filters](http://www.chriswarbo.net/projects/activecode/index.html) |\n|------------------------------------------|---|---|---|\n| Execute shell session                    | ✔️ | ✔️ | ✔️ |\n| Modify markdown file with the new output | 🚧[<sub>[1]</sub>](https://github.com/OceanSprint/tesh/issues/6) | ✔️ | ✔️ |\n| Shared session between code blocks       | ✔️ | ✖️ | ✖️ |\n| Custom PS1 prompts                       | ✔️ | ✖️ | ✖️ |\n| Assert non-zero exit codes               | ✔️ | ✖️ | ✖️ |\n| Setup the shell environment              | ✔️ | ✖️ | ✖️ |\n| Reference fixtures from other snippets   | ✔️ | ✖️ | ✖️ |\n| Wildcard matching of the command output  | ✔️ | ✖️ | ✖️ |\n| Starts the shell in debugging mode       | ✔️ | ✖️ | ✖️ |\n\n* ✔️: Supported\n* C: Possible but you have to write some code yourself\n* 🚧: Under development\n* ✖️: Not supported\n* ?: I don\'t know.\n\n\n## Developing `tesh`\n\nYou need to have [poetry](https://python-poetry.org/) and Python 3.9 through 3.11 installed on your machine.\n\nAlternatively, if you use [nix](https://nix.dev/tutorials/declarative-and-reproducible-developer-environments), run `nix-shell` to drop into a shell that has everything prepared for development.\n\nThen you can run `make tests` to run all tests & checks. Additional `make` commands are available:\n\n```\n# run tesh on all Markdown files\n$ make tesh\n\n# run flake8 linters on changed files only\n$ make lint\n\n# run flake8 linters on all files\n$ make lint all=true\n\n# run mypy type checker\n$ make types\n\n# run unit tests\n$ make unit\n\n# run a subset of unit tests (regex find)\n$ make unit filter=foo\n\n# re-lock Python dependencies (for example after adding or removing one from pyproject.toml)\n$ make lock\n```\n',
    'author': 'Domen Kozar',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
