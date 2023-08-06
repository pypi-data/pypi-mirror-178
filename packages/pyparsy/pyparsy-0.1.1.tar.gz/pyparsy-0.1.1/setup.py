# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyparsy', 'pyparsy.exceptions', 'pyparsy.internal', 'pyparsy.validator']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0',
 'parsel>=1.7.0,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'schema>=0.7.5,<0.8.0']

setup_kwargs = {
    'name': 'pyparsy',
    'version': '0.1.1',
    'description': 'HTML parsing library using YAML definitions and XPath',
    'long_description': '![Logo](https://raw.githubusercontent.com/vkolev/parsy/master/images/parsy-logo.png)\n\n![CI](https://github.com/vkolev/parsy/actions/workflows/main.yml/badge.svg?branch=master) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyparsy) ![PyPI](https://img.shields.io/pypi/v/pyparsy)\n\n# PyParsy\n\nParsy is a HTML parsing library using YAML definition files. The idea is to use the YAML file as\nsort of intent - what you want to have as a result and let Parsy do the heavy lifting for you.\n\nThe YAML files contain:\n- The desired structure of the output\n- XPath variants of the parsed items\n\n## Features\n\n- YAML File definitions\n- Intent instead of coding\n- support for XPath and Regex\n- Different output formats e.g. JSON, YAML, XML\n\n## Installation\n\nUsing pip:\n```shell\npip install pyparsy\n```\n\n## Running Tests\n\nTo run tests, run the following command\n\n```bash\n  poetry run pytest\n```\n\n## Examples\n\nWe can consider as an example the amazon bestseller page. First we define the .yaml definition file:\n\n```yaml\ntitle:\n  selector: //div[contains(@class, "_card-title_")]/h1/text()\n  selector_type: XPATH\n  return_type: STRING\npage:\n  selector: //ul[contains(@class, "a-pagination")]/li[@class="a-selected"]/a/text()\n  selector_type: XPATH\n  return_type: INTEGER\nproducts:\n  selector: //div[@id="gridItemRoot"]\n  selector_type: XPATH\n  multiple: true\n  return_type: MAP\n  children:\n    image:\n      selector: //img[contains(@class, "a-dynamic-image")]/@src\n      selector_type: XPATH\n      return_type: STRING\n    title:\n      selector: //a[@class="a-link-normal"]/span/div/text()\n      selector_type: XPATH\n      return_type: STRING\n    price:\n      selector: //span[contains(@class, "a-color-price")]/span/text()\n      selector_type: XPATH\n      return_type: FLOAT\n    asin:\n      selector: //div[contains(@class, "sc-uncoverable-faceout")]/@id\n      selector_type: XPATH\n      return_type: STRING\n    reviews_count:\n      selector: //div[contains(@class, "sc-uncoverable-faceout")]/div/div/a/span/text()\n      selector_type: XPATH\n      return_type: INTEGER\n```\n\nFor the example sake let\'s store the file as `amazon_bestseller.yaml`.\n\nThen we can use the PyParsy library in out code:\n\n```python\nimport httpx\nfrom pyparsy import Parsy\n\ndef main():\n    html = httpx.get("https://www.amazon.com/gp/bestsellers/hi/?ie=UTF8&ref_=sv_hg_1")\n    parser = Parsy("amazon_bestseller.yaml")\n    result = parser.parse(html.text)\n    print(result)\n    \nif __name__ == "__main__":\n    main()\n```\n\nFor more examples please see the tests for the library.\n\n## Documentation\n\n[Documentation](https://parsy.readthedocs.com) (hopefuly some day)\n\n## Acknowledgements\n\n - [selectorlib](https://selectorlib.com/) - It is the main inspiration for this project\n - [Scrapy](https://scrapy.org/) - One of the best crawling libraries for Python\n - [Tiangolo](https://tiangolo.com/projects) - His projects are real inspiration to produce great software\n\n\n## Contributing\n\n',
    'author': 'Vladimir Kolev',
    'author_email': 'vladimir.r.kolev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vkolev/parsy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
