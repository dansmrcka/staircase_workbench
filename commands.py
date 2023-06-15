import FreeCAD as App
import FreeCADGui
import Part,PartGui 
import Spreadsheet
class Create_Part():
    """Create random Part object"""

    def GetResources(self):
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "MenuText": "Testing object",
                "ToolTip" : "Create random object"}

    def Activated(self):
        doc=App.activeDocument() 
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
        sheet = doc.addObject("Spreadsheet::Sheet","DimensionsSource")
        sheet.Label = "Dimensions"
        sheet.set('A1','10mm')
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

        sheet = App.activeDocument.getObject("DimensionsSource")

        sketch = doc.addObject("Sketcher::SketchObject", "Top view")
        sketch.addGeometry(Part.LineSegment(App.Vector(1.2, 1.8, 0), App.Vector(5.2, 5.3, 0)), False)
        sketch.addConstraint(Sketcher.Constraint("Distance", 0, 1, 0, 2, sheet.get('A1')))
        doc.recompute()
        
    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand("Create part", Create_Part())
FreeCADGui.addCommand("Create dimensions", Generate_Spreadsheet())
FreeCADGui.addCommand("Create sketches", Generate_Sketches())
