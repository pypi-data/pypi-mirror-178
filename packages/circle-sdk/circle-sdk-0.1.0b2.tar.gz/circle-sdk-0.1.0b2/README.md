# Circle APIs Python Library

[![pypi](https://img.shields.io/pypi/v/circle-sdk)](https://pypi.org/project/circle-sdk)

The Circle Python library provides convenient access to the Circle API for
applications written in Python. For the API reference, see the [Circle API docs](https://developers.circle.com/reference). Also see this project's [PyPI package page](https://pypi.org/project/circle-sdk/).

## Requirements

Python 3.7+ and Node 10+ (optional for contributing and development).

## Installation

The recommended way of installation is using the Python Package Index (PyPI): 
```sh
python3 -m pip install circle-sdk
```

The other option requires you to clone this repo and run
```sh
python3 -m pip install -e /Path/to/this/repo/root
``` 

## Python Typing
We strongly recommended that you use this SDK with Python typing extensions: we recommend using the VS Code IDE, downloading the [Python IntelliSense extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python), and enabling type checking for your workspace (see [this guide](https://www.emmanuelgautier.com/blog/enable-vscode-python-type-checking)).

## Usage

```python
import circle_sdk
from circle_sdk.apis.tags import subscriptions_api
from circle_sdk.model.subscription_request import SubscriptionRequest
from pprint import pprint


configuration = circle_sdk.Configuration(
    host = "https://api-sandbox.circle.com",
    access_token = '<replace-me-with-your-api-key>'
)


with circle_sdk.ApiClient(configuration) as api_client:

    api_instance = subscriptions_api.SubscriptionsApi(api_client)

    body = SubscriptionRequest(
        endpoint="https://example.org/py/notifications"
    )
    
    try:
        api_response = api_instance.create_subscription(body=body)
        pprint(api_response)
    except circle_sdk.ApiException as e:
        print("Exception when calling SubscriptionsApi->create_subscription: %s\n" % e)

```

## Development
Clone this repo and install development dependencies using 

```sh
# For codegen tools and git hook checks
yarn install

# For the Python SDK's dependencies
python3 -m pip install -r requirements.txt
```

1. Run the codegen:

    ```sh
    yarn gen-sdk <sdk-version>      # e.g. yarn gen-sdk 0.1.0-beta.0
    ```

## Contributions

Please follow the [Conventional Commits][convencomms] format for all commits when creating a contributing pull request for this repo.

[convencomms]: https://www.conventionalcommits.org/en/v1.0.0/