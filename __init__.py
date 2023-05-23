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
from bpy.app.handlers import persistent


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

from . ea_op import EA_OT_Master_Clock_Button, EA_OT_Round_FPS_Button, EA_OT_DUET_R_Button, EA_OT_DUET_L_Button, EA_OT_Export_Data_Button, EA_OT_Import_Data_Button, EA_OT_FREE_CHANNEL_Button, MY_OT_SaveAllPreferences, MY_OT_AddFreeChannelInput, MY_OT_CleanFreeChannelInput, SEQUENCE_OT_custom_add_movie_strip, EA_OT_Master_Clock_Button_Adapt, EA_OT_Master_Clock_Button_Move,  EA_OT_AdaptionInfoButton

from . ea_pnl import EA_PT_Panel, EA_PT_Panel_Inputs, EA_PT_Panel_Export, EA_PT_Panel_Free_Channel, EA_PT_Panel_Video_Import, EA_PT_Panel_Import

from . ea_export_data import ExportSomeData
from . ea_import_data import ImportSomeData

from .ea_ot_right_click_handler import SEQUENCER_MT_custom_menu


from .ea_global_variables import FREE_CHANNEL_VARS_PG, FREE_CHANNEL_Preferences, SavePreferencesOperator

from .ea_constants import frame_from_smpte


#Regular classes
classes = (EA_OT_Master_Clock_Button, EA_OT_Round_FPS_Button, EA_OT_DUET_R_Button, EA_OT_DUET_L_Button, EA_OT_FREE_CHANNEL_Button, EA_OT_Export_Data_Button, EA_OT_Import_Data_Button, EA_PT_Panel_Video_Import, EA_PT_Panel, EA_PT_Panel_Inputs, EA_PT_Panel_Export,
           ExportSomeData, ImportSomeData, SEQUENCER_MT_custom_menu, FREE_CHANNEL_VARS_PG, FREE_CHANNEL_Preferences, EA_PT_Panel_Free_Channel, MY_OT_SaveAllPreferences, SavePreferencesOperator, MY_OT_AddFreeChannelInput, MY_OT_CleanFreeChannelInput, SEQUENCE_OT_custom_add_movie_strip, EA_OT_Master_Clock_Button_Adapt, EA_OT_Master_Clock_Button_Move,  EA_OT_AdaptionInfoButton, EA_PT_Panel_Import)
def register():

    bpy.types.Scene.master_time = bpy.props.StringProperty(name="master_time", default="00:00:00:00")
    bpy.types.Scene.master_time_frame = bpy.props.IntProperty(name="master_time_frame")
    bpy.types.Scene.master_time_adaption = bpy.props.StringProperty(
        name="master_time_adaption", default="00:00:00:00")
    
    bpy.types.Scene.active_input = bpy.props.IntProperty(
        name="active_input")
    

    #Button toggles for each input
    bpy.types.WindowManager.duet_left_operator_toggle = bpy.props.BoolProperty(
        default=False,
        update=update_function_duet_left_operator_toggle)
    
    # Button toggles for each input
    bpy.types.WindowManager.duet_right_operator_toggle = bpy.props.BoolProperty(
        default=False,
        update=update_function_duet_right_operator_toggle)
    
    # Button toggles for each input
    bpy.types.WindowManager.free_channel_operator_toggle = bpy.props.BoolProperty(
        default=False,
        update=update_function_free_channel_operator_toggle)



    #Button that toggles export
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.app.handlers.load_post.append(load_handler)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

    for c in classes:
        
        bpy.utils.register_class(c)

    
    bpy.types.SEQUENCER_MT_context_menu.append(custom_menu_func)


@persistent
def load_handler(dummy):
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(meta_text_handler)
    bpy.app.handlers.render_pre.append(meta_text_handler)


def unregister():
    del bpy.types.Scene.master_time
    del bpy.types.Scene.master_time_adaption
    del bpy.types.Scene.master_time_frame
    del bpy.types.Scene.active_input
    del bpy.types.WindowManager.duet_left_operator_toggle
    del bpy.types.WindowManager.duet_right_operator_toggle
    del bpy.types.WindowManager.free_channel_operator_toggle
    
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for c in classes:
       
        bpy.utils.unregister_class(c)


    bpy.types.SEQUENCER_MT_context_menu.remove(custom_menu_func)




def update_function_duet_left_operator_toggle(self, context):
    if self.duet_left_operator_toggle:
        first = bpy.ops.myaddon

        first.duet_left_operator_toggle('INVOKE_DEFAULT')
    return


def update_function_duet_right_operator_toggle(self, context):
    if self.duet_right_operator_toggle:
        first = bpy.ops.myaddon

        first.duet_right_operator_toggle('INVOKE_DEFAULT')
    return


def update_function_free_channel_operator_toggle(self, context):
    if self.free_channel_operator_toggle:
        first = bpy.ops.myaddon

        first.free_channel_operator_toggle('INVOKE_DEFAULT')
    return

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Text Export Operator")


def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="Text Import Operator")

def meta_text_handler(scene, depsgraph):

    # Projected frames from master clock
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time

    frames_from_master_clock = frame_from_smpte(calc_master_time)

    for strip in scene.sequence_editor.sequences_all:
        if strip.type == 'TEXT':

            if strip.name == '@master.time':
                
                fps = bpy.context.scene.render.fps
                fps_base = bpy.context.scene.render.fps_base
                fps_real = fps / fps_base

                # Input SMPTE formatted string
                smpte_string_current = bpy.utils.smpte_from_frame(
                    (scene.frame_current + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)

                # Split the string using ":" as the delimiter
                hours_curr, minutes_curr, seconds_curr, frames_curr = smpte_string_current.split(
                    ":")

                strip.text = str(hours_curr) + ':' + str(minutes_curr) + \
                     ':' + str(seconds_curr) + '+' + str(frames_curr)
                 




def custom_menu_func(self, context):
    layout = self.layout
    layout.menu(SEQUENCER_MT_custom_menu.bl_idname)
