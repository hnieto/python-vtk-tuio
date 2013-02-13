'''
TestDemo.py is a used to verify that TUIO events are being properly received and tracked.
A small number will be used to represent cursors.
'''

import vtk
import math
from MultiTouch import CursorTracker

try:
    import tuio
except ImportError, ioe:
    print >>sys.stderr, """
    You have to install PyTUIO and copy it into your $PYTHONPATH.
    You can grab a tarball from: http://code.google.com/p/pytuio/
    """
    sys.exit(2)
        
class Marker:
    def __init__(self, id):
        # Create text mapper and 2d actor to display finger position.
        self.textMapper = vtk.vtkTextMapper()
        self.textMapper.SetInput(id)  
        self.tprop = self.textMapper.GetTextProperty()
        self.tprop.SetFontFamilyToArial()
        self.tprop.SetFontSize(30)
        self.tprop.BoldOn()
        self.tprop.ShadowOn()
        self.tprop.SetColor(1, 0, 0)
        self.textActor = vtk.vtkActor2D()
        self.textActor.VisibilityOff()
        self.textActor.SetMapper(self.textMapper)

class MultiTouchTest:

    def __init__(self):

        # Create the Renderer, RenderWindow, etc. and set the Picker.
        self.ren = vtk.vtkRenderer()
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.ren.SetViewport(0,0,1,1)
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renwin)
        
        # Create text mappers and 2d actors to display finger position.
        self.fingerMarker1 = Marker("(1)")
        self.fingerMarker2 = Marker("(2)")
        self.fingerMarker3 = Marker("(3)")
        self.fingerMarker4 = Marker("(4)")
        self.fingerMarker5 = Marker("(5)")

        # Add the actors to the renderer, set the background and size
        self.ren.AddActor2D(self.fingerMarker1.textActor)
        self.ren.AddActor2D(self.fingerMarker2.textActor)
        self.ren.AddActor2D(self.fingerMarker3.textActor)
        self.ren.AddActor2D(self.fingerMarker4.textActor)
        self.ren.AddActor2D(self.fingerMarker5.textActor)
        self.ren.SetBackground(0, 0, 0)
        self.renwin.SetSize(680, 460)
        #self.renwin.FullScreenOn()
        
        '''
        TUIO STUFF
        '''
        self.tracking = tuio.Tracking('')
        self.tracker = CursorTracker(8)
        self.terminate = False
        
    def Start(self):
        self.renwin.Render()
        self.RunTUIO()
        
    def RunTUIO(self):
        while not self.terminate :
            while self.tracking.update():
                # read the socket empty
                pass

            self.tracker.update(self.tracking.cursors())
            self.CheckGesture()

    def CheckGesture(self):
        
        if self.tracker.fingers_detected() == 0:
            print "No Fingers Detected"
            self.fingerMarker1.textActor.VisibilityOff()
            self.fingerMarker2.textActor.VisibilityOff()
            self.fingerMarker3.textActor.VisibilityOff()
            self.fingerMarker4.textActor.VisibilityOff()
            self.fingerMarker5.textActor.VisibilityOff()
            self.renwin.Render()
        
        elif self.tracker.fingers_detected() == 1:
            print "1 Finger Detected"
            fingerID1 = self.tracker._seen.keys()[0]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            
            # hide all other markers
            self.fingerMarker2.textActor.VisibilityOff()
            self.fingerMarker3.textActor.VisibilityOff()
            self.fingerMarker4.textActor.VisibilityOff()
            self.fingerMarker5.textActor.VisibilityOff()
            self.renwin.Render()
                    
        elif self.tracker.fingers_detected() == 2:
            print "2 Fingers Detected"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            finger2CurrCoords = self.tracker._coords[fingerID2]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            self.fingerMarker2.textActor.VisibilityOn()
            
            # hide all other markers
            self.fingerMarker3.textActor.VisibilityOff()
            self.fingerMarker4.textActor.VisibilityOff()
            self.fingerMarker5.textActor.VisibilityOff()
            self.renwin.Render()
            
        elif self.tracker.fingers_detected() == 3:
            print "3 Fingers Detected"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            fingerID3 = self.tracker._seen.keys()[2]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            finger2CurrCoords = self.tracker._coords[fingerID2]
            finger3CurrCoords = self.tracker._coords[fingerID3]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[:2])
            self.fingerMarker3.textActor.SetPosition(finger3CurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            self.fingerMarker2.textActor.VisibilityOn()
            self.fingerMarker3.textActor.VisibilityOn()
            
            # hide all other markers
            self.fingerMarker4.textActor.VisibilityOff()
            self.fingerMarker5.textActor.VisibilityOff()
            self.renwin.Render()
            
        elif self.tracker.fingers_detected() == 4:
            print "4 Fingers Detected"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            fingerID3 = self.tracker._seen.keys()[2]
            fingerID4 = self.tracker._seen.keys()[3]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            finger2CurrCoords = self.tracker._coords[fingerID2]
            finger3CurrCoords = self.tracker._coords[fingerID3]
            finger4CurrCoords = self.tracker._coords[fingerID4]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[:2])
            self.fingerMarker3.textActor.SetPosition(finger3CurrCoords[:2])
            self.fingerMarker4.textActor.SetPosition(finger4CurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            self.fingerMarker2.textActor.VisibilityOn()
            self.fingerMarker3.textActor.VisibilityOn()
            self.fingerMarker4.textActor.VisibilityOn()
            
            # hide all other markers
            self.fingerMarker5.textActor.VisibilityOff()
            self.renwin.Render()
            
        elif self.tracker.fingers_detected() == 5:
            print "5 Fingers Detected"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            fingerID3 = self.tracker._seen.keys()[2]
            fingerID4 = self.tracker._seen.keys()[3]
            fingerID5 = self.tracker._seen.keys()[4]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            finger2CurrCoords = self.tracker._coords[fingerID2]
            finger3CurrCoords = self.tracker._coords[fingerID3]
            finger4CurrCoords = self.tracker._coords[fingerID4]
            finger5CurrCoords = self.tracker._coords[fingerID5]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[:2])
            self.fingerMarker3.textActor.SetPosition(finger3CurrCoords[:2])
            self.fingerMarker4.textActor.SetPosition(finger4CurrCoords[:2])
            self.fingerMarker5.textActor.SetPosition(finger5CurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            self.fingerMarker2.textActor.VisibilityOn()
            self.fingerMarker3.textActor.VisibilityOn()
            self.fingerMarker4.textActor.VisibilityOn()
            self.fingerMarker5.textActor.VisibilityOn()
            self.renwin.Render()
            
        elif self.tracker.fingers_detected() == 8:
            self.terminate = True
        
    def Kill(self):
        print "Stopping TestDemo TUIO tracking"
        self.tracking.stop()
        print "TestDemo.py Terminated"
        self.iren.GetRenderWindow().Finalize()
