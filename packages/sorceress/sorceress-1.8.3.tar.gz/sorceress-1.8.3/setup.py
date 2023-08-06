# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sorceress']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sorceress',
    'version': '1.8.3',
    'description': 'Python package for creating optical illusions',
    'long_description': '# sorceress 1.8\n\n[![PyPI version](https://badge.fury.io/py/sorceress.svg)](https://badge.fury.io/py/sorceress) [![Jekyll site CI](https://github.com/altunenes/sorceress/actions/workflows/jekyll.yml/badge.svg)](https://github.com/altunenes/sorceress/actions/workflows/jekyll.yml)\n[![Downloads](https://pepy.tech/badge/sorceress)](https://pepy.tech/project/sorceress)\n\n### Purpose of package\n\nThis package\'s purpose is to create optical illusions in a simple way. The package is written in Python. however, the repo also includes JavaScript.  In [explanations](https://altunenes.github.io/sorceress/explanations%20of%20illusions/) section, you can find the explanations of the illusions.\n\nIf you find visual illusions fascinating this package is for you. You can reproduce the illusions in the literature with a few lines of code.\n\nMore importantly, we shouldn\'t take optical illusions as just fun. Optical illusions help us to research how the visual system of the brain ,which is the most complex mechanism, processes such cues. Most of the optical illusions in this package are seriously researched in the neuroscience literature. And I must say that the "causation" of the most of effects is still debated in the literature according to my humble knowledge. Optical illusions are researching not only in human vision but in other animals. So we can get a lot of insights from an evolutionary perspective.\n\nIn summary, I think this topic is very important, especially in vision studies.\n\nFor all optical illusions check this documentation: [altunenes.github.io/sorceress/](https://altunenes.github.io/sorceress/)\n\n### Getting started🚀️\n\nThe package can be found on PyPI hence you can install it via pip.\n\n```\npip install sorceress\n```\n\n```\n#importing\nfrom sorceress import sorceress\n```\n\n### Features\n\n[For the API, click here](https://altunenes.github.io/sorceress/api_reference/)\n\n+ Illusions in Python\n  - chromatic\n  - dotill\n  - realtimegrid\n  - addlines\n  - eyecolour\n  - dakinPex\n  - bruno\n  - dolboeuf\n  - kanizsa\n  - tAki2001\n  - cafewall\n  - ccob\n  - ebbinghaus\n  - whiteill\n  - enigma\n  - blackhole\n  - colorgrids\n  - munker\n  - munker2\n  - grids2\n  - pareidolia\n\n **Illusions in JavaScript**\n\n  - footsteps\n  - thelilac\n  - EyeMovements\n  - spatialmotion\n  - Motion Induced Blindness (2 versions)\n  - Depth Perception\n\n## Examples\n\n[In this page](https://altunenes.github.io/sorceress/explanations%20of%20illusions/), you can find all illusions, explanations, code, and how to use it. I show just a few examples on this page.\n\n```\nfrom sorceress import sorceress\nsorceress.chromatic("myimage.jpg",circle=False, method="CMCCAT2000", gif=True, Gifduration=7)\nsorceress.addlines("myimage.png",linecolour1=(0,255,0),linecolour2=(0,255,255),linecolour3=(255,0,0))\n```\n\nAs you can see above, you can use the package in a very simple way. You will need to install the following packages to use the package. You will not need to import them, the package will do it for you.\n\n```\npip install opencv-python\npip install numpy\npip install matplotlib\npip install imageio\npip install Pillow\npip install colour-science\n```\n\n## Contribution\n\nAny contribution, bug report, or suggestion is always welcome.\n\n##Author\n\n+ Main Maintainer: Enes Altun\n',
    'author': 'altunenes',
    'author_email': 'enesaltun2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/altunenes/sorceress',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
