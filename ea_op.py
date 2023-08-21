import bpy
import datetime
from bpy.types import Operator
from bpy.app.handlers import persistent
from .ea_inputswitch import inputSwitchClass
from .ea_constants import Constants
from .ea_global_variables import SavePreferencesOperator

from .ea_constants import frame_from_smpte

from .ea_duet_hotkey import auto_drag_strip

import os

class MY_OT_SaveAllPreferences(bpy.types.Operator):
    bl_idname = "my.preferencesavecall"
    bl_label = "Call Function"
    bl_description = "Save to presets"
    index: bpy.props.IntProperty()
    

    def execute(self, context):
        
        bpy.ops.preferences.save()

        return {'FINISHED'}
    

class EA_OT_AdaptionInfoButton(bpy.types.Operator):
    """Tooltip for this operator"""
    bl_idname = "object.adaption_info_button"
    bl_label = "Adaption or Move"
    bl_description = "The adapt time can be used to stretch or shrink a clip, in case when there are missing or additional frames. It can also be used to move a clip to a specific master clock position. To move a clip, please create a meta strip from audio and video, place a marker where in the video it should move from (Hotkey M), a Move button should appear"

    def execute(self, context):
        #bpy.ops.wm.url_open(url="https://github.com/Rockfella/ergolabs")
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
    bl_label = "Set Time"
    bl_description = "Sets the master clock to the frame selected in the timeline"

    def execute(self, context):
        # button_function(self, context)

        if check_string_format(context.scene.master_time):
            print("String is in the correct format.")
            setNewMasterClock(self, context)

        else:
            print("String is not in the correct format.")

        return {'FINISHED'}


class EA_OT_Master_Clock_Button_Adapt(Operator):
    bl_idname = "myaddon.master_button_operator_push"
    bl_description = "Shrinks or stretches the clip to master time"
    bl_label = "Looks like the adaption is large, still want to adapt?"
 
    def execute(self, context):
        # button_function(self, context)

        if check_string_format(context.scene.master_time_adaption):
            print("String is in the correct format.")

            #Add function that pushes the active strip to whatever frame the master_push variables says it should be at
            scene = bpy.context.scene
            fps = bpy.context.scene.render.fps
            fps_base = bpy.context.scene.render.fps_base
            fps_real = fps / fps_base

            # Hold the current frame in memory so we can go back 
            remember_current_frame = scene.frame_current
            
            # Projected frames from master clock
            calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
            calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time
            calc_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].master_time_adaption

            frames_from_master_clock = frame_from_smpte(calc_master_time)

            # Input SMPTE formatted string
            smpte_string_current = bpy.utils.smpte_from_frame(
                (scene.frame_current + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)


            frames_from_current_master_clock = frame_from_smpte(smpte_string_current)
            frames_from_time_pusher = frame_from_smpte(
                calc_master_time_adaption)
            total_frames_to_change = frames_from_time_pusher - frames_from_current_master_clock
            
            split_and_shift(round(total_frames_to_change))

            #reset the current frame to where we where taking the shift into account
            scene.frame_current = remember_current_frame + round(total_frames_to_change)
           

        else:
            print("String is not in the correct format.")

        return {'FINISHED'}
    #TODO: FIGURE OUT HOW THIS CAN BE DONE WITHOUT A COPY OF THE ABOVE CODE
    def invoke(self, context, event):

        # ------------------------------------------------------------------------
        #    Adaption handler, to make sure not too big changes to the strip is made
        # ------------------------------------------------------------------------
        
        # Add function that pushes the active strip to whatever frame the master_push variables says it should be at
        scene = bpy.context.scene
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        

    

        # Projected frames from master clock
        calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
        calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time
        calc_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].master_time_adaption
        frames_from_master_clock = frame_from_smpte(calc_master_time)

        # Input SMPTE formatted string
        smpte_string_current = bpy.utils.smpte_from_frame(
            (scene.frame_current + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)

        frames_from_current_master_clock = frame_from_smpte(
            smpte_string_current)
        frames_from_time_pusher = frame_from_smpte(calc_master_time_adaption)
        total_frames_to_change = frames_from_time_pusher - frames_from_current_master_clock
        


        #Too big adaptions should not be performed, if for example the user imports a 60 FPS to a 30 FPS project, the fps should first be converted seperatly
        if abs(total_frames_to_change) > 150:
            self.report({'ERROR'}, "The adoption is too large, please convert the clip fps before importing it instead")
            return {'CANCELLED'}
        elif abs(total_frames_to_change) >= 50:
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)
        

