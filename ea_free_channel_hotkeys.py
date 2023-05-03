import bpy
import time
import datetime
from bpy.types import Operator
from .ea_constants import Constants


from .ea_duet_hotkey import executeTheReleaseFromKey, executeThePressFromKey



class onPressKeyFreeChannelF(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_f"
    bl_label = "onPressKey_free_channel_F"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = 'F'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannelF(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_f"
    bl_label = "onReleaseKey_free_channel_F"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = 'F'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
