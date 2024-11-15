import bpy 
from . import ea_hand_exertion_hotkey as hand
from . import ea_free_channel_hotkeys as free
from . import ea_PMC_channel_hotkeys as pmc



from .ea_constants import Constants


# TODO: register all that are inside this file in the right place

# HAND_EXERTIONS HOTKEYS and OPERATORS
addon_keymaps_active = []
hand_exertions_hotkey_press_executions = (hand.onPressKeyZERO, hand.onPressKeyONE, hand.onPressKeyTWO, hand.onPressKeyTHREE, hand.onPressKeyFOUR,
                                hand.onPressKeyFIVE, hand.onPressKeySIX, hand.onPressKeySEVEN, hand.onPressKeyEIGHT, hand.onPressKeyNINE, hand.onPressKeyTEN)

hand_exertions_hotkey_release_executions = (hand.onReleaseKeyZERO, hand.onReleaseKeyONE, hand.onReleaseKeyTWO, hand.onReleaseKeyTHREE, hand.onReleaseKeyFOUR,
                                  hand.onReleaseKeyFIVE, hand.onReleaseKeySIX, hand.onReleaseKeySEVEN, hand.onReleaseKeyEIGHT, hand.onReleaseKeyNINE, hand.onReleaseKeyTEN)

hand_exertions_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']

free_channel_press_executions = [free.onPressKeyFreeChannel0, free.onPressKeyFreeChannel1, free.onPressKeyFreeChannel2, free.onPressKeyFreeChannel3,
                                 free.onPressKeyFreeChannel4, free.onPressKeyFreeChannel5, free.onPressKeyFreeChannel6, free.onPressKeyFreeChannel7, 
                                 free.onPressKeyFreeChannel8, free.onPressKeyFreeChannel9]
free_channel_release_executions = [free.onReleaseKeyFreeChannel0, free.onReleaseKeyFreeChannel1, free.onReleaseKeyFreeChannel2, free.onReleaseKeyFreeChannel3, 
                                   free.onReleaseKeyFreeChannel4, free.onReleaseKeyFreeChannel5, free.onReleaseKeyFreeChannel6, free.onReleaseKeyFreeChannel7, 
                                   free.onReleaseKeyFreeChannel8, free.onReleaseKeyFreeChannel9]

free_channel_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                        'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']


pmc_channel_press_executions = [pmc.onPressKeyPostureMoveCode0, pmc.onPressKeyPostureMoveCode1, pmc.onPressKeyPostureMoveCode2, 
                                pmc.onPressKeyPostureMoveCode3, pmc.onPressKeyPostureMoveCode4, pmc.onPressKeyPostureMoveCode5, 
                                pmc.onPressKeyPostureMoveCode6, pmc.onPressKeyPostureMoveCode7, pmc.onPressKeyPostureMoveCode8, 
                                pmc.onPressKeyPostureMoveCode9]
pmc_channel_release_executions = [pmc.onReleaseKeyPostureMoveCode0, pmc.onReleaseKeyPostureMoveCode1, pmc.onReleaseKeyPostureMoveCode2, 
                                  pmc.onReleaseKeyPostureMoveCode3, pmc.onReleaseKeyPostureMoveCode4, pmc.onReleaseKeyPostureMoveCode5, 
                                  pmc.onReleaseKeyPostureMoveCode6, pmc.onReleaseKeyPostureMoveCode7, pmc.onReleaseKeyPostureMoveCode8, 
                                  pmc.onReleaseKeyPostureMoveCode9]

pmc_channel_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                        'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']


#store which operations that have been registered for un-reg in the switch
addon_keymaps_active_operations = []







