import bpy 


from .ea_duet_hotkey import onPressKeyZERO, onPressKeyONE, onPressKeyTWO, onPressKeyTHREE, onPressKeyFOUR, onPressKeyFIVE, onPressKeySIX, onPressKeySEVEN, onPressKeyEIGHT, onPressKeyNINE, onPressKeyTEN
from .ea_duet_hotkey import onReleaseKeyZERO, onReleaseKeyONE, onReleaseKeyTWO, onReleaseKeyTHREE, onReleaseKeyFOUR, onReleaseKeyFIVE, onReleaseKeySIX, onReleaseKeySEVEN, onReleaseKeyEIGHT, onReleaseKeyNINE, onReleaseKeyTEN
from .ea_free_channel_hotkeys import onPressKeyFreeChannel0, onPressKeyFreeChannel1, onPressKeyFreeChannel2, onPressKeyFreeChannel3, onPressKeyFreeChannel4, onPressKeyFreeChannel5, onPressKeyFreeChannel6, onPressKeyFreeChannel7, onPressKeyFreeChannel8, onPressKeyFreeChannel9
from .ea_free_channel_hotkeys import onReleaseKeyFreeChannel0, onReleaseKeyFreeChannel1, onReleaseKeyFreeChannel2, onReleaseKeyFreeChannel3, onReleaseKeyFreeChannel4, onReleaseKeyFreeChannel5, onReleaseKeyFreeChannel6, onReleaseKeyFreeChannel7, onReleaseKeyFreeChannel8, onReleaseKeyFreeChannel9


from .ea_constants import Constants

# TODO: register all that are inside this file in the right place

# DUET HOTKEYS and OPERATORS
addon_keymaps_active = []
duet_hotkey_press_executions = (onPressKeyZERO, onPressKeyONE, onPressKeyTWO, onPressKeyTHREE, onPressKeyFOUR,
                                onPressKeyFIVE, onPressKeySIX, onPressKeySEVEN, onPressKeyEIGHT, onPressKeyNINE, onPressKeyTEN)

duet_hotkey_release_executions = (onReleaseKeyZERO, onReleaseKeyONE, onReleaseKeyTWO, onReleaseKeyTHREE, onReleaseKeyFOUR,
                                  onReleaseKeyFIVE, onReleaseKeySIX, onReleaseKeySEVEN, onReleaseKeyEIGHT, onReleaseKeyNINE, onReleaseKeyTEN)

duet_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']

free_channel_press_executions = [onPressKeyFreeChannel0, onPressKeyFreeChannel1, onPressKeyFreeChannel2, onPressKeyFreeChannel3,
                                 onPressKeyFreeChannel4, onPressKeyFreeChannel5, onPressKeyFreeChannel6, onPressKeyFreeChannel7, onPressKeyFreeChannel8, onPressKeyFreeChannel9]
free_channel_release_executions = [onReleaseKeyFreeChannel0, onReleaseKeyFreeChannel1, onReleaseKeyFreeChannel2, onReleaseKeyFreeChannel3, onReleaseKeyFreeChannel4, onReleaseKeyFreeChannel5, onReleaseKeyFreeChannel6, onReleaseKeyFreeChannel7, onReleaseKeyFreeChannel8, onReleaseKeyFreeChannel9]

free_channel_hotkeys = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
                        'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE']



#store which operations that have been registered for un-reg in the switch
addon_keymaps_active_operations = []







class inputSwitchClass:

    def input_switch(self, value=str):
        
        if value == Constants.DUET_LEFT[0]: #--------------------------------------------------- Constants.DUET_LEFT[0]:
            
            #set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.DUET_LEFT[0]

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
            for key in duet_hotkeys:
            
                bpy.utils.register_class(
                    duet_hotkey_press_executions[press_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    duet_hotkey_press_executions[press_executions_index])

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        duet_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                
                    kmi = km.keymap_items.new(
                        duet_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                    addon_keymaps_active.append((km, kmi))
                    

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in duet_hotkeys:
            
                bpy.utils.register_class(
                    duet_hotkey_release_executions[release_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    duet_hotkey_release_executions[release_executions_index])
                

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        duet_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                    kmi = km.keymap_items.new(
                        duet_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
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

        elif value == Constants.DUET_RIGHT[0]:  # --------------------------------------------------- Constants.DUET_RIGHT[0]:
            
            # set active input
            bpy.data.scenes[bpy.context.scene.name].active_input = Constants.DUET_RIGHT[0]

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
            for key in duet_hotkeys:

                bpy.utils.register_class(
                    duet_hotkey_press_executions[press_executions_index])
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    duet_hotkey_press_executions[press_executions_index])
                
                
                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        duet_hotkey_press_executions[press_executions_index].bl_idname, 'ONE', 'PRESS', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:

                    kmi = km.keymap_items.new(
                        duet_hotkey_press_executions[press_executions_index].bl_idname, key, 'PRESS', ctrl=False, shift=False)

                    addon_keymaps_active.append((km, kmi))
                    

                press_executions_index += 1

            # handle the keymap

            release_executions_index = 0
            for key in duet_hotkeys:

                bpy.utils.register_class(
                    duet_hotkey_release_executions[release_executions_index])
                
                # store the operations for later un-reg
                addon_keymaps_active_operations.append(
                    duet_hotkey_release_executions[release_executions_index])
                

                # To reach the full scale of OMNI-RES 0-10, ctrl + 1 = 10
                if key == 'TEN':
                    kmi = km.keymap_items.new(
                        duet_hotkey_release_executions[release_executions_index].bl_idname, 'ONE', 'RELEASE', ctrl=True, shift=False)
                    addon_keymaps_active.append((km, kmi))
                    
                else:
                    kmi = km.keymap_items.new(
                        duet_hotkey_release_executions[release_executions_index].bl_idname, key, 'RELEASE', ctrl=False, shift=False)
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
