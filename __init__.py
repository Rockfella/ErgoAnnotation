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

from . ea_op import EA_OT_Master_Clock_Button
from . ea_op import EA_OT_Round_FPS_Button
from . ea_pnl import EA_PT_Panel

from . ea_hotkey import onPressKeyZERO, onPressKeyONE, onPressKeyTWO, onPressKeyTHREE, onPressKeyFOUR, onPressKeyFIVE, onPressKeySIX, onPressKeySEVEN, onPressKeyEIGHT, onPressKeyNINE, onPressKeyTEN
from . ea_hotkey import onReleaseKeyZERO, onReleaseKeyONE, onReleaseKeyTWO, onReleaseKeyTHREE, onReleaseKeyFOUR, onReleaseKeyFIVE, onReleaseKeySIX, onReleaseKeySEVEN, onReleaseKeyEIGHT, onReleaseKeyNINE, onReleaseKeyTEN


#TODO: register all that are inside this file in the right place

#HotkeyOperators-----------------------------------------------
addon_keymaps = []


duet_hotkey_press_executions = (onPressKeyZERO, onPressKeyONE, onPressKeyTWO, onPressKeyTHREE, onPressKeyFOUR,
                                onPressKeyFIVE, onPressKeySIX, onPressKeySEVEN, onPressKeyEIGHT, onPressKeyNINE, onPressKeyTEN)

duet_hotkey_release_executions = (onReleaseKeyZERO, onReleaseKeyONE, onReleaseKeyTWO, onReleaseKeyTHREE, onReleaseKeyFOUR,
                                  onReleaseKeyFIVE, onReleaseKeySIX, onReleaseKeySEVEN, onReleaseKeyEIGHT, onReleaseKeyNINE, onReleaseKeyTEN)


duet_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']


#Regular classes
classes = (EA_OT_Master_Clock_Button, EA_OT_Round_FPS_Button, EA_PT_Panel)
def register():

    bpy.types.Scene.master_time = bpy.props.StringProperty(name="master_time")
    bpy.types.Scene.master_time_frame = bpy.props.IntProperty(name="master_time_frame")

    for c in classes:
        
        bpy.utils.register_class(c)

    #HOTKEY REGISTER

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='SequencerCommon', space_type='SEQUENCE_EDITOR')

    press_executions_index = 0
    for key in duet_hotkeys:
        
        bpy.utils.register_class(
            duet_hotkey_press_executions[press_executions_index])

        # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
        if key == 'TEN':
            kmi = km.keymap_items.new(
                duet_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)
            addon_keymaps.append((km, kmi))
        else:

            kmi = km.keymap_items.new(
                duet_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

            addon_keymaps.append((km, kmi))

        press_executions_index += 1
  
    # handle the keymap

    
    release_executions_index = 0
    for key in duet_hotkeys:
        

        bpy.utils.register_class(
            duet_hotkey_release_executions[release_executions_index])
        # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
        if key == 'TEN':
            kmi = km.keymap_items.new(
                duet_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
            addon_keymaps.append((km, kmi))
        else:
            kmi = km.keymap_items.new(
                duet_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
            addon_keymaps.append((km, kmi))

        release_executions_index += 1





def unregister():
    del bpy.types.Scene.master_time
    del bpy.types.Scene.master_time_frame
    

    for c in classes:
        print("Un-register regular class")
        bpy.utils.unregister_class(c)


    #HOTKEY UNREG
    unreg_executions_index = 0
    for key in duet_hotkeys:
       
        bpy.utils.unregister_class(duet_hotkey_press_executions[unreg_executions_index])

        bpy.utils.unregister_class(duet_hotkey_release_executions[unreg_executions_index])

        unreg_executions_index += 1

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    
    
