# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interval_timer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'interval-timer',
    'version': '1.0.0',
    'description': 'interval-timer is a Python package that enables iterating over a sequence of regular time intervals with high precision.',
    'long_description': "# interval-timer\n\n**interval-timer** is a Python package that enables iterating over a sequence of regular time intervals with high precision.\n\n## Installation\n\nInstall from [PyPI](https://pypi.org/project/interval-timer/) via:\n\n```shell\npip install interval-timer\n```\n\n## Usage\n\nBasic usage is as follows:\n\n```python\nfrom interval_timer import IntervalTimer\n\nfor interval in IntervalTimer(0.5):\n    print(interval)\n    \n    # Execute code exactly every half second here\n    ...\n```\n\nOutput:\n\n```\nInterval(index=0, time=0.000, lag=0.000)\nInterval(index=1, time=0.500, lag=0.000)\nInterval(index=2, time=1.000, lag=0.000)\n...\n```\n\nFor more usage examples see [examples/](examples).\n\n## Description\n\n`IntervalTimer` is an iterator object that returns `Interval` objects at regular time intervals. Code can then be executed upon each time interval, and the intervals will stay synchronised even when the code execution time is non-zero.\n\n`IntervalTimer` is a more precise replacement for a loop that contains a wait. The following code:\n    \n```python\nfrom time import sleep\n\n# Iterates approximately every half second\nfor i in range(5):\n    print(i)\n    sleep(0.5)\n```\n\ncan be replaced with:\n\n```python\nfrom interval_timer import IntervalTimer\n\n# Iterates exactly every half second\nfor interval in IntervalTimer(0.5, stop=5):\n    print(interval)\n```\n\n**interval-timer** uses [perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter) under the hood to obtain high precision timing. It will not suffer from drift over long time periods.\n\nIf an interval iteration is delayed due to slow code execution, then future intervals will still be synchronised to absolute time if they're given time to catch up. The caller can see if synchronisation has been temporarily lost by checking if the `Interval` object's `lag` attribute returns a non-zero value (see the [lag.py](examples/lag.py) example).\n\n## Timing diagram\n\n![Timing diagram](timing.svg)\n\nThe above timing diagram shows that each returned `Interval` object has the following attributes:\n- `time`: the nominal start time of the interval. Always has equal value to the `end_time` value of the previous interval.\n- `buffer`: the length of time before the interval start time that the interval was requested. The minimum buffer is zero.\n- `lag`: The length of time after the interval start time that the interval was requested. The minimum lag is zero. If the lag is non-zero, then the code executed within the previous interval took longer than the interval period, which is generally undesirable.\n",
    'author': 'morefigs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/morefigs/interval-timer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
