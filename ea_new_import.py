from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import bpy
import csv
from .ea_constants import frame_from_smpte, pickTagColorForHandExertions, frame_from_smpte_for_importer
import os
from datetime import datetime, timedelta, time
import numpy as np
import collections
from .ea_constants import Constants
from .ea_import_helper import move_strips_to_end_at, matlab_to_python_datetime, iso8601_to_python_datetime, downsample_data, upsample_data, is_iso8601, is_matlab_datetime, is_day_month_year, get_smtp_at_zero, is_numeric

#TODO: Add more columns to the below handling, also name each "animation" to the column header for easy understanding


def read_and_import(context, self, filepath, channel_to_import_to, import_type, interpolate_data, interpolate_start, sync_to_masterclock, number_of_columns):
    
    scene = bpy.context.scene
    sequencer = scene.sequence_editor_create()
    
    fps = bpy.context.scene.render.fps
    fps_base = bpy.context.scene.render.fps_base
    fps_real = fps / fps_base
    
    #Sync value for csv to mastertime
    amount_to_move = 0
    
    scene = bpy.context.scene
    
    def read_csv(file_path, default_delimiter=','):
        data = {}
        frames = []
        start_date_time = "None"

        try:
            with open(file_path, mode='r') as file:
                sniffer = csv.Sniffer()
                sample = file.read(2048)  # Increase the sample size to 2048 bytes
                file.seek(0)
                try:
                    dialect = sniffer.sniff(sample)
                    #print("Delimiter of csv:", dialect.delimiter)
                except csv.Error:
                    dialect = csv.get_dialect('excel')  # Fallback to default 'excel' dialect
                    dialect.delimiter = default_delimiter

                reader = csv.reader(file, dialect)
                header = next(reader)  # Read the header row

                #print("header", header)
                
                current_column = 0
                for col_name in header[:number_of_columns]:  # Ensure correct number of columns
                    
                    original_col_name = col_name
                    while col_name in data:
                         col_name = f"{original_col_name}_2"
                         header[current_column] = col_name
                    data[col_name] = []
                    current_column += 1
                    
                for i, row in enumerate(reader, start=1):
                    frames.append(i)

                    if i == 1:
                        start_date_time = row[0]

                    for col_name, value in zip(header[:number_of_columns], row[:number_of_columns]):

                        data[col_name].append(value)
                
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return frames, data, start_date_time
    
    
    
    def create_graph_editor_item(frames, values, scale_factor, amount_to_move, col_name):
        # Create an Empty object
        bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
        empty = bpy.context.object
        empty.name = col_name
        #print("values", values)
        # Add a custom property
        bpy.types.Object.imported_graph = bpy.props.FloatProperty(name=col_name, default=0.0)
        empty["imported_graph"] = 0.0

        # Get the action associated with the empty object, create if it doesn't exist
        if not empty.animation_data:
            empty.animation_data_create()
            
        if not empty.animation_data.action:
            empty.animation_data.action = bpy.data.actions.new(name=col_name)
           

        action = empty.animation_data.action
        
        # Create an F-Curve for the custom property
        fcurve = action.fcurves.new(data_path=f'{col_name}', index=0)
        
        loc_frames = frames
        loc_values = [float(x) for x in values]
        float_downsampled_values = [float(item) for item in loc_values]
        # Downsample the frames and values
        
        
        #Besides scaling, lets interpolate the data to reduce number of keyframes per frame
       #if interpolate_data:
       #    loc_frames = frames[::int(scale_factor * interpolate_start)]
       #    loc_values = float_downsampled_values[::int(scale_factor * interpolate_start)]
        if interpolate_data and scale_factor < 1:
            loc_frames = downsample_data(frames, interpolate_start, fps_real)
            loc_values = downsample_data(loc_values, interpolate_start, fps_real)
            
        elif interpolate_data and scale_factor > 1:
            
            loc_frames = upsample_data(frames, interpolate_start, fps_real)
            loc_values = upsample_data(loc_values, interpolate_start, fps_real)
        
        # Insert keyframes directly into the F-Curve
        keyframe_points = fcurve.keyframe_points
        keyframe_points.add(len(loc_frames))

        for i, (frame, value) in enumerate(zip(loc_frames, loc_values)):
      
            scaled_frame = frame * scale_factor
            
            #We want to add a move based on the first row in the csv, compared with mastertime 0
            if not sync_to_masterclock:
                amount_to_move = 0
                
            keyframe_points[i].co = (scaled_frame + amount_to_move, value)
            keyframe_points[i].interpolation = 'LINEAR'
        
  
        fcurve.update()


    def smooth_graph_editor_keys():
        #Smooth the curve to reduce aliasing, not a perfect solution but minimizes dependencies
        for area in bpy.context.screen.areas:
            
            if area.type == 'GRAPH_EDITOR':
                
                for region in area.regions:
                    if region.type == 'WINDOW':
                        
                        override = {
                            'window': bpy.context.window,
                            'screen': bpy.context.screen,
                            'area': area,
                            'region': region,
                            'space_data': area.spaces.active
                        }
                        
                        with bpy.context.temp_override(**override):

                            bpy.ops.graph.select_all(action='SELECT')
                            bpy.ops.graph.smooth()
                            bpy.ops.graph.select_all(action='DESELECT')

                        break
                break
        
     
    def find_area_adjust_content(editor):
        
        for area in bpy.context.screen.areas:
            
            if area.type == editor:
                
                for region in area.regions:
                    if region.type == 'WINDOW':
                        
                        override = {
                            'window': bpy.context.window,
                            'screen': bpy.context.screen,
                            'area': area,
                            'region': region,
                            'space_data': area.spaces.active
                        }

                        
                        with bpy.context.temp_override(**override):
                            if editor == "GRAPH_EDITOR":
                                bpy.ops.graph.view_all()
                                bpy.ops.graph.select_all(action='DESELECT')
                            elif editor == "SEQUENCE_EDITOR":

                                #For some reason we need to do this 2 times in order to get all strips in view
                                bpy.ops.sequencer.view_all()
                                bpy.ops.sequencer.view_all()
                                bpy.ops.sequencer.select_all(action='DESELECT')
                        
                        break
                break   


    def create_sequencer_and_graph_editor_window():
        context = bpy.context.copy()
        old_areas = bpy.context.screen.areas[:]

        # Find the Sequence Editor area and duplicate it
        for area in bpy.context.screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                context['area'] = area
                with bpy.context.temp_override(**context):
                    bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
                break

        # Find the new area by comparing the old and new lists of areas
        new_area = next(area for area in bpy.context.screen.areas if area not in old_areas)

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
                
                

        with bpy.context.temp_override(**override):
            bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.5)

        # Find the new area created by the split
        split_area = next(area for area in bpy.context.screen.areas if area not in old_areas)

        # Change the type of the new split area to the Graph Editor
        split_area.type = 'GRAPH_EDITOR'
        for space in split_area.spaces:
            if space.type == 'GRAPH_EDITOR':
                space.show_region_ui = False
                space.show_locked_time = True
                space.dopesheet.show_only_selected = False
                space.use_auto_merge_keyframes = False
                space.use_realtime_update = False

        # Select all empty objects
        for obj in bpy.context.scene.objects:
            if obj.type == 'EMPTY':
                obj.select_set(True)

        find_area_adjust_content("SEQUENCE_EDITOR")
        find_area_adjust_content("GRAPH_EDITOR")

        toggle_channels_region('GRAPH_EDITOR', show=False)

    def create_visual_strips_actipass(day_to_data):
       color_mapping = {
           6: "COLOR_01",
           5: "COLOR_02",
           7: "COLOR_02",
           2: "COLOR_03",
           3: "COLOR_04",
           4: "COLOR_04",
           10: "COLOR_05",
           11: "COLOR_05",
           1: "COLOR_06",
           8: "COLOR_06",
           9: "COLOR_08"
       }
       
       y_position_cache = {i: 386 - (100 * i) for i in range(11)}
       image_cache = {}
       
       for day_index, (date, activities) in enumerate(sorted(day_to_data.items())):
           darr = np.array(activities, dt)
           channel_start = channel_to_import_to
           channel = channel_start - day_index
           frame_start = 1
           current_activity = None
           current_strip = None

           if import_type == Constants.IMPORT_ACTIPASS:
               for activity in activities:
                   if activity != current_activity:
                       if current_strip:
                           current_strip.frame_final_duration = int(frame_start - current_strip.frame_start)

                       color_switch = color_mapping.get(activity, "COLOR_05")
                       channel_display_position_y = y_position_cache.get(channel_start - channel, 386)

                       image_path = os.path.join(image_dir, f"{activity}.png")
                       if image_path not in image_cache:
                           image_cache[image_path] = os.path.isfile(image_path)
                       
                       if image_cache[image_path]:
                           img = bpy.data.images.load(image_path)
                           current_strip = sequencer.sequences.new_image(
                               name=f"Image Strip {activity}_{day_index}",
                               filepath=image_path,
                               channel=channel,
                               frame_start=int(frame_start),
                               fit_method='FIT',
                           )
                       else:
                           current_strip = sequencer.sequences.new_effect(
                               name=f"Text Strip {activity}_{day_index}",
                               type='TEXT',
                               frame_start=frame_start,
                               frame_end=frame_start + 10,
                               channel=channel,
                           )
                           current_strip.text = activity
                       
                       current_strip.color_tag = color_switch
                       current_strip.transform.offset_x = -737
                       current_strip.transform.offset_y = channel_display_position_y
                       current_strip.transform.scale_x = 0.4 if image_cache[image_path] else 0.6
                       current_strip.transform.scale_y = 0.4 if image_cache[image_path] else 0.6

                       current_activity = activity
                   frame_start += fps_real

               if current_strip:
                   current_strip.frame_final_duration = int(frame_start - current_strip.frame_start)
               
               channel_to_rename = bpy.context.scene.sequence_editor.channels[channel]
               channel_to_rename.name = str(date)

               highest_entry_count = max(len(entry_list) for entry_list in day_to_data.values())
               if import_type == Constants.IMPORT_ACTIPASS:
                   move_strips_to_end_at(channel_start, highest_entry_count)
    
    
    def master_time_strip_exists():
        exists = False
        for area in bpy.context.screen.areas:
            # Check if the area type is 'GRAPH_EDITOR'
            if area.type == "SEQUENCE_EDITOR":
                for strip in scene.sequence_editor.sequences_all:
                    if strip.type == 'TEXT':
                        if strip.name == '@master.time':
                            exists = True
                            break
        
        return exists
           
    # Read the CSV data
    frames, data, start_date_time = read_csv(filepath)
    

    
    
    # Collect data for each day, used for Actipass
    image_dir = os.path.dirname(filepath)
    day_to_data = collections.defaultdict(list)
    datapoint = collections.namedtuple('datapoint',['date','mvc'])
    dt = np.dtype([('date', 'datetime64[us]'), ('mvc', 'f4')])
    date_counter = []
    
    
    #Calculate the sync difference, only if a master time exists
    master_time_there = master_time_strip_exists()                       
                    
    if master_time_there and sync_to_masterclock:
        amount_to_move = sync_csv_and_mastertime(start_date_time)
        self.report({'INFO'}, "Adding synced csv data.")
    elif master_time_there is False and sync_to_masterclock:
        self.report({'INFO'}, "Master time is missing, please add to sync.")
    else:
        self.report({'INFO'}, "Adding csv data without sync.")
                                
                    
    
    ######################################################################################
    #                                                                                    #
    #                   Prepare the read of data based on import type                    #
    #                                                                                    #
    ######################################################################################
    
    if import_type == Constants.IMPORT_EMG or import_type == Constants.IMPORT_ACC:
        # Get the current FPS setting from the render settings
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base

        # Original FPS of the data
        original_fps = interpolate_start

        scale_factor = 1
        if interpolate_data:
            # Calculate the scaling factor
            scale_factor = fps_real / original_fps
            
            
        skip_time_column = True
        channels_added = False
        for index, (col_name, values) in enumerate(data.items()):
            print("data", data.keys())
            if skip_time_column:
                skip_time_column = False
                continue
            
            if values:
                if is_numeric(values[1]):
                    if index <= number_of_columns:
                        #Create the empty object in the 3d space and set keyframes based on CSV data, applying the scaling factor
                        create_graph_editor_item(frames, values, scale_factor, amount_to_move, col_name)
                        channels_added =True
                    else:
                        self.report({'INFO'}, f"{col_name} was not imported.")
                elif not is_numeric(values[1]):
                    self.report({'INFO'}, f"{col_name} was not imported. Not numerical.")
            
        if channels_added:
            create_sequencer_and_graph_editor_window()
            smooth_graph_editor_keys()
            self.report({'INFO'}, "Data successfully imported.")
        else: 
            self.report({'INFO'}, f"Error no Data was imported. From {filepath}")
        
    elif import_type == Constants.IMPORT_ACTIPASS:
        
        list_activities = []
        list_cadence = []
        list_date_time = []
        # Extract activities and cadence data from the input
        for item_index, (col_name, values) in enumerate(data.items()):
            
            if col_name == "Activity":
                list_activities = [int(value.strip()) for value in values]
            elif col_name == "Steps":
                list_cadence = [float(value.strip()) for value in values]
            elif col_name == "DateTime":
                list_date_time = [float(value.strip()) for value in values]


        # Process activities and cadence
        for i, activity in enumerate(list_activities):
            if activity == 5:
                real_cadence = list_cadence[i] * 60
                if real_cadence < 100:
                    activity = 13  # Walk_slow
                else:
                    activity = 14  # Walk_Fast

            # Convert MATLAB datenum to Python datetime
            matlab_datenum = float(list_date_time[i])
            date_time = matlab_to_python_datetime(matlab_datenum)

            # Collect the data for this day
            day_to_data[date_time.date()].append(activity)
            date_counter.append(date_time.date())

        create_visual_strips_actipass(day_to_data)
        for date, activities in day_to_data.items():
            print(f"Date: {date}")
            for activity in activities[:10]:  # Slice the list to get only the first 10 items
                print(activity)
        
