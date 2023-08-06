# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiproof', 'multiproof.tests']

package_data = \
{'': ['*']}

install_requires = \
['eth-abi>=3.0.1,<4.0.0', 'web3>=6.0.0b7,<7.0.0']

setup_kwargs = {
    'name': 'multiproof',
    'version': '0.1.1',
    'description': 'A Python library to generate merkle trees and merkle proofs.',
    'long_description': '# Stakewise python realization of `@openzeppelin/merkle-tree`\n\n## NB! Library is not well tested and not ready for the production use\n\n**A Python library to generate merkle trees and merkle proofs.**\nWell suited for airdrops and similar mechanisms in combination with OpenZeppelin Contracts [`MerkleProof`] utilities.\n\n[`MerkleProof`]: https://docs.openzeppelin.com/contracts/4.x/api/utils#MerkleProof\n\n## Quick Start\n\n``` shell\npoetry install\n```\n\n### Building a Tree\n\n```python\nfrom multiproof import StandardMerkleTree\n\nvalues = [\n    ["0x1111111111111111111111111111111111111111", 5000000000000000000],\n    ["0x2222222222222222222222222222222222222222", 2500000000000000000]\n]\n\ntree = StandardMerkleTree.of(values, ["address", "uint256"])\n\nprint(\'Merkle Root:\', tree.root)\n```\n\n# todos\n- extend tests\n- add docs\n',
    'author': 'StakeWise Labs',
    'author_email': 'info@stakewise.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stakewise/multiproof',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