class EA_OT_Master_Clock_Button_Move(Operator):
    bl_idname = "myaddon.master_button_operator_move"
    bl_description = "Move the selected clip according to master clock"
    bl_label = "The strip might get over another clip"

    def execute(self, context):
        # button_function(self, context)
        # Get all markers
       
        #Calculates the difference between the marker and the specific adaptation time and moves the strip accordingly 
        calculate_execute_the_strip_move(self, context, False)

        return {'FINISHED'}
    

    def invoke(self, context, event):
        
        is_moving_back = calculate_execute_the_strip_move(self, context, True)

        if is_moving_back:
            return context.window_manager.invoke_confirm(self, event)
        else:
            return self.execute(context)
        


def calculate_execute_the_strip_move(self, context, justcalc):
    
    #We need a marker for this operation
    markers = bpy.context.scene.timeline_markers
    # Get sequence editor
    seq_editor = bpy.context.scene.sequence_editor
    #Get the marker that is placed over the strip within its range and consider this the "orginin" frame
    for marker in markers:
        if seq_editor.active_strip.frame_final_start <= marker.frame <= seq_editor.active_strip.frame_final_end:
            # Projected frames from master clock
            calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
            calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time
            calc_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].master_time_adaption
            frames_from_master_clock = frame_from_smpte(calc_master_time)
            initial_frame = marker.frame

            frame_from_time_pusher = frame_from_smpte(
                calc_master_time_adaption)

            

            smtp_at_zero = bpy.utils.smpte_from_frame(
                (0 + frames_from_master_clock - calc_master_frame))

            frames_at_zero = frame_from_smpte(smtp_at_zero)

            actual_time_frame_from_pusher = frame_from_time_pusher - frames_at_zero

            the_frame_change = initial_frame - actual_time_frame_from_pusher


            # Ensure the active strip is the one you're interested in
            if seq_editor.active_strip and seq_editor.active_strip.type == 'MOVIE':
               # If it's not a meta strip, make it one
               name_of_movie, ex = os.path.splitext(seq_editor.active_strip.name)
               sound_file = f"{name_of_movie}.001"
               sound_strip = next((strip for strip in seq_editor.sequences_all if strip.type ==
                                  'SOUND' and strip.name == sound_file), None)

               if sound_strip:
                    # Deselect all strips
                    for strip in seq_editor.sequences_all:
                        strip.select = False    
                    # Select only the movie and sound strips
                    seq_editor.active_strip.select = True
                    sound_strip.select = True

                    # Create a meta strip from the selected strips
                    bpy.ops.sequencer.meta_make()

            #Sends back a bool if the function only wanted to provide if the move is negative, see difference at def invoke
            if justcalc:
                if the_frame_change > 0:
                    return True    
                else:
                    return False

            if the_frame_change < 0:
                seq_editor.active_strip.frame_start += abs(
                    the_frame_change)
                bpy.context.scene.timeline_markers.remove(
                        bpy.context.scene.timeline_markers[marker.name])
                bpy.context.window.scene.frame_current = round(
                        actual_time_frame_from_pusher)
            elif the_frame_change > 0:
                seq_editor.active_strip.frame_start -= abs(
                        the_frame_change)
                bpy.context.scene.timeline_markers.remove(
                bpy.context.scene.timeline_markers[marker.name])
                bpy.context.window.scene.frame_current = round(
                        actual_time_frame_from_pusher)
            elif the_frame_change == 0:
                    return {'FINISHED'}
            #Break to avoid it finding more markers and doing the loop again
            break
   

# TODO: CONSIDER REMOVING THE ROUND FPS
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


