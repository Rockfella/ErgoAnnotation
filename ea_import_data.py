from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte
import os


def read_some_data(context, filepath, unix_time_start, unix_time_end):
    # Assuming images are in the same directory as the CSV file
    image_dir = os.path.dirname(filepath)

    # Get a reference to the current scene and the sequencer
    scene = bpy.context.scene
    sequencer = scene.sequence_editor_create()

    current_activity = None
    current_strip = None
    index = 0
    render_fps = bpy.context.scene.render.fps
    fps_base = bpy.context.scene.render.fps_base if bpy.context.scene.render.fps_base != 0 else 1

    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if unix_time_start <= index <= unix_time_end:
                # Get the activity and remove leading/trailing spaces
                activity = row[1].strip()
                if activity != current_activity:
                    # The activity has changed, create a new image strip
                    image_path = os.path.join(image_dir, f"{activity}.png")
                    if os.path.isfile(image_path):
                        img = bpy.data.images.load(image_path)
                        frame_duration = int(render_fps / fps_base)
                        frame_start = index * frame_duration + 1
                        frame_end = frame_start + frame_duration - 1
                        current_strip = sequencer.sequences.new_image(
                            name=f"Image Strip {activity}_{index}",
                            filepath=image_path,
                            channel=7,  # You can change the channel if needed
                            frame_start=frame_start,
                            #frame_end=frame_end,
                            fit_method='FIT',
                        )

                        # Adjust the position and scale of the strip
                        current_strip.transform.offset_x = -737  # Adjust the horizontal position
                        current_strip.transform.offset_y = -75  # Adjust the vertical position
                        current_strip.transform.scale_x = 1.0  # Adjust the horizontal scale
                        current_strip.transform.scale_y = 1.0  # Adjust the vertical scale
                    else:
                        # If there's no image, create a text strip instead
                        frame_duration = int(render_fps / fps_base)
                        frame_start = index * frame_duration + 1
                        frame_end = frame_start + frame_duration - 1
                        current_strip = sequencer.sequences.new_effect(
                            name=f"Text Strip {activity}_{index}",
                            type='TEXT',
                            frame_start=frame_start,
                            frame_end=frame_end,
                            channel=7,
                        )
                        # Adjust the position and scale of the strip
                        current_strip.transform.offset_x = -737  # Adjust the horizontal position
                        current_strip.transform.offset_y = -75  # Adjust the vertical position
                        current_strip.transform.scale_x = 1.0  # Adjust the horizontal scale
                        current_strip.transform.scale_y = 1.0  # Adjust the vertical scale
                        
                        current_strip.text = activity
                    current_activity = activity
                else:
                    # The activity has not changed, extend the duration of the current strip
                    if current_strip:
                        current_strip.frame_final_end += frame_duration - 1
                index += 1

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since it's how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Data from CSV"

    # ImportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    unix_time_start: IntProperty(name="Start at Row", default=0)
    unix_time_end: IntProperty(name="End at Row", default=0)

    type: EnumProperty(
        name="File FPS",
        description="Choose FPS for import",
        items=(
            ('OPT_A', "1", "1 FPS"),
            ('OPT_B', "5", "5 FPS"),
            ('OPT_C', "10", "10 FPS"),
            ('OPT_D', "20", "20 FPS"),
            ('OPT_E', "30", "30 FPS"),
            ('OPT_F', "40", "40 FPS"),
            ('OPT_G', "50", "50 FPS"),
            ('OPT_H', "60", "60 FPS"),
            ('OPT_I', "70", "70 FPS"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return read_some_data(context, self.filepath, self.unix_time_start, self.unix_time_end)
