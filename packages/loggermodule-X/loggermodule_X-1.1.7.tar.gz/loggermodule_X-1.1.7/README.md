# Logger Module X

Just logging python file !

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install loggermodule-X
```

## Usage

Param = View in python file :P
```python
from loggermodule_X import logger_x

if __name__ == '__main__':
    loggerX = logger_x(__file__)
    log = loggerX.configLogger()
    log.info('THIS is info msg !!')
    log.debug('THIS is debug msg !!')
    log.error('THIS is error msg !!')
    log.warning('THIS is warning msg !!')
    log.critical('THIS is critical msg !!')

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Infoquest Limited](https://www.infoquest.co.th/)