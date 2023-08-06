# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecs_framework']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.11.0,<0.12.0',
 'deepmerge==1.0.1',
 'immutables>=0.19,<0.20',
 'multipledispatch>=0.6.0,<0.7.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'pecs-framework',
    'version': '1.0.5',
    'description': 'The ✨Respectably Muscled✨ Python Entity Component System',
    'long_description': '# PECS\n[![Tests](https://github.com/krummja/PECS/actions/workflows/main.yml/badge.svg)](https://github.com/krummja/PECS/actions/workflows/main.yml) [![Coverage Status](https://coveralls.io/repos/github/krummja/PECS/badge.svg?branch=master)](https://coveralls.io/github/krummja/PECS?branch=master)\n\n![Armstrong](/static/lm_pecs_armstrong.png)\n\nPECS is the ✨Respectably Muscled✨ Python ECS library that aims to provide a powerful, user-friendly, and fast-as-hell framework for game development.\n\nThis library is the spiritual successor to my prior ECS library, [ECStremity](https://github.com/krummja/ECStremity). Both this and its predecessor were inspired by the JavaScript ECS library [geotic](https://github.com/ddmills/geotic), created and maintained by [@ddmills](https://github.com/ddmills). I highly recommend checking out that project as well as the excellent resources cited in its README.\n\nWhat is ECS, you ask? [Check it out](https://medium.com/ingeniouslysimple/entities-components-and-systems-89c31464240d)!\n\n## Installation\n\nInstall the package from PyPI using pip:\n\n```\npip install pecs-framework\n```\n\nOr grab it directly from this repository:\n\n```\npip install git+https://github.com/krummja/PECS\n```\n\n## Usage and Examples\n\nTo start flexing your PECS, import the library and set up some components.\n\n```python\nimport pecs_framework as pecs\n\n\nclass Position(pecs.Component):\n    """Representation of an Entity\'s position in 2D space."""\n\n    def __init__(self, x: int = 0, y: int = 0) -> None:\n        self.x = x\n        self.y = y\n        \n        \nclass Velocity(pecs.Component):\n    """Representation of an Entity\'s velocity in 2D space."""\n    \n    def __init__(self, x: int = 0, y: int = 0) -> None:\n        self.x = x\n        self.y = y\n        \n        \nclass Health(pecs.Component):\n    """Representation of an Entity\'s health."""\n    \n    def __init__(self, maximum: int) -> None:\n        self.maximum = maximum\n        self.current = maximum  \n        \n        \nclass IsFrozen(pecs.Component):\n    """Flag Component denoting a frozen Entity."""\n\n\necs = pecs.Engine()\n\n# All Component and Prefab classes must be registered with the engine.\necs.register_component(Position)\necs.register_component(Health)\necs.register_component(IsFrozen)\n\n# Create a World to hold and create entities and queries.\nworld = ecs.create_world()\n\n# We can then ask the World instance to create Entity instances for us.\nentity = world.create_entity()\n\n# Finally, we can add components to our newly created Entity.\nentity.add(Position, { \'x\': 10, \'y\': -2 })\nentity.add(Health, { \'maximum\': 100 })\nentity.add(IsFrozen)\n```\n\n### Queries\n\nThe easiest way to build out systems is through world queries. To make a system that tracks and updates the components relevant to movement, we might query for `Position` and `Velocity` components. Because we want our entities to move, we want to exclude those marked with the `IsFrozen` flag. Perhaps we also want to grab only those entities that can fly through `Wings` or swim through `Fins`: \n\n```python\nkinematics = world.create_query(\n     all_of = [Position, Velocity],\n     any_of = [Wings, Fins],\n    none_of = [IsFrozen],\n)\n```\n\nQueries can specify `all_of`, `any_of`, or `none_of` quantifiers. The query in the example above asks for entities that must have **both** `Position` **and** `Velocity`, may have **either** `Wings` **or** `Fins`, and **must not** have `IsFrozen`.\n\nWe can access the result set of the query and do some operation on them every loop cycle:\n\n```python\ndef process(dt):\n    for entity in targets.result:\n        entity[Position].x += entity[Velocity].x * dt\n        entity[Position].y += entity[Velocity].y * dt\n```\n\n### Broadcasting Events to Components\n\nComplex interactions within and among entities can be achieved by firing events on an entity. This creates an `EntityEvent` that looks for methods on all of the entity\'s methods prefixed with `on_`.\n\n```python\nzombie.fire_event(\'attack\', {\n    \'target\': survivor,\n    \'multiplier\': 1.5\n})\n```\n\nOn the `zombie` entity, we might have attached an `Attacker` component with the following logic:\n\n```python\nclass Attacker(pecs.Component):\n\n    def __init__(self, strength: int) -> None:\n        self.strength = strength\n\n    def on_attack(self, evt: pecs.EntityEvent) -> pecs.EntityEvent:\n        target = evt.data.target\n        target.fire_event(\'damage_taken\', {\n            \'amount\': self.strength * evt.data.multiplier\n        })\n        evt.handle()\n```\n\nWhen we execute `fire_event` with the event name `attack`, the event system will find all `on_attack` methods on that entity\'s components. If we want the event propagation to stop at a particular component, we can call `evt.handle()` which will immediately break broadcasting down the component list.  \n\nInternally, the `EntityEvent` class puts together an instance of the class `EventData`, which provides access to the properties defined in the `fire_event` call.\n\n```python\nzombie.fire_event(\'attack\', {\n    \'target\': survivor,                 # <-- We defined \'target\' here\n    \'multiplier\': 1.5                   # <-- and \'multiplier\' here\n})\n\ndef on_attack(self, evt: pecs.EntityEvent) -> pecs.EntityEvent:\n    target = evt.data.target            # --> survivor\n    multiplier = evt.data.multiplier    # --> 1.5\n```\n\nActions can also be defined as a tuple and passed into the `fire_event` method. This allows for easy abstraction over variables used in the event:\n\n```python\nattack_against = (lambda target : (\'attack\', {\n    \'target\': target,\n    \'multiplier\': 1.5\n}))\n\nzombie.fire_event(attack_against(survivor))\n```\n',
    'author': 'Jonathan Crum',
    'author_email': 'crumja4@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/krummja/PECS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
