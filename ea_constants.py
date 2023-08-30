import bpy
class Constants:

    #INPUT TYPES, id:, channel:
    DUET_LEFT = (1, 5, "DUET LEFT")
    DUET_RIGHT = (2, 6, "DUET RIGHT")
    FREE_CHANNEL = (3, 7, "FC")
    
    IMPORT_ACTIPASS = (1, "ActiPass")
    IMPORT_EMG = (2, "EMG")
    IMPORT_EMG_RAINFLOW = (3, "EMG_RAINFLOW")

    POSTURE = (3, 6, "POSTURE")
    EXPORT_TYPES = ["MASTER CLOCK", "DUET LEFT", "DUET RIGHT", "FREE CHANNEL"]
    OMNI_RES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 

    #str_OMNI_RES name, label, value  
    str_OMNI_RES = [('OMNI_RES_0', 'OMNI-RES 0', '0'),
                     ('OMNI_RES_1', 'OMNI-RES 1', '1'),
                     ('OMNI_RES_2', 'OMNI-RES 2', '2'),
                     ('OMNI_RES_3', 'OMNI-RES 3', '3'),
                     ('OMNI_RES_4', 'OMNI-RES 4', '4'),
                     ('OMNI_RES_5', 'OMNI-RES 5', '5'),
                     ('OMNI_RES_6', 'OMNI-RES 6', '6'),
                     ('OMNI_RES_7', 'OMNI-RES 7', '7'),
                     ('OMNI_RES_8', 'OMNI-RES 8', '8'),
                     ('OMNI_RES_9', 'OMNI-RES 9', '9'),
                     ('OMNI_RES_10', 'OMNI-RES 10', '10')]


    str_CALIBRATIONS = [('calibration_shake_IMU', 'Shake IMU', 'Shake IMU'),
                        ('calibration_start_video', 'Start Video', 'Start Video'),
                        ('calibration_start_EMG', 'Start EMG', 'Start EMG'),
                        ('calibration_SyncPoint', 'SyncPoint', 'SyncPoint'),
                        ('calibration_wave_arms_3_times', 'Wave arms 3 times', 'Wave arms 3 times'),
                        ('calibration_R_Fle_Ext', 'R Fle-Ext', 'R Fle-Ext'),
                        ('calibration_0deg_reference', '0deg reference', '0deg reference'),
                        ('calibration_Ipose', 'Ipose', 'Ipose'),
                        ('calibration_neck_back_flexion', 'Neck-back flexion', 'Neck-back flexion'),
                        ('calibration_Rarm_neutral', 'Rarm neutral', 'Rarm neutral'),
                        ('calibration_Larm_neutral', 'Larm neutral', 'Larm neutral'),
                        ('calibration_Tpose', 'Tpose', 'Tpose'),
                        ('calibration_arms_forward_90deg', 'Arms forward 90deg', 'Arms forward 90deg'),
                        ('calibration_EMG_cali_rest', 'EMG cali rest', 'EMG cali rest'),
                        ('calibration_EMG_cali_Trap', 'EMG cali Trap', 'EMG cali Trap'),
                        ('calibration_EMG_cali_Deltoid', 'EMG cali Deltoid', 'EMG cali Deltoid'),
                        ('calibration_EMG_cali_Forearm', 'EMG cali Forearm', 'EMG cali Forearm')]
    
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


