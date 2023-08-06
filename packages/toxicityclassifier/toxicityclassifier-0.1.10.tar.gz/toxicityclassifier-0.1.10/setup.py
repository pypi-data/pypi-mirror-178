# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toxicityclassifier']

package_data = \
{'': ['*'], 'toxicityclassifier': ['models/*']}

setup_kwargs = {
    'name': 'toxicityclassifier',
    'version': '0.1.10',
    'description': 'Module encoding and encrypting text by key',
    'long_description': '# ToxicityClassificator\nModule for predicting toxicity messages in Russian and English\n## Usage example\n```python\nfrom toxicityclassifier import *\n\nclassifier = ToxicityClassificator()\n\nprint(classifier.predict(text))          # (0 or 1, probability)\nprint(classifier.get_probability(text))  # probability\nprint(classifier.classify(text))         # 0 or 1\n```\n\n## Weights\nWeight for classification (if probability >= weight => 1 else 0)\n```python\nclassifier.weight = 0.5\n```\n\\\nWeight for language detection (English or Russian)\n\nif the percentage of the Russian language >= language_weight, then the Russian model is used, otherwise the English one\n```python\nclassifier.language_weight = 0.5\n```\n',
    'author': 'D1ffic00lt',
    'author_email': 'dm.filinov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/D1ffic00lt/toxicity-classification-module',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