def toggle_channels_region(area_type, show=True):
    # Check Blender version
    if bpy.app.version >= (4, 1, 0):
        for area in bpy.context.screen.areas:
            if area.type == area_type:
                for space in area.spaces:
                    if space.type == area_type:
                        space.show_region_channels = show
    else:
        print("This function requires Blender version 4.1 or above.")

      
def convert_date_time_to_SMPT(date):
    
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base
        # Convert the start_time input time to SMPT
        hh = date.hour
        mm = date.minute
        ss = date.second
        micro = date.microsecond
        seconds = micro / 1_000_000
        print("Microseconds to seconds:", seconds)
        ff = float(seconds * fps_real)
        start_time_final = f"{hh:02}:{mm:02}:{ss:02}:{ff}"
        return start_time_final
    
def sync_csv_and_mastertime(start_date_time):
    
    smtp_at_zero = get_smtp_at_zero()
    print("smtp_at_zero", smtp_at_zero)
    frames_at_mastertime_zero = frame_from_smpte_for_importer(smtp_at_zero)
    csv_frame_from_smpte = None
    
    if is_iso8601(start_date_time):
        iso_datenum = start_date_time
        date = iso8601_to_python_datetime(
                        iso_datenum)
        
        
        smtp_from_datetime  = convert_date_time_to_SMPT(date)

        csv_frame_from_smpte = frame_from_smpte_for_importer(smtp_from_datetime)
                    
    elif is_matlab_datetime(start_date_time):
        matlab_datenum = float(start_date_time)
        date = matlab_to_python_datetime(
                        matlab_datenum)
        
        smtp_from_datetime  = convert_date_time_to_SMPT(date)

        csv_frame_from_smpte = frame_from_smpte_for_importer(smtp_from_datetime)
        
    elif is_day_month_year(start_date_time):
        date = datetime.strptime(start_date_time, "%d-%b-%Y %H:%M:%S")
        
        smtp_from_datetime  = convert_date_time_to_SMPT(date)
        csv_frame_from_smpte = frame_from_smpte_for_importer(smtp_from_datetime)
    
    if csv_frame_from_smpte:
        print("csv_frame_from_smpte", csv_frame_from_smpte)
        print("frames_at_mastertime_zero", frames_at_mastertime_zero)
        move_amount = (csv_frame_from_smpte - frames_at_mastertime_zero) - 1 #TODO: 
    else:
        move_amount = 0
        
    return move_amount



