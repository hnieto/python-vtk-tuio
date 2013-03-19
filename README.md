# Python-VTK with TUIO

![Python-VTK-TUIO](https://dl.dropbox.com/u/25652072/DemoChooser.png)

This project uses the [pyTUIO library](http://code.google.com/p/pytuio/) to obtain multitouch information that is then used to interact with a VTK session. 

## Description

The `Main.py` script will launch the VTK GUI session seen above. This session will act as our Demo launcher. Using one finger will rotate the scene. 
Two fingers will allow the user to select an object with the second finger. Hovering over the main sphere will display four additional spheres. 
Selecting any of these spheres will automatically close the current VTK session and launch a different demo.

Each demo creates an instance of `CursorTracker` located in `MultiTouch.py`. The `CursorTracker` object will maintain a dictionary of each recorded finger/cursor
and it's start, previous, and current positions. Each demo uses this information to create gestures like pinch zooming, rotating, and panning. 


## Sagital Slice Demo

Displays a sagital view of the head. The scene can only be rotated along its x axis. 
**IMPORTANT** 
Make sure to pass the correct path to the `/headsq` directory as an arguement to the `vtkVolume16Reader` method `SetFilePrefix()`.

![MedicalSliceDemo] (https://dl.dropbox.com/u/25652072/MedicalSliceDemo.png)


## Muliple Slices Demo

This example reads a volume dataset, extracts two isosurfaces that represent the skin and bone, creates three orthogonal planes
(sagittal, axial, coronal), and displays them. 
**IMPORTANT**  
Make sure to pass the correct path to the `/headsq` directory as an arguement to the `vtkVolume16Reader` method `SetFilePrefix()`.

![MedicalDemo] (https://dl.dropbox.com/u/25652072/MedicalDemo.png)


## MultiTouch Test Demo

TestDemo.py is a used to verify that TUIO events are being properly received and tracked.
A small number will be used to represent cursors.

![TestDemo] (https://dl.dropbox.com/u/25652072/TestDemo.png)


## Gestures

**Rotate:** 1 finger swipe 
**Zoom In:** 2 finger reverse pinch 
**Zoom Out:** 2 finger pinch 
**Pan:** Requires 3 fingers. 3rd finger position is used to translate image 
**Close Demo:** 4 fingers  


## Requirements

* Python
* VTK
* Python [pyTUIO library](http://code.google.com/p/pytuio/)
