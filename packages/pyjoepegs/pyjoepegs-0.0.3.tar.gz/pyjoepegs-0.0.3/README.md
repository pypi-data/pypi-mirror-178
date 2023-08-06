# pyjoepegs

python api client for [joepegs](https://joepegs.dev/api)

## Install

```bash
pip install pyjoepegs
```

## Quick start

```python
from pyjoepegs import JoepegsAPI
api = JoepegsAPI(api_key=<API_KEY>)

actvities_client = api.activities()
collections_client = api.collections()
items_client = api.items()
maker_orders_client = api.maker_orders()
owners_client = api.owners()
sales_client = api.sales()
search_client = api.search()
users_client = api.users()
```
