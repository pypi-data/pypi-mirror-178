# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_json_logs']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'jsonpath-ng>=1.5.3,<2.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'rich-json-logs',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Readme\n\nColored-logs is a command line tool written in Python that allows to visualize logs in a tabular format. \n\nBy default it tries to parse json logs and extract the relevant columns passed as options. If a list of columns is not provided it uses the default value `@timestamp,log.level,message`. You can also use jsonpath to extract nested json columns (even with `.` in the column name) like `@timestamp,log.logger,$.\'log.origin\'.\'file.name\',message`. In case a column is not present in a json line, the value for that column will be filled with `-` instead.\n\nIn case the logs are not json, it will avoid parsing the text and insert it as the last column of the table.\n\nYou can either use the script to visualize logs from a file on your local filesystem with ndjson format (1 json per line)\n\n```bash\npython main.py -i sample.log\n```\n\n or otherwise read from Stdin using a pipe command\n\n```bash\ncat sample.log | python main.py | less -r\n```\n\nIn the first example, the python script already comes with a pager, while in the second example you need to use an external pager. Here `less -r` supports colored output.\n\n## Install\nYou need to install some required libraries that are listed on requirements.txt\n\n```bash\npip install -r requirements.txt\n```\n\n## Help\nIn order to see the list of supported options, you can issue the following command\n\n```bash\n› python main.py --help                          \nUsage: main.py [OPTIONS]\n\nOptions:\n  -i, --input-path TEXT  Input path\n  -c, --columns TEXT     Columns to filter\n  --help                 Show this message and exit.\n```\n\n## Kubectl plugin\nColored-logs can be used as a kubectl plugin by wrapping it in a bash script\n\n```bash\n#!/bin/bash\n/usr/local/bin/kubectl logs $1 -n $2 --context $3 \\\n        | python main.py \\\n        | less -r\n```\n\nI have attached the following script at `bin/kubectl-rich.sh`. In order to use it as a kubectl plugin, the following script needs to be added to the PATH environment variable.\n\nFinally it can be used as following\n\n```bash\nkubectl rich <pod-name> <namespace> <context>\n```\n\n## K9s plugin\nYou can also use the kubectl plugin here provided as a [K9s plugin](https://k9scli.io/topics/plugins/) by adding the following entry to the `~/.k9s/plugin.xml` file. Once you are inside k9s on the Pod view, you can type `ctrl+j` to use colored-logs to visualize logs in a tabular form. \n\n```bash\nplugin:\n  rich:\n    shortCut: Ctrl-J\n    confirm: false\n    description: "Logs (rich)"\n    scopes:\n      - po\n    command: kubectl\n    background: false\n    args:\n      - rich\n      - $NAME\n      - $NAMESPACE\n      - $CONTEXT\n```',
    'author': 'gsantoro',
    'author_email': 'giuseppe.santoro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
