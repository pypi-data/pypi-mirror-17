"""
Copyright 2011 Ryan Fobel and Christian Fobel

This file is part of Microdrop.

Microdrop is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Microdrop is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Microdrop.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import OrderedDict
from copy import deepcopy
try:
    import cPickle as pickle
except ImportError:
    import pickle
import cStringIO as StringIO
import itertools as it
import json
import logging
import re
import sys
import time

from microdrop_utility import Version, FutureVersionError
import numpy as np
import pandas as pd
import yaml
import zmq_plugin as zp
import zmq_plugin.schema

from .plugin_manager import emit_signal, get_service_names


logger = logging.getLogger(__name__)


def protocol_to_frame(protocol_i):
    '''
    Parameters
    ----------
    protocol_i : microdrop.protocol.Protocol
        Microdrop protocol.

        .. note::
            A Microdrop protocol object is stored as pickled in the
            ``protocol`` file in each experiment log directory.

    Returns
    -------
    pandas.DataFrame
         Data frame with rows indexed by 0-based step number and columns
         indexed (multi-index) first by plugin name, then by step field name.

         .. note::
             Values may be Python objects.  In future versions
             of Microdrop, values *may* be restricted to json
             compatible types.
    '''
    plugin_names_i = sorted(reduce(lambda a, b:
                                   a.union(b.plugin_data.keys()),
                                   protocol_i.steps, set()))
    frames_i = OrderedDict()

    for plugin_name_ij in plugin_names_i:
        try:
            frame_ij = pd.DataFrame(map(pickle.loads,
                                        [s.plugin_data.get(plugin_name_ij)
                                         for s in protocol_i.steps]))
        except Exception, exception:
            print >> sys.stderr, exception
        else:
            frames_i[plugin_name_ij] = frame_ij
    df_protocol = pd.concat(frames_i.values(), axis=1, keys=frames_i.keys())
    df_protocol.index.name = 'step_i'
    df_protocol.columns.names = ['plugin_name', 'step_field']
    return df_protocol


def protocol_to_json(protocol):
    '''
    Parameters
    ----------
    protocol : microdrop.protocol.Protocol
        Microdrop protocol.

        .. note::
            A Microdrop protocol object is stored as pickled in the
            ``protocol`` file in each experiment log directory.

    Returns
    -------
    str
        json-encoded dictionary, with two top-level keys:
         - ``keys``:
               * Each key is a list containing a plugin name and a
                 corresponding step field name.
         - ``values``:
               * Maps to list of records (i.e., lists), one per protocol
                 step.
        Each record in the ``values`` list may be *zipped together* with
        ``keys`` to yield a plugin field name to value mapping for a single
        protocol step.
    '''
    df_protocol = protocol.to_frame()
    return json.dumps({'values': df_protocol.values.tolist(),
                       'keys': df_protocol.columns.values.tolist()},
                      cls=zp.schema.PandasJsonEncoder)


class Protocol():
    class_version = str(Version(0,2))

    def __init__(self, name=None):
        self.steps = [Step()]
        self.name = None
        self.plugin_data = {}
        self.plugin_fields = {}
        self.n_repeats = 1
        self.current_step_attempt = 0
        self.current_step_number = 0
        self.current_repetition = 0
        self.version = self.class_version

    @classmethod
    def load(cls, filename):
        """
        Load a Protocol from a file.

        Args:
            filename: path to file.
        Raises:
            TypeError: file is not a Protocol.
            FutureVersionError: file was written by a future version of the
                software.
        """
        logger.debug("[Protocol].load(\"%s\")" % filename)
        logger.info("Loading Protocol from %s" % filename)
        start_time = time.time()
        out = None
        with open(filename, 'rb') as f:
            try:
                out = pickle.load(f)
                logger.debug("Loaded object from pickle.")
            except Exception, e:
                logger.debug("Not a valid pickle file. %s." % e)
        if out==None:
            with open(filename, 'rb') as f:
                try:
                    out = yaml.load(f)
                    logger.debug("Loaded object from YAML file.")
                except Exception, e:
                    logger.debug("Not a valid YAML file. %s." % e)
        if out==None:
            raise TypeError
        out.filename = filename

        # enable loading of old protocols that were loaded as relative packages
        # (i.e., not subpackages of microdrop).
        if str(out.__class__) == 'protocol.Protocol':
            out.__class__ = cls

        # check type
        if out.__class__ != cls:
            raise TypeError, "File is wrong type: %s" % out.__class__
        if not hasattr(out, 'version'):
            out.version = str(Version(0))
        out._upgrade()

        enabled_plugins = get_service_names(env='microdrop.managed') + \
            get_service_names('microdrop')

        for k, v in out.plugin_data.items():
            if k in enabled_plugins:
                try:
                    out.plugin_data[k] = pickle.loads(v)
                except Exception, e:
                    out.plugin_data[k] = yaml.load(v)
        for i in range(len(out)):
            for k, v in out[i].plugin_data.items():
                if k in enabled_plugins:
                    try:
                        out[i].plugin_data[k] = pickle.loads(v)
                    except Exception, e:
                        # enable loading of old protocols where the
                        # dmf_device_controller was imported as a relative
                        # package
                        v = v.replace('!!python/object:gui.'
                                          'dmf_device_controller.',
                                      '!!python/object:microdrop.gui.'
                                          'dmf_device_controller.')
                        out[i].plugin_data[k] = yaml.load(v)
        logger.debug("[Protocol].load() loaded in %f s." % \
                     (time.time()-start_time))
        return out

    def _upgrade(self):
        """
        Upgrade the serialized object if necessary.

        Raises:
            FutureVersionError: file was written by a future version of the
                software.
        """
        logger.debug("[Protocol]._upgrade()")
        version = Version.fromstring(self.version)
        logger.debug('[Protocol] version=%s, class_version=%s' % (str(version), self.class_version))
        if version > Version.fromstring(self.class_version):
            logger.debug('[Protocol] version>class_version')
            raise FutureVersionError(Version.fromstring(self.class_version), version)
        elif version < Version.fromstring(self.class_version):
            if version < Version(0,1):
                for k, v in self.plugin_data.items():
                    self.plugin_data[k] = yaml.dump(v)
                for step in self.steps:
                    for k, v in step.plugin_data.items():
                        step.plugin_data[k] = yaml.dump(v)
                self.version = str(Version(0,1))
                logger.debug('[Protocol] upgrade to version %s' % self.version)
            if version < Version(0,2):
                self.current_step_attempt = 0
                self.version = str(Version(0,2))
                logger.debug('[Protocol] upgrade to version %s' % self.version)
        # else the versions are equal and don't need to be upgraded

    @property
    def plugins(self):
        return set(self.plugin_data.keys())

    def plugin_name_lookup(self, name, re_pattern=False):
        if not re_pattern:
            return name

        for plugin_name in self.plugins:
            if re.search(name, plugin_name):
                return plugin_name
        return None

    def get_step_values(self, plugin_name):
        logging.debug('[Protocol] plugin_data=%s' % self.plugin_data)
        return self.plugin_data.get(plugin_name)

    def get_data(self, plugin_name):
        logging.debug('[Protocol] plugin_data=%s' % self.plugin_data)
        return self.plugin_data.get(plugin_name)

    def set_data(self, plugin_name, data):
        self.plugin_data[plugin_name] = data

    def __len__(self):
        return len(self.steps)

    def __getitem__(self, i):
        return self.steps[i]

    def save(self, filename, format='pickle'):
        out = deepcopy(self)
        if hasattr(out, 'filename'):
            del out.filename

        # convert plugin data objects to strings
        for k, v in out.plugin_data.items():
            out.plugin_data[k] = pickle.dumps(v, -1)

        for step in out.steps:
            for k, v in step.plugin_data.items():
                step.plugin_data[k] = pickle.dumps(v, -1)

        with open(filename, 'wb') as f:
            if format=='pickle':
                pickle.dump(out, f, -1)
            elif format=='yaml':
                yaml.dump(out, f)
            else:
                raise TypeError

    def get_step_number(self, default):
        if default is None:
            return self.current_step_number
        return default

    def get_step(self, step_number=None):
        step_number = self.get_step_number(step_number)
        return self.steps[step_number]

    def current_step(self):
        return self.steps[self.current_step_number]

    def insert_steps(self, step_number=None, count=None, values=None):
        if values is None and count is None:
            raise ValueError, 'Either count or values must be specified'
        elif values is None:
            values = [Step()] * count
        for value in values[::-1]:
            self.insert_step(step_number, value, notify=False)
        emit_signal('on_steps_inserted', args=range(step_number, step_number +
                                                    len(values)))

    def insert_step(self, step_number=None, value=None, notify=True):
        if step_number is None:
            step_number = self.current_step_number
        if value is None:
            value = Step()
        self.steps.insert(step_number, value)
        emit_signal('on_step_created', args=[self.current_step_number])
        if notify:
            emit_signal('on_step_inserted', args=[self.current_step_number])

    def delete_step(self, step_number):
        step_to_remove = self.steps[step_number]
        del self.steps[step_number]
        emit_signal('on_step_removed', args=[step_number, step_to_remove])

        if len(self.steps) == 0:
            # If we deleted the last remaining step, we need to insert a new
            # default Step
            self.insert_step(0, Step())
            self.goto_step(0)
        elif self.current_step_number == len(self.steps):
            self.goto_step(step_number - 1)
        else:
            self.goto_step(self.current_step_number)

    def delete_steps(self, step_ids):
        sorted_ids = sorted(step_ids)
        # Process deletion of steps in reverse order to avoid ID mismatch due
        # to deleted rows.
        sorted_ids.reverse()
        for id in sorted_ids:
            self.delete_step(id)

    def next_step(self):
        if self.current_step_number == len(self.steps) - 1:
            self.insert_step(step_number=self.current_step_number,
                             value=self.current_step().copy(), notify=False)
            self.next_step()
            emit_signal('on_step_inserted', args=[self.current_step_number])
        else:
            self.goto_step(self.current_step_number + 1)

    def next_repetition(self):
        if self.current_repetition < self.n_repeats - 1:
            self.current_repetition += 1
            self.goto_step(0)

    def prev_step(self):
        if self.current_step_number > 0:
            self.goto_step(self.current_step_number - 1)

    def first_step(self):
        self.current_repetition = 0
        self.goto_step(0)

    def last_step(self):
        self.goto_step(len(self.steps) - 1)

    def goto_step(self, step_number):
        logging.debug('[Protocol].goto_step(%s)' % step_number)
        original_step_number = self.current_step_number
        self.current_step_number = step_number
        emit_signal('on_step_swapped', [original_step_number, step_number])

    def to_frame(self):
        '''
        Returns
        -------
        pandas.DataFrame
            Data frame with multi-index columns, indexed first by plugin name,
            then by plugin step field name.

            .. note::
                If an exception is encountered while processing a plugin value,
                the plugin causing the exception is skipped and protocol values
                related to the plugin are not included in the result.

        See Also
        --------
        :meth:`to_json`, :meth:`to_ndjson`
        '''
        return protocol_to_frame(self)

    def to_json(self):
        '''
        Returns
        -------
        str
            json-encoded dictionary, with two top-level keys:
             - ``keys``:
                   * Each key is a list containing a plugin name and a
                     corresponding step field name.
             - ``values``:
                   * Maps to list of records (i.e., lists), one per protocol
                     step.
            Each record in the ``values`` list may be *zipped together* with
            ``keys`` to yield a plugin field name to value mapping for a single
            protocol step.

        See Also
        --------
        :meth:`to_frame`, :meth:`to_ndjson`
        '''
        return protocol_to_json(self)

    def to_ndjson(self, ostream=None):
        '''
        Write protocol as newline delimted JSON (i.e., `ndjson`_, see
        `specification`_).

        Each subsequent line in the output is a nested JSON record, list), one
        line per protocol step.  The keys of the top-level object of each record
        correspond to plugin names.  The second-level keys correspond to the
        step field name.

        Parameters
        ----------
        ostream : file-like, optional
            Output stream to write to.

        Returns
        -------
        None or str
            If :data:`ostream` parameter is ``None``, return output as string.

        See Also
        --------
        :meth:`to_frame`, :meth:`to_json`


        .. _`ndjson`: http://ndjson.org/
        .. _`specification`: http://specs.frictionlessdata.io/ndjson/
        '''
        df_protocol = self.to_frame()

        if ostream is None:
            ostream = StringIO.StringIO()
            return_required = True
        else:
            return_required = False

        field_groups = [(group_i, list(fields_i))
                        for group_i, fields_i in
                        it.groupby(df_protocol.columns.values, lambda v: v[0])]
        field_counts = np.cumsum([len(f[1]) for f in field_groups])
        field_bases = field_counts.copy()
        field_bases[1:] = field_counts[:-1]
        field_bases[0] = 0

        try:
            for row_i in df_protocol.values:
                row_dict_i = dict([(plugin_name_j,
                                    dict(zip(zip(*fields_j)[1],
                                             row_i[start_j:end_j])))
                                for (plugin_name_j, fields_j), start_j, end_j
                                in zip(field_groups, field_bases[:-1],
                                        field_counts[:-1])])
                print >> ostream, json.dumps(row_dict_i,
                                             cls=zp.schema.PandasJsonEncoder)
        finally:
            if return_required:
                return ostream.getvalue()


class Step(object):
    def __init__(self, plugin_data=None):
        if plugin_data is None:
            self.plugin_data = {}
        else:
            self.plugin_data = deepcopy(plugin_data)

    def copy(self):
        return Step(plugin_data=deepcopy(self.plugin_data))

    @property
    def plugins(self):
        return set(self.plugin_data.keys())

    def plugin_name_lookup(self, name, re_pattern=False):
        if not re_pattern:
            return name

        for plugin_name in self.plugins:
            if re.search(name, plugin_name):
                return plugin_name
        return None

    def get_data(self, plugin_name):
        logging.debug('[Step] plugin_data=%s' % self.plugin_data)
        return self.plugin_data.get(plugin_name)

    def set_data(self, plugin_name, data):
        self.plugin_data[plugin_name] = data
