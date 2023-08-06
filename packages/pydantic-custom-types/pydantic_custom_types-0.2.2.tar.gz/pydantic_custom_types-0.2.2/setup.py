# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_custom_types',
 'pydantic_custom_types.active_directory',
 'pydantic_custom_types.dns',
 'pydantic_custom_types.ip',
 'pydantic_custom_types.kubernetes']

package_data = \
{'': ['*']}

install_requires = \
['build>=0.9.0,<0.10.0', 'python-decouple>=3.6,<4.0']

setup_kwargs = {
    'name': 'pydantic-custom-types',
    'version': '0.2.2',
    'description': 'Custom types for pydantic used in SRE peipelins for validation input vars',
    'long_description': '# pydantic custom types\nA collection of custom types for pydantic  \nhttps://github.com/pydantic/pydantic\n\nUseful for validation input parameters for infrastructure pipelines when building kubernetes apps/clusters\n\n## Requirements\n\n`python >= 3.10`\n\n## Installation\n\n`pip install pydantic-custom-types`\n\n## Examples\n\n```python\nfrom pydantic import BaseModel\nfrom pydantic_custom_types.kubernetes import NamespaceName, SecretName\n\nclass K8sNamespace(BaseModel):\n    # These string types only allow: lowercase/numbers/dash, cannot start with dash/number\n    # NamepaceName has linit at 63 characters\n    # SecretName has linit at 63 characters\n    name: NamespaceName \n    secret_name: SecretName\n\n# will pass\nK8sNamespace(\n    name="my-namespace",\n    secret_name="my-secret"\n)\n\n# will not pass\nK8sNamespace(\n    name="-0mynameSpace",\n    secret_name="0mysecret"\n)\n```',
    'author': 'per lejon',
    'author_email': 'per.lejon@netigate.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
