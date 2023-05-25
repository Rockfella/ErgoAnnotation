from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte
import os
from datetime import datetime, timedelta

import collections


def matlab_to_python_datetime(matlab_datenum):
    return datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum % 1) - timedelta(days=366)


def read_some_data(context, filepath, csv_row_start, csv_row_end):
    # Assuming images are in the same directory as the CSV file
    image_dir = os.path.dirname(filepath)

    print("Start and end row in CSV")
    print(csv_row_start)
    print(csv_row_end)

    # Get a reference to the current scene and the sequencer
    scene = bpy.context.scene
    sequencer = scene.sequence_editor_create()

    render_fps = bpy.context.scene.render.fps

    # Collect data for each day
    day_to_data = collections.defaultdict(list)

    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        # Skip the first row
        next(reader)

        for index, row in enumerate(reader):
            if csv_row_start <= index <= csv_row_end:
                # Get the activity and remove leading/trailing spaces
                activity = row[1].strip()

                # assuming row[0] is the MATLAB datenum
                matlab_datenum = float(row[0])
                date = matlab_to_python_datetime(
                    matlab_datenum).date()  # get the date

                # Collect the data for this day
                day_to_data[date].append(activity)

    # Process the data day by day
    for day_index, (date, activities) in enumerate(sorted(day_to_data.items())):
        channel = 10 - day_index  # Start from channel 10 and go down
        frame_start = 1  # Each day starts at frame 1

        current_activity = None
        current_strip = None

        for activity in activities:
            if activity != current_activity:
                # The activity has changed, if there was a previous strip, extend its end
                if current_strip:
                    current_strip.frame_final_end = frame_start


                #Switch the strip color in sequencer depending on activity
                color_switch = "COLOR_05"

                if activity == "6":
                    color_switch = "COLOR_01"
                elif activity == "5" or activity == "7":
                    color_switch = "COLOR_02"
                elif activity == "2":
                    color_switch = "COLOR_03"
                elif activity == "3" or activity == "4":
                    color_switch = "COLOR_04"
                elif activity == "10" or activity == "11":
                    color_switch = "COLOR_05"
                elif activity == "1" or activity == "8":
                    color_switch = "COLOR_06"
                elif activity == "9":
                    color_switch = "COLOR_08"

                channel_display_position_y = 386
                if channel == 10:
                    channel_display_position_y = 386
                elif channel == 9:
                    channel_display_position_y = 386 - (100 *1)
                elif channel == 8:
                    channel_display_position_y = 386 - (100 * 2)
                elif channel == 7:
                    channel_display_position_y = 386 - (100 * 3)
                elif channel == 6:
                    channel_display_position_y = 386 - (100 * 4)
                elif channel == 5:
                    channel_display_position_y = 386 - (100 * 5)
                elif channel == 4:
                    channel_display_position_y = 386 - (100 * 6)
                elif channel == 3:
                    channel_display_position_y = 386 - (100 * 7)
                elif channel == 2:
                    channel_display_position_y = 386 - (100 * 8)
                elif channel == 1:
                    channel_display_position_y = 386 - (100 * 9)


                # Create a new strip for the new activity
                image_path = os.path.join(image_dir, f"{activity}.png")
                if os.path.isfile(image_path):
                    img = bpy.data.images.load(image_path)
                    current_strip = sequencer.sequences.new_image(
                        name=f"Image Strip {activity}_{day_index}",
                        filepath=image_path,
                        channel=channel,
                        frame_start=frame_start,
                        fit_method='FIT',
                    )
                    current_strip.color_tag = color_switch
                    # Adjust the position and scale of the strip
                    current_strip.transform.offset_x = -737  # Adjust the horizontal position
                    # Adjust the vertical position
                    current_strip.transform.offset_y = channel_display_position_y
                    current_strip.transform.scale_x = 0.5  # Adjust the horizontal scale
                    current_strip.transform.scale_y = 0.5  # Adjust the vertical scale
                else:
                    # If there's no image, create a text strip instead
                    current_strip = sequencer.sequences.new_effect(
                        name=f"Text Strip {activity}_{day_index}",
                        type='TEXT',
                        frame_start=frame_start,
                        frame_end=frame_start + 10,
                        channel=channel,
                    )
                    current_strip.color_tag = color_switch
                    # Adjust the position and scale of the strip
                    current_strip.transform.offset_x = -737  # Adjust the horizontal position
                    # Adjust the vertical position
                    current_strip.transform.offset_y = channel_display_position_y
                    current_strip.transform.scale_x = 0.5  # Adjust the horizontal scale
                    current_strip.transform.scale_y = 0.5  # Adjust the vertical scale

                    current_strip.text = activity
                current_activity = activity

            frame_start += render_fps

        # After all activities have been processed, extend the final strip to the end
        #if current_strip:
        #   current_strip.frame_end = frame_start

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
