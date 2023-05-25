from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte
import os


def read_some_data(context, filepath, csv_row_start, csv_row_end):
    # Assuming images are in the same directory as the CSV file
    image_dir = os.path.dirname(filepath)

    print("Start and end row in CSV")
    print(csv_row_start)
    print(csv_row_end)

    # Get a reference to the current scene and the sequencer
    scene = bpy.context.scene
    sequencer = scene.sequence_editor_create()

    current_activity = None
    current_strip = None
    index = 0
    render_fps = bpy.context.scene.render.fps

    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        # Skip the first row
        next(reader)

        for row in reader:
            if csv_row_start <= index <= csv_row_end:
                # Get the activity and remove leading/trailing spaces
                activity = row[1].strip()
                frame_start = index * render_fps

                if activity != current_activity:
                    # The activity has changed, if there was a previous strip, extend its end
                    if current_strip:
                        current_strip.frame_final_end = frame_start

                    # Create a new strip for the new activity
                    image_path = os.path.join(image_dir, f"{activity}.png")
                    if os.path.isfile(image_path):
                        img = bpy.data.images.load(image_path)
                        current_strip = sequencer.sequences.new_image(
                            name=f"Image Strip {activity}_{index}",
                            filepath=image_path,
                            channel=7,  # You can change the channel if needed
                            frame_start=frame_start,
                            fit_method='FIT',
                        )

                        # Adjust the position and scale of the strip
                        current_strip.transform.offset_x = -737  # Adjust the horizontal position
                        current_strip.transform.offset_y = -75  # Adjust the vertical position
                        current_strip.transform.scale_x = 1.0  # Adjust the horizontal scale
                        current_strip.transform.scale_y = 1.0  # Adjust the vertical scale
                    else:
                        # If there's no image, create a text strip instead
                        current_strip = sequencer.sequences.new_effect(
                            name=f"Text Strip {activity}_{index}",
                            type='TEXT',
                            frame_start=frame_start,
                            frame_end=frame_start + render_fps - 1,  # added frame_end
                            channel=7,
                        )
                        # Adjust the position and scale of the strip
                        current_strip.transform.offset_x = -737  # Adjust the horizontal position
                        current_strip.transform.offset_y = -75  # Adjust the vertical position
                        current_strip.transform.scale_x = 1.0  # Adjust the horizontal scale
                        current_strip.transform.scale_y = 1.0  # Adjust the vertical scale

                        current_strip.text = activity
                    current_activity = activity

            index += 1

        # After all rows have been read, extend the final strip to the end
       # if current_strip:
       #     current_strip.frame_final_end = index * render_fps

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

    csv_row_start: IntProperty(name="Start at Row", default=0)
    csv_row_end: IntProperty(name="End at Row", default=100)

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
        return read_some_data(context, self.filepath, self.csv_row_start, self.csv_row_end)
