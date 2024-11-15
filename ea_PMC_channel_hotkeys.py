import bpy
#import time
#import datetime
from bpy.types import Operator
#from .ea_constants import Constants


from .ea_hand_exertion_hotkey import executeTheReleaseFromKey, executeThePressFromKey



class onPressKeyPostureMoveCode0(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_0"
    bl_label = "onPressKey_posture_move_code_0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        
        
 

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode0(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_0"
    bl_label = "onReleaseKey_posture_move_code_0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        
        return {'FINISHED'}
    

class onPressKeyPostureMoveCode1(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_1"
    bl_label = "onPressKey_posture_move_code_1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}

class onReleaseKeyPostureMoveCode1(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_1"
    bl_label = "onReleaseKey_posture_move_code_1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        
        return {'FINISHED'}
    

class onPressKeyPostureMoveCode2(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_2"
    bl_label = "onPressKey_posture_move_code_2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode2(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_2"
    bl_label = "onReleaseKey_posture_move_code_2"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}
    

class onPressKeyPostureMoveCode3(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_3"
    bl_label = "onPressKey_posture_move_code_3"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode3(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_3"
    bl_label = "onReleaseKey_posture_move_code_3"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}


class onPressKeyPostureMoveCode4(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_4"
    bl_label = "onPressKey_posture_move_code_4"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode4(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_4"
    bl_label = "onReleaseKey_posture_move_code_4"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}


class onPressKeyPostureMoveCode5(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_5"
    bl_label = "onPressKey_posture_move_code_5"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode5(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_5"
    bl_label = "onReleaseKey_posture_move_code_5"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}


class onPressKeyPostureMoveCode6(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_6"
    bl_label = "onPressKey_posture_move_code_6"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode6(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_6"
    bl_label = "onReleaseKey_posture_move_code_6"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}


class onPressKeyPostureMoveCode7(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_7"
    bl_label = "onPressKey_posture_move_code_7"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode7(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_7"
    bl_label = "onReleaseKey_posture_move_code_7"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}
    

class onPressKeyPostureMoveCode8(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_8"
    bl_label = "onPressKey_posture_move_code_8"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode8(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_8"
    bl_label = "onReleaseKey_posture_move_code_8"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}


class onPressKeyPostureMoveCode9(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_posture_move_code_9"
    bl_label = "onPressKey_posture_move_code_9"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        bpy.data.scenes[context.scene.name].active_hotkey = int(hotkey)
        executeThePressFromKey(
            self, context, hotkey)
        

        return {'FINISHED'}


class onReleaseKeyPostureMoveCode9(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_posture_move_code_9"
    bl_label = "onReleaseKey_posture_move_code_9"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeTheReleaseFromKey(
            self, context, hotkey)
        
        return {'FINISHED'}
