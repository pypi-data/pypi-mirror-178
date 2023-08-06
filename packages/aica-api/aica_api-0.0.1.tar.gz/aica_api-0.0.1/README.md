# Python AICA API Client

The AICA API client module provides simple functions for interacting with the AICA API.

```shell
pip install aica-api
```

The client can be used to easily make API calls as shown below:

```python
from aica_api.client import AICA

aica = AICA()

aica.set_application('my_application.yaml')
aica.init_application()
aica.start_application()

aica.load_component('my_component')
aica.unload_component('my_component')

aica.stop_application()
aica.reset_application()
```

## Upcoming features

- Better API documentation
- Helper functions to handle API response objects
- Websocket subscriptions to component states, predicates, and logical conditions
