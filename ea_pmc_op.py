import ast
import bpy
from .ea_constants import Constants
from .ea_constants import  get_pmc_options
from .ea_hand_exertion_hotkey import auto_drag_strip


      
class SEQUENCER_OT_pmc_menu_operator(bpy.types.Operator):
    bl_idname = "sequencer.custom_menu_pmc_operator"
    bl_label = "PMC Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print("EXECUTED THIS")
        #self.report({'INFO'}, "PMC Option Selected")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Check if the handler is active before removing it
        if auto_drag_strip in bpy.app.handlers.frame_change_post:
            bpy.app.handlers.frame_change_post.remove(auto_drag_strip)
            print("auto_drag_strip handler removed")
        
        wm = context.window_manager
        return wm.invoke_popup(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select an Option:")
        curren_input = bpy.data.scenes[bpy.context.scene.name].active_input
        active_strip = context.scene.sequence_editor.active_strip
        split_text = active_strip.name.split(',')
        input_model = split_text[0].strip()
        input_category = split_text[1].strip()
        input_id = int(split_text[2].strip())
        
        if curren_input == Constants.POST_MOVE_CODE[0]:
            options_for_category = get_pmc_options(input_id)
            print("Displaying options")
            if options_for_category[0]:
                id_for_category = options_for_category[1]
                options_list = list(options_for_category[0].keys())
                for index, key in enumerate(options_list):
                    op = layout.operator(f"sequencer.pmc_option_{index + 1}", text=str(key))
                    selected_options_details = options_for_category[0].get(key)
                    op.option_info = f"{key}, {selected_options_details}"
            else:
                layout.label(text="No available options")
                return {'CANCELLED'}
        else:
            layout.label(text="No available options")
            return {'CANCELLED'}

def break_down_and_edit_active_strip(new_input):
    act_strip = bpy.context.scene.sequence_editor.active_strip
    act_name = act_strip.name
    act_components = [component.strip() for component in act_name.split(',')]
    
    
    split_new_input = new_input.split(',', 1) 
    first_word = split_new_input[0].strip()
    description_option = split_new_input[1].strip()
    parsed_description_option = ast.literal_eval(description_option)
    id_value = parsed_description_option.get('id')
    
    active_input = act_components[0]
    joined_name = f"{active_input}, {first_word}, {id_value}"
    act_components[1] = first_word  # Replace with the new second word
    act_components[2] = str(id_value)
    
    
    output_name = ', '.join(act_components)
    act_strip.name = output_name
    act_strip.text = joined_name
    
    return joined_name
    

         
        
class SEQUENCER_OT_pmc_option_1(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_1"
    bl_label = "Option 1"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        
        updated_input = break_down_and_edit_active_strip(self.option_info)
        
        #bpy.ops.sequencer.custom_menu_pmc_operator('EXEC_DEFAULT')
        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")

        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_2(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_2"
    bl_label = "Option 2"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)
        
        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_3(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_3"
    bl_label = "Option 3"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)
        
        

        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}
    
class SEQUENCER_OT_pmc_option_4(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_4"
    bl_label = "Option 4"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_5(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_5"
    bl_label = "Option 5"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_6(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_6"
    bl_label = "Option 6"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        


        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_7(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_7"
    bl_label = "Option 7"
    option_info: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)
        
        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_8(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_8"
    bl_label = "Option 8"
    option_info: bpy.props.StringProperty()
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        

        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_9(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_9"
    bl_label = "Option 9"
    option_info: bpy.props.StringProperty()
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}

class SEQUENCER_OT_pmc_option_10(bpy.types.Operator):
    bl_idname = "sequencer.pmc_option_10"
    bl_label = "Option 10"
    option_info: bpy.props.StringProperty()
    def invoke(self, context, event):
        # Access the event data here
        self.event = event
        
        # Optionally call execute from invoke
        return self.execute(context)
    def execute(self, context):
        updated_input = break_down_and_edit_active_strip(self.option_info)

        
        
        self.report({'INFO'}, f"Changed to: {updated_input}")
        return {'FINISHED'}



