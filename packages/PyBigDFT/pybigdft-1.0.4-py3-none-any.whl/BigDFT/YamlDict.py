"""
YamlDict is a simple DictType MutableMapping object that mirrors its state
to a YAML compliant file

YamlDict behaves in most ways like a standard dictionary, with the added
effect that all changes are mirrored to a YAML file at fname.

Initialise either with a dict, or initialise empty and assign just as with
a standard dict:

>>> a = YamlDict({'key': 'value'})
>>> b = YamlDict()
>>> b['key'] = 'value'
>>> print(a == b)
>>> True

Because all changes are synced to file, YamlDicts initialised to the same
filename will share values:

>>> a = YamlDict({'key': 'value'}, fname = 'test.yaml')
>>> b = YamlDict(fname = 'test.yaml')
>>> print(b.dict)
>>> {'key': 'value'}

Additionally, a YamlDict initialised on top of a file with data in it will add
any initial data to that file

>>> a = YamlDict({'firstval': 1}, fname='merge.yaml')
>>> b = YamlDict({'secondval': 2}, fname='merge.yaml')
>>> print(b.dict)
>>> {'firstval': 1, 'secondval': 2}

Unless you pass ``overwrite=True``, in which case the new YamlDict will be
enforced to the state at initialisation:

>>> c = YamlDict(fname='merge.yaml', overwrite=True)
>>> print(c.dict)
>>> {}
>>> d = YamlDict({'newval': 'val'}, fname='merge.yaml', overwrite=True)
>>> print(d.dict)
>>> {'newval': 'val'}

YamlDict also has inbuilt name validation. Any fname passed will be converted
to an ``os.path.abspath`` string, and the filetype enforced to ``.yaml``
(or ``.yml``)

.. note::

    Nested objects can currently pose problems if they are being dynamically
    updated, as shown here:

    >>> test = YamlDict({'a': {'b': 2}})
    >>> test['a']['b'] = 10
    >>> print(test.dict)
    >>> {'a': {'b': 2}}
"""

import os
import yaml
from collections.abc import MutableMapping


class YamlDict(MutableMapping):
    """
    DictType Object for storing data in a YAML formatted database

    Arguments:
        initial (dict, optional):
            initial dict to start with
        fname (str, optional):
            filename for the database
        overwrite (bool, optional):
            overwrite file with initial, or empty dict
    """
    def __init__(self, initial: dict = None,
                 fname: str = 'database.yaml',
                 overwrite: bool = False):

        self._fpath = self._validate_name(fname)

        self.read()  # initially read the file

        if initial is None:
            initial = {}

        if overwrite:
            self._store = initial
        else:
            self._store.update(initial)

        self.write()

    def __getitem__(self, key):
        self.read()
        return self._store[key]

    def __setitem__(self, key, val):
        self._store[key] = val
        self.write()

    def __delitem__(self, key):
        del self._store[key]
        self.write()

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __str__(self):
        return f'YamlDict({self._store})'

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._store == other._store

    @staticmethod
    def _validate_name(name):
        """
        given name, return a valid full path to the database file

        Arguments:
            name (str):
                input name

        Returns:
            str:
                absolute path to the file
        """
        # force yaml filetype
        if not any(name.endswith(f) for f in ['.yml', '.yaml']):
            if '.' in name:
                name = '.'.join(name.split('.')[:-1]) + '.yaml'
            else:
                name += '.yaml'

        path = os.path.abspath(name)

        return path

    def read(self):
        """
        Read the yaml file into the internal dict.

        Shouldn't be necessary for the user to call this method, but can be
        done so in order to force an update or for debugging

        Returns:
            dict:
                loaded dict as stored internally
        """
        if os.path.isfile(self._fpath):
            with open(self._fpath, 'r') as o:
                self._store = yaml.safe_load(o)

            if self._store is None:
                self._store = {}
        else:
            self._store = {}
            self.write()

        return self._store

    def write(self):
        """
        Export the internal dict to yaml file.

        Shouldn't be necessary for the user to call this method, but can be
        done so in order to force an update or for debugging

        Returns:
            dict:
                internal dict as written
        """
        with open(self._fpath, 'w+') as o:
            if len(self._store) != 0:
                yaml.dump(self._store, o)
            else:
                o.write('')

        return self._store

    @property
    def dict(self):
        """
        Return the internal dict

        Returns:
            dict:
                internal dict
        """
        return self.read()
