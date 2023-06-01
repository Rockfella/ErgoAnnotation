from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte
import os
from datetime import datetime, timedelta

import collections


def move_strips_to_end_at(channel, end_frame):
    seqs = bpy.context.scene.sequence_editor.sequences
    strips_on_channel = [s for s in seqs if s.channel == channel]

    if not strips_on_channel:  # If there are no strips on the channel, exit the function
        return

    # Find the start frame of the first strip and the end frame of the last strip on the channel
    start_frame = min(s.frame_start for s in strips_on_channel)
    last_end_frame = max(s.frame_final_end for s in strips_on_channel)

    # Calculate the difference between the desired end frame and the current last end frame
    frame_diff = end_frame - last_end_frame

    # Move all strips by the calculated difference
    for strip in strips_on_channel:
        strip.frame_start += frame_diff


def matlab_to_python_datetime(matlab_datenum):
    return datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum % 1) - timedelta(days=366)


def read_some_data(context, filepath, csv_row_start, csv_row_end, create_3d_objects):
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

    actvtColors = {
        'NW-Gray': (128.0/255, 128.0/255, 128.0/255),
        'Lie-Lavender': (229.0/255, 229.0/255, 250.0/255),
        'Sit-Yellow': (255.0/255, 255.0/255, 0.0/255),
        'Stand-LimeGreen': (50.0/255, 204.0/255, 50.0/255),
        'Move-DarkGreen': (0.0/255, 100.0/255, 0.0/255),
        'Walk-DarkOrange': (255.0/255, 139.0/255, 0.0/255),
        'Run-Red': (227.0/255, 18.0/255, 32.0/255),
        'Stair-Cornsilk': (255.0/255, 248.0/255, 219.0/255),
        'Cycle-Purple': (128.0/255, 0.0/255, 128.0/255),
        'Other-Sienna': (159.0/255, 82.0/255, 45.0/255),
        'SlpInBed-DodgerBlue': (30.0/255, 143.0/255, 255.0/255),
        'SlpOUTBed-Aquamarine': (113.0/255, 217.0/255, 226.0/255),
        'Bed-DeepSkyBlue': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue1': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue2': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue3': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue4': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue5': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue6': (0.0/255, 191.0/255, 255.0/255),
        'Bed-DeepSkyBlue7': (0.0/255, 191.0/255, 255.0/255)
    }

    if create_3d_objects:

        # Create a list of the color tuples
        colors = list(actvtColors.values())
        boxes = []

        for i in range(20):
                # Add a cube
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))

            ob = bpy.context.object

            image_path = os.path.join(image_dir, f"{i+1}.png")

            # Set dimensions and location
            ob.dimensions = (1.0, 1.0, 1.0)
            ob.location.x += ob.dimensions.x / 4

            # Rename the object
            ob.name = "Activity_" + str(i+1)

            # Create a new material
            mat = bpy.data.materials.new(name="Color_Material_" + str(i+1))
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]

            # Set the material's diffuse color
            base_color = colors[i] + (1.0,)  # color values and alpha
            bsdf.inputs['Base Color'].default_value = base_color

            # If the image file exists, create a texture and apply it to the material #TODO: remove 0 == 1 if textures should be added
            if os.path.isfile(image_path) and 0 == 1:
                tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_image.image = bpy.data.images.load(image_path)
                tex_image.extension = 'REPEAT'  # Set texture to repeat

                # Add a texture coordinate and mapping node
                coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
                mapping = mat.node_tree.nodes.new('ShaderNodeMapping')
                mapping.inputs['Scale'].default_value = (
                    10.0, 10.0, 10.0)  # Scale the texture to repeat

                # Link the texture coordinate and mapping nodes
                mat.node_tree.links.new(mapping.inputs[0], coord.outputs['UV'])
                mat.node_tree.links.new(tex_image.inputs[0], mapping.outputs[0])

                # Create a new mix node and set it up to mix based on the texture's alpha
                mix_node = mat.node_tree.nodes.new('ShaderNodeMixRGB')
                mix_node.inputs['Color1'].default_value = base_color
                mat.node_tree.links.new(
                    mix_node.inputs['Color2'], tex_image.outputs['Color'])
                mat.node_tree.links.new(
                    mix_node.inputs['Fac'], tex_image.outputs['Alpha'])

                # Link mix node to BSDF node
                mat.node_tree.links.new(
                    bsdf.inputs['Base Color'], mix_node.outputs['Color'])

            # Add the material to the object
            ob.data.materials.append(mat)

            # Set the origin
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

            # Add the box to the list
            boxes.append(ob)
    


    #remember dates
    date_counter = []

    # Select the object you want to duplicate
   
 

    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        # Skip the first row
        next(reader)

        for index, row in enumerate(reader):
            if csv_row_start <= index <= csv_row_end:
                # Get the activity and remove leading/trailing spaces
                activity = row[1].strip()
                cadence = row[2].strip()

                #Calculate walk & run differention 
                if int(activity) == 5:
                    print(cadence)
                    #Cadence is per minute, each row is a second from ActiPass data
                    real_cadence = float(cadence) * 60
                    if real_cadence < 100:
                        #Walk_slow - Picked 13 as this is not a value found in the export
                        activity = "13"
                    elif real_cadence >= 100:
                        #Walk_Fast
                        activity = "14"
                    else:
                        activity = "5"


                # assuming row[0] is the MATLAB datenum
                matlab_datenum = float(row[0])
                date = matlab_to_python_datetime(
                    matlab_datenum).date()  # get the date

                # Collect the data for this day
                day_to_data[date].append(activity)

                date_counter.append(date)

    # Process the data day by day
    for day_index, (date, activities) in enumerate(sorted(day_to_data.items())):
        channel_start = 10 #Which channel day one should end up on
        channel = channel_start - day_index  # Start from channel 10 and go down
        frame_start = 1  # Each day starts at frame 1

        current_activity = None
        current_strip = None
        current_3dObject = None

        for activity in activities:

            #Pick the right3D Object
            if create_3d_objects:
                object_to_duplicate = boxes[int(activity)]

            if activity != current_activity:
                # The activity has changed, if there was a previous strip, extend its end
                if current_strip:
                    current_strip.frame_final_duration = int(frame_start - current_strip.frame_start)

                if current_3dObject:
                    
                    current_3dObject.dimensions.x =   (
                        frame_start / 200) - current_3dObject.location.x


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
               
                if channel == channel_start:
                    channel_display_position_y = 386
                elif channel == channel_start - 1:
                    channel_display_position_y = 386 - (100 *1)
                elif channel == channel_start - 2:
                    channel_display_position_y = 386 - (100 * 2)
                elif channel == channel_start - 3:
                    channel_display_position_y = 386 - (100 * 3)
                elif channel == channel_start - 4:
                    channel_display_position_y = 386 - (100 * 4)
                elif channel == channel_start - 5:
                    channel_display_position_y = 386 - (100 * 5)
                elif channel == channel_start - 6:
                    channel_display_position_y = 386 - (100 * 6)
                elif channel == channel_start - 7:
                    channel_display_position_y = 386 - (100 * 7)
                elif channel == channel_start - 8:
                    channel_display_position_y = 386 - (100 * 8)
                elif channel == channel_start - 9:
                    channel_display_position_y = 386 - (100 * 9)
                elif channel == channel_start - 10:
                    channel_display_position_y = 386 - (100 * 10)


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
                    current_strip.transform.scale_x = 0.6  # Adjust the horizontal scale
                    current_strip.transform.scale_y = 0.6  # Adjust the vertical scale
                    
                    if create_3d_objects:

                        # Create the 3D objects
                        duplicated_object = object_to_duplicate.copy()
                        duplicated_object.data = object_to_duplicate.data.copy()
                        duplicated_object.animation_data_clear()
                        bpy.context.collection.objects.link(duplicated_object)

                        one_frame_in_threeD = (frame_start / 200)
                        # Translate the duplicated object
                        # Example: translate along the X-axis with increasing spacing
                        translation_amount = (one_frame_in_threeD, (channel * 2), 0.0)
                        duplicated_object.location = translation_amount
                        current_3dObject = duplicated_object
                        #print(duplicated_object.location)
                    

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
                    current_strip.transform.scale_x = 0.6  # Adjust the horizontal scale
                    current_strip.transform.scale_y = 0.6  # Adjust the vertical scale

                    current_strip.text = activity
                current_activity = activity
                

            frame_start += render_fps

        # After each day, if there is a current strip, extend its end
        if current_strip:
            current_strip.frame_final_duration = int(frame_start - current_strip.frame_start)
    
        # Rename the channel´s according to date
        channel_str_name = 'Channel ' + str(channel)
        if channel_str_name in bpy.context.scene.sequence_editor.channels:
            # Get the sequence editor
            seq_editor = bpy.context.scene.sequence_editor
            # Get the channel to rename and lock
            channel_to_rename = seq_editor.channels[channel_str_name]
            # Rename the channel
            channel_to_rename.name = str(date)

    
    #Remember the highest entry value for the moce_strips_to_end
    highest_entry_count = 0
    for date, entry_list in day_to_data.items():
        entry_count = len(entry_list)
        last_entry = entry_list[-1]  # Retrieve the last entry using indexing
        print(f"{date}: {entry_count} entries. Last entry: {last_entry}")
        if entry_count > highest_entry_count:
            highest_entry_count = entry_count


    #Take the first channel and move the data to the end of the day as this is not full 24h recording
    move_strips_to_end_at(channel_start, highest_entry_count)


   
        

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

    create_3d_Objects: BoolProperty(name="Create 3d objects", default=False)

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
        return read_some_data(context, self.filepath, self.csv_row_start, self.csv_row_end, self.create_3d_Objects)
