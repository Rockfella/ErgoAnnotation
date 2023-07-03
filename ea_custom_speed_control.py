import bpy
# This global variable will store the state of our operator
custom_playback_operator_running = None


class CustomPlaybackOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.custom_playback_operator"
    bl_label = "Start / Stop Custom Playback"

    # The timer object
    _timer = None

    # The fractional part of the frame number
    frame_fraction = 0.0

    def modal(self, context, event):
        global custom_playback_operator_running
        if custom_playback_operator_running is None:
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # Update the current frame number and the fractional part of the frame number according to speed factor
            self.frame_fraction += context.scene.playback_speed_factor
            context.scene.frame_set(
                context.scene.frame_current + int(self.frame_fraction))
            self.frame_fraction %= 1.0
        return {'PASS_THROUGH'}

    def execute(self, context):
        global custom_playback_operator_running
        if custom_playback_operator_running is not None:
            custom_playback_operator_running.cancel(context)
            custom_playback_operator_running = None
            return {'CANCELLED'}

        self._timer = context.window_manager.event_timer_add(
            1.0 / context.scene.render.fps, window=context.window)
        self.frame_fraction = 0.0
        context.window_manager.modal_handler_add(self)
        custom_playback_operator_running = self
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        global custom_playback_operator_running
        context.window_manager.event_timer_remove(self._timer)
        custom_playback_operator_running = None

# New draw function to append to the SEQUENCER_HT_header draw function


def draw_header_func(self, context):
    layout = self.layout
    scene = context.scene

    # Render settings
    layout.prop(scene, "playback_speed_factor", text="Playback Speed")

    # Operator
    layout.operator("wm.custom_playback_operator")
