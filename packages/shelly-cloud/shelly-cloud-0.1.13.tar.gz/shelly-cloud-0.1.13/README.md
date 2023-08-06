# shelly-cloud

A python library to access the Shelly cloud API. Refer also to the [Shelly API Docs](https://shelly-api-docs.shelly.cloud/cloud-control-api/communication). This repo provides functionality for:

- Getting devices status
- Getting the status of a single device
- Getting a list of device IDs

## Installing the library locally

Python3 is recommended for this project.

```bash
python -m pip install -e .
```

> **This is needed for the first time when working with the library/examples/tests.**

## Example usage

Create a `.env` file and set the environment variables according to `.env.example`:

```bash
cp .env.example .env
```

Then run the the example script

```bash
python examples/simple.py
```

or

```python
from shellyapi.shellyapi import ShellyApi

shelly = ShellyApi('provide_api_url', 'provide_api_token')
# or you can define additional optional parameters
# shelly = ShellyApi('provide_api_url', 'provide_api_token', timeout=10)

print(shelly.get_device_ids())
```

## Development

### Linting

```bash
pylint shellyapi/*.py tests/*.py examples/*.py
```

### Unit testing

```bash
python -m unittest -v tests/*.py
```
