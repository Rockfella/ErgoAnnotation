import bpy


from bpy.types import Panel
from .ea_constants import Constants
from .ea_ot_right_click_handler import CreatedOperatorsFreeChannel


class EA_PT_Panel(Panel):
    bl_label = "Master Time"
    bl_idname = "SEQUENCER_PT_my_addon_panel2"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout
        # Get sequence editor
        seq_editor = bpy.context.scene.sequence_editor

        # Get all markers
        markers = bpy.context.scene.timeline_markers
        # Add a button with a callback to the button_function
        #TODO: CONSIDER REMOVING THE ROUND FPS 
       # layout.operator("myaddon.round_fps_button_operator")
        scene = bpy.context.scene
        if '@master.time' in (strip.name for strip in scene.sequence_editor.sequences_all if strip.type == 'TEXT'):
            print("")
        else:
            layout.operator("myaddon.master_button_operator")
            layout.prop(context.scene, "master_time", text="Time",
                        expand=True)
            
        
        
        for strip in scene.sequence_editor.sequences_all:
              
            if strip.type == 'TEXT':
                if strip.name == '@master.time':

                    layout.prop(context.scene, "master_time_adaption", text="Adapt",
                        expand=True)
                    row = layout.row()
                   
                    row = layout.row()
                    row.operator("object.adaption_info_button",
                                 text="", icon='QUESTION')
                    
                    layout.operator(
                        "myaddon.master_button_operator_push", text="Stretch or Shrink to time")
                    
                    #A new option to move the strip according the the master time will pop up, if there is a meta strip selected and there is a marker placed within its range, that one will be used to move the strip according to master clock
                   
                    show_button = False


                    for marker in markers:
                        if seq_editor.active_strip.frame_final_start <= marker.frame <= seq_editor.active_strip.frame_final_end:
                            show_button = True
                            break  # No need to check further, we found a marker that matches the condition
                        
                    if show_button:
                        if seq_editor.active_strip:
                            layout.operator("myaddon.master_button_operator_move", text="Move to Time")
                    else:
                        layout.label(
                            text="Hover over questionmark icon to learn how to move clip.")
                        
                   
                   
                   


class EA_PT_Panel_Free_Channel(Panel):
    bl_label = "Free Channel Inputs"
    bl_idname = "SEQUENCER_PT_my_addon_panel_free_channel"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        free_channel_vars = addon_prefs.free_channel_vars
        
        slots_to_show = free_channel_vars.slots_to_show
        
        

        row_second = layout.row()
        op = row_second.operator(
            "my.preferencesaddfreechannelinput", text="Add Input")

        # Loop through each StringProperty in the class
        loop_index = 0
        for key, prop in free_channel_vars.bl_rna.properties.items():
            # Skip properties that are not StringProperties
            
            if key.startswith('slot_') and loop_index <= slots_to_show:

               
            
                row_next = layout.row()
                split = row_next.split(factor=1.0)
                if (loop_index + 1) <= 10:
                    default = str('SEQUENCE_COLOR_0')
                    loop_index_str = str(loop_index + 1)
                    iconstr = default + loop_index_str

                    if (loop_index + 1) == 1:
                        iconstr = str('SEQUENCE_COLOR_01')
                    elif (loop_index + 1) == 2:
                        iconstr = str('SEQUENCE_COLOR_02')
                    elif (loop_index + 1) == 3:
                        iconstr = str('SEQUENCE_COLOR_03')
                    elif (loop_index + 1) == 4:
                        iconstr = str('SEQUENCE_COLOR_04')
                    elif (loop_index + 1) == 5:
                        iconstr = str('SEQUENCE_COLOR_05')
                    elif (loop_index + 1) == 6:
                        iconstr = str('SEQUENCE_COLOR_06')
                    elif (loop_index + 1) == 7:
                        iconstr = str('SEQUENCE_COLOR_07')
                    elif (loop_index + 1) == 8:
                        iconstr = str('SEQUENCE_COLOR_08')
                    elif (loop_index + 1) >= 10:
                        iconstr = str('SEQUENCE_COLOR_04')


                    prop_ui = split.prop(free_channel_vars, key, text='NUM ' + str(loop_index), icon= iconstr,
                                         expand=True)
                else:
                    prop_ui = split.prop(free_channel_vars, key, text=str(loop_index),
                                         expand=True)
                current_value = getattr(free_channel_vars, key)
                    
                
                

                loop_index += 1

        row_first = layout.row()
        op = row_first.operator("my.preferencesavecall", text="Save Inputs")
        row_third = layout.row()
        op = row_third.operator(
            "my.preferencescleanfreechannelinput", text="Clean all")
            

        
            
       

class EA_PT_Panel_Inputs(Panel):
    bl_label = "Input Model"
    bl_idname = "SEQUENCER_PT_my_addon_panel_inputs"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout
        # First row
        row = layout.row(align=True)
        col = row.column_flow(columns=2)
        #col.operator("myaddon.duet_l_button_operator")

        # duet_left_operator_toggle
        wm = context.window_manager
        duet_left_label = "DUET LEFT" if wm.duet_left_operator_toggle else "DUET LEFT"
        col.prop(wm, 'duet_left_operator_toggle',
                 text=duet_left_label, toggle=True)
        # duet_right_operator_toggle
        duet_right_label = "DUET RIGHT" if wm.duet_left_operator_toggle else "DUET RIGHT"
        col.prop(wm, 'duet_right_operator_toggle',
                 text=duet_right_label, toggle=True)

        #col.operator("myaddon.duet_r_button_operator")

        # Second row

       
        row = layout.row(align=True)
        col = row.column_flow(columns=2)
        free_channel_label = "FREE CHANNEL" if wm.duet_left_operator_toggle else "FREE CHANNEL"
        col.prop(wm, 'free_channel_operator_toggle',
                 text=free_channel_label, toggle=True)
        
        
class EA_PT_Panel_Export(Panel):
    bl_label = "Export File"
    bl_idname = "SEQUENCER_PT_my_addon_panel3"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        # Add a button with a callback to the button_function
        layout.operator("myaddon.export_data_operator")


class EA_PT_Panel_Import(Panel):
    bl_label = "Import File"
    bl_idname = "SEQUENCER_PT_my_addon_panel_import_file"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        # Add a button with a callback to the button_function
        layout.operator("myaddon.import_data_operator")
        

class EA_PT_Panel_Video_Import(Panel):
    bl_label = "Import"
    bl_idname = "SEQUENCER_PT_video_import"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        # Add a button with a callback to the button_function
        layout.operator("sequence.custom_add_movie_strip")
        
