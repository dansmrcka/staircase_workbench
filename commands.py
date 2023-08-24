import FreeCAD as App
import FreeCADGui
import Part,PartGui 
import Spreadsheet
import Sketcher
class Create_Part():
    """Create random Part object"""

    def GetResources(self):
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "MenuText": "Testing object",
                "ToolTip" : "Create random object"}

    def Activated(self):
        doc=App.ActiveDocument() 
        # add a line element to the document and set its points 
        l=Part.LineSegment()
        l.StartPoint=(0.0,0.0,0.0)
        l.EndPoint=(1.0,1.0,1.0)
        doc.addObject("Part::Feature","Line").Shape=l.toShape() 
        doc.recompute()

        box = Part.makeBox(100, 20, 5)
        # tube = circle.extrude(App.Vector(0, 0, 2))
        Part.show(box)

        # polygon = Part.makePolygon([App.Vector(0, 5, 0), App.Vector(10, 0, 0), App.Vector(5,5,0), App.Vector(0,5,0)])
        # stair_face = Part.Face(polygon)
        # Part.show(stair_face.extrude(App.Vector(0,0,5)))
        # object = (stair_face.extrude(App.Vector(0,0,5)))
        # Part.show(object.translate(App.Vector(0,0,20)))

        App.Console.PrintMessage('Done!\n')

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class Generate_Spreadsheet():
    def GetResources(self):
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "MenuText": "Add table",
                "ToolTip" : "table"}
    def Activated(self):
        App.Console.PrintMessage('Hello World!\n')

        doc=App.activeDocument() 
        sheet = doc.addObject("Spreadsheet::Sheet","Dimensions")
        sheet.Label = "Dimensions"
        sheet.set('A1','General')

        sheet.set('B2','Length')
        sheet.setAlias('C2','length')
        sheet.set('C2','2m')

        sheet.set('B3','Width')
        sheet.setAlias('C3','width')
        sheet.set('C3','15dm')

        sheet.set('B4','Height')
        sheet.setAlias('C4','height')
        sheet.set('C4','2m')

        sheet.set('B5','Staircase width')
        sheet.setAlias('C5','staircase_width')
        sheet.set('C5','1m')

        doc.recompute()
        
    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class Generate_Sketches():
    def GetResources(self):
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "Accel"   : "Shift+S", # a default shortcut (optional)
                "MenuText": "Add high-level sketches",
                "ToolTip" : "sketches"}
    def Activated(self):
        App.Console.PrintMessage('Generating sketches\n')

        doc=App.activeDocument() 

        dimensions = App.ActiveDocument.getObject("Dimensions")

        l = dimensions.get('length')
        w = dimensions.get('width')
        h = dimensions.get('height')


        sketchTop = doc.addObject("Sketcher::SketchObject", "Top_view")
        sketchTop.Placement = App.Placement(App.Vector(0.000000, 0.000000, h), App.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
        sketchTop.MapMode = "Deactivated"

        (geoList, conList) = self.createRectangle(l, w)
        conList.append(Sketcher.Constraint('DistanceX',2,1,2,2,dimensions.get('width')))
        conList.append(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, l))

        sketchTop.addGeometry(geoList,False)
        sketchTop.addConstraint(conList)

        del geoList, conList

        sketchLeft = doc.addObject("Sketcher::SketchObject", "Left_side")
        sketchLeft.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000), App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        sketchLeft.MapMode = "Deactivated"

        (geoList, conList) = self.createRectangle(l, h)
        sketchLeft.addGeometry(geoList,False)
        sketchLeft.addConstraint(conList)

        # sketchLeft.addGeometry(Part.LineSegment(App.Vector(1.2, 1.8, 0), App.Vector(5.2, 5.3, 0)), False)
        # # sketch.addConstraint(Sketcher.Constraint("Distance", 0, 1, 0, 2, sheet.get('A1')))

        # sketchRight = doc.addObject("Sketcher::SketchObject", "Right_side")
        # sketchRight.addGeometry(Part.LineSegment(App.Vector(1.2, 1.8, 0), App.Vector(5.2, 5.3, 0)), False)
        # # sketch.addConstraint(Sketcher.Constraint("Distance", 0, 1, 0, 2, sheet.get('A1')))
        doc.recompute()

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

    def createRectangle(self, length, width):
        V1 = App.Vector(0, 0, 0)
        V2 = App.Vector(0, length, 0)
        V3 = App.Vector(width, length, 0)
        V4 = App.Vector(width, 0, 0)

        geoList = []
        geoList.append(Part.LineSegment(V1, V2))
        geoList.append(Part.LineSegment(V2, V3))
        geoList.append(Part.LineSegment(V3, V4))
        geoList.append(Part.LineSegment(V4, V1))

        conList = []
        conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
        conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
        conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
        conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
        conList.append(Sketcher.Constraint('Horizontal',0))
        conList.append(Sketcher.Constraint('Horizontal',2))
        conList.append(Sketcher.Constraint('Vertical',1))
        conList.append(Sketcher.Constraint('Vertical',3))

        # conList.append(Sketcher.Constraint('Coincident',-1,1,0,1))

        return geoList, conList



FreeCADGui.addCommand("Create part", Create_Part())
FreeCADGui.addCommand("Create dimensions", Generate_Spreadsheet())
FreeCADGui.addCommand("Create sketches", Generate_Sketches())
