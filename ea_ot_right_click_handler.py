import bpy
import datetime
#from bpy.types import Operator
#from bpy.types import Sequence
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


class SEQUENCER_OT_add_comment(bpy.types.Operator):
    bl_idname = "sequencer.add_comment"
    bl_label = "Add Comment"
    bl_description = "Add a comment to the selected strip"
    
    def_comment: bpy.props.StringProperty(
        name="Comment",
        description="",
        default=""
        ) # type: ignore

    def execute(self, context):
        scene = bpy.context.scene
        if not scene.sequence_editor:
            print("No sequence editor found in the active scene.")
            return
        active_strip = context.scene.sequence_editor.active_strip
        
        #Add a custom property named Comment, which can be retrieved later
        if active_strip:
            active_strip["Comment"] = self.def_comment
            self.report({'INFO'}, f"Comment added: {self.def_comment}.")
        else: 
            self.report({'INFO'}, "No active strip found.")
            
        return {'FINISHED'}

    def invoke(self, context, event):
        active_strip = context.scene.sequence_editor.active_strip
        if "Comment" in active_strip:
            current_comment = active_strip["Comment"]
            #Change the placeholder input to the found comment
            self.def_comment = current_comment
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "def_comment")
        



class SEQUENCER_OT_custom_comment(bpy.types.Operator):
    bl_idname = "sequencer.custom_comment"
    bl_label = "Comment Annotation"
    bl_description = "Add a comment to the strip."

    @classmethod
    def poll(cls, context):
        return context.selected_sequences

    def execute(self, context):
        bpy.ops.sequencer.add_comment('INVOKE_DEFAULT')
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
                    
            
