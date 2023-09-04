from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte, pickTagColorForDuet
import os
from datetime import datetime, timedelta, time
import re
import numpy as np

import collections
from .ea_constants import Constants
from .ea_import_helper import decimal_percentage_to_range, move_to_lowest_channel, create3dObjects, move_strips_to_end_at, matlab_to_python_datetime, iso8601_to_python_datetime, downsample_data, detect_delimiter, is_iso8601, is_matlab_datetime, is_day_month_year, find_date_format, find_first_row_with_date, smpte_to_time, get_smtp_at_zero


def read_some_data(context, filepath, csv_row_start, csv_row_end, create_3d_objects, channel_to_import_to, import_type, interpolate_data, interpolate_start, trim_emg_to_masterclock, emg_rain_flow_mvc_collected):

    # Ensure the system console is open

    # Assuming images are in the same directory as the CSV file
    image_dir = os.path.dirname(filepath)

    # print("Start and end row in CSV")
    # print(csv_row_start)
    # print(csv_row_end)

    # Get a reference to the current scene and the sequencer
    scene = bpy.context.scene
    sequencer = scene.sequence_editor_create()

    fps = bpy.context.scene.render.fps
    fps_base = bpy.context.scene.render.fps_base
    fps_real = int(fps / fps_base)

    # Collect data for each day, used for Actipass and EMG import
    day_to_data = collections.defaultdict(list)

    # Collect data from EMG_RAINFLOW
    rainflow_data = collections.defaultdict(list)

    start_row_in_csv = csv_row_start

    # Find the first row in the csv where the date and time is equal to zero time to trim the data
    if import_type == Constants.IMPORT_EMG:
        # Projected frames from master clock
        calc_master_frame = bpy.data.scenes[bpy.context.scene.name].master_time_frame
        calc_master_time = bpy.data.scenes[bpy.context.scene.name].master_time
        frames_from_master_clock = frame_from_smpte(calc_master_time)

        smtp_at_zero = bpy.utils.smpte_from_frame(
            (1 + frames_from_master_clock - calc_master_frame))

        # print(smtp_at_zero)

        # Split into components
        hh, mm, ss, ff = map(int, smtp_at_zero.split(':'))

        # Convert the SMTP at zero to datetime.time object
        zero_time = time(int(hh), int(mm), int(ss))

        if trim_emg_to_masterclock:
            start_row_in_csv = find_first_row_with_date(
                filepath, zero_time, detect_delimiter(filepath))
    # 3d boxes if necessary
    boxes = []

    # Creates 3d Objects in the 3d workspace
    if create_3d_objects:

        boxes = create3dObjects(image_dir)
        print("Number of boxes: ", len(boxes))

    # remember dates
    date_counter = []

    # remember rainflow layers
    rainflow_layers_counter = 0

    # Select the object you want to duplicate

    # Check which delimiter is used

    delimiter = detect_delimiter(filepath)

    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        # Skip the first row
        next(reader)
        print("Start row based on cut", start_row_in_csv)
        if start_row_in_csv < 0:
            for i in range(start_row_in_csv):
                next(reader)

        for index, row in enumerate(reader):
            ######################################################################################
            #                                                                                    #
            #                   Prepare the read of data based on import type                    #
            #                                                                                    #
            ######################################################################################
            if import_type == Constants.IMPORT_ACTIPASS:

                # If the import_type is Actipass:
                if csv_row_start <= index <= csv_row_end:
                    # Get the activity and remove leading/trailing spaces
                    activity = row[1].strip()
                    cadence = row[2].strip()

                    # Calculate walk & run differention
                    if int(activity) == 5:
                        # print(cadence)
                        # Cadence is per minute, each row is a second from ActiPass data
                        real_cadence = float(cadence) * 60
                        if real_cadence < 100:
                            # Walk_slow - Picked 13 as this is not a value found in the export
                            activity = "13"
                        elif real_cadence >= 100:
                            # Walk_Fast
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

            elif import_type == Constants.IMPORT_EMG:
                # If the import_type is EMG:
                if start_row_in_csv <= index <= csv_row_end:
                    # Get the activity and remove leading/trailing spaces
                    csv_date = row[0]
                    # print("CSV Date: ", csv_date)
                    if is_iso8601(csv_date):

                        # assuming row[0] is the MATLAB datenum
                        iso_datenum = row[0]
                        date = iso8601_to_python_datetime(
                            iso_datenum)  # get the date

                        percent_mvc = float(row[1].strip())

                        # Collect the data for this day
                        day_to_data[date].append(percent_mvc)

                        date_counter.append(date)

                    elif is_matlab_datetime(csv_date):

                        # assuming row[0] is the MATLAB datenum
                        matlab_datenum = float(row[0])
                        date = matlab_to_python_datetime(
                            matlab_datenum)  # get the date

                        percent_mvc = float(row[1].strip())

                        # Collect the data for this day
                        day_to_data[date].append(percent_mvc)

                        date_counter.append(date)
                    elif is_day_month_year(csv_date):
                        # print("Yes got here")
                        # Parse the date
                        date = datetime.strptime(csv_date, "%d-%b-%Y %H:%M:%S")

                        percent_mvc = float(row[1].strip())

                        # Collect the data for this day
                        day_to_data[date].append(percent_mvc)

                        date_counter.append(date)
            #JOHAN
            elif import_type == Constants.IMPORT_EMG_RAINFLOW:
                # If the import_type is EMG_RAINFLOW:
                if start_row_in_csv <= index <= csv_row_end:
                    # Get the activity and remove leading/trailing spaces
                    csv_date = row[3]
                    # print("CSV Date: ", csv_date)
                    if is_iso8601(csv_date):

                        # assuming row[] is the MATLAB datenum
                        datenum_start = row[3]
                        datenum_end = row[4]

                        start_time = iso8601_to_python_datetime(
                            datenum_start)  # get the date

                        end_time = iso8601_to_python_datetime(
                            datenum_end)

                        # Convert the start_time input time to SMPT
                        hh = start_time.hour
                        mm = start_time.minute
                        ss = start_time.second
                        ff = "00"
                        start_time_final = f"{hh:02}:{mm:02}:{ss:02}:{ff}"
 
                        # Convert the start_time input time to SMPT
                        hh_end = end_time.hour
                        mm_end = end_time.minute
                        ss_end = end_time.second
                        ff = "00"
                        end_time_final = f"{hh_end:02}:{mm_end:02}:{ss_end:02}:{ff}"

                        #Time converted to frames
                        frame_at_start_time = frame_from_smpte(start_time_final)
                        frame_at_end_time = frame_from_smpte(end_time_final)

                        #Input columns
                        pre_count = row[0].strip()
                        pre_range = row[1].strip()
                        pre_mean = row[2].strip()
                        # Check if the input contains "." or ",""
                        if ',' in pre_count:
                            pre_count = pre_count.replace(',', '.')

                        if ',' in pre_range:
                            pre_range = pre_range.replace(',', '.')

                        if ',' in pre_mean:
                            pre_mean = pre_mean.replace(',', '.')



                        nr_count = float(pre_count)
                        kg_range = float(pre_range)
                        kg_mean = float(pre_mean)

                        overlap = False
                        overlap_number = 0
                        for key in rainflow_data:
                            for interval in rainflow_data[key]:
                                # Check if the time ranges overlap
                                if (start_time <= interval['end_time']) and (end_time >= interval['start_time']):
                                    overlap = True
                                    overlap_number += 1
                                    #break

                        if overlap:
                            rainflow_layers_counter += 1

                        #Johan
                        #Calculate the OMNI-RES Equivalent for this data
                        omni_res = decimal_percentage_to_range(
                            kg_range / emg_rain_flow_mvc_collected)

                        results_dict = {
                            'count': nr_count,
                            'range': kg_range,
                            'mean': kg_mean,
                            'start_time': start_time,
                            'start_frame': frame_at_start_time,
                            'end_time': end_time,
                            'end_frame': frame_at_end_time,
                            'overlap_number': overlap_number,
                            'omni_res': omni_res
                        }

                        # Collect the data for this 
                        rainflow_data[rainflow_layers_counter].append(
                            results_dict)

                    elif is_matlab_datetime(csv_date):

                        datenum_start = row[3]
                        datenum_end = row[4]

                        start_time = matlab_to_python_datetime(
                            datenum_start)  # get the date

                        end_time = matlab_to_python_datetime(
                            datenum_end)
                        #TODO: IMPORT ABOVE

                    elif is_day_month_year(csv_date):

                        datenum_start = row[3]
                        datenum_end = row[4]

                        start_time = datetime.strptime(
                            datenum_start)  # get the date

                        end_time = datetime.strptime(
                            datenum_end)
                        # TODO: IMPORT ABOVE



                        
        print(rainflow_data)
        print("overlapping layers", rainflow_layers_counter)
        print("Number of items in rainflow_data", len(rainflow_data))
        key_counter = 0 
        for key in rainflow_data:
            for interval in rainflow_data[key]:
                key_counter += 1
        print("Number of keys in rainflow_data", key_counter)
        # else:
        #    #TODO: First listen to the import on column 1, see what timeDate format, now matlab is the only format
        #    activity = row[1].strip()
        #    # assuming row[0] is the MATLAB datenum
        #    matlab_datenum = float(row[0])
        #    date = matlab_to_python_datetime(
        #        matlab_datenum).date()  # get the date
