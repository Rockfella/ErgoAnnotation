import bpy
class Constants:

    #INPUT TYPES, id:, channel:
    HAND_EX_R = (1, 5, "HAND EXERTION R")
    HAND_EX_L = (2, 6, "HAND EXERTION L")
    FREE_CHANNEL = (3, 7, "FC")
    POST_MOVE_CODE = (4, 7, "PMC")
    
    IMPORT_ACTIPASS = (1, "ActiPass")
    IMPORT_EMG = (2, "EMG")
    IMPORT_EMG_RAINFLOW = (3, "EMG_RAINFLOW")
    IMPORT_ACC = (4, "ACC")

    POSTURE = (3, 6, "POSTURE")
    EXPORT_TYPES = ["MASTER CLOCK", "DUET LEFT", "DUET RIGHT", "FREE CHANNEL"]
    OMNI_RES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 

    POSTURES_INPUT = {
    "Lying": {
        "description": "Individual lying prone, supine or on the right/left side. Knees can be flexed or extended.",
        "hotkey": 1,
        "id": 10,
        "options": {
            "Lying supine": {"description": "Individual lying supine on any surface, knees and hips and can be flexed or extended.", "id": 101},
            "Lying side": {"description": "Individual lying on right or left side. Must truly be on side otherwise classify as prone or supine.", "id": 102},
            "Lying prone": {"description": "Individual lying prone on any surface, knees can be flexed or extended.", "id": 103}
        }
    },
    "Sitting": {
        "description": "Individual sitting on any surface (floor, couch, beanbag, chair, stool, swivel chair) with any leg posture (including “W sitting”, cross legged sitting, legs out straight etc).",
        "hotkey": 2,
        "id": 20,
        "options": {
            "Low kneeling": {"description": "Individual sitting on knees with bottom on heels.", "id": 201},
            "High kneeling": {"description": "Individual on knees with bottom off heels.", "id": 202},
            "Half kneeling": {"description": "Individual on one knee with other foot on floor, bottom off heels.", "id": 203}
        }
    },
    "Standing still": {
        "description": "Individual standing still with legs completely stationary, to be classified as standing the child must not be taking small steps and stay on the same spot for at least 2 seconds.",
        "hotkey": 3,
        "id": 30,
        "options": {}
    },
    "Moving": {
        "description": "Focusing on the right thigh (i.e. where the accelerometer is placed), the child is standing while fidgeting with legs or talking tiny steps on the same spot. The child should have a weight transfer between legs.",
        "hotkey": 4,
        "id": 40,
        "options": {
        }
    },
    "Walking": {
        "description": "Individual walking at any speed, to be classified as walking there needed to be a full gait cycle present (i.e. 2 steps).",
        "hotkey": 5,
        "id": 50,
        "options": {
        }
    },
    "Running": {
        "description": "Individual running at any speed.",
        "hotkey": 6,
        "id": 60,
        "options": {
        }
    },
    "Stair climbing": {
        "description": "Individual walks or runs upstairs or downstairs.",
        "hotkey": 7,
        "id": 70,
        "options": {
            "Walking upstairs": {"description": "Walking upstairs", "id": 701},
            "Walking downstairs": {"description": "Individual walks downstairs.", "id": 702},
            "Running upstairs": {"description": "Individual runs upstairs.", "id": 703},
            "Running downstairs": {"description": "Individual runs downstairs.", "id": 704}
        }
    },
    "Cycling": {
        "description": "Individual is cycling on a pedal-cycle.",
        "hotkey": 8,
        "id": 80,
        "options": {}
    },
    "Other": {
        "description": "Any movement that is not captured above. Coder will specify what the child is doing and why it cannot be considered as any of the above listed postures/movements.",
        "hotkey": 9,
        "id": 90,
        "options": {
            "Transition": {"description": "Includes all transitional movements including sit to stand, stand to sit, lie to stand, stand to lie, rolling over. Transition needs to be at least 2 seconds. If less than that then same as previous posture and movement (i.e. the middle of the previous second).", "id": 901},
            "Skipping": {"description": "Child skipping or variations of skipping due to differences in motor development (e.g. some younger children when instructed to skip used a galloping action).", "id": 901},
            "Jumping": {"description": "Individual jumps continuously either on the spot or travelling forwards or jumps off an object (e.g. jumps off stairs).", "id": 902},
            "Climbing": {"description": "Individual is climbing something, e.g. a tree or on a Monkeybar.", "id": 903},
            "Handstand": {"description": "Individual attempts a handstand. Dependent upon proficiency and motor development this may be placing their hands on the ground and kicking feet off ground or may be a sustained handstand.", "id": 904},
            "Cartwheel": {"description": "Individual attempts a cartwheel. As for handstand this may be placing hands on ground and kicking feet off one at a time.", "id": 905},
            "Throwing and catching ball": {"description": "Individual throwing or catching a ball.", "id": 906},
            "All fours": {"description": "Includes crawling, bear walking.", "id": 907}
        }
    },
        "None": {
        "description": "No input set for this hotkey.",
        "hotkey": 0,
        "id": 99,
        "options": {
            "Unsure": {"description": "The coder is uncertain of what to code.", "id": 991},
            "Uncodable": {"description": "The Individual is outside of the view of the video recording or could not be confidently annotated due to image quality.", "id": 992}
        }
    },
       
}





    #str_OMNI_RES name, label, value  
    str_MAGNITUDE = [('MAGNITUDE_0', 'MAGNITUDE 0', '0'),
                     ('MAGNITUDE_1', 'MAGNITUDE 1', '1'),
                     ('MAGNITUDE_2', 'MAGNITUDE 2', '2'),
                     ('MAGNITUDE_3', 'MAGNITUDE 3', '3'),
                     ('MAGNITUDE_4', 'MAGNITUDE 4', '4'),
                     ('MAGNITUDE_5', 'MAGNITUDE 5', '5'),
                     ('MAGNITUDE_6', 'MAGNITUDE 6', '6'),
                     ('MAGNITUDE_7', 'MAGNITUDE 7', '7'),
                     ('MAGNITUDE_8', 'MAGNITUDE 8', '8'),
                     ('MAGNITUDE_9', 'MAGNITUDE 9', '9'),
                     ('MAGNITUDE_10', 'MAGNITUDE 10', '10')]


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


