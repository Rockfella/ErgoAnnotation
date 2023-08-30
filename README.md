# ErgoAnnotation

Ergoannotation is..

---

## Table of Contents

1. [Installation](#Installation)
2. [How to use](#How-to-use)
3. [Concluding Remarks](#Concluding-Remarks)
4. [License](#License)


---

## Installation

Requirements
Blender: This addon is designed for Blender version 3.5.1. Make sure to have this version or newer installed.



### Blender


[Download blender from official site](https://www.blender.org/download/)



### ErgoAnnotation - Blender Addon
Install Addon in blender: 
Blender -> Edit -> Preferences -> Add-ons -> Install -> Find zip file and enable (the left check box)
Under Video Sequencer - New File - Video Editing -> Sequencer toggle "n" panel, see ErgoAnnotation tab

## Start Configuration
We have created a start-up file which is included in this repo. "start_up_file.blend", if you would like to use 
the best "standard" configuration for working with videos in blender open the file. Press: File -> Defaults -> 
Save Startup File. This way the configuration will remain throughout different projects.

![](https://github.com/Rockfella/rockfella_public/blob/main/start_up_file.gif)



---

## How to use

### Start a new project
In the welcome window of Blender, select New -> Video Editing. Or File -> New -> Video Editing, this takes you to the video sequencer where most of the work is done.
input 00:00:00:00, HH:MM:SS:FF where FF is frames.
### Find the panel
The ErgoAnnotation panel can be found in the sequencer window. If its not visible, you can toggle the panels visability using the Hotkey "N". 

![](https://github.com/Rockfella/rockfella_public/blob/main/toggle_panel.gif)

### Add your videos
Add your videos using the sequencer window Add -> Movie, this way we ensure that the relative file paths are kept. 

![](https://github.com/Rockfella/rockfella_public/blob/main/add_movie.gif)

### Set preview range
Like any video software, you have to specify when the project time should start and end. In Blender its called "range". To set the projects range to the newly imported video strip, you can either do: Click on the video strip, View -> Range -> Set Frame Range to Strips or right click the video and press "Set Range to Strip"


![](https://github.com/Rockfella/rockfella_public/blob/main/set_range.gif)

### Set Master Clock

After that, set the master clock.

[See how](https://i.imgur.com/EtameVt.gif)






---

## Concluding Remarks



---

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.