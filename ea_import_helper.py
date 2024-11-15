import bpy
import csv
from .ea_constants import frame_from_smpte
import os
from datetime import datetime, timedelta, time
import re
import numpy as np


from .ea_constants import Constants



def create3dObjects(image_dir):
    actvtColors = Constants.actvtColors
    # Create a list of the color tuples
    colors = list(actvtColors.values())
    theboxes = []

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
            mat.node_tree.links.new(
                tex_image.inputs[0], mapping.outputs[0])
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

        theboxes.append(ob)

    return theboxes


def move_strips_to_end_at(channel, end_frame):
    print("Move strips to the end")
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


def matlab_to_python_datetime(matlab_datenum_str):
    matlab_datenum = float(matlab_datenum_str)
    return datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum % 1) - timedelta(days=366)


def iso8601_to_python_datetime(iso8601_string):
    cleaned_string = re.sub(' +', ' ', iso8601_string)
    try:
        return datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M")


def downsample_data(data, old_fps, new_fps):
    # Create an array representing the old timestamps
    old_time = np.linspace(0, len(data)/old_fps, len(data))

    # Create an array representing the new timestamps
    new_time = np.linspace(0, len(data)/old_fps,
                           round(len(data)*new_fps/old_fps))

    # Interpolate the data to the new timestamps
    new_data = np.interp(new_time, old_time, data)

    return new_data

def upsample_data(data, old_fps, new_fps):
    if new_fps <= old_fps:
        raise ValueError("New FPS should be greater than old FPS for up-sampling.")

    # Create an array representing the old timestamps
    old_time = np.linspace(0, len(data) / old_fps, len(data))

    # Create an array representing the new timestamps
    new_time = np.linspace(0, len(data) / old_fps, round(len(data) * new_fps / old_fps))

    # Interpolate the data to the new timestamps
    new_data = np.interp(new_time, old_time, data)

    return new_data

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def detect_delimiter(csv_file):
    with open(csv_file, 'r') as f:
        line = f.readline()
        # Add any other delimiters you need to check
        delimiters = [';', ',', '\t']
        counts = {delimiter: line.count(delimiter) for delimiter in delimiters}
    return max(counts, key=counts.get)


def is_iso8601(date_string):
    cleaned_string = re.sub(' +', ' ', date_string)
    try:
        datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        try:
            datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M:%S.%f")
            return True
        except ValueError:
            try:
                datetime.strptime(cleaned_string, "%Y-%m-%d %H:%M")
                return True
            except ValueError:
                return False


def is_matlab_datetime(date_string):
    try:
        float(date_string)
        return True
    except ValueError:
        return False



def is_day_month_year(date_string):
    cleaned_string = re.sub(' +', ' ', date_string)
    try:
        # Check if date_string is in "Day-Month-Year Hour:Minute:Second" format
        datetime.strptime(cleaned_string, "%d-%b-%Y %H:%M:%S")
        return True
    except ValueError:
        return False


def find_date_format(date_string):
    if is_iso8601(date_string):
        return iso8601_to_python_datetime
    elif is_matlab_datetime(date_string):
        return matlab_to_python_datetime
    elif is_day_month_year(date_string):
        return lambda s: datetime.strptime(s, "%d-%b-%Y %H:%M:%S")
    else:
        return None  # or raise an error




def find_first_row_with_date(filepath_find_first, target_date, delimiter):
    print("Starting to find the date ROW")
    with open(filepath_find_first, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        # Skip the first row
        next(reader)

        # Determine the date format
        first_row = next(reader)
        date_converter = find_date_format(first_row[0])

        # Go back to the beginning of the file
        f.seek(0)
        next(reader)  # Skip the header again

        for index, row in enumerate(reader):
            csv_date = row[0]

            date = date_converter(csv_date)
            dateTime = date.time()

            if dateTime == target_date:
                print("DONE: Starting to find the date ROW")
                return index

    return 0  # Return None if no row with the target date was found


def smpte_to_time(smpte_str):
    hh, mm, ss, ff = smpte_str.split(":")
    return time(hour=int(hh), minute=int(mm), second=int(ss))


def get_smtp_at_zero():
    calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
    calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time
    calc_master_time_adaption = bpy.data.scenes[bpy.context.scene.name].master_time_adaption
    frames_from_master_clock = frame_from_smpte(calc_master_time)
    smtp_at_zero = bpy.utils.smpte_from_frame(
        (0 + frames_from_master_clock - calc_master_frame))
    return smtp_at_zero


def can_move_to_channel(strip, desired_channel):
    """Check if the strip can be moved to the desired channel without overlap."""
    for s in bpy.context.scene.sequence_editor.sequences_all:
        if s == strip:  # Don't check against itself
            continue
        if s.channel == desired_channel:
            if (s.frame_final_start < strip.frame_final_end) and (s.frame_final_end > strip.frame_start):
                return False
    return True


def move_to_lowest_channel(strip):
    """Move the strip to the lowest possible channel."""
    desired_channel = 1
    while not can_move_to_channel(strip, desired_channel):
        desired_channel += 1
    strip.channel = desired_channel


def decimal_percentage_to_range(decimal_percentage):
    """Convert a decimal percentage to a number in the range of 1-10."""
    if decimal_percentage < 0:
        return 1
    elif decimal_percentage > 1:
        return 10
    return 1 + (decimal_percentage * 9)
