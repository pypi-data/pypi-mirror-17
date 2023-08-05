# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""
Monkey patches for fixes in Eppy which have not yet made it to the released
version. These will be removed as soon as Eppy catches up.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy import idfreader
import eppy
from eppy.modeleditor import IDF as BaseIDF
from eppy.modeleditor import addthisbunch
from eppy.modeleditor import newrawobject
from eppy.modeleditor import obj2bunch


def addfunctions2new(abunch, key):
    """Monkeypatched bugfix for add functions to a new bunch/munch object"""
    snames = [
        "BuildingSurface:Detailed",
        "Wall:Detailed",
        "RoofCeiling:Detailed",
        "Floor:Detailed",
        "FenestrationSurface:Detailed",
        "Shading:Site:Detailed",
        "Shading:Building:Detailed",
        "Shading:Zone:Detailed", ]
    snames = [sname.upper() for sname in snames]
    if key.upper() in snames:
        abunch.__functions.update({
            'area': eppy.function_helpers.area,
            'height': eppy.function_helpers.height,
            'width': eppy.function_helpers.width,
            'azimuth': eppy.function_helpers.azimuth,
            'tilt': eppy.function_helpers.tilt,
            'coords': eppy.function_helpers.getcoords,
        })
    return abunch


idfreader.addfunctions2new = addfunctions2new


class IDF(BaseIDF):
    """Monkey-patched IDF to fix copyidfobject and newidfobject."""
    
    def __init__(self, *args, **kwargs):
        super(IDF, self).__init__(*args, **kwargs)
    
    def copyidfobject(self, idfobject):
        """Monkey-patched to add the return value.
        """
        abunch = addthisbunch(self.idfobjects,
                              self.model,
                              self.idd_info,
                              idfobject)
        abunch = addfunctions2new(abunch, abunch.key)
        
        return abunch

    def newidfobject(self, key, aname='', **kwargs):
        """
        Add a new idfobject to the model. If you don't specify a value for a
        field, the default value will be set.

        For example ::

            newidfobject("CONSTRUCTION")
            newidfobject("CONSTRUCTION",
                Name='Interior Ceiling_class',
                Outside_Layer='LW Concrete',
                Layer_2='soundmat')

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        aname : str, deprecated
            This parameter is not used. It is left there for backward 
            compatibility.
        **kwargs
            Keyword arguments in the format `field=value` used to set the value
            of fields in the IDF object when it is created. 

        Returns
        -------
        EpBunch object

        """
        obj = newrawobject(self.model, self.idd_info, key)
        abunch = obj2bunch(self.model, self.idd_info, obj)
        self.idfobjects[key].append(abunch)
        for k, v in list(kwargs.items()):
            abunch[k] = v
        abunch = addfunctions2new(abunch, abunch.key)
        return abunch
        