def pickTagColorForHandExertions(key):

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


def pickVisualTextColorForHandExertions(key):

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


    hours_seconds_frames = ((hours * 60) * 60) * fps_real
    minutes_seconds_frames = (minutes * 60) * fps_real
    seconds_frames = seconds * fps_real

    # Calculate the total number of frames
    total_frames = (hours_seconds_frames +
                    minutes_seconds_frames + seconds_frames + frames)

    # print(hours_seconds_frames, minutes_seconds_frames,
    #      seconds_frames, frames_frames)
    return total_frames

def frame_from_smpte_for_importer(smpte_timecode: str, fps=None, fps_base=None) -> int:

    if fps == None or fps_base == None:
        # Use current scene fps if fps and fps_base are not provided
        fps = bpy.context.scene.render.fps
        fps_base = bpy.context.scene.render.fps_base
        fps_real = fps / fps_base
        
    def has_decimal(value):
        return '.' in value
    # Split the timecode into its components
    timecode_parts = smpte_timecode.split(':')
    hours = int(timecode_parts[0])
    minutes = int(timecode_parts[1])
    seconds = int(timecode_parts[2])
    if has_decimal(timecode_parts[3]):
        frames = float(timecode_parts[3])
    else:
        frames = int(timecode_parts[3])
    print("frames", frames)
    #print("FPS_REAL")
    #print(fps_real)

    hours_seconds_frames = ((hours * 60) * 60) * fps_real
    minutes_seconds_frames = (minutes * 60) * fps_real
    seconds_frames = seconds * fps_real

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



def get_pmc_id(hotkey):
    
    return_str = -1
    for category, details in Constants.POSTURES_INPUT.items():
        
        if int(details['hotkey']) == int(hotkey):
            
            return_str = details['id']
        
    
    return return_str

def get_pmc_value(hotkey):
    #print("Hotkey request:", hotkey)
    return_str = "None"
    for category, details in Constants.POSTURES_INPUT.items():
        
        if int(details['hotkey']) == int(hotkey):
            #print("details['hotkey']", details['hotkey'])
            #print(category)
            return_str = str(category)
        
    
    return return_str


def get_pmc_description(hotkey):
    #print("Hotkey request:", hotkey)
    return_str = "None"
    for category, details in Constants.POSTURES_INPUT.items():
        
        if int(details['hotkey']) == int(hotkey):
            #print("details['hotkey']", details['hotkey'])
            #print(category)
            return_str = str(details['description'])
        
    
    return return_str

def get_pmc_options(id_request):

    return_list = []
    for category, details in Constants.POSTURES_INPUT.items():
        
        if details['id'] == id_request:
            
            return_list.append(details['options'])
            return_list.append(details['id'])
        else:
            category_id = find_category_id_for_option_id(id_request)
            
            if category_id == details['id']:
            
                return_list.append(details['options'])
                return_list.append(details['id'])

    
    
    return return_list
    
def find_category_id_for_option_id(option_id):
    for category, details in Constants.POSTURES_INPUT.items():
        for option, option_details in details['options'].items():
            if int(option_details['id']) == option_id:
                return int(details['id'])
    return None
