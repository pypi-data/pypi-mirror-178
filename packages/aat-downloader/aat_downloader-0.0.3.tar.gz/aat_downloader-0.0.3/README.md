# AAT Downloader
> A package that helps download mobile AAT data.


## Install

`pip install aat_downloader`

## How to use

To use this package, first download the google-services.json file from the settings of your Firebase realtime database.

### Downloading data

```python
%load_ext autoreload
%autoreload 2
from aat_downloader.downloader import Downloader
# Initiate downloader with path to google services file (downloaded from Firebase)
downloader = Downloader("data/external/google-services.json")
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload


```python
# Specify experiment name and storage folder and download data
downloader.download("eeg", "data/raw")
```

### Deleting data
To delete data run the following function (replace "fooddemo" with the experiment you want to delete).

```python
downloader.delete_participants("fooddemo")
```

    Warning: Are you sure you want to delete participants of experiment: fooddemo?
     y