class EA_OT_Import_Data_Button(Operator):
    bl_idname = "myaddon.import_data_operator"
    bl_label = "Import Data from CSV"
    bl_description = "Import Data from CSV, make sure to spec type Date Time"

    def execute(self, context):
        # button_function(self, context)

        print("EXPORT")
        bpy.ops.import_test.some_data('INVOKE_DEFAULT')

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
        channel=4
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

# ------------------------------------------------------------------------
#    MASTER CLOCK SYNC FUNCTIONS //////////////////////////////////////////
# ------------------------------------------------------------------------

def split_and_shift(num_cuts):

    
   
    # Get sequence editor
    seq_editor = bpy.context.scene.sequence_editor
    # Get current frame
    current_frame = bpy.context.scene.frame_current

    #Strips that will be adapted
    strip1 = None
    strip2 = None

    #If the user has selected a meta strip, work with that, otherwise just take the recommended channel 1 & 2 and see if there are strips there
    if seq_editor.active_strip and seq_editor.active_strip.type == 'META':
        strip1 = seq_editor.active_strip
        strip2 = None

    #Grab from channel 1-2
    else:
            # Get the strips from channel 1 and 2 which include the current frame
        strip1 = next((s for s in seq_editor.sequences if s.channel == 1 and s.frame_final_start <=
                  current_frame and s.frame_final_end >= current_frame), None)
        strip2 = next((s for s in seq_editor.sequences if s.channel == 2 and s.frame_final_start <=
                  current_frame and s.frame_final_end >= current_frame), None)

    #If there are no such strips, return, nothing to be done
    if strip1 is None and strip2 is None:
        return
    

    # Give the cut strips a unique name, so we can find them later
    time_now = datetime.datetime.now()
    formatted_date_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
    original_strip_names = []
    
    #Information to be stored for the cuts
    save_oneframe_final_start = 0
    save_oneframe_final_end = 0
    save_oneframe_final_duration = 0

    strips_to_cut = []
    if strip1 is not None:
        strip1.name = str(formatted_date_time)
        original_strip_names.append(strip1.name.split(
            ".")[0])
        # Save atlease one of the strips start and duration for later, if we add frames with gap_insert, we need to remove this after we are done
        save_oneframe_final_start = strip1.frame_final_start
        save_oneframe_final_end = strip1.frame_final_end
        save_oneframe_final_duration = strip1.frame_final_duration
        strips_to_cut.append(strip1)

    if strip2 is not None:
        strip2.name = str(formatted_date_time)
        original_strip_names.append(strip2.name.split(
            ".")[0])
        # Save atlease one of the strips start and duration for later, if we add frames with gap_insert, we need to remove this after we are done
        save_oneframe_final_start = strip2.frame_final_start
        save_oneframe_final_end = strip2.frame_final_end
        save_oneframe_final_duration = strip2.frame_final_duration
        strips_to_cut.append(strip2)
    
    
    
    # ------------------------------------------------------------------------
    #    If the adaption requires us to add empty frames to fill lost frames
    # ------------------------------------------------------------------------
    if num_cuts > 0:
        gap_start = save_oneframe_final_end + num_cuts

        # Calculate the split points
        split_points = [(save_oneframe_final_start + i * (save_oneframe_final_duration //
                         (num_cuts + 1))) for i in range(1, num_cuts + 1)]

        # Reverse the list to start cutting from the end
        split_points.reverse()

        # Split and shift the strips
        for sp in split_points:
            bpy.context.window.scene.frame_current = sp

            # Deselect all strips
            bpy.ops.sequencer.select_all(action='DESELECT')

            # Select the strips to cut
            for s in strips_to_cut:
                s.select = True
            

            # Cut the strips
            bpy.ops.sequencer.split(frame=sp)

            # Deselect all strips
            bpy.ops.sequencer.select_all(action='DESELECT')

            bpy.ops.sequencer.gap_insert(frames=1)
            
        #Get the newly cut pieces    
        new_strips = [s for s in seq_editor.sequences if s.name.split(".")[
                0] in original_strip_names]

        #Select and move the new strips
        for s in new_strips:
            s.select = True
            #In order for the metastrip to land on the same channel, they need to be considered "active"
            seq_editor.active_strip = s
        bpy.ops.sequencer.meta_make()
            

        # After all splits and shifts, shift all subsequent strips back to the left
        bpy.context.window.scene.frame_current = gap_start
        for s in seq_editor.sequences:
            if s.frame_final_start >= gap_start:
                # shift the strips back to the left by the same amount as the inserted gaps
                s.frame_start -= num_cuts

    
    # ------------------------------------------------------------------------
    #    If the adaption requires us to remove frames to sync with master clock
    # ------------------------------------------------------------------------
    elif num_cuts < 0:
        num_cuts = abs(num_cuts)

        # Calculate the split points
        split_points = [(save_oneframe_final_start + i * (save_oneframe_final_duration //
                         (num_cuts + 1))) for i in range(1, num_cuts + 1)]

        # Reverse the list to start cutting from the end
        split_points.reverse()

        # Split and shift the strips
        for sp in split_points:
            bpy.context.window.scene.frame_current = sp
            # Deselect all strips
            bpy.ops.sequencer.select_all(action='DESELECT')

            for s in strips_to_cut:
                s.select = True
            
            # Cut the strips
            bpy.ops.sequencer.split(frame=sp)
            
            # Deselect all strips
            bpy.ops.sequencer.select_all(action='DESELECT')


        #Keep the strips separated if channel 1,2 has been used instead of a meta strip
        new_strips_one = []
        new_strips_two = []

        #Separating audio and video strip into different lists to keep track, if the user has created a meta out of the clip it will use one method, otherwise default to using channel 1-2
        if seq_editor.active_strip and seq_editor.active_strip.type == 'META':
            new_strips_one = [s for s in seq_editor.sequences if s.name.split(
                ".")[0] in original_strip_names]
            new_strips_two = []
        else:
            new_strips_one = [s for s in seq_editor.sequences if s.name.split(
             ".")[0] in original_strip_names and s.channel == 1]
            new_strips_two = [s for s in seq_editor.sequences if s.name.split(
             ".")[0] in original_strip_names and s.channel == 2]
        
        #Sort the new strips
        sorted_sequences_one = sorted(
            new_strips_one, key=lambda s: s.name, reverse=True)
        sorted_sequences_two = sorted(
            new_strips_two, key=lambda s: s.name, reverse=True)
        
        #Sort the original list to take into account that we work backwards, this is required to handle Blenders naming of cuts
        if sorted_sequences_one:
            keep_last_item = sorted_sequences_one[-1]
            del sorted_sequences_one[-1]
            sorted_sequences_one.insert(0, keep_last_item)

        if sorted_sequences_two:
            keep_last_item = sorted_sequences_two[-1]
            del sorted_sequences_two[-1]
            sorted_sequences_two.insert(0, keep_last_item)

        #Keepiong track of the move_index
        index_counter_channel_one = 0
        index_counter_channel_two = 0

        #Move index is added since "remove gap" is not fully functioning in blender, this in order for clips that are after the adapted clip doesn't move from orginal time
        move_index = []
        for i in range(num_cuts + 1):
            move_index.append(i)

        #Find the clips and start moving them accoring to the move:index
        #Start with channel 1
        for s in sorted_sequences_one:
            s.frame_final_start = s.frame_final_start + 1
            s.frame_start -= (1 + move_index[index_counter_channel_one])
            index_counter_channel_one += 1

                
        #Then channel two    
        for s in sorted_sequences_two:
            s.frame_final_start = s.frame_final_start + 1
            s.frame_start -= (1 + move_index[index_counter_channel_two])
            index_counter_channel_two += 1

        #When they have been aligned and are ready, make a meta strip out of them
        print_index = 0
        for one in new_strips_one:
            
            one.select = True
            
            # In order for the metastrip to land on the same channel, they need to be considered "active"
            seq_editor.active_strip = s
            print_index += 1
        for two in new_strips_two:
            
            two.select = True

            # In order for the metastrip to land on the same channel, they need to be considered "active"
            seq_editor.active_strip = s
            print_index += 1
        bpy.ops.sequencer.meta_make()
