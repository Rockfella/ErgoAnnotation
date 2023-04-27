import bpy

from bpy.types import Panel


class EA_PT_Panel(Panel):
    bl_label = "Master Clock"
    bl_idname = "SEQUENCER_PT_my_addon_panel2"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        # Add a button with a callback to the button_function
        layout.operator("myaddon.round_fps_button_operator")
        layout.operator("myaddon.master_button_operator")
        layout.prop(context.scene, "master_time", text="Time",
                    expand=True)
        # Add an input field with a callback to the input_function


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
        #col.operator("myaddon.round_fps_button_operator")
        
        
class EA_PT_Panel_Export(Panel):
    bl_label = "Export"
    bl_idname = "SEQUENCER_PT_my_addon_panel3"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'ERGONOMICS'

    def draw(self, context):
        layout = self.layout

        # Add a button with a callback to the button_function
        layout.operator("myaddon.export_data_operator")
        


