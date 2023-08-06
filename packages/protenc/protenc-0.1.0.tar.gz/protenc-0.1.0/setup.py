# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protenc']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.80,<2.0',
 'lmdb>=1.3.0,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'torch>=1.13.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'protenc',
    'version': '0.1.0',
    'description': 'Simplify extraction of protein embedding from various models.',
    'long_description': "protenc\n=======\n\nprotenc is a library to simplify extraction of protein embeddings from various pre-trained models, including:\n\n* [ProtTrans](https://github.com/agemagician/ProtTrans) family\n* [ESM](https://github.com/facebookresearch/esm)\n* AlphaFold (coming soon™)\n\nIt provides a programmatic Python API as well as a highly flexible bulk extraction script, supporting many input and\noutput formats.\n\n**Note:** the project is work in progress.\n\nUsage\n-----\n\n**Installation**\n\n```bash\npip install protenc\n```\n\n**Python API**\n\n```python\nimport protenc\nimport torch\n\n# List available models\nprint(protenc.list_models())\n\n# Instantiate a model\nmodel = protenc.get_model('esm2_t33_650M_UR50D')\n\nproteins = [\n  'MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG',\n  'KALTARQQEVFDLIRDHISQTGMPPTRAEIAQRLGFRSPNAAEEHLKALARKGVIEIVSGASRGIRLLQEE'\n]\n\nbatch = model.prepare_sequences(proteins)\n\n# Move to GPU if available\nif torch.cuda.is_available():\n  model = model.to('cuda')\n  batch = protenc.utils.to_device(batch, 'cuda')\n\nfor embed in model(batch):\n  # Embeddings have shape [L, D] where L is the sequence length and D the \n  # embedding dimensionality.\n  print(embed.shape)\n  \n  # Derive a single per-protein embedding vector by averaging along the \n  # sequence dimension\n  embed.mean(0)\n```\n\n**Command-line interface**\n\nComing soon.\n\nDevelopment\n-----------\n\nClone the repository:\n\n```bash\ngit clone git+https://github.com/kklemon/protenc.git\n```\n\nInstall dependencies via [Poetry](https://python-poetry.org/):\n\n```bash\npoetry install\n```\n\nTodo\n----\n\n- [ ] Support for more input formats\n  - [X] CSV\n  - [ ] Parquet\n  - [ ] FASTA\n  - [ ] JSON\n- [ ] Support for more output formats\n  - [X] LMDB\n  - [ ] HDF5\n  - [ ] DataFrame\n  - [ ] Pickle\n- [ ] Large models support\n  - [ ] Model offloading\n  - [ ] Sharding\n- [ ] Support for more protein language models\n  - [ ] While ProtTrans family\n  - [ ] While ESM family\n    - [ ] AlphaFold (?)\n- [ ] Implement all remaining TODOs in code\n- [ ] Distributed inference\n- [ ] Maybe support some sort of optimized inference such as quantization\n  - This may be up to the model providers\n- [ ] Improve documentation\n- [ ] Support translation of gene sequences\n",
    'author': 'Kristian Klemon',
    'author_email': 'kristian.klemon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