def pickTagColorForDuet(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    color_array = ["COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04", "COLOR_06"]

    if 0 <= int_key <= 2:
        return color_array[3]  # green
    elif 3 <= int_key <= 4:
        return color_array[2]  # yellow
    elif 5 <= int_key <= 6:
        return color_array[1]  # orange
    elif 7 <= int_key <= 8:
        return color_array[0]  # red
    elif 9 <= int_key <= 10:
        return color_array[4]  # purple

    else:
        return color_array[3]  # green


def pickTagColorForFreeMode(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    color_array = ["COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04", "COLOR_05", "COLOR_06", "COLOR_07", "COLOR_08", "COLOR_09"]

    if int_key == 0:
        return color_array[0]  
    elif int_key == 1:
        return color_array[1]  
    elif int_key == 2:
        return color_array[2]
    elif int_key == 3:
        return color_array[3]
    elif int_key == 4:
        return color_array[4]
    elif int_key == 5:
        return color_array[5]
    elif int_key == 6:
        return color_array[6]
    elif int_key == 7:
        return color_array[7]
    elif int_key == 8:
        return color_array[8]
    elif int_key == 9:
        return color_array[3]

    else:
        return color_array[3]  # green


def pickVisualTextColorForDuet(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    color_array = ["COLOR_01", "COLOR_02", "COLOR_03", "COLOR_04", "COLOR_06"]

    if 0 <= int_key <= 2:
        return (0.48, 0.80, 0.48, 1.00)  # green
    elif 3 <= int_key <= 4:
        return (0.95, 0.86, 0.33, 1.00)  # yellow
    elif 5 <= int_key <= 6:
        return (0.95, 0.64, 0.33, 1.00)  # orange
    elif 7 <= int_key <= 8:
        return (0.89, 0.38, 0.36, 1.00)  # red
    elif 9 <= int_key <= 10:
        return (0.55, 0.35, 0.85, 1.00)  # purple

    else:
        return (0.48, 0.80, 0.48, 1.00)  # green
    

def pickVisualTextColorForFreeMode(key):

    # ColorTag for num hotkeys
    int_key = int(key)

    if int_key == 0:
        return (0.88, 0.38, 0.36, 1.00)  # red
    elif int_key == 1:
        return (0.94, 0.64, 0.33, 1.00)  # orange
    elif int_key == 2:
        return (0.94, 0.86, 0.33, 1.00)  # yellow
    elif int_key == 3:
        return (0.48, 0.80, 0.48, 1.00)  # green
    elif int_key == 4:
        return (0.36, 0.71, 0.91, 1.00)  # blue
    elif int_key == 5:
        return (0.55, 0.35, 0.85, 1.00)  # purple
    elif int_key == 6:
        return (0.77, 0.45, 0.72, 1.00)  # pink
    elif int_key == 7:
        return (0.47, 0.33, 0.25, 1.00)  # brown
    elif int_key == 8:
        return (0.37, 0.37, 0.37, 1.00)  # gray
    elif int_key == 9:
        return (0.48, 0.80, 0.48, 1.00)   # green

    else:
        return (0.48, 0.80, 0.48, 1.00)  # green




def frame_from_smpte(smpte_timecode: str, fps=None, fps_base=None) -> int:

    if fps == None or fps_base == None:
        # Use current scene fps if fps and fps_base are not provided
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base

    # Split the timecode into its components
    timecode_parts = smpte_timecode.split(':')
    hours = int(timecode_parts[0])
    minutes = int(timecode_parts[1])
    seconds = int(timecode_parts[2])
    frames = int(timecode_parts[3])

    #print("FPS_REAL")
    #print(fps_real)

    hours_seconds_frames = ((hours * 60) * 60) * fps_real
    minutes_seconds_frames = (minutes * 60) * fps_real
    seconds_frames = seconds * fps_real
    frames_frames = frames

    # Calculate the total number of frames
    total_frames = (hours_seconds_frames +
                    minutes_seconds_frames + seconds_frames + frames)

    # print(hours_seconds_frames, minutes_seconds_frames,
    #      seconds_frames, frames_frames)
    return total_frames


def get_slot_value(context, index):
    addon_prefs = context.preferences.addons[__package__].preferences
    free_channel_vars = addon_prefs.free_channel_vars
    # Access the slot using the provided index
    slot_key = f"slot_{index}"
    slot_value = getattr(free_channel_vars, slot_key)
    return str(slot_value)
