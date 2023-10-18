import math
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy_extras.io_utils import ExportHelper
import bpy
import csv
from .ea_constants import Constants
from .ea_constants import frame_from_smpte
import os


def get_fill_color(value_scale):
    def interpolate(start, end, fraction):
        return tuple(int(start[i] + (end[i] - start[i]) * fraction) for i in range(3))

    # Define color points based on the given data
    color_points = [
        (0.05, (42, 255, 0)),
        (0.10, (114, 255, 0)),
        (0.20, (199, 255, 0)),
        (0.30, (255, 246, 0)),
        (0.40, (255, 212, 0)),
        (0.50, (255, 110, 0)),
        (0.60, (255, 46, 0)),
        (0.864, (255, 46, 0))
    ]

    # Return the first color for values smaller or equal to the first threshold
    if value_scale <= color_points[0][0]:
        return color_points[0][1]

    # Find the appropriate color or interpolation between colors
    for i in range(len(color_points) - 1):
        if value_scale <= color_points[i+1][0]:
            fraction = (
                value_scale - color_points[i][0]) / (color_points[i+1][0] - color_points[i][0])
            return interpolate(color_points[i][1], color_points[i+1][1], fraction)

    # If value_scale is beyond the provided range, return the last color
    return color_points[-1][1]


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def create_a4_svg_with_text_and_table(filepath, text_content, column_1_data, column_2_data, column_3_data, column_4_data, column_5_data, str_list_to_report):
    # Define the SVG structure for an A4 paper
    a4_width = 2100  # in mm
    a4_height = 2970  # in mm
    title_font_size = 72  # Original was 24, 300% larger is 72
    text_x = a4_width / 2
    # 10 pixels from top and adjusted to account for font size
    text_y = 10 + title_font_size

    table_width = a4_width * 0.85
    table_start_x = (a4_width - table_width) / 2
    cell_width = table_width / 4
    cell_height = a4_height / 35
    table_start_y = text_y + 100  # Adjusted to be just below the title

    # Generate SVG for the table cells and their text
    table_elements = []
    for row in range(14):  # Adjusted for an additional row
        for col in range(4):  # Adjusted for 4 columns
            x = table_start_x + col * cell_width
            y = table_start_y + row * cell_height

            # Create cell rectangle
            fill_color = "lightgray" if row == 0 else "white"
            print("The sum of the column 3 is")
            the_sum_of_cumulative = sum(column_3_data)
            probability = 0.0
            if the_sum_of_cumulative > 0.0:
                probability = due_probability(the_sum_of_cumulative)
            else:
                probability = 0.0

            #Color the Damage
            if 0 < row < 12 and col == 2:

                if column_3_data[row - 1] > 0:

                    fill_color = rgb_to_hex(get_fill_color(due_probability(column_3_data[row - 1])))
               

            cell_rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" style="fill:{fill_color};stroke:black;stroke-width:0.5" />'
            if row == 12:
                
                if col == 2:
                    fill_color = rgb_to_hex(get_fill_color(probability))
                    cell_rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" style="fill:{fill_color};stroke:black;stroke-width:0.0" />'
                else:
                    cell_rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" style="fill:{fill_color};stroke:black;stroke-width:0.0" />'

            if row == 13:

                if col == 2:
                    fill_color = rgb_to_hex(get_fill_color(probability))
                    cell_rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" style="fill:{fill_color};stroke:black;stroke-width:0.0" />'
                else:
                    cell_rect = f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" style="fill:{fill_color};stroke:black;stroke-width:0.0" />'




            table_elements.append(cell_rect)

            # Create text for cell
            text_x_center = x + cell_width / 2
            text_y_center = y + cell_height / 2
            column_names = [
                "OMNI-RES Scale", "Repetitions (per work day)", "Damage (cumulative)", "% Total (damage)"]
            if row == 0:
                cell_text = column_names[col]
                text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="28" fill="black" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'
            elif row == 12:  # Adjusted for the additional row
                if col == 1:
                    cell_text = f"Total Cumulative Damage:"
                    text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="24" fill="black" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'
                elif col == 2:
                    
                    cell_text = f"{sum(column_3_data):.5f}"
                    text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="24" fill="black" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'
                else:
                    continue  # Skip adding text for other columns in the 11th row

            elif row == 13:  # Adjusted for the additional row
                if col == 1:
                    cell_text = f"Probability of DUE Outcome (%):"
                    text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="24" fill="black" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'
                elif col == 2:
                    
                    probability_percentage = "{:.1%}".format(probability)
                    cell_text = f"{probability_percentage}"
                    text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="24" fill="black" font-weight="bold" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'
                else:
                    continue  # Skip adding text for other columns in the 11th row






            else:
                if 0 < row < 12 and col == 0:
                    #print(row)
                    cell_text = f'{column_1_data[row - 1]}'
                elif 0 < row < 12 and col == 1:
                    #print(row)
                    cell_text = f'{column_2_data[row - 1]}'
                elif 0 < row < 12 and col == 2:
                    #print(row)
                    #cell_text = f'{column_3_data[row - 1]}'
                    cell_text = "{:.6f}".format(column_3_data[row - 1])
                elif 0 < row < 12 and col == 3:
                    #print(row)
                    
                    #if the sum is larger than zero, otherwise dont 
                    if the_sum_of_cumulative > 0:

                        cell_text = "{:.1%}".format(
                            column_3_data[row - 1] / the_sum_of_cumulative)
                    else:
                        cell_text = "{:.1%}".format(0.00000)
                else:
                    cell_text = f'R{row}C{col+1}'

                text_element = f'<text x="{text_x_center}" y="{text_y_center}" font-family="Arial" font-size="24" fill="black" text-anchor="middle" alignment-baseline="middle">{cell_text}</text>'

            table_elements.append(text_element)

        added_row_height = 0
        for s in str_list_to_report:
            string_to_append = f'<text x = "10" y = "{1400 + added_row_height}" font-family = "Arial" font-size = "24" fill = "black" text-anchor = "start"> {s}</text>'
            table_elements.append(string_to_append)
            added_row_height += 40

        citation = """
                        <a xlink:href="https://journals.sagepub.com/doi/abs/10.1177/0018720818789319" target="_blank">
                            <text x="10" y="1700" font-family="Arial" font-size="24" fill="black" text-anchor="start">
                                This report was possible due to the work conducted by:
                                <tspan x="10" dy="40">Gallagher, S., Schall Jr, M. C., Sesek, R. F., &amp; Huangfu, R. (2018).</tspan>
                                <tspan x="10" dy="40">An Upper Extremity Risk Assessment Tool Based on Material Fatigue Failure Theory: The Distal Upper Extremity Tool (DUET).</tspan>
                                <tspan x="10" dy="40">Human factors, 60(8), 1146-1162.</tspan>
                            </text>
                        </a>
                        """
        table_elements.append(citation)

    table_svg = "\n".join(table_elements)

    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <svg width="100%" height="100%" viewBox="0 0 {a4_width} {a4_height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <rect width="{a4_width}" height="{a4_height}" style="fill:white;stroke:black;stroke-width:1" />
            <text x="{text_x}" y="{text_y}" font-family="Arial" font-size="{title_font_size}" fill="black" text-anchor="middle" alignment-baseline="hanging">{text_content}</text>
            {table_svg}
        </svg>
        """


    # Save the SVG data to a file
    with open(filepath, 'w') as f:
        f.write(svg_content)


def write_some_data(context, filepath, export_duet_risk_report, report_method_choosen, percentage_of_workday, total_hours_of_workday, duet_options):
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

    # Creating a list based of the master clock
    for frame in range(scene.frame_start, scene.frame_end + 1):
        # Input SMPTE formatted string
        smpte_string_current = bpy.utils.smpte_from_frame(
            (frame + frames_from_master_clock - calc_master_frame), fps=fps, fps_base=fps_base)
        data_master_clock.append(smpte_string_current)

    # Building a list of strips with their range and append them to the right dict
    sir_data_DUET_L = []
    sir_data_DUET_R = []
    sir_data_FREE_CHANNEL = []

    # Sorting sequence_strips based on channel values in descending order
    sorted_strips = sorted(sequence_strips, key=lambda s: s.channel, reverse=True)

    for strip in sorted_strips:
        filter_name = strip.name.split(',')
        if strip.type == 'TEXT' and strip.name.count(',') > 2:
            
            start_frame = int(strip.frame_start)
            end_frame = start_frame + int(strip.frame_final_duration)
            

            filer_name_one_removed_spaces = filter_name[1].replace(
                " ", "")

            # Sort the strip.names into the right cathegories
            if filter_name[0] == Constants.DUET_LEFT[2]:
                sir_data_DUET_L.append(
                    (start_frame, end_frame, filer_name_one_removed_spaces))

            elif filter_name[0] == Constants.DUET_RIGHT[2]:
                sir_data_DUET_R.append(
                    (start_frame, end_frame, filer_name_one_removed_spaces))

            elif filter_name[0] == Constants.FREE_CHANNEL[2]:
                sir_data_FREE_CHANNEL.append(
                    (start_frame, end_frame, filer_name_one_removed_spaces))

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

    # Combine all lists into a dict that speeds up the csv export
    data = {
        "master_clock": data_master_clock,
        "DUET_L": data_data_DUET_L,
        "DUET_R": data_data_DUET_R,
        "FREE_CHANNEL": data_FREE_CHANNEL
    }

    # Save to csv file
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        for i in range(len(data_master_clock)):
            row = {key: values[i] for key, values in data.items()}
            writer.writerow(row)
    
    if export_duet_risk_report:
        # Get the active scene
        scene = bpy.context.scene

        # Calculate the total number of frames
        total_frames = scene.frame_end - scene.frame_start + 1

        # Calculate the effective frames per second (FPS)
        effective_fps = scene.render.fps / scene.render.fps_base

        # Calculate the duration in seconds
        duration_seconds = total_frames / effective_fps

        # Convert the duration to minutes
        duration_minutes = duration_seconds / 60

        total_minutes_of_work = total_hours_of_workday * 60
        str_list_to_report = []

        multiplication_value = 1

        # Multiplication value:
        if report_method_choosen == 'percentage':
            
            if percentage_of_workday == 100.0:
                multiplication_value = 1
            else:
                # Percentage_value
                multiplication_value = ((100 - percentage_of_workday) / 10)
            
            str_to_report_1 = f"Duration of rating: {duration_minutes:.2f} minutes"
            str_to_report_2 = f"Total minutes of work per day: {(duration_minutes * multiplication_value):.2f} minutes"
            str_to_report_3 = f"The rating represents: {(percentage_of_workday):.2f}% of the total work"
            str_list_to_report.append(str_to_report_1)
            str_list_to_report.append(str_to_report_2)
            str_list_to_report.append(str_to_report_3)


        
        if report_method_choosen == 'actual_time':
            

            # Set the multiplcations value 
            multiplication_value = total_minutes_of_work / duration_minutes 

            str_to_report_1 = f"Duration of rating: {duration_minutes:.2f} minutes"
            str_to_report_2 = f"Total minutes of work per day: {total_minutes_of_work:.2f} minutes"
            str_to_report_3 = f"The rating represents: {(duration_minutes / total_minutes_of_work):.2f}% of the total work"
            str_list_to_report.append(str_to_report_1)
            str_list_to_report.append(str_to_report_2)
            str_list_to_report.append(str_to_report_3)




        
        # Function to get risk counts from a given data list
        damage_per_cycle_weighting = [
            0.00000026,
            0.00000045,
            0.00000137,
            0.00000413,
            0.00001262,
            0.00003801,
            0.00011625,
            0.00035014,
            0.00105374,
            0.00322581,
            0.00970874,
        ]
        def get_risk_counts(data_list):
            # Initializing all values 0-10 with count 0
            counts = {str(i): 0 for i in range(11)}
            for _, _, risk_value in data_list:
                if risk_value in counts:
                    counts[risk_value] += 1
            return counts

        duet_r_counts = get_risk_counts(sir_data_DUET_R)
        duet_l_counts = get_risk_counts(sir_data_DUET_L)

        # new filename
        base_name, ext = os.path.splitext(filepath)
        new_filepath = f"{base_name}_duet_risk_report.csv"

        column_1_svg_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        column_2_svg_data = []
        column_3_svg_data = []
        column_4_svg_data = []
        column_5_svg_data = []

        # Save the risk report to the new csv file
        with open(new_filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')  # Use tab as delimiter
    
            # Write DUET_R section
            writer.writerow(["DUET_R"])
            writer.writerow(["Value", "Count", "Cumulative Damage"])
            

            for i in range(11):
                count_value = int(duet_r_counts[str(i)] * multiplication_value)
                cumulative = format(round(damage_per_cycle_weighting[i] * count_value, 5), ",.5f")
                writer.writerow([str(i), " " + str(count_value), cumulative])

                if duet_options == "OPTION1":  # DUET Right selected
                    column_2_svg_data.append(count_value)
                    column_3_svg_data.append(float(cumulative))
    
            writer.writerow([])  # Empty line for separation

            # Write DUET_L section
            writer.writerow(["DUET_L"])
            writer.writerow(["Value", "Count", "Cumulative Damage"])
            for i in range(11):
                count_value = int(duet_l_counts[str(i)] * multiplication_value)
                cumulative = format(round(damage_per_cycle_weighting[i] * count_value, 5), ",.5f")
                writer.writerow([str(i), " " + str(count_value), cumulative])

                if duet_options == "OPTION2":  # DUET Left selected
                    column_2_svg_data.append(count_value)
                    column_3_svg_data.append(float(cumulative))
    

        # Specify where you want to save the SVG
        svg_filepath = f"{base_name}_duet_risk_report.svg"

        for i in range(11):
            if len(duet_r_counts) > len(duet_l_counts):
                # Create the SVG with text and table
                print("fff")
        duet_report_titel = ""
        if duet_options == "OPTION1":  # DUET Right selected
            duet_report_titel = "DUET Right Hand Scores"
        elif duet_options == "OPTION2":
            duet_report_titel = "DUET Left Hand Scores"
        create_a4_svg_with_text_and_table(svg_filepath, duet_report_titel, column_1_svg_data,
                                          column_2_svg_data, column_3_svg_data, column_3_svg_data, column_3_svg_data, str_list_to_report)
        
        

            
    return {'FINISHED'}


def due_probability(cd):
    """
    Calculate the Probability of Distal Upper Extremity Outcome based on DUET Cumulative Damage using log base 10.

    Parameters:
    - cd (float): DUET Cumulative Damage.

    Returns:
    - float: Probability of DUE outcome.
    """
    # Calculate Y' from the regression equation using log base 10
    y_prime = 0.573 + 0.747 * math.log10(cd)
    
    # Calculate the probability P(Outcome) using Y'
    probability = math.exp(y_prime) / (1 + math.exp(y_prime))

    return probability




class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    export_duet_risk_report: BoolProperty(
        name="Create DUET Report",
        description="Exports a SVG detailing the DUET Risks",
        default=True,
    )

    use_percentage_duet: BoolProperty(
        name="Use percentage as input",
        description="If you choose this method, the number of cycles will be multiplied with the percentage to cover a full workday.",
        default=True,
    )
    percentage_of_workday: FloatProperty(
        name="This work represent percentage / day ", description="How much time does the annotation represent of the full workday?", min=0.0, max=100.0, default=20.0)
    
    use_exact_value_duet: BoolProperty(
        name="Use task duration(hours) as input",
        description="If you choose this method, the number of cycles will first be avaraged per minute, then multipled by the number of hours per day. ",
        default=True,
    )
    
    total_hours_of_workday: FloatProperty(
        name="Total work of this kind h / day", description="How many hours in a work day?", min=0.0, max=16.0, default=5.0)


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

    duet_options_items = [
        ("OPTION1", "DUET Right", "The report will be for right hand"),
        ("OPTION2", "DUET Left", "The report will be for left hand"),
        
    ]


    duet_options: EnumProperty(
        name="HAND",
        description="Choose an option",
        items=duet_options_items,
        default="OPTION1"
    )

    report_methods = ['percentage', 'actual_time']
    report_method_choosen = 'percentage'
    
    def draw(self, context):

        text_lines_use_percentage_duet = [
            'Percentage of workday: How many',
            'percent of the work day did',
            'the annotations reflect?',
            'If you choose this method,',
            'the number of cycles will be ',
            'multiplied, so that the report ',
            'reflects a full work day.'
        ]
        text_lines_use_actual_duet = [
            'When using this method, we calculate', 'the grip counts per minute', 'and multiply this value', 'with the minutes of work performed', 'per day.' 
          
        ]
        layout = self.layout
        layout.prop(self, "export_duet_risk_report")
      
        if self.export_duet_risk_report:
            layout.prop(self, "use_percentage_duet")
            layout.prop(self, "use_exact_value_duet")
            layout.prop(self, "duet_options")
            
            if self.use_percentage_duet:
                self.report_method_choosen = 'percentage'
                self.use_exact_value_duet = False
                layout.prop(self, 'percentage_of_workday')
                for line in text_lines_use_percentage_duet:
                    layout.label(text=line)
            elif self.use_exact_value_duet:
                self.report_method_choosen = 'actual_time'
                self.use_percentage_duet = False
                
                layout.prop(self, 'total_hours_of_workday')
                for line in text_lines_use_actual_duet:
                    layout.label(text=line)
                
                


    def execute(self, context):
        return write_some_data(context, self.filepath, self.export_duet_risk_report, self.report_method_choosen, self.percentage_of_workday, self.total_hours_of_workday, self.duet_options)


# Only needed if you want to add into a dynamic menu
# def menu_func_export(self, context):
#    self.layout.operator(ExportSomeData.bl_idname, text="Text Export Operator")
#
#
# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
# def register():
#    bpy.utils.register_class(ExportSomeData)
#    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
#
#
# def unregister():
#    bpy.utils.unregister_class(ExportSomeData)
#    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
#
#
# if __name__ == "__main__":
#    register()
#
#    # test call
#    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
#
