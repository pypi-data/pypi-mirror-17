
# TQCLI - TranQuant Client

TQCLI is the client application for using [TranQuant services](http://tranquant.com)

[TranQuant](http://tranquant.com) is a data marketplace that delivers real-time or batch data at a large scale from suppliers to end-users.

This client will allow you to upload and download data to and from TranQuant platform efficiently


## How to install TQCLI?

1) Install [Python3](https://www.python.org/downloads/) and the Python package manager, [`pip`](https://pip.pypa.io/en/stable/installing/).

2) Install the `tqcli` command line app.

If you have `pip` installed:

    pip3 install tqcli --no-cache-dir

If you want to install the latest version from GitHub:

    git clone https://github.com/Tranquant/tqcli.git
    cd tqcli
    python3 setup.py install

## How to use TQCLI?

    # 1- Create a Data Source on http://tranquant.com website
    # 2- You will see a command generated with datasource id that looks like:
    
    tqcli --datasource-id <a-datasource-id> --input <path-to-dataset-file>
    
    # 3- Go back to http://tranquant.com and view your published datasource
    # 4- You will find the dataset available under that datasource now!


If you have any questions please contact us `info@tranquant.com`

You can also join our channel: [![Gitter](https://badges.gitter.im/tqcli/Lobby.svg)](https://gitter.im/tqcli/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)

## Troubleshooting install

### Windows

#### I can't install TQCLI from source because of a permission denied error.

If you get an error like the following, then you probably have an old version of `pip` installed where this error has since been fixed.

```
Cleaning up...
  Exception:
Traceback (most recent call last):
  File "C:\Python34\lib\shutil.py", line 370, in _rmtree_unsafe
    os.unlink(fullname)
PermissionError: [WinError 5] Access is denied: '<LONG_USER_TEMP_PATH>'
```

To install the latest version of `pip` on Windows, run the following command:

`python -m pip install -U pip`