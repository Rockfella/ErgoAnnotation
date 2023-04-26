# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ergoannotation",
    "author" : "Johan Sleman",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy



from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       )
from bpy.types import (Panel,
                       AddonPreferences,
                       Operator,
                       PropertyGroup,
                       )

from . ea_op import EA_OT_Master_Clock_Button, EA_OT_Round_FPS_Button, EA_OT_DUET_R_Button, EA_OT_DUET_L_Button

from . ea_pnl import EA_PT_Panel, EA_PT_Panel_Inputs



#Regular classes
classes = (EA_OT_Master_Clock_Button, EA_OT_Round_FPS_Button, EA_OT_DUET_R_Button, EA_OT_DUET_L_Button,
           EA_PT_Panel, EA_PT_Panel_Inputs)
def register():

    bpy.types.Scene.master_time = bpy.props.StringProperty(name="master_time")
    bpy.types.Scene.master_time_frame = bpy.props.IntProperty(name="master_time_frame")
    bpy.types.Scene.active_input = bpy.props.IntProperty(
        name="active_input")
    for c in classes:
        
        bpy.utils.register_class(c)



def unregister():
    del bpy.types.Scene.master_time
    del bpy.types.Scene.master_time_frame
    del bpy.types.Scene.active_input
    

    for c in classes:
       
        bpy.utils.unregister_class(c)
