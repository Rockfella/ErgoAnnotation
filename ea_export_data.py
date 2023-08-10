from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper
import bpy
import csv
from .ea_constants import Constants
from .ea_constants import frame_from_smpte

def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")

    scene = bpy.context.scene

    # Cache the sequence strips
    sequence_strips = list(scene.sequence_editor.sequences)

    
    # MASTER TIME LIST
    data_master_clock = []
    # Projected frames from master clock
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time

    frames_from_master_clock = frame_from_smpte(calc_master_time)

    fps = bpy.context.scene.render.fps
    fps_base = bpy.context.scene.render.fps_base
    fps_real = fps / fps_base
    
    #Creating a list based of the master clock 
    for frame in range(scene.frame_start, scene.frame_end + 1):
        # Input SMPTE formatted string
        smpte_string_current = bpy.utils.smpte_from_frame(
        (frame + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)
        data_master_clock.append(smpte_string_current)
    
    

    # Building a list of strips with their range and append them to the right dict
    sir_data_DUET_L = []
    sir_data_DUET_R = []
    sir_data_FREE_CHANNEL = []
    for strip in sequence_strips:
        filter_name = strip.name.split(',')
        if strip.type == 'TEXT' and filter_name[0]:
            start_frame = int(strip.frame_start)
            end_frame = start_frame + int(strip.frame_final_duration)
            filter_name = strip.name.split(',')

            #Sort the strip.names into the right cathegories 
            if filter_name[0] == Constants.DUET_LEFT[2]:
                sir_data_DUET_L.append(
                    (start_frame, end_frame, filter_name[1]))

            elif filter_name[0] == Constants.DUET_RIGHT[2]:
               sir_data_DUET_R.append((start_frame, end_frame, filter_name[1]))
                   
            elif filter_name[0] == Constants.FREE_CHANNEL[2]:
               sir_data_FREE_CHANNEL.append(
                   (start_frame, end_frame, filter_name[1]))
                   
            
    # Sort the list by start_frame
    sir_data_DUET_L.sort()
    sir_data_DUET_R.sort()
    sir_data_FREE_CHANNEL.sort()

    # Building a dictionary of active strips for each frame
    active_strips_data_DUET_L = {}
    active_strips_data_DUET_R = {}
    active_strips_data_FREE_CHANNEL = {}
    for frame in range(scene.frame_start, scene.frame_end + 1):
        active_strips_data_DUET_L[frame] = [name for start, end,
                                name in sir_data_DUET_L if start <= frame < end]
        active_strips_data_DUET_R[frame] = [name for start, end,
                                            name in sir_data_DUET_R if start <= frame < end]
        active_strips_data_FREE_CHANNEL[frame] = [name for start, end,
                                                  name in sir_data_FREE_CHANNEL if start <= frame < end]

    data_data_DUET_L = []
    data_data_DUET_R = []
    data_FREE_CHANNEL = []

    for frame, strips in active_strips_data_DUET_L.items(): 
        data_data_DUET_L.append(strips)
    
    for frame, strips in active_strips_data_DUET_R.items():
        data_data_DUET_R.append(strips)
    
    for frame, strips in active_strips_data_FREE_CHANNEL.items():
        data_FREE_CHANNEL.append(strips)

    #Combine all lists into a dict that speeds up the csv export
    data = {
        "master_clock": data_master_clock,
        "DUET_L": data_data_DUET_L,
        "DUET_R": data_data_DUET_R,
        "FREE_CHANNEL": data_FREE_CHANNEL
    }


    #Save to csv file
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        for i in range(len(data_master_clock)):
            row = {key: values[i] for key, values in data.items()}
            writer.writerow(row)

    return {'FINISHED'}


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
        options={'HIDDEN'},
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
        options={'HIDDEN'},
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