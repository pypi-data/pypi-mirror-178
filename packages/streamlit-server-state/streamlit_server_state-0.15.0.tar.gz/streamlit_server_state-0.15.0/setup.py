# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_server_state']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.0', 'streamlit>=0.65.0']

setup_kwargs = {
    'name': 'streamlit-server-state',
    'version': '0.15.0',
    'description': '',
    'long_description': '# streamlit-server-state\nA "server-wide" state shared across the sessions.\n\n[![Tests](https://github.com/whitphx/streamlit-server-state/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/whitphx/streamlit-server-state/actions/workflows/tests.yml?query=branch%3Amain)\n\n[![PyPI](https://img.shields.io/pypi/v/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)\n[![PyPI - License](https://img.shields.io/pypi/l/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)\n\n[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D2ERWFG)\n\n<a href="https://www.buymeacoffee.com/whitphx" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180" height="50" ></a>\n\n[![GitHub Sponsors](https://img.shields.io/github/sponsors/whitphx?label=Sponsor%20me%20on%20GitHub%20Sponsors&style=social)](https://github.com/sponsors/whitphx)\n\n```python\nimport streamlit as st\n\nfrom streamlit_server_state import server_state, server_state_lock\n\nst.title("Global Counter Example")\n\nwith server_state_lock["count"]:  # Lock the "count" state for thread-safety\n    if "count" not in server_state:\n        server_state.count = 0\n\nincrement = st.button("Increment")\nif increment:\n    with server_state_lock.count:\n        server_state.count += 1\n\ndecrement = st.button("Decrement")\nif decrement:\n    with server_state_lock.count:\n        server_state.count -= 1\n\nst.write("Count = ", server_state.count)\n\n```\n\nAs above, the API is similar to [the built-in SessionState](https://blog.streamlit.io/session-state-for-streamlit/), except one major difference - a "lock" object.\nThe lock object is introduced for thread-safety because the server-state is accessed from multiple sessions, i.e. threads.\n\n## Auto-rerun\nWhen you assign a value to a server-state item, `server-state[key]`,\nserver-state automatically triggers re-running of all other sessions in which that server-state item is referred to so that all the references to the server-state return the latest value and all the sessions are kept up-to-date.\n\nFor example, with this mechanism, the [sample chat app (`app_chat.py`)](./app_chat.py) keeps showing the latest message list for all users.\n\n### Suppressing auto-rerun\n\nWhen this auto-rerun mechanism is not good for your use case, you can suppress auto-reruns upon the value assignments by using `no_rerun` context as below.\n```python\nfrom streamlit_server_state import server_state, no_rerun\n\n\nwith no_rerun:\n    server_state["foo"] = 42  # This does not trigger re-running of other sessions\n```\n\n### Manually trigger re-running\nUpon each value assignment, server-state checks whether the value has been changed and skips re-running if it has not for efficiency.\nThis works well in most cases, but it does not for example when the value is a complex mutable object and its field is mutated, while such usages are not recommended.\n\nAs exceptions, in such cases where the auto-rerun mechanism does not work well, you can manually trigger re-running by using `force_rerun_bound_sessions(key)`.\n\n```python\nif "foo" not in server_state:\n    server_state["foo"] = SomeComplexObject()\n\nserver_state["foo"].field = 42  # If this assignment does not trigger re-running,\n\nforce_rerun_bound_sessions("foo")  # You can do this.\n```\n\nBackground: https://discuss.streamlit.io/t/new-library-streamlit-server-state-a-new-way-to-share-states-across-sessions-on-the-server/14981/10\n\n## Examples\n* [`app_global_count`](./app_global_count.py): A sample app like [the official counter example for SessionState](https://blog.streamlit.io/session-state-for-streamlit/) which uses `streamlit-server-state` instead and the counter is shared among all the sessions on the server. This is a nice small example to see the usage and behavior of `streamlit-server-state`. Try to open the app in multiple browser tabs and see the counter is shared among them.\n* [`app_global_slider`](./app_global_slider.py): A slider widget (`st.slider`) whose value is shared among all sessions.\n* [`app_chat.py`](./app_chat.py): A simple chat app using `streamlit-server-state`.\n* [`app_chat_rooms.py`](./app_chat_rooms.py): A simple chat app with room separation.\n  [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/whitphx/streamlit-server-state/main/app_chat_rooms.py)\n\n## Resources\n* [New library: streamlit-server-state, a new way to share states among the sessions on the server (Streamlit Community)](https://discuss.streamlit.io/t/new-library-streamlit-server-state-a-new-way-to-share-states-among-the-sessions-on-the-server/14981)\n',
    'author': 'Yuichiro Tachibana (Tsuchiya)',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/whitphx/streamlit-server-state',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.11.*',
}


setup(**setup_kwargs)
