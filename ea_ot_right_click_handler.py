import bpy
import datetime
from bpy.types import Operator
from bpy.types import Sequence
from .ea_constants import Constants

from .ea_constants import pickTagColorForDuet, pickVisualTextColorForDuet
# Add the active_input property to bpy.types.Scene
# bpy.types.Scene.active_input = bpy.props.IntProperty(name="Active Input", default=1)

# Define the custom operators for options 1-3
# ... (same as the previous example) ...

# Define the custom operators for options A-C

operators_info_DUET = Constants.str_OMNI_RES
operators_info_CALIBRATIONS = Constants.str_CALIBRATIONS


def execute_operator(newValue):
    def execute(self, context):
        print(f"Executing operator: {newValue}")

        active_strip = context.scene.sequence_editor.active_strip

        
        
        if active_strip:

            old_input_str = active_strip.name.split(",")
            old_input_type, old_indput_value, old_indput_id, old_input_date = old_input_str[
            0], old_input_str[1], old_input_str[2], old_input_str[3]
           
            if old_input_type == Constants.DUET_LEFT[2]:
                
                active_strip.name = str(old_input_type) + ", " +  str(newValue) + "," + str(old_indput_id) + ", " + str(datetime.datetime.now())
                active_strip.color_tag = pickTagColorForDuet(newValue)

                if hasattr(active_strip, "text"):
                    active_strip.text = str(old_input_type) + " OMNI-RES:" + str(newValue) 
                    active_strip.color = pickVisualTextColorForDuet(newValue)

            elif old_input_type == Constants.DUET_RIGHT[2]:
                
                active_strip.name = str(old_input_type) + ", " + str(newValue) + "," + str(
                    old_indput_id) + ", " + str(datetime.datetime.now())
                active_strip.color_tag = pickTagColorForDuet(newValue)

                if hasattr(active_strip, "text"):
                    active_strip.text = str(
                        old_input_type) + " OMNI-RES:" + str(newValue)
                    active_strip.color = pickVisualTextColorForDuet(newValue)

            elif old_input_type == Constants.FREE_CHANNEL[2]:
               
                active_strip.name = str(old_input_type) + ", " + str(newValue) + "," + str(old_indput_id) + ", " + str(datetime.datetime.now())
                active_strip.color_tag = "COLOR_04"
                if hasattr(active_strip, "text"):
                    active_strip.text = str(
                        old_input_type) + ", " + str(newValue) + "," + str(old_indput_id)
                    


        return {'FINISHED'}
    return execute

# Create and register operator classes in a loop for duet
created_operators_for_duet = []
for name, label, value in operators_info_DUET:
    class_dict = {
        'bl_idname': f"sequencer.{name.lower()}",
        'bl_label': label,
        'execute': execute_operator(value),

    }
    operator_class = type(name, (bpy.types.Operator,), class_dict)
    created_operators_for_duet.append(operator_class)
    bpy.utils.register_class(operator_class)


# Create and register operator classes in a loop for calibrations
created_operators_for_calibrations = []
for name, label, value in operators_info_CALIBRATIONS:
    class_dict = {
        'bl_idname': f"sequencer.{name.lower()}",
        'bl_label': label,
        'execute': execute_operator(value),

    }
    operator_class = type(name, (bpy.types.Operator,), class_dict)
    created_operators_for_calibrations.append(operator_class)
    bpy.utils.register_class(operator_class)



class SEQUENCER_MT_custom_menu(bpy.types.Menu):
    bl_label = "ERGOANNOTATION"
    bl_idname = "SEQUENCER_MT_custom_menu"

   

    def draw(self, context):
        

        layout = self.layout
        active_strip = context.scene.sequence_editor.active_strip if context.scene.sequence_editor else None

        if active_strip:  # Check if any sequence is active
            # Get the first index of the sequence's name
            first_index = active_strip.name.split(",")[0]
            print(first_index)
            if first_index == Constants.DUET_LEFT[2]:

                for operator in created_operators_for_duet:
                    layout.operator(operator.bl_idname)

            elif first_index == Constants.DUET_RIGHT[2]:

                for operator in created_operators_for_duet:
                    layout.operator(operator.bl_idname)

                
            elif first_index == Constants.FREE_CHANNEL[2]:
               

                for operator in created_operators_for_calibrations:
                    layout.operator(operator.bl_idname)
            
            

