# Pupygrib

Pupygrib (pronounced *puppy grib* and short for PUre PYthon GRIB) is a
light-weight pure Python GRIB reader.  It's purpose is to extract data
from GRIB files with as little effort as possible.  The user can then
freely choose how to further process the data (*read: pupygrib will
not help you*).


## Features

This project is in the alpha phase, which means that many planned
features are missing and implemented features are not well tested.  It
also means that the API may change in future version.  The implemented
features are:

* Iterate over and extract the raw fields from GRIB edition 1 messages
  in a file.
* Extract simply packed grid-point data values from GRIB edition 1
  messages.
* Extract the coordinates for these values if they are on a
  latitude/longitude grid.

The planned features are:

* Be able to easily identify (filter) the messages.
* Be able to extract the data values for other packings.
* Be able to extract the coordinates of other grid types.
* Support for GRIB edition 2.


## Requirements

* [Python](https://www.python.org) 2.7, 3.4 or 3.5.  Earlier Python 3
  versions may work, but they are not tested.
* [Numpy](http://www.numpy.org)
* [Six](https://pypi.python.org/pypi/six)


## Installation

```
$ pip install pupygrib
```

For development, the following command will install all extra
requirements, including test requirements:

```
$ pip install pupygrib[dev,test]
```


## Usage

To use pupygrib, you will need a good understanding of the GRIB
format, especially since table lookups are not yet implemented.  ECMWF
provides an overview of GRIB
[edition 1](http://apps.ecmwf.int/codes/grib/format/grib1/overview)
and
[edition 2](http://apps.ecmwf.int/codes/grib/format/grib2/overview)
that can be used as references.

Iterate over the messages in a GRIB file and extract the coordinates
and values:

```python
>>> import pupygrib
>>> with open('tests/data/regular_latlon_surface.grib1', 'rb') as stream:
...     for i, msg in enumerate(pupygrib.read(stream), 1):
...         lons, lats = msg.get_coordinates()
...         values = msg.get_values()
...         print("Message {}: {:.3f} {}".format(i, values.mean(), lons.shape))
...
Message 1: 291.585 (31, 16)

```

Access a section of a GRIB message and print its fields:

```python
>>> with open('tests/data/regular_latlon_surface.grib1', 'rb') as stream:
...     msg, = pupygrib.read(stream)
>>> sorted(msg[0].fieldnames)  # fieldnames is a set, so we can't trust the order
['editionNumber', 'identifier', 'totalLength']
>>> msg[0].totalLength
1100
>>> msg[3] is None  # the bit-map section is not included in this message
True

```


## Development

Pull requests are most welcome!  I do ask that you add test cases and
update the documentation for any new features.  Make sure that the
following checks (coding style and unit tests, respectively) pass
without any warnings or errors.  [Tox](https://tox.readthedocs.io/)
should have at least one supported Python 2 and Python 3 version
available.

```
$ flake8
$ tox
```


## License

Pupygrib is being developed by
[Mattias Jakobsson](mailto:mattias.jakobsson@smhi.se) at
[SMHI](http://www.smhi.se).  It is released under the
[GNU General Public License v3](LICENSE.txt) or later (GPLv3+).


