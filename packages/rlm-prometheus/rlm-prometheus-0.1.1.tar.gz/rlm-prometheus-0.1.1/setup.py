# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rlm_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.1,<2.0.0',
 'prometheus-client>=0.15.0,<0.16.0',
 'python-box>=6.1.0,<7.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['rlm_exporter = rlm_prometheus.cli:run_rlm_exporter']}

setup_kwargs = {
    'name': 'rlm-prometheus',
    'version': '0.1.1',
    'description': 'Prometheus metrics collector and exporter for RLM (Reprise License Manager)',
    'long_description': "# RLM-Prometheus\n\n[Prometheus][1] exporter providing metrics from a Reprise License Manager (RLM)\ninstance.\n\n## Installation\n\nExample installation on Debian / Ubuntu:\n\n```bash\n# required for creating Python virtualenvs:\napt install python3-venv\n\n# create a virtualenv in /opt:\npython3 -m venv /opt/rlm-exporter\n\n# update 'pip' and install the 'rlm-exporter' package:\n/opt/rlm-exporter/bin/pip install --upgrade pip\n/opt/rlm-exporter/bin/pip install rlm-exporter\n```\n\n## Running as a service\n\n```bash\nadduser --system rlmexporter\ncp -v /opt/rlm-exporter/lib/python*/site-packages/resources/systemd/rlm-exporter.service  /etc/systemd/system/\nsystemctl daemon-reload\nsystemctl edit rlm-exporter.service\n```\n\nThe last command will open an editor with the override configuration of the\nservice's unit file. Add a section like this **at the top** of the override\nfile, with the bare minimum of setting `RLM_ISV` and most likely also `RLM_URI`:\n\n```text\n[Service]\n### specific configuration for the RLM exporter service:\nEnvironment=RLM_ISV=example_isv\nEnvironment=RLM_URI=http://license-server.example.xy:5054\n```\n\nFinally enable the service and start it right away. The second line will show\nthe log messages on the console until `Ctrl+C` is pressed. This way you should\nbe able to tell if the service has started up properly and is providing metrics\non the configured port:\n\n```bash\nsystemctl enable --now rlm-exporter.service\njournalctl --follow --unit rlm-exporter\n```\n\n## Firewall settings for RLM on Windows\n\nFor the metrics collection it is obviously necessary the exporter can gather data from\nyour RLM instance. The standard approach is to send requests to RLM's built-in web\nserver. By default access to it is blocked and those restrictions should not be lifted\nmore than necessary.\n\nThere is an example snippet in [Open-RlmFirewallPort.ps1][2] that demonstrates how to\nadjust the Windows firewall so the collector's host IP address is allowed to connect\nto RLM.\n\n[1]: https://prometheus.io/\n[2]: resources/powershell/Open-RlmFirewallPort.ps1\n",
    'author': 'Niko Ehrenfeuchter',
    'author_email': 'nikolaus.ehrenfeuchter@unibas.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/rlm-prometheus/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
