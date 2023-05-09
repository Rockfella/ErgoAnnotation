import bpy

from bpy.types import Operator
from bpy.app.handlers import persistent
from .ea_inputswitch import inputSwitchClass
from .ea_constants import Constants
from .ea_global_variables import SavePreferencesOperator


class MY_OT_SaveAllPreferences(bpy.types.Operator):
    bl_idname = "my.preferencesavecall"
    bl_label = "Call Function"
    bl_description = "Save to presets"
    index: bpy.props.IntProperty()
    

    def execute(self, context):
        
        bpy.ops.preferences.save()

        return {'FINISHED'}
    

class MY_OT_AddFreeChannelInput(bpy.types.Operator):
    bl_idname = "my.preferencesaddfreechannelinput"
    bl_label = "Call Function"
    bl_description = "Add inputs available for the free channel"
    text: bpy.props.StringProperty(default="Add Input")

    def execute(self, context):
        
        #Add the number of slots visible
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        free_channel_vars = addon_prefs.free_channel_vars

        #setting a cap on how many slots that can be added
        if free_channel_vars.slots_to_show < 20:
            free_channel_vars.slots_to_show += 1
            bpy.ops.preferences.save()
        else:
            self.text = "Slots filled"
            free_channel_vars.slots_to_show = 3
            
        return {'FINISHED'}


class MY_OT_CleanFreeChannelInput(bpy.types.Operator):
    bl_idname = "my.preferencescleanfreechannelinput"
    bl_label = "Really want to clear all?"
    bl_description = "Clear the list of inputs for the free channel"
    text: bpy.props.StringProperty(default="Add Input")

    def execute(self, context):

        # Add the number of slots visible
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        free_channel_vars = addon_prefs.free_channel_vars

        # Loop through each StringProperty in the class
        loop_index = 0
        for key, prop in free_channel_vars.bl_rna.properties.items():
            # Skip properties that are not StringProperties

            if key.startswith('slot_'):
                clean_str = str("Empty") + str(loop_index)
                setattr(free_channel_vars, key, clean_str)
                loop_index += 1
        free_channel_vars.slots_to_show = 3
        bpy.ops.preferences.save()

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class EA_OT_Master_Clock_Button(Operator):
    bl_idname = "myaddon.master_button_operator"
    bl_label = "Set Master Clock"
    bl_description = "Sets the master clock to the frame selected in the timeline"

    def execute(self, context):
        # button_function(self, context)

        if check_string_format(context.scene.master_time):
            print("String is in the correct format.")
            setNewMasterClock(self, context)

        else:
            print("String is not in the correct format.")

        return {'FINISHED'}


class EA_OT_Round_FPS_Button(Operator):
    bl_idname = "myaddon.round_fps_button_operator"
    bl_label = "Round FPS"
    bl_description = "Rounds the FPS to help determine exact frames"
    def execute(self, context):
        # button_function(self, context)
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base

        bpy.context.scene.render.fps = round(fps_real)
        bpy.context.scene.render.fps_base = 1.00

        return {'FINISHED'}


class EA_OT_DUET_L_Button(Operator):
    bl_idname = "myaddon.duet_left_operator_toggle"
    bl_label = "My Operator"

    def modal(self, context, event):

        if not context.window_manager.duet_left_operator_toggle:
            context.window_manager.event_timer_remove(self._timer)
            print("Stopped")

            #Stop the input for this one, but only in case the user press the same button again to turn off and has not pressed another button
            if bpy.data.scenes[bpy.context.scene.name].active_input == Constants.DUET_LEFT[0]: #if it remains the same as before, it means the button has been turned off from itself
                inputSwitchClass.input_switch(self, -2)


            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):

        #turn off the other buttons
        context.window_manager.duet_right_operator_toggle = False
        context.window_manager.free_channel_operator_toggle = False

        self._timer = context.window_manager.event_timer_add(
            time_step = 0.05, window = context.window)
        
        print("Start")
        inputSwitchClass.input_switch(self, Constants.DUET_LEFT[0])
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class EA_OT_DUET_R_Button(Operator):
    bl_idname = "myaddon.duet_right_operator_toggle"
    bl_label = "My Operator"

    def modal(self, context, event):

        if not context.window_manager.duet_right_operator_toggle:
            context.window_manager.event_timer_remove(self._timer)
            print("Stopped")

            # Stop the input for this one, but only in case the user press the same button again to turn off and has not pressed another button
            # if it remains the same as before, it means the button has been turned off from itself
            if bpy.data.scenes[bpy.context.scene.name].active_input == Constants.DUET_RIGHT[0]:
                inputSwitchClass.input_switch(self, -2)
            
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # turn off the other buttons
        context.window_manager.duet_left_operator_toggle = False
        context.window_manager.free_channel_operator_toggle = False

        self._timer = context.window_manager.event_timer_add(
            time_step=0.05, window=context.window)

        print("Start")
        inputSwitchClass.input_switch(self, Constants.DUET_RIGHT[0])
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class EA_OT_FREE_CHANNEL_Button(Operator):
    bl_idname = "myaddon.free_channel_operator_toggle"
    bl_label = "My Operator"

    def modal(self, context, event):

        if not context.window_manager.free_channel_operator_toggle:
            context.window_manager.event_timer_remove(self._timer)
            print("Stopped")

            # Stop the input for this one, but only in case the user press the same button again to turn off and has not pressed another button
            # if it remains the same as before, it means the button has been turned off from itself
            if bpy.data.scenes[bpy.context.scene.name].active_input == Constants.FREE_CHANNEL[0]:
                inputSwitchClass.input_switch(self, -2)

            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # turn off the other buttons
        context.window_manager.duet_left_operator_toggle = False
        context.window_manager.duet_right_operator_toggle = False

        self._timer = context.window_manager.event_timer_add(
            time_step=0.05, window=context.window)

        print("Start")
        inputSwitchClass.input_switch(self, Constants.FREE_CHANNEL[0])
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class EA_OT_Export_Data_Button(Operator):
    bl_idname = "myaddon.export_data_operator"
    bl_label = "Export Data"
    bl_description = "Export Data to CSV"

    def execute(self, context):
        # button_function(self, context)
        
        print("EXPORT")
        bpy.ops.export_test.some_data('INVOKE_DEFAULT')

        return {'FINISHED'}


