class Constants:

    #INPUT TYPES, id:, channel:
    DUET_LEFT = (1, 4, "DUET LEFT")
    DUET_RIGHT = (2, 5, "DUET RIGHT")
    FREE_CHANNEL = (3, 6, "FC")

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