#
        #    # Collect the data for this day
        #    day_to_data[date].append(activity)
#
        #    date_counter.append(date)

        # lets downsample the data
        if interpolate_data and import_type == Constants.IMPORT_EMG:
            fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
            # downsample the data for each day
            for date in day_to_data:
                day_to_data[date] = downsample_data(
                    day_to_data[date], interpolate_start, fps)  # adjust numbers as needed

    num_days = len(day_to_data)
    num_entries = sum(len(values) for values in day_to_data.values())
    print(num_days)
    print(num_entries)
    # print(day_to_data)

    has_created_emg_bar = False
    frame_memory = 0

    give_first = False
    move_emg_data_frames = 0

    # Figure out the start frame for the emgdata:
    if import_type == Constants.IMPORT_EMG:
        date, activities = next(iter(sorted(day_to_data.items())))

        emg_time_str = str(date.time())

        ff = "00"
        hh, mm, ss = emg_time_str.split(":")
        emg_final_time_str = f"{hh}:{mm}:{ss}:{ff}"

        frame_at_emg_time_str = frame_from_smpte(emg_final_time_str)

        smtp_at_zero = get_smtp_at_zero()

        video_clip_zero_time = smpte_to_time(smtp_at_zero)

        # Only produce a movement of frames if the emg collection occured after the video recording started
        if date.time() > video_clip_zero_time:

            frames_at_zero = frame_from_smpte(smtp_at_zero)
            # print("Frames at zero", frame_at_emg_time_str - frames_at_zero)
            move_emg_data_frames = frame_at_emg_time_str - frames_at_zero

    ######################################################################################

    #                                                                                    #

    #       When the data has been imported, we decide what should be done with it       #

    #                                                                                    #

    ######################################################################################
    
    # Process the data day by day
    for day_index, (date, activities) in enumerate(sorted(day_to_data.items())):
        channel_start = channel_to_import_to  # Which channel day one should end up on
        channel = channel_start - day_index  # Start from channel 10 and go down
        frame_start = 1  # Each day starts at frame 1

        current_activity = None
        current_strip = None
        current_3dObject = None

        if import_type == Constants.IMPORT_ACTIPASS:

            ######################################################################################
            #                                                                                    #
            #                                Actipass Import  - Visuals                          #
            #                                                                                    #
            ######################################################################################

            for activity in activities:

                # Pick the right3D Object
                if create_3d_objects:

                    object_to_duplicate = boxes[int(activity)]

                if activity != current_activity:
                    # The activity has changed, if there was a previous strip, extend its end
                    if current_strip:
                        current_strip.frame_final_duration = int(
                            frame_start - current_strip.frame_start)

                    if current_3dObject:

                        current_3dObject.dimensions.x = (
                            frame_start / 200) - current_3dObject.location.x

                    # Switch the strip color in sequencer depending on activity
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
                        channel_display_position_y = 386 - (100 * 1)
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
                        current_strip.transform.scale_x = 0.4  # Adjust the horizontal scale
                        current_strip.transform.scale_y = 0.4  # Adjust the vertical scale

                        if create_3d_objects:

                            # Create the 3D objects
                            duplicated_object = object_to_duplicate.copy()
                            duplicated_object.data = object_to_duplicate.data.copy()
                            duplicated_object.animation_data_clear()
                            bpy.context.collection.objects.link(
                                duplicated_object)

                            one_frame_in_threeD = (frame_start / 200)
                            # Translate the duplicated object
                            # Example: translate along the X-axis with increasing spacing
                            translation_amount = (
                                one_frame_in_threeD, (channel * 2), 0.0)
                            duplicated_object.location = translation_amount
                            current_3dObject = duplicated_object
                            # print(duplicated_object.location)

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

                frame_start += fps_real

            # After each day, if there is a current strip, extend its end
            if current_strip:
                current_strip.frame_final_duration = int(
                    frame_start - current_strip.frame_start)

            # Rename the channel´s according to date
            channel_to_rename = bpy.context.scene.sequence_editor.channels[channel]
            channel_to_rename.name = str(date)

            # Remember the highest entry value for the moce_strips_to_end
            highest_entry_count = 0
            for date, entry_list in day_to_data.items():
                entry_count = len(entry_list)
                # Retrieve the last entry using indexing
                last_entry = entry_list[-1]
                print(f"{date}: {entry_count} entries. Last entry: {last_entry}")
                if entry_count > highest_entry_count:
                    highest_entry_count = entry_count

                # Take the first channel and move the data to the end of the day as this is not full 24h recording if its Acti-pass Data
                if import_type == Constants.IMPORT_ACTIPASS:
                    move_strips_to_end_at(
                        channel_start, highest_entry_count)
                # TODO: Add elif what should it do to the data if its not Acti-pass

                scn = bpy.context.scene
                seq = scn.sequence_editor

        ######################################################################################
        #                                                                                    #
        #                           EMG Import   - Visuals                                   #
        #                                                                                    #
        ######################################################################################
        if import_type == Constants.IMPORT_EMG:

            if not has_created_emg_bar:
                bpy.context.scene.frame_current = bpy.context.scene.frame_start
                # Set the frame range and channel
                frame_start = bpy.context.scene.frame_start
                frame_end = bpy.context.scene.frame_end
                frame_current = bpy.context.scene.frame_current
                channel = 13

                # Colors
                # Green, Yellow, Red
                colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]

                # Set the width and height of the image
                image_width = 47
                image_height = 227

                # Create a new image
                image = bpy.data.images.new(
                    "Color Image", width=image_width, height=image_height)

                # Simple linear interpolation function

                def lerp(a, b, t):
                    return a * (1 - t) + b * t

                # Set each pixel of the image to the corresponding color, interpolating between colors
                for y in range(image_height):
                    # Determine the indices of the two colors to interpolate between and the interpolation factor
                    y_scaled = y / (image_height - 1) * (len(colors) - 1)
                    color_index = int(y_scaled)
                    t = y_scaled - color_index

                    color1 = colors[color_index]
                    color2 = colors[min(color_index + 1, len(colors) - 1)]

                    # Interpolate between the colors
                    color = [lerp(c1, c2, t) for c1, c2 in zip(
                        color1, color2)] + [1.0]  # RGBA

                    for x in range(image_width):
                        image.pixels[(y*image_width+x) *
                                     4:(y*image_width+x+1)*4] = color

                # Save the image
                # Save the image to the current blend file directory
                filepath = bpy.path.abspath('//')
                image_filepath = os.path.join(filepath, "Color.png")
                image.file_format = 'PNG'

                # Check if the image file already exists
                if not os.path.exists(image_filepath):
                    image.filepath_raw = image_filepath
                    image.save()

                 # Create the crop
                crop_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
                    name="EMG_COVER",
                    type='COLOR',
                    channel=channel,
                    frame_start=frame_start,
                    frame_end=frame_end
                )
                # Create the image strip
                strip = bpy.context.scene.sequence_editor.sequences.new_image(
                    name="EMG_BAR",
                    filepath=image_filepath,
                    channel=channel - 1,
                    frame_start=frame_start
                )

                # Create black color strip
                color_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
                    name="Black Border",
                    type='COLOR',
                    channel=channel - 2,
                    frame_start=frame_start,
                    frame_end=frame_end
                )
                color_strip.color = (0, 0, 0)
                crop_strip.color = (0, 0, 0)

                strip.frame_final_duration = frame_end - frame_start + 1

                width = bpy.context.scene.render.resolution_x / 2

                strip.transform.offset_x = width * -0.88

                color_strip.transform.offset_x = strip.transform.offset_x - 1
                color_strip.transform.offset_y = strip.transform.offset_y - 1
                color_strip.transform.scale_x = 0.026
                color_strip.transform.scale_y = 0.21268

                crop_strip.transform.offset_x = strip.transform.offset_x - 1
                crop_strip.transform.offset_y = strip.transform.offset_y - 1
                crop_strip.transform.scale_x = 0.026
                crop_strip.transform.scale_y = 0.21268

                has_created_emg_bar = True

            if trim_emg_to_masterclock:

                smtp_at_zero = get_smtp_at_zero()

                # print(smtp_at_zero)

                # Split into components
                hh, mm, ss, ff = map(int, smtp_at_zero.split(':'))

                # Convert the SMTP at zero to datetime.time object
                zero_time = time(int(hh), int(mm), int(ss))

                # highest_percent_mvc = max(activities)

                if date.time() >= zero_time:
                    if not give_first:
                        print(date.time(), zero_time)
                        give_first = True

                    # calculate the percentage
                    # percent_mvc = activity / highest_percent_mvc
                    # set the crop

            push_late_emg = 0
            for event in activities:
                # print(date.time())
                bpy.context.scene.sequence_editor.sequences_all["EMG_COVER"].crop.min_y = int(
                    (1076 * event))
                # set the keyframe
                bpy.context.scene.sequence_editor.sequences_all["EMG_COVER"].crop.keyframe_insert(
                    'min_y', frame=move_emg_data_frames + frame_start + frame_memory)
                frame_start += 1
                frame_memory += 1  # Move to the next frame

    for key in rainflow_data:

        

        ######################################################################################
        #                                                                                    #
        #                               EMG_RAINFLOW   - Visuals                             #
        #                                                                                    #
        ######################################################################################
        
        if import_type == Constants.IMPORT_EMG_RAINFLOW:
            # Johan
            #TODO: PRINT OMNIRES
            
            for interval in rainflow_data[key]:
                # Check if the time ranges overlap
                # if (start_time <= interval['end_time']) and (end_time >= interval['start_time']):
                #    overlap = True
                #    break
                #print(interval['start_time'].time())
                #print("Start", interval['start_frame'])
               # print("End", interval['end_frame'])
                use_start_frame = int(interval['start_frame'])
                use_end_frame = int(interval['end_frame'])
                if use_start_frame == use_end_frame:
                    use_end_frame = use_start_frame + 10
                current_strip = sequencer.sequences.new_effect(
                    name=f"Range {interval['range']} Mean: {interval['mean']}",
                    type='TEXT',
                    frame_start=use_start_frame,
                    frame_end=use_end_frame,
                    channel=interval['overlap_number'] + 1,
                )
                current_strip.color_tag = pickTagColorForDuet(interval['omni_res'])
                # Adjust the position and scale of the strip
                current_strip.transform.offset_x = -737  # Adjust the horizontal position
                # Adjust the vertical position
                current_strip.transform.offset_y = 386
                current_strip.transform.scale_x = 0.6  # Adjust the horizontal scale
                current_strip.transform.scale_y = 0.6
                current_strip.text = f"Range {interval['range']} Mean: {interval['mean']}"


                # After creation, make sure they are arranged on the channels 
                if bpy.context.scene.sequence_editor:
                
                    # Sort strips by their start frame so that we handle them in the order they appear in the timeline
                    all_strips = sorted(
                        bpy.context.scene.sequence_editor.sequences_all, key=lambda s: s.frame_start)

                    for strip in all_strips:
                        move_to_lowest_channel(strip)
                        # Adjust the vertical scale

    ########################################################
    #                                                      #
    #          Window handling when importing EMG          #
    #                                                      #
    ########################################################
    if import_type == Constants.IMPORT_EMG:

        # Call user prefs window
        context = bpy.context.copy()

        # Store the current list of areas
        old_areas = bpy.context.screen.areas[:]

        # Find the Sequence Editor area and duplicate it
        for area in bpy.context.screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                context['area'] = area
                bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
                break

        # Find the new area by comparing the old and new lists of areas
        new_area = next(
            area for area in bpy.context.screen.areas if area not in old_areas)

        # Store the list of areas again before the split
        old_areas = bpy.context.screen.areas[:]

        # Split this new area
        override = bpy.context.copy()
        override['area'] = new_area

        for space in new_area.spaces:
            if space.type == 'SEQUENCE_EDITOR':
                space.show_region_ui = False
                space.show_region_channels = False

                space.show_locked_time = True

        bpy.ops.screen.area_split(override, direction='HORIZONTAL', factor=0.5)

        # Find the new area created by the split
        split_area = next(
            area for area in bpy.context.screen.areas if area not in old_areas)
        # bpy.ops.wm.context_toggle(data_path="space_data.show_region_channels")

        # Change the type of the new split area to the Graph Editor
        split_area.type = 'GRAPH_EDITOR'
        for space in split_area.spaces:
            if space.type == 'GRAPH_EDITOR':
                space.show_region_ui = False

                space.show_locked_time = True

        # Smooth the curve to reduce aliasing, not perfect solution but minimizes dependancies

        for area in bpy.context.screen.areas:
            if area.type == 'GRAPH_EDITOR':
                override = {'window': bpy.context.window,
                            'screen': bpy.context.screen, 'area': area}
                bpy.ops.graph.smooth(override)
                break

    # split_area.header_text_set("EMG DATA")
    # for region in split_area.regions:
    #    if region.type == 'TOOLS':
    #        if region.width == 1:
    #            print("toolshelf closed")
    #        else:
    #            print("toolshelf open")
    #            bpy.ops.object.hide_tools()
    #
    #    elif region.type == 'UI':
    #        if region.width == 1:
    #            print("properties closed")
    #        else:
    #            print("properties open")
    #            bpy.ops.object.hide_tools()

    for area in bpy.context.screen.areas:
        if area.type == 'GRAPH_EDITOR':
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            bpy.ops.graph.view_selected(ctx)

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
    # Setting_variables
    create_3d_Objects_var = False
    import_type = None

    csv_row_start: IntProperty(name="Start at Row", default=0)
    csv_row_end: IntProperty(name="End at Row", default=1200000)
    channel_to_import_to: IntProperty(name="Channel to import to", default=10,
                                      description="Choose the channel to begin import too, if it contains multiple days they will decend")

    is_actipass_data: BoolProperty(name="ActiPass", default=False)
    create_3d_Objects: BoolProperty(name="Create 3d objects", default=False)

    is_EMG_data: BoolProperty(name="EMG", default=False)
    is_EMG_rainflow_data: BoolProperty(name="EMG_rainflow", default=False)
    interpolate_data: BoolProperty(name="Interpolate", default=True)
    trim_emg_to_masterclock: BoolProperty(
        name="Trim to Master Time", default=True)
    interpolate_start: IntProperty(name="Interp.Rows/s", default=1000)
    emg_rain_flow_mvc_collected: IntProperty(name="MVC in KG", default=10)

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

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'channel_to_import_to')

        # TODO: ADD other potential settings

       # If none are checked, display all
        if not (self.is_EMG_data or self.is_EMG_rainflow_data or self.is_actipass_data):
            layout.prop(self, 'is_EMG_data')
            layout.prop(self, 'is_EMG_rainflow_data')
            layout.prop(self, 'is_actipass_data')
        else:
            # If one is checked, only display that one
            if self.is_EMG_data:
                layout.prop(self, 'is_EMG_data')
            elif self.is_EMG_rainflow_data:
                layout.prop(self, 'is_EMG_rainflow_data')
            elif self.is_actipass_data:
                layout.prop(self, 'is_actipass_data')

        lines_actipass = ['You need to set render Frame Rate',
                          '(Output Properties -> Frame Rate)',
                          f'to 1 it´s currently set to: {bpy.context.scene.render.fps}',
                          'If not, data collection from multiple,', 
                          'days will not be correct',
                          'If the data collection is less than a ',
                          'day, there is no need to change the fps.'
                          'The 1s data will automatically be sampled',
                          'to the video fps.'
                          
                          ]
        
        lines_emg = ['If the dateTime format is correct,',
                     '(eg. 2023-02-20  10:36:00 in first column),',
                     'the master time is used to synch the data.',
                     'If there is no master time added,',
                     'it starts from frame 1.',
                     'Atm. Only column 2 is imported'
                     ]

        lines_emg_rainflow = ['If the dateTime format is correct,',
                              '(eg. 2023-02-20  10:36:00 in first column),',
                              'the master time is used to synch the data.',
                              'If there is no master time added,',
                              'it starts from frame 1.',
                              'Atm. Column 1 and 2 is imported'
                              ]

        if self.is_actipass_data:
            layout.prop(self, 'create_3d_Objects')
            layout.prop(self, 'csv_row_start')
            layout.prop(self, 'csv_row_end')
            self.import_type = Constants.IMPORT_ACTIPASS
            if bpy.context.scene.render.fps > 1:

                layout.label(text="Important", icon='ERROR')
                for line in lines_actipass:
                    layout.label(text=line)

            if self.create_3d_Objects:
                self.create_3d_Objects_var = True

        elif self.is_EMG_data:
            self.import_type = Constants.IMPORT_EMG
            layout.prop(self, 'csv_row_start')
            layout.prop(self, 'csv_row_end')
            layout.prop(self, 'interpolate_data')
            layout.prop(self, 'trim_emg_to_masterclock')
            layout.prop(self, 'interpolate_start')
            layout.label(text="Important", icon='ERROR')
            for line in lines_emg:
                layout.label(text=line)

        elif self.is_EMG_rainflow_data:
            self.import_type = Constants.IMPORT_EMG_RAINFLOW
            layout.prop(self, 'csv_row_start')
            layout.prop(self, 'csv_row_end')
            layout.prop(self, 'emg_rain_flow_mvc_collected')
            layout.label(text="Important", icon='ERROR')
            for line in lines_emg_rainflow:
                layout.label(text=line)

    def execute(self, context):
        # Check if the Blender file is saved
        if not bpy.data.filepath:
            self.report({'WARNING'}, "Please save the Blender file first.")
            return {'CANCELLED'}

        return read_some_data(
            context,
            self.filepath,
            self.csv_row_start,
            self.csv_row_end,
            self.create_3d_Objects,
            self.channel_to_import_to,
            self.import_type,
            self.interpolate_data,
            self.interpolate_start,
            self.trim_emg_to_masterclock,
            self.emg_rain_flow_mvc_collected
        )
