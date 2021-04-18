# mock_apollo_server
This project is developed to mock Apollo (Ctrip) server APIs in python.

## Feature support
This project currently supports 4 APIs for fetching config:
* GET /configs/:appId/:cluster/:namespace
* GET /configfiles/json/:appId/:cluster/:namespace
* GET /services/config
* GET /notifications/v2 _(long polling)_

# Usage Guide
`$ python3 server.py`


