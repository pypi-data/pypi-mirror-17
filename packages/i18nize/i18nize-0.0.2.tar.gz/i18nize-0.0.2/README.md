# i18nize
This is a simple Client that integrates with the localization service www.i18nize.com

```pip install i18nize```


### Config parameters
| Name        | Type | Required | What? |
| ------------- |-------------|-------------|-------------|
| project_id | String | Yes | This should be the id of your project |
| live | Boolean | Yes | Set to *true* if you want to download your live locales otherwise your dev locales will get downloaded |

### Example config
```json
{
    "project_id": "fee43d29-090e-432d-bb62-c1755bbf6a79",
    "live": true
}
```

### Example usage
```python
from i18nize.client import Client

client = Client(config_path='/path/to/my/config/i18nize.json', destination_path='/path/to/my/dest')
client.get_all_locales()

**OUTPUT:**
*>> Downloaded en to dist/locales/en.json (live: True)*
*>> Downloaded sv to dist/locales/sv.json (live: True)*
```