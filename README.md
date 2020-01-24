## A convenient PayWhirl API wrapper in Python

The [PayWhirl] Python library is provided to allow developers to access PayWhirl
services without needing to write their own API wrappers.

The [Documentation] linked here and below contains all of the available methods
for interacting with your PayWhirl account. If you would like to see additional
functionality added, feel free to submit an issue or a pull request.

  [PayWhirl]: https://app.paywhirl.com/
  [Python]: https://www.python.org/
  [Documentation]: https://api.paywhirl.com/

### Usage Guide

- [Documentation]

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [About](#about)

## Requirements

- [Python]: Python 3.5+

## Installation

```bash
$ pip3 install --upgrade paywhirl
```

## Usage

To create a new PayWhirl object, you need to pass your API key and
secret, which can be found in the [API key section of the main site](https://app.paywhirl.com/api-keys).

```python
from paywhirl import PayWhirl, HTTPError

api_key = 'pwpk_xxxxxxxxxxxxxxx'
api_secret = 'pwpsk_xxxxxxxxxxx'

pw = PayWhirl(api_key, api_secret)

try:
    print(pw.get_account())
except HTTPError as e:
    print(e.response.status_code)
    print(e.response.text)
```

## License

PayWhirl is copyright © 2016-2018 [PayWhirl Inc.][PayWhirl] This library is free
software, and may be redistributed under the terms specified in the [license].

  [license]: LICENSE

## About

[PayWhirl Inc.][PayWhirl] and the names and logos for PayWhirl are
trademarks of PayWhirl inc.

For additional information, please see our [Terms of Use](https://app.paywhirl.com/terms) and [Privacy Policy](https://app.paywhirl.com/privacy)
