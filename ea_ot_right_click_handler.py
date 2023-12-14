import bpy
import datetime
from bpy.types import Operator
from bpy.types import Sequence
from .ea_constants import Constants

from .ea_constants import pickTagColorForHandExertions, pickVisualTextColorForHandExertions, get_slot_value, pickVisualTextColorForFreeMode, pickTagColorForFreeMode
# Add the active_input property to bpy.types.Scene
# bpy.types.Scene.active_input = bpy.props.IntProperty(name="Active Input", default=1)

# Define the custom operators for options 1-3
# ... (same as the previous example) ...

# Define the custom operators for options A-C


def show_warning(message):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title="Warning", icon='ERROR')

operators_info_HAND_EX = Constants.str_MAGNITUDE


def execute_operator(IntValue):
    def execute(self, context):
        print(f"Executing operator: {IntValue}")

        active_strip = context.scene.sequence_editor.active_strip
       
        selected_strips = [strip for strip in bpy.context.scene.sequence_editor.sequences_all if strip.select]

        #for strip in selected_strips:
            #print(strip.name)
        #This one changes below, if its freeChannel input
        newValue = IntValue
        
        if len(selected_strips) > 1:
            #show_warning("More than one strip was selected, ctrl + z to restore")
            self.report(
                {'WARNING'}, "More than one strip was selected, ctrl + z to restore")
        
        if len(selected_strips) > 0:
            for strip in selected_strips:
                print(strip.name)
                old_input_str = strip.name.split(",")
                old_input_type, old_indput_value, old_indput_id, old_input_date = old_input_str[
                    0], old_input_str[1], old_input_str[2], old_input_str[3]

                if old_input_type == Constants.HAND_EX_L[2]:

                    strip.name = str(old_input_type) + ", " + str(newValue) + "," + str(
                        old_indput_id) + ", " + str(datetime.datetime.now())
                    strip.color_tag = pickTagColorForHandExertions(newValue)

                    if hasattr(strip, "text"):
                        strip.text = str(
                            old_input_type) + " MAGNITUDE:" + str(newValue)
                        strip.color = pickVisualTextColorForHandExertions(newValue)

                elif old_input_type == Constants.HAND_EX_R[2]:

                    strip.name = str(old_input_type) + ", " + str(newValue) + "," + str(
                        old_indput_id) + ", " + str(datetime.datetime.now())
                    strip.color_tag = pickTagColorForHandExertions(newValue)

                    if hasattr(strip, "text"):
                        strip.text = str(
                            old_input_type) + " MAGNITUDE:" + str(newValue)
                        strip.color = pickVisualTextColorForHandExertions(newValue)

                elif old_input_type == Constants.FREE_CHANNEL[2]:

                    # Instead of using the IntValue, we get the AddonPreference value that is stored.
                    newValue = get_slot_value(context, IntValue)

                    strip.name = str(old_input_type) + ", " + str(newValue) + "," + str(
                        old_indput_id) + ", " + str(datetime.datetime.now())
                    strip.color_tag = pickTagColorForFreeMode(IntValue)
                    if hasattr(strip, "text"):
                        strip.text = str(
                            old_input_type) + ", " + str(newValue)
                        strip.color = pickVisualTextColorForFreeMode(
                            IntValue)

            

    
                    


        return {'FINISHED'}
    return execute

# Create and register operator classes in a loop for HAND_EX
created_operators_for_hand_ex = []
for name, label, value in operators_info_HAND_EX:
    class_dict = {
        'bl_idname': f"sequencer.{name.lower()}",
        'bl_label': label,
        'execute': execute_operator(value),

    }
    operator_class = type(name, (bpy.types.Operator,), class_dict)
    created_operators_for_hand_ex.append(operator_class)
    bpy.utils.register_class(operator_class)




class CreatedOperatorsFreeChannel:

    created_operators_for_free_channel = []

    
loop_index = 0
for i in range(20):
     
    default_name = "MY_OT_FREE_CHANNEL_SLOT_"
    new_name = str(default_name) + str(loop_index)
    class_dict = {
         'bl_idname': f"sequencer.{new_name.lower()}",
         'bl_label': new_name,
        'execute': execute_operator(loop_index),

    }
    operator_class = type(new_name, (bpy.types.Operator,), class_dict)
    CreatedOperatorsFreeChannel.created_operators_for_free_channel.append(
        operator_class)
    bpy.utils.register_class(operator_class)
    
    #print(operator_class.bl_label)
    loop_index += 1


class SEQUENCER_OT_SetRangeToStrips(bpy.types.Operator):
    bl_idname = "sequencer.set_range_to_strips_custom"
    bl_label = "Set Range to Strip"
    bl_description = "Set the scene's start and end frame to the selected strip"

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        bpy.ops.sequencer.set_range_to_strips()
        return {'FINISHED'}


class SEQUENCER_MT_custom_menu(bpy.types.Menu):
    bl_label = "Edit Annotation"
    bl_idname = "SEQUENCER_MT_custom_menu"

   

    def draw(self, context):
        

        layout = self.layout
        active_strip = context.scene.sequence_editor.active_strip if context.scene.sequence_editor else None
        selected_strips = [
            strip for strip in bpy.context.scene.sequence_editor.sequences_all if strip.select]

        # Get the names of all selected strips
        selected_names = [strip.name.split(",")[0]
                          for strip in selected_strips]

        # Check if all names are the same by converting the list to a set and checking its length
        all_have_same_name = len(set(selected_names)) == 1

        if all_have_same_name:
            print("All selected strips have the same name.")
        else:
            print("Not all selected strips have the same name.")

        #TODO: OK NOW WE CAN START BUILDING SO THAT IT ONLY WORKS IF THEY HAVE THE SAME NAME 

        if not all_have_same_name:
            #show_warning(
              #   "Selected strips needs to be of the same kind")
            #self.report(
              #  {'WARNING'}, "Selected strips needs to be of the same kind")
            layout.label(text='Selected strips needs to be of the same type')
            return {'CANCELLED'}

        if len(selected_strips) > 0:  # Check if any sequence is active
            # Get the first index of the sequence's name
            first_index = selected_strips[0].name.split(",")[0]
            print(first_index)
            if first_index == Constants.HAND_EX_L[2]:

                for operator in created_operators_for_hand_ex:
                    layout.operator(operator.bl_idname)

            elif first_index == Constants.HAND_EX_R[2]:

                for operator in created_operators_for_hand_ex:
                    layout.operator(operator.bl_idname)

                
            elif first_index == Constants.FREE_CHANNEL[2]:
               
                addon_prefs = bpy.context.preferences.addons[__package__].preferences
                free_channel_vars = addon_prefs.free_channel_vars

                slots_to_show = free_channel_vars.slots_to_show
               
                limited_loop = 0
                
                    
                for operator in CreatedOperatorsFreeChannel.created_operators_for_free_channel:
                    if limited_loop <= slots_to_show:
                        layout.operator(operator.bl_idname, text=get_slot_value(
                            context, limited_loop))
                        limited_loop += 1
                    else:
                        break
                    
            
#def get_slot_value(context, index):
#    addon_prefs = context.preferences.addons[__package__].preferences
#    free_channel_vars = addon_prefs.free_channel_vars
#    # Access the slot using the provided index
#    slot_key = f"slot_{index}"
#    slot_value = getattr(free_channel_vars, slot_key)
#    return str(slot_value)