class inputSwitchClass:

    def input_switch(self, value=str):
        
        if value == Constants.HAND_EX_L[0]: #--------------------------------------------------- Constants.HAND_EX_L[0]:
            
            #set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.HAND_EX_L[0]

            #CLEAR OLD KEYMAPS
            # HOTKEY UNREG
            unreg_executions_index = 0
            for i in addon_keymaps_active_operations:


                bpy.utils.unregister_class(
                    addon_keymaps_active_operations[unreg_executions_index])

                #bpy.utils.unregister_class(
                #    addon_keymaps_active_operations[unreg_executions_index])

                unreg_executions_index += 1
            #clear the active operations    
            addon_keymaps_active_operations.clear()
            # handle the keymap
            for km, kmi in addon_keymaps_active:
                km.keymap_items.remove(kmi)
            addon_keymaps_active.clear()







            # HOTKEY REGISTER

            # handle the keymap
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(
                name='SequencerCommon', space_type='SEQUENCE_EDITOR')

            press_executions_index = 0
            for key in hand_exertions_hotkeys:
            
                bpy.utils.register_class(
                    hand_exertions_hotkey_press_executions[press_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    hand_exertions_hotkey_press_executions[press_executions_index])

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                    addon_keymaps_active.append((km, kmi))
                    

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in hand_exertions_hotkeys:
            
                bpy.utils.register_class(
                    hand_exertions_hotkey_release_executions[release_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    hand_exertions_hotkey_release_executions[release_executions_index])
                

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
                    addon_keymaps_active.append((km, kmi))
                   

                release_executions_index += 1


            # ------------------------------------------------------------------------
            #    EXTRA UI
            # ------------------------------------------------------------------------
            # Change the channel name, but only if it hasnt been done
            #if 'Channel 5' in bpy.context.scene.sequence_editor.channels:
            #    # Get the sequence editor
            #    seq_editor = bpy.context.scene.sequence_editor
            #    # Get the channel to rename and lock
            #    channel_to_rename = seq_editor.channels['Channel 5']
            #    #Rename the channel
            #    channel_to_rename.name = 'ANNOTATION'

        elif value == Constants.HAND_EX_R[0]:  # --------------------------------------------------- Constants.HAND_EX_R[0]:
            
            # set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.HAND_EX_R[0]

            # HOTKEY UNREG
            unreg_executions_index = 0
            for i in addon_keymaps_active_operations:
                
                bpy.utils.unregister_class(
                    addon_keymaps_active_operations[unreg_executions_index])

                #bpy.utils.unregister_class(
                #    addon_keymaps_active_operations[unreg_executions_index])

                unreg_executions_index += 1
            # clear the active operations
            addon_keymaps_active_operations.clear()

            # handle the keymap
            for km, kmi in addon_keymaps_active:
                km.keymap_items.remove(kmi)
            addon_keymaps_active.clear()


            # HOTKEY REGISTER

            # handle the keymap
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(
                name='SequencerCommon', space_type='SEQUENCE_EDITOR')

            press_executions_index = 0
            for key in hand_exertions_hotkeys:

                bpy.utils.register_class(
                    hand_exertions_hotkey_press_executions[press_executions_index])
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    hand_exertions_hotkey_press_executions[press_executions_index])
                
                
                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:

                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                    addon_keymaps_active.append((km, kmi))
                    

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in hand_exertions_hotkeys:

                bpy.utils.register_class(
                    hand_exertions_hotkey_release_executions[release_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    hand_exertions_hotkey_release_executions[release_executions_index])
                

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                    kmi = km.keymap_items.new(
                        hand_exertions_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    

                release_executions_index += 1

            # ------------------------------------------------------------------------
            #    EXTRA UI
            # ------------------------------------------------------------------------
            #Change the channel name, but only if it hasnt been done
            #if 'Channel 6' in bpy.context.scene.sequence_editor.channels:
            #    # Get the sequence editor
            #    seq_editor = bpy.context.scene.sequence_editor
            #    # Get the channel to rename and lock
            #    channel_to_rename = seq_editor.channels['Channel 6']
            #    # Rename the channel
            #    channel_to_rename.name = 'ANNOTATION'





        elif value == Constants.FREE_CHANNEL[0]:  # --------------------------------------------------- Constants.FREE_CHANNEL[0]:
            
            # set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.FREE_CHANNEL[0]

            # HOTKEY UNREG
            unreg_executions_index = 0
            for i in addon_keymaps_active_operations:
                
                bpy.utils.unregister_class(
                    addon_keymaps_active_operations[unreg_executions_index])

                #bpy.utils.unregister_class(
                #    addon_keymaps_active_operations[unreg_executions_index])

                unreg_executions_index += 1
            # clear the active operations
            addon_keymaps_active_operations.clear()

            # handle the keymap
            for km, kmi in addon_keymaps_active:
                km.keymap_items.remove(kmi)
            addon_keymaps_active.clear()


            # HOTKEY REGISTER

            # handle the keymap
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(
                name='SequencerCommon', space_type='SEQUENCE_EDITOR')

            press_executions_index = 0
            for key in free_channel_hotkeys:

                bpy.utils.register_class(
                    free_channel_press_executions[press_executions_index])
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    free_channel_press_executions[press_executions_index])

                
                kmi = km.keymap_items.new(
                    free_channel_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                addon_keymaps_active.append((km, kmi))

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in free_channel_hotkeys:

                bpy.utils.register_class(
                    free_channel_release_executions[release_executions_index])

                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    free_channel_release_executions[release_executions_index])

               
                kmi = km.keymap_items.new(
                    free_channel_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
                addon_keymaps_active.append((km, kmi))

                release_executions_index += 1
                
                

            # ------------------------------------------------------------------------
            #    EXTRA UI
            # ------------------------------------------------------------------------
            # Change the channel name, but only if it hasnt been done
            #if 'Channel 7' in bpy.context.scene.sequence_editor.channels:
            #    # Get the sequence editor
            #    seq_editor = bpy.context.scene.sequence_editor
            #    # Get the channel to rename and lock
            #    channel_to_rename = seq_editor.channels['Channel 7']
            #    # Rename the channel
            #    channel_to_rename.name = 'ANNOTATION'
        #
        #POSTURE MOVEMENT CODE
        elif value == Constants.POST_MOVE_CODE[0]:  # --------------------------------------------------- Constants.POST_MOVE_CODE[0]:
                    #Register the timer for guide button-updates

            # set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.POST_MOVE_CODE[0]

            # HOTKEY UNREG
            unreg_executions_index = 0
            for i in addon_keymaps_active_operations:
                
                bpy.utils.unregister_class(
                    addon_keymaps_active_operations[unreg_executions_index])

                #bpy.utils.unregister_class(
                #    addon_keymaps_active_operations[unreg_executions_index])

                unreg_executions_index += 1
            # clear the active operations
            addon_keymaps_active_operations.clear()

            # handle the keymap
            for km, kmi in addon_keymaps_active:
                km.keymap_items.remove(kmi)
            addon_keymaps_active.clear()


            # HOTKEY REGISTER

            # handle the keymap
            wm = bpy.context.window_manager
            km = wm.keyconfigs.addon.keymaps.new(
                name='SequencerCommon', space_type='SEQUENCE_EDITOR')

            press_executions_index = 0
            for key in pmc_channel_hotkeys:

                bpy.utils.register_class(
                    pmc_channel_press_executions[press_executions_index])
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    pmc_channel_press_executions[press_executions_index])

                
                kmi = km.keymap_items.new(
                    pmc_channel_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                addon_keymaps_active.append((km, kmi))

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in pmc_channel_hotkeys:

                bpy.utils.register_class(
                    pmc_channel_release_executions[release_executions_index])

                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    pmc_channel_release_executions[release_executions_index])

               
                kmi = km.keymap_items.new(
                    pmc_channel_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
                addon_keymaps_active.append((km, kmi))

                release_executions_index += 1








        elif value == "3":  # --------------------------------------------------- other
            print("Value is 3")
        else:
            print("Remove all hotkeys")

            # HOTKEY UNREG
            unreg_executions_index = 0
            for i in addon_keymaps_active_operations:
               
                bpy.utils.unregister_class(
                    addon_keymaps_active_operations[unreg_executions_index])

                # bpy.utils.unregister_class(
                #    addon_keymaps_active_operations[unreg_executions_index])

                unreg_executions_index += 1
            # clear the active operations
            addon_keymaps_active_operations.clear()

            # handle the keymap
            for km, kmi in addon_keymaps_active:
                km.keymap_items.remove(kmi)
            addon_keymaps_active.clear()
    
    
    
