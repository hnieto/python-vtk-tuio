from vtk import *
from DemoChooser import DemoChooser
from MultipleSlices import MultipleSlices
from SingleSlice import SingleSlice
from MultiTouchTest import MultiTouchTest

if __name__ == '__main__':
    gui = DemoChooser()
    gui.Start()
    nextDemo = gui.GetPickedDemo()
    gui.Kill()
        
    try:
        while True:
            
            if nextDemo == 0:
                gui = DemoChooser()
                gui.Start()
                nextDemo = gui.GetPickedDemo()
                gui.Kill()
                
            elif nextDemo == 1:
                singleSlice = SingleSlice()
                singleSlice.Start()
                singleSlice.Kill()
                nextDemo = 0
                
            elif nextDemo == 2:
                multipleSlices = MultipleSlices()
                multipleSlices.Start()
                multipleSlices.Kill()
                nextDemo = 0
                
            elif nextDemo == 3:
                multiTouchTest = MultiTouchTest()
                multiTouchTest.Start()
                multiTouchTest.Kill()
                nextDemo = 0
                
            else:
                nextDemo = 0
            
    except KeyboardInterrupt:
        print "Program Terminating"
