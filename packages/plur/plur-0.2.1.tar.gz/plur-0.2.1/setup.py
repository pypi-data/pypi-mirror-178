# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['plur']
install_requires = \
['flake8-pyproject>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'plur',
    'version': '0.2.1',
    'description': '🔢 Simple universal word pluralizer 🔢',
    'long_description': '# plur: 🔢 simple universal word pluralizer 🔢\n\nTired of seeing `1 branch(es) deleted`?\n\nSick of\n\n    es = \'\' if len(branches) == 1 else \'es\'\n    print(f\'{len(branches) branch{es} created\')\n\nor even worse?\n\nTry `plur` for your tiny pluralization needs.\n\n* No dictionary file!\n* No dependencies!\n* No salesperson will call!\n\nExamples:\n\n    import plur\n\n    dogs = [\'fido\', \'rover\']\n    print(plur(\'dog\', dogs))  # prints: 2 dogs\n\n    dogs.pop()\n    print(plur(\'dog\', dogs))  # prints: 1 dog\n\n    dogs.pop()\n    print(plur(\'dog\', dogs))  # prints: 0 dogs\n\n    # Great for f-strings\n\n    dogs = \'fido\', \'rover\'\n    print(f\'Today we have {plur("dog", dogs)}\')\n\nFor words you use a lot, you can quine or defer operation\n\n    dog = plur(\'dog\')\n    cat = plur(\'cat\')\n    ox = plur(\'ox\', \'-en\')\n\n    print(dog(dogs), \'live in my house with\', ox(ox_list))\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
