from vtk import *
from DemoChooser import DemoChooser
from MedicalDemo import MedicalDemo
from MedicalSliceDemo import MedicalSliceDemo
from TestDemo import TestDemo

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
                medSliceDemo = MedicalSliceDemo()
                medSliceDemo.Start()
                medSliceDemo.Kill()
                nextDemo = 0
                
            elif nextDemo == 2:
                medDemo = MedicalDemo()
                medDemo.Start()
                medDemo.Kill()
                nextDemo = 0
                
            elif nextDemo == 3:
                testDemo = TestDemo()
                testDemo.Start()
                testDemo.Kill()
                nextDemo = 0
                
            else:
                nextDemo = 0
            
    except KeyboardInterrupt:
        print "Program Terminating"
