# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gameoflife_ndimage']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'numpy>=1.23.5,<2.0.0',
 'pillow>=9.3.0,<10.0.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'gameoflife-ndimage',
    'version': '0.1.3',
    'description': 'Quick simulation of arbitrary rulesets for nearest-neighbour cellular automata. Uses scipy.ndimage.correlate, and can export videos via ffmpeg-python.',
    'long_description': '# Cellular Automata Simulator\n\nUses `numpy` and `scipy.ndimage` to quickly simulate arbitrary rulesets for nearest-neighbours cellular automata. Can\ngenerate videos and images of the results via `ffmpeg-python` and `pillow`.\n\n### Usage example:\n\n```python\nimport gameoflife_ndimage.simulation as sim\nfrom gameoflife_ndimage.video import Recorder\n\nif __name__ == \'__main__\':\n    rules = sim.Rules2D.classic()\n    size = (256, 256)\n    draw_params = sim.DrawParams(dead_color=[0, 0, 0], alive_color=[255, 255, 255], resize_factor=4)\n\n    state = sim.State2D.random(rules, size)\n    input_wh = tuple(a * draw_params.resize_factor for a in state.wh)\n    recorder = Recorder(\n        framerate=5,\n        input_wh=input_wh,\n        output_path="output/gol_classic_{}x{}_from_random.mp4".format(*size),\n    )\n    state.run_and_record(100, draw_params, recorder)\n    recorder.close()\n```',
    'author': 'RundownRhino',
    'author_email': '52856631+RundownRhino@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RundownRhino/Cellular-Automata-Simulator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
