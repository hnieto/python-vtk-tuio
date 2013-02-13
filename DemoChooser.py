'''
DemoChooser.py is a simple user interface for switching between vtk demos.
It contains its own tuio "thread" and gesture functions.
The program will terminate once the user selects a demo and will be relaunched by Visualizer.py when that demo ends.
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
    
class Sphere:
    def __init__(self, center, radius, color):
        self.sphere = vtk.vtkSphereSource()
        self.sphere.SetCenter(center)
        self.sphere.SetRadius(radius)
        self.sphere.SetThetaResolution(30)
        self.sphere.SetPhiResolution(30)
        self.sphereMapper = vtk.vtkPolyDataMapper()
        self.sphereMapper.SetInput(self.sphere.GetOutput())
        self.sphereActor = vtk.vtkActor()
        self.sphereActor.GetProperty().SetColor(color)
        self.sphereActor.GetProperty().SetRepresentationToWireframe()
        self.sphereActor.VisibilityOff()
        self.sphereActor.SetMapper(self.sphereMapper)
        
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

class DemoChooser:

    def __init__(self):

        # Create the Renderer, RenderWindow, etc. and set the Picker.
        self.ren = vtk.vtkRenderer()
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.ren.SetViewport(0,0,1,1)
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renwin)
        self.propPicker = vtk.vtkPropPicker()
        self.iren.SetPicker(self.propPicker)
        
        # blue sphere, will show four spheres when hovered on
        self.blueSphere = Sphere((0,0,0), 3.0, (0,0,1))
        self.blueSphere.sphereActor.VisibilityOn()
        self.greenSphere = Sphere((4,4,0), 1.0, (0,1,0))
        self.redSphere = Sphere((4,-4,0), 1.0, (1,0,0))
        self.yellowSphere = Sphere((-4,4,0), 1.0, (1,1,0))
        self.purpleSphere = Sphere((-4,-4,0), 1.0, (1,0,1))
        
        # Create text mappers and 2d actors to display finger position.
        self.fingerMarker1 = Marker("(1)")
        self.fingerMarker2 = Marker("(2)")
        self.fingerMarker3 = Marker("(3)")

        # Add the actors to the renderer, set the background and size
        self.ren.AddActor(self.blueSphere.sphereActor)
        self.ren.AddActor(self.greenSphere.sphereActor)
        self.ren.AddActor(self.redSphere.sphereActor)
        self.ren.AddActor(self.yellowSphere.sphereActor)
        self.ren.AddActor(self.purpleSphere.sphereActor)
        self.ren.AddActor2D(self.fingerMarker1.textActor)
        self.ren.AddActor2D(self.fingerMarker2.textActor)
        self.propPicker.AddObserver("EndPickEvent", self.Pick)
        self.ren.SetBackground(0, 0, 0)
        self.renwin.SetSize(680, 460)
        #self.renwin.FullScreenOn()
        
        '''
        TUIO STUFF
        '''
        self.tracking = tuio.Tracking('')
        self.tracker = CursorTracker(2)
        self.pickedDemo = 0
        
    def Start(self):
        self.renwin.Render()
        self.RunTUIO()
        
    def RunTUIO(self):
        while (self.pickedDemo == 0) :
            while self.tracking.update():
                # read the socket empty
                pass

            self.tracker.update(self.tracking.cursors())
            self.CheckGesture()

    def CheckGesture(self):
        self.NONE = 0 
        self.ROTATE = 1 
        self.PICK = 2
        
        if self.tracker.fingers_detected() == self.NONE:
            print "No Fingers Detected"
            self.fingerMarker1.textActor.VisibilityOff()
            self.fingerMarker2.textActor.VisibilityOff()
            self.renwin.Render()
        
        elif self.tracker.fingers_detected() == self.ROTATE:
            print "Rotating"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerPrevCoords = self.tracker._prevCoords[fingerID1]
            fingerCurrCoords = self.tracker._coords[fingerID1]
            
            # show finger marker
            self.fingerMarker1.textActor.SetPosition(fingerCurrCoords[:2])
            self.fingerMarker1.textActor.VisibilityOn()
            
            # hide all other markers
            self.fingerMarker2.textActor.VisibilityOff()
            
            self.Rotate(self.ren, self.renwin, self.ren.GetActiveCamera(), fingerPrevCoords[0]/10, fingerPrevCoords[1]/10, fingerCurrCoords[0]/10, fingerCurrCoords[1]/10)

        elif self.tracker.fingers_detected() == self.PICK:
            print "Picking Mode"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
                        
            # show finger markers
            self.fingerMarker1.textActor.SetPosition(self.tracker._coords[fingerID1][:2])
            self.fingerMarker2.textActor.SetPosition(self.tracker._coords[fingerID2][:2])
            self.fingerMarker2.textActor.VisibilityOn()  
            self.propPicker.PickProp(self.tracker._coords[fingerID2][0], self.tracker._coords[fingerID2][1], self.ren)
        
    def Rotate(self, ren, renwin, camera, startx, starty, curx, cury):  
        camera.Azimuth(startx-curx)
        camera.Elevation(starty-cury)
        camera.OrthogonalizeViewUp()
        renwin.Render()
        
    def Pick(self, object, event):        
        pickedSphere = self.propPicker.GetActor()
        if pickedSphere == None:            
            self.Wireframe(self.ren, self.renwin)
        elif pickedSphere.GetBounds() == self.blueSphere.sphereActor.GetBounds():
            print 'you picked blue'
            pickedSphere.GetProperty().SetRepresentationToSurface()
            self.blueSphere.sphereActor.VisibilityOn()
            self.greenSphere.sphereActor.VisibilityOn()
            self.redSphere.sphereActor.VisibilityOn()
            self.yellowSphere.sphereActor.VisibilityOn()
            self.purpleSphere.sphereActor.VisibilityOn()
        elif pickedSphere.GetBounds() == self.greenSphere.sphereActor.GetBounds():
            print 'you picked green'
            pickedSphere.GetProperty().SetRepresentationToSurface()
            self.pickedDemo = 1
        elif pickedSphere.GetBounds() == self.redSphere.sphereActor.GetBounds():
            print 'you picked red'
            pickedSphere.GetProperty().SetRepresentationToSurface()
            self.pickedDemo = 2
        elif pickedSphere.GetBounds() == self.yellowSphere.sphereActor.GetBounds():
            print 'you picked yellow'
            pickedSphere.GetProperty().SetRepresentationToSurface()
            self.pickedDemo = 3
        elif pickedSphere.GetBounds() == self.purpleSphere.sphereActor.GetBounds():
            print 'you picked purple'
            pickedSphere.GetProperty().SetRepresentationToSurface()
            self.pickedDemo = 4
        self.iren.Render()
        
    def Wireframe(self, ren, renwin):
        actors = ren.GetActors()
        actors.InitTraversal()
        actor = actors.GetNextItem()
        while actor:
            actor.GetProperty().SetRepresentationToWireframe()
            actor = actors.GetNextItem()
        renwin.Render()
        
    def GetPickedDemo(self):
        return self.pickedDemo
        
    def Kill(self):
        print "Stopping DemoChooser TUIO tracking"
        self.tracking.stop()
        print "DemoChooser.py Terminated"
        self.iren.GetRenderWindow().Finalize()