class SEQUENCE_OT_custom_add_movie_strip(bpy.types.Operator):
    """Custom Add Movie Strip Operator"""
    bl_idname = "sequence.custom_add_movie_strip"
    bl_label = "Import Video"
    bl_description = "Import video to sequencer"
    filepath: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH',
    )

    def execute(self, context):
        # Set the channels for video and audio
        video_channel = 0
        audio_channel = 1

        # Add movie strip using the correct "Add Movie" operator
        bpy.ops.sequencer.movie_strip_add(
            filepath=self.filepath, channel=video_channel, frame_start=1)

        # Move the audio strip to the desired channel
        for strip in bpy.context.selected_sequences:
            if strip.type == 'SOUND':
                strip.channel = audio_channel
                strip.name = 'SOUND'

         # Change the channel name, but only if it hasnt been done
            if 'Channel 1' in bpy.context.scene.sequence_editor.channels:
                # Get the sequence editor
                seq_editor = bpy.context.scene.sequence_editor
                # Get the channel to rename and lock
                channel_to_rename = seq_editor.channels['Channel 1']
                # Rename the channel
                channel_to_rename.name = 'SOUND'
            if 'Channel 2' in bpy.context.scene.sequence_editor.channels:
                # Get the sequence editor
                seq_editor = bpy.context.scene.sequence_editor
                # Get the channel to rename and lock
                channel_to_rename = seq_editor.channels['Channel 2']
                # Rename the channel
                channel_to_rename.name = 'VIDEO'

        #Adapt the scene frame duration to the movieclip
        scene = bpy.context.scene
        sequence_duration = 0
        sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
        for sequence in sequences:
            if sequence.type == 'MOVIE':

            # sequence_duration = sequence.frame_end - sequence.frame_start
            # sequence.frame_start = newStart - current_distance_for_master
                sequence_duration = sequence.frame_duration
            # sequence.frame_end = newStart + sequence_duration
            # sequences.remove(sequence)
            # break

        # scene.frame_start = round(newStart) - current_distance_for_master
        scene.frame_end = sequence_duration
        # scene.frame_current = round(newStart)





        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



def check_string_format(string):
    # Split the string by colon ":"
    parts = string.split(":")
    print(parts)
    # Check if the string has exactly 4 parts separated by colons
    if len(parts) != 4:
        return False

    # Check if each part is a two-digit number
    for part in parts:
        if not part.isdigit() or len(part) != 2:
            return False

    return True







# ------------------------------------------------------------------------
#    MASTER CLOCK OPERATORS ////////////////////////////////////////////// START
# ------------------------------------------------------------------------





def setNewMasterClock(self, context):

    context.scene.master_time_frame = context.scene.frame_current

    scene = bpy.context.scene

    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time

  
   

    setWaterMasterTime(self, context)

    # go through all areas until sequence editor is found
    for area in bpy.context.screen.areas:
        if area.type == "SEQUENCE_EDITOR":
            override = bpy.context.copy()
            # change context to the sequencer
            override["area"] = area
            override["region"] = area.regions[-1]
            # run the command with the correct context
            with bpy.context.temp_override(**override):
                bpy.ops.sequencer.view_all()
            break


# ------------------------------------------------------------------------
#    setWaterMasterTime
# ------------------------------------------------------------------------


def setWaterMasterTime(self, context):

    
    scene = bpy.context.scene
    sequences = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences
    # print(sequences)
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame

    for sequence in sequences:
        if sequence.type == 'TEXT':
            if sequence.name == '@master.time':
                sequences.remove(sequence)
                break

    text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
        name="@master.time",
        type='TEXT',
        frame_start=scene.frame_start,
        frame_end=scene.frame_end,
        channel=3
    )
    text_strip.text = ''
    # Set the font and size for the text strip
    text_strip.font_size = 50.0
    # Set the position and alignment of the text strip
    text_strip.location = (0.05, 0.1)  # Set the position of the text strip
    text_strip.use_shadow = False
    text_strip.use_box = True
    text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
    # text_strip.wrap_width = 300  # Set the wrap width of the text strip
    text_strip.align_x = 'LEFT'  # Set the horizontal alignment
    text_strip.align_y = 'CENTER'  # Set the vertical alignment

    
    
   


    




# ------------------------------------------------------------------------
#    MASTER CLOCK OPERATORS ////////////////////////////////////////////// END
# ------------------------------------------------------------------------

