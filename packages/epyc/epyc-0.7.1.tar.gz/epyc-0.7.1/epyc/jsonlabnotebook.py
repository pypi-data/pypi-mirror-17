# Simulation "lab notebook" for collecting results, JSON version
#
# Copyright (C) 2016 Simon Dobson
# 
# Licensed under the GNU General Public Licence v.2.0
#

import epyc

import os
import json
from datetime import datetime
import dateutil.parser


class MetadataEncoder(json.JSONEncoder):
    '''Add support for encoding Python datetime objects within
    JSON objects, using the standard ISO string representation.'''

    def default( self, o ):
        '''If o is a datetime object, convert it to an ISO string. If it is an
        exception, convert it to a string.

        o: the field to serialise
        returns: an ISO string if o is a datetime'''
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            if isinstance(o, Exception):
                return str(o)
            else:
                return super(MetadataEncoder, self).default(o)


class JSONLabNotebook(epyc.LabNotebook):
    '''A lab notebook that persists intself to a JSON file.'''

    def __init__( self, name, create = False, description = None ):
        '''Create a new JSON notebook, using the notebook's name
        as the JSON file. If this file exists, it will be opened
        and loaded unless create is True, in which case it will
        be erased.

        name: JSON file to persist the notebook to
        create: if True, erase existing file (defaults to False)
        description: free text description of the notebook'''
        super(epyc.JSONLabNotebook, self).__init__(name, description)

        # check for the file already existing
        if os.path.isfile(self.name()):
            # file exists, do we load it or create into it?
            if create:
                # empty the file
                with open(self.name(), 'w') as f:
                    f.write('')

                # preserve any description we were passed
                self._description = description
            else:
                # load notebook from file
                self._load(self.name())

    def isPersistent( self ):
        '''Return True to indicate the notebook is persisted to a JSON file.

        returns: True'''
        return True

    def commit( self ):
        '''Persist to disc.'''
        self._save(self.name())
        
    def _load( self, fn ):
        '''Retrieve the notebook from the given file.

        fn: the file name'''

        # if file is empty, create an empty notebook
        if os.path.getsize(fn) == 0:
            self._description = None
            self._results = dict()
            self._pending = dict()
        else:
            # load the JSON object
            with open(fn, "r") as f:
                s = f.read()

                # parse back into appropriate variables
                j = json.loads(s)
                self._description = j['description']
                self._pending = dict(j['pending'])
                self._results = j['results']

                # perform any post-load patching
                self.patch()

    def _patchDatetimeMetadata( self, res, mk ):
        '''Private method to atch an ISO datetime string to a datetime object
        for metadata key mk.

        res: results dict
        mk: metadata key'''
        t = res[epyc.Experiment.METADATA][mk]
        res[epyc.Experiment.METADATA][mk] = dateutil.parser.parse(t)
        
    def patch( self ):
        '''Patch the results dict. The default processes the Experiment.START_TIME
        and Experiment.END_TIME metadata fields back into Python datetime objects
        from ISO strings. This isn't strictly necessary, but it makes notebook
        data structure more Pythonic.'''

        for k in self._results.keys():
            ars = self._results[k]
            for res in ars:
                if isinstance(res, dict) and res[epyc.Experiment.METADATA][epyc.Experiment.STATUS]:
                    # a successful, non-pending result, patch its timing metadata
                    self._patchDatetimeMetadata(res, epyc.Experiment.START_TIME)
                    self._patchDatetimeMetadata(res, epyc.Experiment.END_TIME)
            
    def _save( self, fn ):
        '''Persist the notebook to the given file.

        fn: the file name'''

        # create JSON object
        j = json.dumps({ "description": self.description(),
                         "pending": self._pending.items(),
                         "results": self._results },
                       indent = 4,
                       cls = MetadataEncoder)
        
        # write to file
        with open(fn, 'w') as f:
            f.write(j)
            

    
