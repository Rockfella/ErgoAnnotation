import bpy
# This global variable will store the state of our operator
custom_playback_operator_running = None


# TODO: REMOVE THIS IF UN-USED
class CustomPlaybackOperator(bpy.types.Operator):
    bl_idname = "myaddon.speed_control_operator_toggle"
    bl_label = "Start / Stop Custom Playback"

    # Making is_playing a class variable
    is_playing = False

    def modal(self, context, event):
        if not CustomPlaybackOperator.is_playing:
            self.stop_playback(context)
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def start_playback(self, context):
        print("Playback Started!")
        CustomPlaybackOperator.is_playing = True
        context.window_manager.speed_control_operator_toggle = True

        # Get the window manager's key configurations
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        # Access the frames keymaps
        km = kc.keymaps.get('Frames')
        for kmi in km.keymap_items:
            if kmi.idname == 'screen.frame_offset' and kmi.type == 'LEFT_ARROW':
                # Modify as per your requirement
                kmi.properties.delta = int(-(context.scene.playback_speed_factor))
            elif kmi.idname == 'screen.frame_offset' and kmi.type == 'RIGHT_ARROW':
                # Modify as per your requirement
                kmi.properties.delta = int(context.scene.playback_speed_factor)

    def stop_playback(self, context):
        if not CustomPlaybackOperator.is_playing:
            return  # Avoid multiple stops
        print("Playback Stopped!")
        CustomPlaybackOperator.is_playing = False
        context.window_manager.speed_control_operator_toggle = False

        # Get the window manager's key configurations
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        # Access the frames keymaps
        km = kc.keymaps.get('Frames')
        for kmi in km.keymap_items:
            if kmi.idname == 'screen.frame_offset' and kmi.type == 'LEFT_ARROW':
                kmi.properties.delta = -1  # Modify as per your requirement
            elif kmi.idname == 'screen.frame_offset' and kmi.type == 'RIGHT_ARROW':
                kmi.properties.delta = 1  # Modify as per your requirement

    def invoke(self, context, event):
        if CustomPlaybackOperator.is_playing:
            self.stop_playback(context)
            return {'CANCELLED'}
        else:
            self._timer = context.window_manager.event_timer_add(
                1.0 / context.scene.render.fps, window=context.window)
            self.start_playback(context)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}


def draw_header_func(self, context):
    layout = self.layout
    scene = context.scene
    # TODO: REMOVE THIS IF UN-USED, Code can be used to use the header in the sequencer addon, to set specific options for speed control
    #layout.prop(scene, "playback_speed_factor", text="Playback Speed")

    # Use depress argument to control the visual state of the button.
    #layout.operator("myaddon.speed_control_operator_toggle",
                    #depress=context.window_manager.speed_control_operator_toggle)
