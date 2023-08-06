
#
# based on MDAnalysis.coordinates.DCD from
#
# MDAnalysis --- http://mdanalysis.googlecode.com
# Copyright (c) 2006-2011 Naveen Michaud-Agrawal,
#               Elizabeth J. Denning, Oliver Beckstein,
#               and contributors (see website for details)
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
#     N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and
#     O. Beckstein. MDAnalysis: A Toolkit for the Analysis of
#     Molecular Dynamics Simulations. J. Comput. Chem. 32 (2011), 2319--2327,
#     doi:10.1002/jcc.21787
#

from __future__ import absolute_import

import os
import errno
import types
import numpy as np


class DCDReader( object ):
    # units = { 'time': 'AKMA', 'length': 'Angstrom' }
    def __init__( self, dcdfilename ):
        self.dcdfile = None  # set right away because __del__ checks

        # Issue #32 (MDanalysis): segfault if dcd is 0-size
        # Hack : test here... (but should be fixed in dcd.c)
        stats = os.stat( dcdfilename )
        if stats.st_size == 0:
            raise IOError( errno.ENODATA, "DCD file is zero size", dcdfilename )

        self.dcdfile = dcdfilename
        self.numatoms = 0
        self.numframes = 0
        self.fixed = 0
        self.skip = 1
        self.periodic = False

        self._read_dcd_header()

        self._pos = np.zeros(
            ( self.numatoms, 3 ), dtype=np.float32, order='F'
        )
        self._unitcell = np.zeros( ( 6 ), np.float32 )
        self._x = self._pos[:,0]
        self._y = self._pos[:,1]
        self._z = self._pos[:,2]

        # Read in the first timestep
        self._read_next_timestep()
    def _read_next_timestep( self ):
        return self._read_next_frame(
            self._x, self._y, self._z, self._unitcell, self.skip
        )
    def __getitem__( self, frame ):
        if( np.dtype( type( frame ) ) != np.dtype( int ) ):
            raise TypeError
        if( frame < 0 ):
            # Interpret similar to a sequence
            frame = len(self) + frame
        if( frame < 0 ) or ( frame >= len( self ) ):
            raise IndexError
        self._jump_to_frame( frame )
        self._read_next_frame(
            self._x, self._y, self._z, self._unitcell, 1
        )
        return self._pos
    def __len__(self):
        return self.numframes
    def close( self ):
        self._finish_dcd_read()
        self.dcdfile = None
    def __del__( self ):
        if not self.dcdfile is None:
            self.close()


# Add the c functions to their respective classes so they act as class methods
from . import _dcdmodule

try:
    import new
    DCDReader._read_dcd_header = new.instancemethod( _dcdmodule._read_dcd_header, None, DCDReader )
    DCDReader._read_next_frame = new.instancemethod( _dcdmodule._read_next_frame, None, DCDReader )
    DCDReader._jump_to_frame = new.instancemethod( _dcdmodule._jump_to_frame, None, DCDReader )
    DCDReader._reset_dcd_read = new.instancemethod( _dcdmodule._reset_dcd_read, None, DCDReader )
    DCDReader._finish_dcd_read = new.instancemethod( _dcdmodule._finish_dcd_read, None, DCDReader )
    DCDReader._read_timeseries = new.instancemethod( _dcdmodule._read_timeseries, None, DCDReader )
    del( _dcdmodule )
except ImportError:
    DCDReader._read_dcd_header = lambda self: _dcdmodule._read_dcd_header( self )
    DCDReader._read_next_frame = lambda self, x, y, z, unitcell, skip: _dcdmodule._read_next_frame( self, x, y, z, unitcell, skip )
    DCDReader._jump_to_frame = lambda self, frame: _dcdmodule._jump_to_frame( self, frame )
    DCDReader._reset_dcd_read = lambda self: _dcdmodule._reset_dcd_read( self )
    DCDReader._finish_dcd_read = lambda self: _dcdmodule._finish_dcd_read( self )
    DCDReader._read_timeseries = lambda self: _dcdmodule._read_timeseries( self )
