from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper
import bpy
import csv
from .ea_constants import Constants


def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")

    # Example mockup data
    data = []
    data.append(Constants.EXPORT_TYPES)
    #data.append([10, 20])
    #data.append([30, 40])

    data_master_clock = []
    data_DUET_L = []
    data_DUET_R = []
    data_FREE_CHANNEL = []

    scene = bpy.context.scene
    # Store the current frame to restore it later
    current_frame = scene.frame_current

    # Iterate through each frame in the scene
    for frame in range(scene.frame_start, scene.frame_end + 1):
        # Set the current frame to the frame in the loop
        scene.frame_set(frame)
        # Print the frame number
        is_in_range_data_DUET_L = False
        is_in_range_data_DUET_R = False
        is_in_range_data_FREE_CHANNEL = False
        for strip in scene.sequence_editor.sequences:
            if strip.type == 'TEXT':
               
                if strip.name == '@master.time':
                    data_master_clock.append(strip.text)

                filter_name = strip.name.split(',')
                strip_range_start = strip.frame_final_start
                strip_range_end = (strip_range_start + strip.frame_final_duration) - 1 # -1 to make sure it does not include the end frame

                if strip_range_start <= frame <= strip_range_end:

                    if filter_name[0] == Constants.DUET_LEFT[2]:
                        data_DUET_L.append(filter_name[1])
                        is_in_range_data_DUET_L = True

                    elif filter_name[0] == Constants.DUET_RIGHT[2]:
                        data_DUET_R.append(filter_name[1])
                        is_in_range_data_DUET_R = True

                    elif filter_name[0] == Constants.FREE_CHANNEL[2]:
                        data_FREE_CHANNEL.append(filter_name[1])
                        is_in_range_data_FREE_CHANNEL = True

        if is_in_range_data_DUET_L == False:
            data_DUET_L.append(-1)
        if is_in_range_data_DUET_R == False:
            data_DUET_R.append(-1)
        if is_in_range_data_FREE_CHANNEL == False:
            data_FREE_CHANNEL.append(-1)
                    

    index = 0   
    for d in data_master_clock:
        
        data.append([data_master_clock[index],
                    data_DUET_L[index], data_DUET_R[index], data_FREE_CHANNEL[index]])

        index += 1
        # print("Frame number:", frame)

    # Restore the original frame
    scene.frame_set(current_frame)










    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


## Only needed if you want to add into a dynamic menu
#def menu_func_export(self, context):
#    self.layout.operator(ExportSomeData.bl_idname, text="Text Export Operator")
#
#
## Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
#def register():
#    bpy.utils.register_class(ExportSomeData)
#    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
#
#
#def unregister():
#    bpy.utils.unregister_class(ExportSomeData)
#    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
#
#
#if __name__ == "__main__":
#    register()
#
#    # test call
#    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
#