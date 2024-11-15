
import bpy
#import time
import datetime
from bpy.types import Operator
from .ea_constants import Constants
from .ea_constants import (pickTagColorForHandExertions, pickVisualTextColorForHandExertions, 
                           get_slot_value, pickVisualTextColorForFreeMode, pickTagColorForFreeMode, get_pmc_value, get_pmc_id)

# ------------------------------------------------------------------------
#    HOTKEY: ZERO
# ------------------------------------------------------------------------


class onPressKeyZERO(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_zero"
    bl_label = "onPressKeyZERO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyZERO(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_zero"
    bl_label = "onReleaseKeyZERO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: ONE
# ------------------------------------------------------------------------

class onPressKeyONE(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_one"
    bl_label = "onPressKeyONE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyONE(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_one"
    bl_label = "onReleaseKeyONE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: TWO
# ------------------------------------------------------------------------

class onPressKeyTWO(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_two"
    bl_label = "onPressKeyTWO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTWO(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_two"
    bl_label = "onReleaseKeyTWO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    HOTKEY: THREE
# ------------------------------------------------------------------------


class onPressKeyTHREE(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_three"
    bl_label = "onPressKeyTHREE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTHREE(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_three"
    bl_label = "onReleaseKeyTHREE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    HOTKEY: FOUR
# ------------------------------------------------------------------------


class onPressKeyFOUR(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_four"
    bl_label = "onPressKeyFOUR"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFOUR(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_four"
    bl_label = "onReleaseKeyFOUR"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: FIVE
# ------------------------------------------------------------------------


class onPressKeyFIVE(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_five"
    bl_label = "onPressKeyFIVE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFIVE(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_five"
    bl_label = "onReleaseKeyFIVE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: SIX
# ------------------------------------------------------------------------


class onPressKeySIX(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_six"
    bl_label = "onPressKeySIX"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeySIX(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_six"
    bl_label = "onReleaseKeySIX"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: SEVEN
# ------------------------------------------------------------------------


class onPressKeySEVEN(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_seven"
    bl_label = "onPressKeySEVEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeySEVEN(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_seven"
    bl_label = "onReleaseKeySEVEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: EIGHT
# ------------------------------------------------------------------------


class onPressKeyEIGHT(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_eight"
    bl_label = "onPressKeyEIGHT"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyEIGHT(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_eight"
    bl_label = "onReleaseKeyEIGHT"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    HOTKEY: NINE
# ------------------------------------------------------------------------


class onPressKeyNINE(Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_nine"
    bl_label = "onPressKeyNINE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyNINE(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_nine"
    bl_label = "onReleaseKeyNINE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    HOTKEY: ONE10
# ------------------------------------------------------------------------


class onPressKeyTEN(Operator):
    """On Release"""
    bl_idname = "object.on_press_key_ten"
    bl_label = "onPressKeyTEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '10'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTEN(Operator):
    """On Release"""
    bl_idname = "object.on_release_key_ten"
    bl_label = "onReleaseKeyTEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '10'
        executeTheReleaseFromKey(self, context, hotkey)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    EXECUTE BASED ON HOTKEY
# ------------------------------------------------------------------------


def executeThePressFromKey(self, context, key):
    # global id  # Declare id as global
    
    #Deselect all strips to perfom operations on the newly created strip
    bpy.ops.sequencer.deselect_all_strips()
    
    # Check if the handler is active before removing it
    if auto_drag_strip in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(auto_drag_strip)
        print("auto_drag_strip handler removed")
        bpy.data.scenes[context.scene.name].active_hotkey = -2

    else:
        # Get the active scene
        scene = bpy.context.scene
        sequence_editor = scene.sequence_editor
    
        # Number of sequences to produce ID
        num_sequences = len(sequence_editor.sequences)
        # Next id
        num_sequence_id = num_sequences + 1
    
        
        
        choosen_tag_color = "COLOR_04"
    
        
    
        curren_input = bpy.data.scenes[bpy.context.scene.name].active_input
        current_input_str = ""
        text_strip_visual_text = ""
        text_strip_visual_location = (0,0)
        text_strip_visual_color = (0.35, 0.82, 0.51, 1.0) #default
    
        current_input_channel = -1
        if curren_input == Constants.HAND_EX_L[0]:
            current_input_str = Constants.HAND_EX_L[2]
            current_input_channel = Constants.HAND_EX_L[1]
            text_strip_visual_text = current_input_str + " MAGNITUDE:" + str(key)
            text_strip_visual_location = (0.05, 0.18)
            choosen_tag_color = pickTagColorForHandExertions(key)
            text_strip_visual_color = pickVisualTextColorForHandExertions(key)
            
    
        elif curren_input == Constants.HAND_EX_R[0]:
            current_input_str = Constants.HAND_EX_R[2] 
            current_input_channel = Constants.HAND_EX_R[1]
            text_strip_visual_text = current_input_str + " MAGNITUDE:" + str(key)
            text_strip_visual_location = (0.05, 0.25)
            choosen_tag_color = pickTagColorForHandExertions(key)
            text_strip_visual_color = pickVisualTextColorForHandExertions(key)
    
        elif curren_input == Constants.FREE_CHANNEL[0]:
            current_input_str = Constants.FREE_CHANNEL[2]
            current_input_channel = Constants.FREE_CHANNEL[1]
            text_strip_visual_text = current_input_str + ", " + get_slot_value(context, key)
            text_strip_visual_location = (0.05, 0.32)
            choosen_tag_color = pickTagColorForFreeMode(key)
            text_strip_visual_color = pickVisualTextColorForFreeMode(key)
            
           
        elif curren_input == Constants.POST_MOVE_CODE[0]:
            current_input_str = Constants.POST_MOVE_CODE[2]
            current_input_channel = Constants.POST_MOVE_CODE[1]
            
            pmc_value = get_pmc_value(key)
            pmc_id = get_pmc_id(key)
            
            text_strip_visual_text = current_input_str + ", " + pmc_value + ", " + str(pmc_id)
            text_strip_visual_location = (0.05, 0.32)
            choosen_tag_color = pickTagColorForFreeMode(key)
            text_strip_visual_color = pickVisualTextColorForFreeMode(key)
    
        #Remember the default channel to help the visual position
        current_input_channel_base = current_input_channel
    
        time_now = datetime.datetime.now()
        formatted_date_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
        sequence_name_hand_exertion = current_input_str + ", " + key + ", " + str(num_sequence_id) + ", " + formatted_date_time
        sequence_name_free_channel = current_input_str + ", " + str(get_slot_value(context, key)) + \
            ", " + str(num_sequence_id) + ", " + formatted_date_time
            
        sequence_name_pmc_channel = text_strip_visual_text  + \
            ", " + str(num_sequence_id) + ", " + formatted_date_time
    
        current_frame = bpy.context.scene.frame_current
        
    
        #In case HAND_EXERTIONS is active we can direclty use the hotkey as str, otherwise use other
        image_str = ""
        if curren_input == Constants.HAND_EX_L[0]:
            image_str = sequence_name_hand_exertion
    
        elif curren_input == Constants.HAND_EX_R[0]:
            image_str = sequence_name_hand_exertion
        elif curren_input == Constants.FREE_CHANNEL[0]:
            image_str = sequence_name_free_channel
            
        elif curren_input == Constants.POST_MOVE_CODE[0]:
            image_str = sequence_name_pmc_channel
    
        strip_exists = False
    
        if sequence_editor is not None:
            free_channel_found = False
        
        while not free_channel_found:
            strip_exists = False
            for seq in sequence_editor.sequences:
                if seq.channel == current_input_channel and (seq.frame_final_start <= current_frame and seq.frame_final_end >= current_frame):
                    strip_exists = True
                    current_input_channel += 1  # Move to the channel above
                   
                    break
                
            # If after checking all strips, no strip occupies the current channel at the given frame:
            if not strip_exists:
                free_channel_found = True
                add_strip(image_str, current_frame, current_input_channel, text_strip_visual_text,
                          text_strip_visual_color, text_strip_visual_location, choosen_tag_color, current_input_channel_base)


def add_strip(image_str, current_frame, current_input_channel, text_strip_visual_text, text_strip_visual_color, text_strip_visual_location, choosen_tag_color, current_input_channel_base):
    text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
        name=image_str,
        type='TEXT',
        frame_start=current_frame,
        frame_end=current_frame + 5,
        channel=current_input_channel
    )
    
    #Selecting the newly created strip so operations can be run on it
    text_strip.select = True
    bpy.context.scene.sequence_editor.active_strip = text_strip
    
    text_strip.text = text_strip_visual_text
    # Set the font and size for the text strip
    text_strip.font_size = 50.0
    text_strip.color = text_strip_visual_color

    text_strip.use_bold = True
    # Set the position and alignment of the text strip
    # Set the position of the text strip
    text_strip.location = visual_location_from_channel(
        current_input_channel, current_input_channel_base, text_strip_visual_location)
    text_strip.use_shadow = True
    text_strip.use_box = True
    text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
    # text_strip.wrap_width = 300  # Set the wrap width of the text strip
    text_strip.align_x = 'LEFT'  # Set the horizontal alignment
    text_strip.align_y = 'CENTER'  # Set the vertical alignment
    text_strip.color_tag = choosen_tag_color

    current_frame = bpy.context.scene.frame_current

    seq_editor = bpy.context.scene.sequence_editor
    channel_to_rename = seq_editor.channels[current_input_channel]
    # Rename the channel
    channel_to_rename.name = 'ANNOTATION'

    # If we ever need markers
    # scene.timeline_markers.new(num_markers_str, frame=current_frame)

    # Initiate the drag of the sequence just created
    # Check if there is another stripped being dragged first
    if auto_drag_strip not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(auto_drag_strip)

#Sets the visual position of the text based on the channel 


def visual_location_from_channel(index, current_input_channel_base, text_strip_visual_location):
    x = 0.05 
    start_y = text_strip_visual_location[1]
    increment = 0.07
    return (x, start_y + (index - current_input_channel_base) * increment)

def executeTheReleaseFromKey(self, context, key):

    #TODO: TEST, REMOVE AFTER TESTING
    # If we ever need markers
    # scene.timeline_markers.new(num_markers_str, frame=current_frame)
    print("EXECUTED RELEASE")
    # Stop the drag of the sequence
    
    #if auto_drag_strip in bpy.app.handlers.frame_change_post:
    #    bpy.app.handlers.frame_change_post.remove(auto_drag_strip)
    


def auto_drag_strip(scene, depsgraph):
    #print("DRAGGING")
    active_strip = bpy.context.scene.sequence_editor.active_strip.type
    if active_strip == 'TEXT' and active_strip != '@master.time':
        #TODO: This was added to handle when active strips are deleted
    
        scene = bpy.context.scene

        current_frame = bpy.context.scene.frame_current
        sequence_editor = scene.sequence_editor

        num_sequences = len(sequence_editor.sequences)
        active_strip = sequence_editor.sequences[num_sequences - 1]

        actual_end = (current_frame - active_strip.frame_start + 1) #adding one will make the current input visiable
        active_strip.frame_final_duration = int(actual_end)
    else:
        #If we are trying to drag empty
        bpy.app.handlers.frame_change_post.remove(auto_drag_strip)

