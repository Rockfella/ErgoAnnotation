# ErgoAnnotation
ErgoAnnotation is a tool meant to increase the speed and precision in which video annotations can be produced. The annotations can be used for risk assessments and machine learning or other purposes.  

In addition, there are a few import functions:
1. ActiPass import, enables the user to visualise the ActiPass data and can overlay video. 
2. EMG-data import and synchronization 


Dive into our documentation, try out the software, and enjoy this free tool.

![](https://github.com/Rockfella/rockfella_public/blob/main/annotate_example.gif)

---

## Table of Contents

1. [Installation](#Installation)
2. [How to use](#How-to-use)
3. [Import](#Import)
4. [Handle issues](#Handle-issues)
5. [Future pipeline](#Future-pipeline)
6. [License](#License)


---

## Installation

Requirements
Blender: This addon is designed for Blender version 3.5.1. Make sure to have this version or newer installed.



### Blender


[Download blender from official site](https://www.blender.org/download/)



### ErgoAnnotation - Blender Addon

[Download ergoannotation.zip](https://github.com/Rockfella/ErgoAnnotation/blob/master/latest/ergoannotation.zip)

Install Addon in Blender: 
Blender -> Edit -> Preferences -> Add-ons -> Install -> Find zip file [ergoannotation.zip](https://github.com/Rockfella/ErgoAnnotation/blob/master/latest/ergoannotation.zip). Check enable (the left check box) in the addons panel.

![](https://github.com/Rockfella/rockfella_public/blob/main/install_addon.png)
Under Video Sequencer - New File - Video Editing -> Sequencer toggle "n" panel, see ErgoAnnotation tab
## Start Configuration
We have created a start-up file which is included in this repo. [start_up_file.blend](https://github.com/Rockfella/ErgoAnnotation/blob/master/start_up_file.blend), if you would like to use 
the best "standard" configuration for working with videos in blender open the file. Press: File -> Defaults -> 
Save Startup File. This way the configuration will remain throughout different projects.

![](https://github.com/Rockfella/rockfella_public/blob/main/start_up_file.png)

---

## How to use

### Start a new project
In the welcome window of Blender, select New -> Video Editing. Or File -> New -> Video Editing, this takes you to the video sequencer where most of the work is done.



### Add your videos
Add your videos using the sequencer window Add -> Movie, this way we ensure that the relative file paths are kept. 

![](https://github.com/Rockfella/rockfella_public/blob/main/add_movie.gif)

### Set preview range
Like any video software, you have to specify when the project time should start and end. In Blender its called "range". To set the projects range to the newly imported video strip, you can either do: Click on the video strip, View -> Range -> Set Frame Range to Strips OR right click the video and press "Set Range to Strip"


![](https://github.com/Rockfella/rockfella_public/blob/main/set_range.gif)

### Find the panel
The ErgoAnnotation panel can be found in the sequencer window. If its not visible, you can toggle the panels visibility using the Hotkey "N". 

![](https://github.com/Rockfella/rockfella_public/blob/main/toggle_panel.gif)

### Set Master Time

Adding a "master time" strip will enable the synchronization between video and the annotations and is used when exporting data. In the video, find the frame where the master time is visible and the exact frame where "seconds" indicator is changing. Input that time, in the "master time" input field. HH:MM:SS:FF where FF is frames. If the right frame has been selected where a second has just changed, set "FF (frames)" to :00. Press "Add time layer". Make sure that the time is synched with the video master time. 

![](https://github.com/Rockfella/rockfella_public/blob/main/master_time_colors.gif)

### Start Annotate
Select the input type, DUET RIGHT / LEFT or FREE CHANNEL. Both DUET channels are OMNI-RES meant to be used for the Distal Upper Extremity Tool (DUET). If you would like to add your own annotations add them to the free channel list. The Hotkeys for all channels are NUM 1-9 & NUM 1 + CTRL = 10. Use arrow left / right to seek in slow-motion, arrow up / down for faster seek.

Hotkey "X" is delete in Blender. If you wish to change the input you can right click the strip, Ergoannotation -> change the value. 

![](https://github.com/Rockfella/rockfella_public/blob/main/annotate_example.gif)


### Importing and arranging multiple video recording 
If you wish to import multiple video files, lets say multiple cameras have been used. Follow these instructions:
After you have set the master time layer to one of the videos, this layer can be used to guide a second video. 
First, if you wish to see both clips simultaneously select both clips. In the preview window press Hotkey "s" to 
scale them down. Then select one at the time and move them on the x-axis by pressing Hotkey "G", then "X" to move 
on that axis. When they are aligned in the preview window. Select the newly added video clip and it's 
associated sound clip, right click and "Make Meta Strip".

After that find the added videos master clock in the preview window, select that meta strip press Hotkey "M" 
to set the start position, if you now move the cursor to the ErgoAnnotation panel there should be a "Move Button" 
added. Write down the time displayed in the new video or move the timeline to the second position. Then press "Move"

### Export Annotations to CSV
When the annotations are complete, the annotations can be exported to .csv for further analysis. 

## Import
### ActiPass
Before importing data, it´s required to save the .blend file first. This is important as the Actipass imports use the file folder to find potential icons you can download the icons from this repo: [ActiPass Icons](https://github.com/Rockfella/ErgoAnnotation/blob/master/ActiPassIcons.zip)

Extract the file and place them in the same folder as the .blend file, that way the Icons will be imported to the timeline instead of text. 
Example .csv import file structure:
![](https://github.com/Rockfella/rockfella_public/blob/main/import_example.png)
### EMG-Data import. 
As of now, in the .csv file column 1 should be dateTime. Column 2 is where we import emg data. Additional EMG channels are being worked on. 

## Handle Issues
### Video footage lost frames
Some video recordings might have lost frames, this is a known issue as cameras can have a fluctuating recording-FPS. 
In order to deal with this issue, we have created the stretch and shrink function. This issue is mostly noticed when a master time has been recorded in the footage, before and after. Usually its just a couple of frames missing. Using the recorded master time from the footage, we can however compensate for the loss of frames. After adding a master time layer, using to the first video master time. Look for the second master time, find a second’s switch (when time changes its seconds) in the footage and correct the strip by selecting the movie strip, and noting down the Adapted time. (What the time in the footage should be according to the time layer.)  


![](https://github.com/Rockfella/rockfella_public/blob/main/stretch_shrink.gif)


### .MTS video format
Avoid using MTS format, as seeking (dragging timeline and other jumps in frames) is known to be produce lag with this format.

To convert MTS to MP4 use the simple tool:
https://ffmpeg.org/download.html

When installed, in the same folder as the clip is:
1. Open command promt
2. type "cd c:/your_video_folder"
3. Use the following command to convert .mts to .mp4 “ffmpeg -i your_MTS_Clip_Name.mts -c:v copy -c:a aac -strict experimental -b:a 128k your_New_Output_Name.mp4”

### Video Preview is lagging
In the Video Preview window toggle Hotkey "N" choose tab View and change the proxy render to a lower value

![](https://github.com/Rockfella/rockfella_public/blob/main/view_proxy.png)

---
## Future pipeline
1. Custom .csv import, where the end-user can adjust import configurations.


## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.