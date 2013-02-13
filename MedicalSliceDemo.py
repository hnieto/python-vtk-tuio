'''
This example reads a volume dataset, extracts two isosurfaces that
represent the skin and bone, creates three orthogonal planes
(sagittal, axial, coronal), and displays them.
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
    
WIDTH = 480
HEIGHT = 640
    
class Marker:
    def __init__(self, id):
        # Create text mapper and 2d actor to display finger position.
        self.textMapper = vtk.vtkTextMapper()
        self.textMapper.SetInput(id)  
        self.tprop = self.textMapper.GetTextProperty()
        self.tprop.SetFontFamilyToArial()
        self.tprop.SetFontSize(20)
        self.tprop.BoldOn()
        self.tprop.ShadowOn()
        self.tprop.SetColor(1, 0, 0)
        self.textActor = vtk.vtkActor2D()
        self.textActor.VisibilityOff()
        self.textActor.SetMapper(self.textMapper)

class MedicalSliceDemo:
    def __init__(self):

        # Create the renderer, the render window, and the interactor. The
        # renderer draws into the render window, the interactor enables mouse-
        # and keyboard-based interaction with the scene.
        self.ren = vtk.vtkRenderer()
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(self.renwin)
        
        # Create text mappers and 2d actors to display finger position.
        self.fingerMarker1 = Marker("1")
        self.fingerMarker2 = Marker("2")
        self.fingerMarker3 = Marker("3")

        # The following reader is used to read a series of 2D slices (images)
        # that compose the volume. The slice dimensions are set, and the
        # pixel spacing. The data Endianness must also be specified. The reader
        # usese the FilePrefix in combination with the slice number to construct
        # filenames using the format FilePrefix.%d. (In this case the FilePrefix
        # is the root name of the file: quarter.)
        self.v16 = vtk.vtkVolume16Reader()
        self.v16.SetDataDimensions(64, 64)
        self.v16.SetDataByteOrderToLittleEndian()
        self.v16.SetFilePrefix("/Users/eddie/Programming/Python/python-vtk-tuio/headsq/Data_headsq_quarter")
        self.v16.SetImageRange(1, 93)
        self.v16.SetDataSpacing(3.2, 3.2, 1.5)

        # An isosurface, or contour value of 500 is known to correspond to the
        # skin of the patient. Once generated, a vtkPolyDataNormals filter is
        # is used to create normals for smooth surface shading during rendering.
        # The triangle stripper is used to create triangle strips from the
        # isosurface these render much faster on may systems.
        self.skinExtractor = vtk.vtkContourFilter()
        self.skinExtractor.SetInputConnection(self.v16.GetOutputPort())
        self.skinExtractor.SetValue(0, 500)
        self.skinNormals = vtk.vtkPolyDataNormals()
        self.skinNormals.SetInputConnection(self.skinExtractor.GetOutputPort())
        self.skinNormals.SetFeatureAngle(60.0)
        self.skinStripper = vtk.vtkStripper()
        self.skinStripper.SetInputConnection(self.skinNormals.GetOutputPort())
        self.skinMapper = vtk.vtkPolyDataMapper()
        self.skinMapper.SetInputConnection(self.skinStripper.GetOutputPort())
        self.skinMapper.ScalarVisibilityOff()
        self.skin = vtk.vtkActor()
        self.skin.SetMapper(self.skinMapper)
        self.skin.GetProperty().SetDiffuseColor(1, .49, .25)
        self.skin.GetProperty().SetSpecular(.3)
        self.skin.GetProperty().SetSpecularPower(20)

        # An isosurface, or contour value of 1150 is known to correspond to the
        # skin of the patient. Once generated, a vtkPolyDataNormals filter is
        # is used to create normals for smooth surface shading during rendering.
        # The triangle stripper is used to create triangle strips from the
        # isosurface these render much faster on may systems.
        self.boneExtractor = vtk.vtkContourFilter()
        self.boneExtractor.SetInputConnection(self.v16.GetOutputPort())
        self.boneExtractor.SetValue(0, 1150)
        self.boneNormals = vtk.vtkPolyDataNormals()
        self.boneNormals.SetInputConnection(self.boneExtractor.GetOutputPort())
        self.boneNormals.SetFeatureAngle(60.0)
        self.boneStripper = vtk.vtkStripper()
        self.boneStripper.SetInputConnection(self.boneNormals.GetOutputPort())
        self.boneMapper = vtk.vtkPolyDataMapper()
        self.boneMapper.SetInputConnection(self.boneStripper.GetOutputPort())
        self.boneMapper.ScalarVisibilityOff()
        self.bone = vtk.vtkActor()
        self.bone.SetMapper(self.boneMapper)
        self.bone.GetProperty().SetDiffuseColor(1, 1, .9412)

        # An outline provides context around the data.
        self.outlineData = vtk.vtkOutlineFilter()
        self.outlineData.SetInputConnection(self.v16.GetOutputPort())
        self.mapOutline = vtk.vtkPolyDataMapper()
        self.mapOutline.SetInputConnection(self.outlineData.GetOutputPort())
        self.outline = vtk.vtkActor()
        self.outline.SetMapper(self.mapOutline)
        self.outline.GetProperty().SetColor(0, 0, 0)

        # Now we are creating three orthogonal planes passing through the
        # volume. Each plane uses a different texture map and therefore has
        # diferent coloration.

        # Start by creatin a black/white lookup table.
        self.bwLut = vtk.vtkLookupTable()
        self.bwLut.SetTableRange(0, 2000)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()

        # Now create a lookup table that consists of the full hue circle (from
        # HSV).
        self.hueLut = vtk.vtkLookupTable()
        self.hueLut.SetTableRange(0, 2000)
        self.hueLut.SetHueRange(0, 1)
        self.hueLut.SetSaturationRange(1, 1)
        self.hueLut.SetValueRange(1, 1)
        self.hueLut.Build()

        # Finally, create a lookup table with a single hue but having a range
        # in the saturation of the hue.
        self.satLut = vtk.vtkLookupTable()
        self.satLut.SetTableRange(0, 2000)
        self.satLut.SetHueRange(.6, .6)
        self.satLut.SetSaturationRange(0, 1)
        self.satLut.SetValueRange(1, 1)
        self.satLut.Build()

        # Create the first of the three planes. The filter vtkImageMapToColors
        # maps the data through the corresponding lookup table created above.
        # The vtkImageActor is a type of vtkProp and conveniently displays an
        # image on a single quadrilateral plane. It does this using texture
        # mapping and as a result is quite fast. (Note: the input image has to
        # be unsigned char values, which the vtkImageMapToColors produces.)
        # Note also that by specifying the DisplayExtent, the pipeline
        # requests data of this extent and the vtkImageMapToColors only
        # processes a slice of data.
        self.sagittalColors = vtk.vtkImageMapToColors()
        self.sagittalColors.SetInputConnection(self.v16.GetOutputPort())
        self.sagittalColors.SetLookupTable(self.bwLut)
        self.sagittal = vtk.vtkImageActor()
        self.sagittal.GetMapper().SetInputConnection(self.sagittalColors.GetOutputPort())
        self.sagittal.SetDisplayExtent(32, 32, 0, 63, 0, 92)

        # Create the second (axial) plane of the three planes. We use the same
        # approach as before except that the extent differs.
        self.axialColors = vtk.vtkImageMapToColors()
        self.axialColors.SetInputConnection(self.v16.GetOutputPort())
        self.axialColors.SetLookupTable(self.hueLut)
        self.axial = vtk.vtkImageActor()
        self.axial.GetMapper().SetInputConnection(self.axialColors.GetOutputPort())
        self.axial.SetDisplayExtent(0, 63, 0, 63, 46, 46)

        # Create the third (coronal) plane of the three planes. We use the same
        # approach as before except that the extent differs.
        self.coronalColors = vtk.vtkImageMapToColors()
        self.coronalColors.SetInputConnection(self.v16.GetOutputPort())
        self.coronalColors.SetLookupTable(self.satLut)
        self.coronal = vtk.vtkImageActor()
        self.coronal.GetMapper().SetInputConnection(self.coronalColors.GetOutputPort())
        self.coronal.SetDisplayExtent(0, 63, 32, 32, 0, 92)

        # move camera to view sagital slice 
        self.aCamera = vtk.vtkCamera()
        self.aCamera.SetPosition(1,0,0) # view from positive x axis
        self.aCamera.SetViewUp(0,0,1) # z axis
        self.aCamera.Roll(180) # rotate 180 degrees

        # Actors are added to the renderer.
        #self.ren.AddActor(self.outline)
        self.ren.AddActor(self.sagittal)
        #self.ren.AddActor(self.axial)
        #self.ren.AddActor(self.coronal)
        #self.ren.AddActor(self.skin)
        #self.ren.AddActor(self.bone)
        self.ren.AddActor2D(self.fingerMarker1.textActor)
        self.ren.AddActor2D(self.fingerMarker2.textActor)
        self.ren.AddActor2D(self.fingerMarker3.textActor)

        # Turn off bone for this example.
        self.bone.VisibilityOff()

        # Set skin to semi-transparent.
        self.skin.GetProperty().SetOpacity(0.5)

        # An initial camera view is created.  The Dolly() method moves
        # the camera towards the FocalPoint, thereby enlarging the image.
        self.ren.SetActiveCamera(self.aCamera)
        self.ren.ResetCamera()
        self.aCamera.Dolly(1.5)

        # Set a background color for the renderer and set the size of the
        # render window (expressed in pixels).
        self.ren.SetBackground(1, 1, 1)
        self.renwin.SetSize(640, 480)
        #self.renwin.FullScreenOn()

        # Note that when camera movement occurs (as it does in the Dolly()
        # method), the clipping planes often need adjusting. Clipping planes
        # consist of two planes: near and far along the view direction. The
        # near plane clips out objects in front of the plane the far plane
        # clips out objects behind the plane. This way only what is drawn
        # between the planes is actually rendered.
        self.ren.ResetCameraClippingRange()
                
        '''
        TUIO STUFF
        '''
        self.tracking = tuio.Tracking('')
        self.tracker = CursorTracker(4)
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
        self.NONE = 0 
        self.ROTATE = 1 
        self.ZOOM = 2
        self.PAN = 3
        self.TERMINATE = 4
        
        if self.tracker.fingers_detected() == self.NONE:
            print "No Fingers Detected"
            self.fingerMarker1.textActor.VisibilityOff()
            self.fingerMarker2.textActor.VisibilityOff()
            self.fingerMarker3.textActor.VisibilityOff()
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
            self.fingerMarker3.textActor.VisibilityOff()
            
            self.Rotate(self.ren, self.renwin, self.ren.GetActiveCamera(), fingerPrevCoords[0]/10, fingerPrevCoords[1]/10, fingerCurrCoords[0]/10, fingerCurrCoords[1]/10)

        elif self.tracker.fingers_detected() == self.ZOOM:
            '''
            BUG DESCRIPTION: zooming in/out depends on dollyFactor >/< 1 respectively. 
                             if user zooms out and dollyFactor reaches some value n, where n<1,
                             and then begins to zoom in, the camera will continue to zoom out even 
                             though n is increasing. Only after n>=1 will the camera begin to zoom in.
                             The same effect occurs for the inverse.
            
            BUG STATUS: not fixed, in progress
            '''
            
            #print "Zooming"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            
            finger1StartCoords = self.tracker._startCoords[fingerID1]
            finger1PrevCoords = self.tracker._prevCoords[fingerID1]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            
            finger2StartCoords = self.tracker._startCoords[fingerID2]
            finger2PrevCoords = self.tracker._prevCoords[fingerID2]
            finger2CurrCoords = self.tracker._coords[fingerID2]

            # calculate distance between the finger1's current position and finger2's starting position
            startDist = math.sqrt( (finger1CurrCoords[0] - finger2StartCoords[0])**2 + (finger1CurrCoords[1] - finger2StartCoords[1])**2 )

            # calculate distance between the finger1's current position and finger2's current position
            currentDist = math.sqrt( (finger1CurrCoords[0] - finger2CurrCoords[0])**2 + (finger1CurrCoords[1] - finger2CurrCoords[1])**2 )

            # show finger markers
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[:2])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[:2])
            self.fingerMarker2.textActor.VisibilityOn()  
            
            # hide all other markers
            self.fingerMarker3.textActor.VisibilityOff() 

            if finger1CurrCoords != finger1PrevCoords or finger2CurrCoords != finger2PrevCoords:
                self.Zoom(self.ren, self.renwin, self.ren.GetActiveCamera(), startDist, currentDist)
            else:
                #print 'WILL NOT ZOOM. No change in finger position.'
                pass
            
        elif self.tracker.fingers_detected() == self.PAN:
            print "Panning"
            fingerID1 = self.tracker._seen.keys()[0]
            fingerID2 = self.tracker._seen.keys()[1]
            fingerID3 = self.tracker._seen.keys()[2]
            
            finger1PrevCoords = self.tracker._prevCoords[fingerID1]
            finger1CurrCoords = self.tracker._coords[fingerID1]
            
            finger2PrevCoords = self.tracker._prevCoords[fingerID2]
            finger2CurrCoords = self.tracker._coords[fingerID2]

            finger3PrevCoords = self.tracker._prevCoords[fingerID3]
            finger3CurrCoords = self.tracker._coords[fingerID3]

            # show finger markers
            self.fingerMarker1.textActor.SetPosition(finger1CurrCoords[0], finger1CurrCoords[1])
            self.fingerMarker2.textActor.SetPosition(finger2CurrCoords[0], finger2CurrCoords[1])
            self.fingerMarker3.textActor.SetPosition(finger3CurrCoords[0], finger3CurrCoords[1])
            self.fingerMarker3.textActor.VisibilityOn() 

            self.Pan(self.ren, self.renwin, self.ren.GetActiveCamera(), finger3PrevCoords[0], finger3PrevCoords[1], finger3CurrCoords[0], finger3CurrCoords[1], self.renwin.GetSize()[0]/2.0, self.renwin.GetSize()[1]/2.0)

        elif self.tracker.fingers_detected() == self.TERMINATE:
            self.terminate = True
        
    def Rotate(self, ren, renwin, camera, prevx, prevy, curx, cury):  
        camera.Azimuth(prevx-curx)
        ''' comment out to fix rotation to x axis only '''
        #camera.Elevation(prevy-cury)
        camera.OrthogonalizeViewUp()
        renwin.Render()
        
    def Zoom(self, ren, renwin, camera, startDist, currentDist):
        dollyFactor = pow(1.03,(0.05*(currentDist-startDist)))
        print 'dollyFactor=' + `dollyFactor`
        if camera.GetParallelProjection():
            parallelScale = camera.GetParallelScale()*dollyFactor
            camera.SetParallelScale(parallelScale)
        else:
            camera.Dolly(dollyFactor)
            ren.ResetCameraClippingRange()
        renwin.Render()
        
    def Pan(self, ren, renwin, camera, prevx, prevy, curx, cury, centerX, centerY):
        FPoint = camera.GetFocalPoint()
        FPoint0 = FPoint[0]
        FPoint1 = FPoint[1]
        FPoint2 = FPoint[2]

        PPoint = camera.GetPosition()
        PPoint0 = PPoint[0]
        PPoint1 = PPoint[1]
        PPoint2 = PPoint[2]

        ren.SetWorldPoint(FPoint0, FPoint1, FPoint2, 1.0)
        ren.WorldToDisplay()
        DPoint = ren.GetDisplayPoint()
        focalDepth = DPoint[2]

        APoint0 = centerX+(curx-prevx)
        APoint1 = centerY+(cury-prevy)

        ren.SetDisplayPoint(APoint0, APoint1, focalDepth)
        ren.DisplayToWorld()
        RPoint = ren.GetWorldPoint()
        RPoint0 = RPoint[0]
        RPoint1 = RPoint[1]
        RPoint2 = RPoint[2]
        RPoint3 = RPoint[3]

        if RPoint3 != 0.0:
            RPoint0 = RPoint0/RPoint3
            RPoint1 = RPoint1/RPoint3
            RPoint2 = RPoint2/RPoint3

        camera.SetFocalPoint( (FPoint0-RPoint0)/2.0 + FPoint0, (FPoint1-RPoint1)/2.0 + FPoint1, (FPoint2-RPoint2)/2.0 + FPoint2)
        camera.SetPosition( (FPoint0-RPoint0)/2.0 + PPoint0, (FPoint1-RPoint1)/2.0 + PPoint1, (FPoint2-RPoint2)/2.0 + PPoint2)
        renwin.Render()

    def Kill(self):
        print "Stopping MedicalDemo TUIO tracking"
        self.tracking.stop()
        print "MedicalDemo.py Terminated"
        self.iren.GetRenderWindow().Finalize()
