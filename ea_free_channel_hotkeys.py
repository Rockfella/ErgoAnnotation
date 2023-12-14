import bpy
import time
import datetime
from bpy.types import Operator
from .ea_constants import Constants


from .ea_hand_exertion_hotkey import executeTheReleaseFromKey, executeThePressFromKey



class onPressKeyFreeChannel0(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_0"
    bl_label = "onPressKey_free_channel_0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel0(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_0"
    bl_label = "onReleaseKey_free_channel_0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
    

class onPressKeyFreeChannel1(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_1"
    bl_label = "onPressKey_free_channel_1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}

class onReleaseKeyFreeChannel1(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_1"
    bl_label = "onReleaseKey_free_channel_1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
    

class onPressKeyFreeChannel2(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_2"
    bl_label = "onPressKey_free_channel_2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel2(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_2"
    bl_label = "onReleaseKey_free_channel_2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
    

class onPressKeyFreeChannel3(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_3"
    bl_label = "onPressKey_free_channel_3"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel3(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_3"
    bl_label = "onReleaseKey_free_channel_3"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}


class onPressKeyFreeChannel4(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_4"
    bl_label = "onPressKey_free_channel_4"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel4(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_4"
    bl_label = "onReleaseKey_free_channel_4"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}


class onPressKeyFreeChannel5(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_5"
    bl_label = "onPressKey_free_channel_5"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel5(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_5"
    bl_label = "onReleaseKey_free_channel_5"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}


class onPressKeyFreeChannel6(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_6"
    bl_label = "onPressKey_free_channel_6"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel6(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_6"
    bl_label = "onReleaseKey_free_channel_6"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}


class onPressKeyFreeChannel7(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_7"
    bl_label = "onPressKey_free_channel_7"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel7(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_7"
    bl_label = "onReleaseKey_free_channel_7"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
    

class onPressKeyFreeChannel8(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_8"
    bl_label = "onPressKey_free_channel_8"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel8(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_8"
    bl_label = "onReleaseKey_free_channel_8"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}


class onPressKeyFreeChannel9(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_free_channel_9"
    bl_label = "onPressKey_free_channel_9"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeThePressFromKey(
            self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFreeChannel9(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_free_channel_9"
    bl_label = "onReleaseKey_free_channel_9"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeTheReleaseFromKey(
            self, context, hotkey)
        return {'FINISHED'}
