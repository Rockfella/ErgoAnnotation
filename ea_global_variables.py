import bpy

# Define custom property group
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import PointerProperty, StringProperty

class FREE_CHANNEL_VARS_PG(PropertyGroup):
    slots_to_show: bpy.props.IntProperty(name="SLOTS_TO_SHOW", default=3)
    slot_0: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_0", default="Empty0")
    slot_1: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_1", default="Empty1")
    slot_2: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_2", default="Empty2")
    slot_3: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_3", default="Empty3")
    slot_4: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_4", default="Empty4")
    slot_5: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_5", default="Empty5")
    slot_6: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_6", default="Empty6")
    slot_7: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_7", default="Empty7")
    slot_8: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_8", default="Empty8")
    slot_9: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_9", default="Empty9")
    slot_10: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_10", default="Empty10")
    slot_11: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_11", default="Empty11")
    slot_12: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_12", default="Empty12")
    slot_13: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_13", default="Empty13")
    slot_14: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_14", default="Empty14")
    slot_15: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_15", default="Empty15")
    slot_16: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_16", default="Empty16")
    slot_17: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_17", default="Empty17")
    slot_18: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_18", default="Empty18")
    slot_19: bpy.props.StringProperty(name="FREE_CHANNEL_VAR_19", default="Empty19")
    color_0: bpy.props.FloatVectorProperty(name="Color 0", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.603831, 0.10224, 0.084375))
    color_1: bpy.props.FloatVectorProperty(name="Color 1", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.603831, 0.254152, 0.064804))
    color_2: bpy.props.FloatVectorProperty(name="Color 2", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.450779, 0.366255, 0.049707))
    color_3: bpy.props.FloatVectorProperty(name="Color 3", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.107022, 0.318555, 0.107022))
    color_4: bpy.props.FloatVectorProperty(name="Color 4", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.082282, 0.346709, 0.603831))
    color_5: bpy.props.FloatVectorProperty(name="Color 5", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.266357, 0.099897, 0.701117))
    color_6: bpy.props.FloatVectorProperty(name="Color 6", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.564707, 0.171438, 0.479312))
    color_7: bpy.props.FloatVectorProperty(name="Color 7", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.318555, 0.141266, 0.084375))
    color_8: bpy.props.FloatVectorProperty(name="Color 8", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.215856, 0.215856, 0.215856))
    color_9: bpy.props.FloatVectorProperty(name="Color 9", subtype='COLOR', min=0.0, max=1.0, size=3, default=(0.107022, 0.318555, 0.1070220))

# Define the addon preferences
class FREE_CHANNEL_Preferences(AddonPreferences):
    bl_idname = __package__
    
    # Link the property group to the addon preferences
    free_channel_vars: PointerProperty(type=FREE_CHANNEL_VARS_PG)


class SavePreferencesOperator(bpy.types.Operator):
    bl_idname = "preferences.save"
    bl_label = "Save Preferences"

    def execute(self, context):
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}
