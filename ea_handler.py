
import bpy
import time
import datetime

# ------------------------------------------------------------------------
#    HOTKEY: ZERO
# ------------------------------------------------------------------------


class onPressKeyZERO(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_zero"
    bl_label = "onPressKeyZERO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '0'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyZERO(bpy.types.Operator):
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

class onPressKeyONE(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_one"
    bl_label = "onPressKeyONE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '1'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyONE(bpy.types.Operator):
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

class onPressKeyTWO(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_two"
    bl_label = "onPressKeyTWO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '2'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTWO(bpy.types.Operator):
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


class onPressKeyTHREE(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_three"
    bl_label = "onPressKeyTHREE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '3'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTHREE(bpy.types.Operator):
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


class onPressKeyFOUR(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_four"
    bl_label = "onPressKeyFOUR"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '4'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFOUR(bpy.types.Operator):
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


class onPressKeyFIVE(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_five"
    bl_label = "onPressKeyFIVE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '5'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyFIVE(bpy.types.Operator):
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


class onPressKeySIX(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_six"
    bl_label = "onPressKeySIX"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '6'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeySIX(bpy.types.Operator):
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


class onPressKeySEVEN(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_seven"
    bl_label = "onPressKeySEVEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '7'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeySEVEN(bpy.types.Operator):
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


class onPressKeyEIGHT(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_eight"
    bl_label = "onPressKeyEIGHT"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '8'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyEIGHT(bpy.types.Operator):
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


class onPressKeyNINE(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.on_press_key_nine"
    bl_label = "onPressKeyNINE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '9'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyNINE(bpy.types.Operator):
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


class onPressKeyTEN(bpy.types.Operator):
    """On Release"""
    bl_idname = "object.on_press_key_ten"
    bl_label = "onPressKeyTEN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        hotkey = '10'
        executeThePressFromKey(self, context, hotkey)

        return {'FINISHED'}


class onReleaseKeyTEN(bpy.types.Operator):
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

    # Get the active scene
    scene = bpy.context.scene
    sequence_editor = scene.sequence_editor

    # Number of sequences to produce ID
    num_sequences = len(sequence_editor.sequences)
    # Next id
    num_sequence_id = num_sequences + 1

    # ColorTag for num hotkeys
    int_key = int(key)
    color_array = ["COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04", "COLOR_06"]
    choosen_color = color_array[0]

    if 0 <= int_key <= 2:
        choosen_color = color_array[3]  # green
    elif 3 <= int_key <= 4:
        choosen_color = color_array[2]  # yellow
    elif 5 <= int_key <= 6:
        choosen_color = color_array[1]  # orange
    elif 7 <= int_key <= 8:
        choosen_color = color_array[0]  # red
    elif 9 <= int_key <= 10:
        choosen_color = color_array[4]  # purple

    else:
        choosen_color = color_array[3]  # green

    curren_input = "DUET"
    time_now = datetime.datetime.now()
    formatted_date_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
    sequence_name = curren_input + ", " + \
        str(num_sequence_id) + ", " + formatted_date_time

    current_frame = bpy.context.scene.frame_current
    image_str = sequence_name

    text_strip = bpy.data.scenes[bpy.context.scene.name].sequence_editor.sequences.new_effect(
        name=image_str,
        type='TEXT',
        frame_start=current_frame,
        frame_end=current_frame + 5,
        channel=3
    )
    text_strip.text = 'DUET OMNI-RES ' + str(key)
    # Set the font and size for the text strip
    text_strip.font_size = 50.0
    text_strip.color = (0.35, 0.82, 0.51, 1.0)

    text_strip.use_bold = True
    # Set the position and alignment of the text strip
    # Set the position of the text strip
    text_strip.location = (0.15, 0.18)
    text_strip.use_shadow = True
    text_strip.use_box = True
    text_strip.shadow_color = (0, 0, 0, 0)  # Set the shadow color
    # text_strip.wrap_width = 300  # Set the wrap width of the text strip
    text_strip.align_x = 'CENTER'  # Set the horizontal alignment
    text_strip.align_y = 'CENTER'  # Set the vertical alignment
    text_strip.color_tag = choosen_color

    current_frame = bpy.context.scene.frame_current

    # If we ever need markers
    # scene.timeline_markers.new(num_markers_str, frame=current_frame)

    # Initiate the drag of the sequence just created
    bpy.app.handlers.frame_change_post.append(auto_drag_strip)


def executeTheReleaseFromKey(self, context, key):

    # If we ever need markers
    # scene.timeline_markers.new(num_markers_str, frame=current_frame)

    # Stop the drag of the sequence
    bpy.app.handlers.frame_change_post.remove(auto_drag_strip)


def auto_drag_strip(scene, depsgraph):
    print("DRAGGING")
    scene = bpy.context.scene

    current_frame = bpy.context.scene.frame_current
    sequence_editor = scene.sequence_editor

    num_sequences = len(sequence_editor.sequences)
    active_strip = sequence_editor.sequences[num_sequences - 1]

    actual_end = current_frame - active_strip.frame_start
    active_strip.frame_final_duration = int(actual_end)


# ------------------------------------------------------------------------
#    HANDLE HOTKEYS
# ------------------------------------------------------------------------
# store keymaps here to access after registration
addon_keymaps = []


duet_hotkey_press_executions = [onPressKeyZERO, onPressKeyONE, onPressKeyTWO, onPressKeyTHREE, onPressKeyFOUR,
                                onPressKeyFIVE, onPressKeySIX, onPressKeySEVEN, onPressKeyEIGHT, onPressKeyNINE, onPressKeyTEN]

duet_hotkey_release_executions = [onReleaseKeyZERO, onReleaseKeyONE, onReleaseKeyTWO, onReleaseKeyTHREE, onReleaseKeyFOUR,
                                  onReleaseKeyFIVE, onReleaseKeySIX, onReleaseKeySEVEN, onReleaseKeyEIGHT, onReleaseKeyNINE, onReleaseKeyTEN]


duet_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']


def register():

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='SequencerCommon', space_type='SEQUENCE_EDITOR')

    press_executions_index = 0
    for key in duet_hotkeys:
        print(press_executions_index)
        bpy.utils.register_class(
            duet_hotkey_press_executions[press_executions_index])

        # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
        if key == 'TEN':
            kmi = km.keymap_items.new(
                duet_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)

            addon_keymaps.append(km)
        else:

            kmi = km.keymap_items.new(
                duet_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

            addon_keymaps.append(km)

        press_executions_index += 1

    # handle the keymap

    # km_2 = wm.keyconfigs.addon.keymaps.new(name='SequencerCommon', space_type='SEQUENCE_EDITOR')
    release_executions_index = 0
    for key in duet_hotkeys:
        print(release_executions_index)

        bpy.utils.register_class(
            duet_hotkey_release_executions[release_executions_index])
        # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
        if key == 'TEN':
            kmi_2 = km.keymap_items.new(
                duet_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
            addon_keymaps.append(km)
        else:
            kmi_2 = km.keymap_items.new(
                duet_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
            addon_keymaps.append(km)

        release_executions_index += 1

    # kmi_2 = km.keymap_items.new(
    #    OnRelease.bl_idname, 'ZERO', 'RELEASE', ctrl=False, shift=False)
   # addon_keymaps.append(km_2)


def unregister():

    unreg_executions_index = 0
    for key in duet_hotkeys:

        bpy.utils.unregister_class(
            duet_hotkey_press_executions[unreg_executions_index])

        bpy.utils.unregister_class(
            duet_hotkey_release_executions[unreg_executions_index])

        unreg_executions_index = + 1

    # bpy.utils.unregister_class(onPressKeyONE)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()
