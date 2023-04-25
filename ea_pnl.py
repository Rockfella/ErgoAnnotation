import bpy

from bpy.types import Panel


class EA_PT_Panel(Panel):
    bl_label = "MasterClock"
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




