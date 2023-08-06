A simple API wrapper for Newsworthy's template writer, https://jplusplus-murasaki.herokuapp.com/

## Installation

```sh
pip install murasaki
```

## Usage

```python3
from murasaki import Murasaki


murasaki = Murasaki("https://jplusplus-murasaki.herokuapp.com/", language="sv-SE", timezone="Europe/Stockholm")

context_data = {
  "region": "Tjörns kommun",
}
template = """
| Ovanligt varmt #{ territoryShort(region), "locative" } i går
"""
murasaki.pug(context_data, template)
'Ovanligt varmt på Tjörn i går'

template = "Ovanligt varmt {{ territoryShort(region), 'locative' }} i går"
murasaki.mustache(context_data, template)
'Ovanligt varmt på Tjörn i går'

```

By default we will look for user credentials in `MURASAKI_USER` and `MURASAKI_PWD` respectively.
They can also be set using the `user` and `password` arguments.

## Methods

- **constructor(API_endpoint, language=None, timezone=None, user=process.env.MURASAKI_USER, password=process.env.MURASAKI_PWD)**
- **.pug(data, template)** Render a pug template
- **.pugz(data, template)** Render a gzipped pug template
- **.javascript(data, template)** Render a ECMAScript template literal
- **.mustache(data, template)** Render a Mustache template

## Changelog

- 1.0.1

  - Make language and timezone work properly

- 1.0.0

  - First version