class NewImporter(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_improvement.new_importer"  # important since it's how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Data from CSV"

    # ImportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # Setting variables
    import_type = None

    channel_to_import_to: IntProperty(
        name="Channel to import to", default=10,
        description="Choose the channel to begin import too, if it contains multiple days they will descend"
    )

    is_actipass_data: BoolProperty(name="ActiPass", default=False)
    is_EMG_data: BoolProperty(name="EMG", default=False)
    is_accelerometer_data: BoolProperty(name="Accelerometer", default=False)

    sync_to_masterclock: BoolProperty(
        name="Sync to Master Time", default=True)

    interpolate_data: BoolProperty(name="Interpolate", default=False)
    interpolate_start: FloatProperty(name="Interp.Rows/s", default=1000.0)

    number_of_columns: IntProperty(name="Columns to import", default=10)

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

        if not (self.is_EMG_data or self.is_actipass_data or self.is_accelerometer_data):
            layout.prop(self, 'is_EMG_data')
            layout.prop(self, 'is_accelerometer_data')
            layout.prop(self, 'is_actipass_data')
            
        else:
            if self.is_EMG_data:
                layout.prop(self, 'is_EMG_data')
            elif self.is_accelerometer_data:
                layout.prop(self, 'is_accelerometer_data')
            elif self.is_actipass_data:
                layout.prop(self, 'is_actipass_data')

        lines_actipass = [
            'You need to set render Frame Rate',
            '(Output Properties -> Frame Rate)',
            f'to 1 it´s currently set to: {bpy.context.scene.render.fps}',
            'If not, data collection from multiple,',
            'days will not be correct',
            'If the data collection is less than a ',
            'day, there is no need to change the fps.',
            'The 1s data will automatically be sampled',
            'to the video fps.'
        ]

        lines_emg = [
            'If the dateTime format is correct,',
            '(eg. 2023-02-20  10:36:00 in first column),',
            'the master time is used to synch the data.',
            'If there is no master time added,',
            'it starts from frame 1.'
        ]

        if self.is_actipass_data:
            self.import_type = Constants.IMPORT_ACTIPASS
            if bpy.context.scene.render.fps > 1:
                layout.label(text="Important", icon='ERROR')
                for line in lines_actipass:
                    layout.label(text=line)

        elif self.is_EMG_data:
            self.import_type = Constants.IMPORT_EMG
            layout.prop(self, 'number_of_columns')
            layout.prop(self, 'interpolate_data')
            layout.prop(self, 'sync_to_masterclock')
            layout.prop(self, 'interpolate_start')
            layout.label(text="Important", icon='ERROR')
            for line in lines_emg:
                layout.label(text=line)

        elif self.is_accelerometer_data:
            self.import_type = Constants.IMPORT_ACC
            layout.prop(self, 'number_of_columns')
            layout.prop(self, 'interpolate_data')
            layout.prop(self, 'sync_to_masterclock')
            layout.prop(self, 'interpolate_start')
            layout.label(text="Important", icon='ERROR')
            for line in lines_emg:
                layout.label(text=line)


    def execute(self, context):
        # Check if the Blender file is saved
       #if not bpy.data.filepath:
       #    #TODO: Decide if below is necessary
       #    #self.report({'WARNING'}, "Please save the Blender file first.")
       #    return {'CANCELLED'}

        read_and_import(
            context,
            self,
            self.filepath,
            self.channel_to_import_to,
            self.import_type,
            self.interpolate_data,
            self.interpolate_start,
            self.sync_to_masterclock,
            self.number_of_columns
        )

        return {'FINISHED'}