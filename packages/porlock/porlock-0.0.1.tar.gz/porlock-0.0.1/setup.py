# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['porlock', 'porlock.mixins']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'porlock',
    'version': '0.0.1',
    'description': 'Find unwanted visitors by analyzing behavior',
    'long_description': 'porlock\n=======\nMonitor event logs for potentially fraudulent activity\n\nPremise\n--------------\nOftentimes, specific events in and of themselves don\'t indicate a\nrisk to your systems.  However, when viewed in the context of surrounding\nevents, we can identify potentially risky behavior.\n\nTake the following scenario, represented by the events below: \n- A user calls customer service and requests and one time token for login.\n- The user logs in, and the system requires a password update\n- A few days later, the user comes to the site (from a new IP) and requests a password reset\n- The user proceeds to change their password\n\n```\nEvent: otp_login, date: 2022-11-01 13:43:17 EST, user_id: 1, ip: 10.0.0.1\nEvent: password_change, date: 2022-11-01 13:45:53 EST, user_id: 1, ip: 10.0.0.1\nEvent: password_reset, date: 2022-11-07 17:31:22 EST, user_id: 1, ip: 192.168.0.1\nEvent: password_change, date: 2022-11-07 17:33:11 EST, user_id: 1, ip: 192.168.0.1\n```\n\nNone of the above events, in isolation, look particularly risky, and while it\nis possible that the user simply forgot their new password, when\nviewed along with other events, this sequence of events points to a potential account hijack.\n\nporlock provides a rule framework to help make finding these events and flagging them\npossible.  By identifying events, and subsequent matching events, porlock parses\nlogs over a specified time period to flag risky behavior.\n\nBasic Rules\n--------------\n\n- Rules are written in a simple list format \n  - Note: future versions may support yaml rules\n\n```\n\n    [\n       "Password Change After OTP Login",\n       "otp login",\n       "followed by",\n       "any",\n       ["password change"],\n       "after",\n       "2d",\n       "user",\n       ["password change"],\n       "before",\n       "1h",\n       "14d",\n       "30d"\n    ]\n```\n\n- `Rule Name`: A human readable description of the rule\n- `Event Name`: The name of the initial event to search for\n- `When`: `followed by` or `preceded by` (Currently only `followed by` is supported)\n- `Match`: What type of match to `any`, `all`, `none`, `one`\n- `Matching Events`: a list of events to match\n- `Period When`: whether or not this event should happen `before` or `after` the `Period` parameter\n- `Period`: How long `after` the initial event to start looking (or when to stop looking for `before`)\n- `Identifier`: The field to match events on.  This is typically either a user id, email, or IP address\n- `Secondary Event`: For future use\n- `Secondary Period When`: For future use\n- `Secondary Period`: For future use\n- `Match time frame`: The time frame after (for `followed by`) the initial event occurred to check for matching events\n- `Log time frame`: For future use; The time frame to return all events for a particular `identifier` from the logs\n\n## Parameters\n### When\n- `followed by` - the matching events should come after the initial event\n- `preceded by` - the matching events should come before the initial event (Note: This is still a work in progress)\n\n### Match\n- `any` - can match any of the listed events\n- `all` - must match all of the listed events\n- `none` - must match none of the listed events\n- `one` - must match one and only one of the listed events\n\n### Period When\n- `before` - indicates to check all events prior to the `Period` parameter\n- `after`- indicates to check all events after to the `Period` parameter\n\n### Period\n- The period should be specified by a number followed by one of `s` (seconds), `m` (minutes), `h` (hours), `d` (days), or `w` (weeks)',
    'author': 'David Graves',
    'author_email': 'dgraves@thesummitgrp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
