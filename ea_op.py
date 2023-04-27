import bpy

from bpy.types import Operator
from .ea_inputswitch import inputSwitchClass
from .ea_constants import Constants

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

        self._timer = context.window_manager.event_timer_add(
            time_step=0.05, window=context.window)

        print("Start")
        inputSwitchClass.input_switch(self, Constants.DUET_RIGHT[0])
        context.window_manager.modal_handler_add(self)
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


def frame_from_smpte(smpte_timecode: str, fps=None, fps_base=None) -> int:

    if fps == None or fps_base == None:
        # Use current scene fps if fps and fps_base are not provided
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base

    # Split the timecode into its components
    timecode_parts = smpte_timecode.split(':')
    hours = int(timecode_parts[0])
    minutes = int(timecode_parts[1])
    seconds = int(timecode_parts[2])
    frames = int(timecode_parts[3])

    print("FPS_REAL")
    print(fps_real)

    hours_seconds_frames = ((hours * 60) * 60) * fps_real
    minutes_seconds_frames = (minutes * 60) * fps_real
    seconds_frames = seconds * fps_real
    frames_frames = frames

    # Calculate the total number of frames
    total_frames = (hours_seconds_frames +
                    minutes_seconds_frames + seconds_frames + frames)

    print(hours_seconds_frames, minutes_seconds_frames,
          seconds_frames, frames_frames)
    return total_frames


def setNewMasterClock(self, context):

    context.scene.master_time_frame = context.scene.frame_current

    scene = bpy.context.scene

    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time

    # newStart = frame_from_smpte(calc_master_time)
  #
    # Move the sequence according to the new frame and substract the distance of the marker
    # current_distance_for_master = scene.frame_current
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
        frame_start=scene.frame_start + calc_master_frame,
        frame_end=scene.frame_end,
        channel=2
    )
    text_strip.text = ''
    # Set the font and size for the text strip
    text_strip.font_size = 50.0
    # Set the position and alignment of the text strip
    text_strip.location = (0.1, 0.1)  # Set the position of the text strip
    text_strip.use_shadow = False
    text_strip.use_box = True
    text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
    # text_strip.wrap_width = 300  # Set the wrap width of the text strip
    text_strip.align_x = 'CENTER'  # Set the horizontal alignment
    text_strip.align_y = 'CENTER'  # Set the vertical alignment

    

    def meta_text_handler(scene, depsgraph):

        # Projected frames from master clock
        calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
        calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time

        frames_from_master_clock = frame_from_smpte(calc_master_time)

        for strip in scene.sequence_editor.sequences_all:
            if strip.type == 'TEXT':

                if strip.name == '@master.time':

                    fps = bpy.context.scene.render.fps
                    fps_base = bpy.context.scene.render.fps_base
                    fps_real = fps / fps_base

                    # Input SMPTE formatted string
                    smpte_string_current = bpy.utils.smpte_from_frame(
                        (scene.frame_current + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)

                    # Split the string using ":" as the delimiter
                    hours_curr, minutes_curr, seconds_curr, frames_curr = smpte_string_current.split(
                        ":")

                    strip.text = str(hours_curr) + ':' + str(minutes_curr) + \
                        ':' + str(seconds_curr) + '+' + str(frames_curr)


    #TODO: move these to the init file
    # def registe
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(meta_text_handler)
    bpy.app.handlers.render_pre.append(meta_text_handler)

    def unregister():
        bpy.app.handlers.frame_change_pre.remove(meta_text_handler)
        bpy.app.handlers.render_pre.remove(meta_text_handler)


# ------------------------------------------------------------------------
#    MASTER CLOCK OPERATORS ////////////////////////////////////////////// END
# ------------------------------------------------------------------------

