import FreeCAD as App
import FreeCADGui
import Part,PartGui
import Spreadsheet
import Sketcher
import math
import re

class CreatePart():
    """
    Create random Part object
    """

    def GetResources(self):
        """
        TODO 
        """
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "MenuText": "Testing object",
                "ToolTip" : "Create random object"}

    def Activated(self):
        """
        TODO 
        """

        doc=App.ActiveDocument()
        # add a line element to the document and set its points
        line=Part.LineSegment()
        line.StartPoint=(0.0,0.0,0.0)
        line.EndPoint=(1.0,1.0,1.0)
        doc.addObject("Part::Feature","Line").Shape=line.toShape()
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
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True

class GenerateSpreadsheet():
    """
    Generates spreadsheet
    """
    def GetResources(self):
        """
        TODO 
        """
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "MenuText": "Add table",
                "ToolTip" : "table"}

    def Activated(self):
        """ 
        TODO 
        """

        App.Console.PrintMessage('Hello World!\n')

        doc=App.activeDocument()
        sheet = doc.addObject("Spreadsheet::Sheet","Dimensions")
        sheet.Label = "Dimensions"
        sheet.set('A1','General')

        self.add_table_element(sheet, 'Length', 'B2', '2m', 'length')
        self.add_table_element(sheet, 'Width', 'B3', '1.5m', 'width')
        self.add_table_element(sheet, 'Heigth', 'B4', '2m', 'height')
        self.add_table_element(sheet, 'Staircase width', 'B5', '1m', 'staircase_width')
        self.add_table_element(sheet, 'Sides width', 'B6', '4.5cm', 'side_width')
        self.add_table_element(sheet, 'Step sink', 'B7', '2cm', 'step_sink')
        self.add_table_element(sheet, 'Wall offset', 'B8', '2cm', 'wall_offset')
        self.add_table_element(sheet, 'Step overlay', 'B9', '2cm', 'step_overlay')
        self.add_table_element(sheet, 'Last step', 'B10', '15cm', 'last_step_width')
        self.add_table_element(sheet, 'First step distance', 'B11', '3cm', 'first_step_dist')

        doc.recompute()

    def IsActive(self):
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True

    def add_table_element(self, sheet, name, name_pos, value, alias):
        """ 
        function to simplify adding an element to the table 
        """

        reg = re.findall(r'[A-Z]|[0-9]+', name_pos)
        value_pos =chr(ord(reg[0])+1)+reg[1]

        sheet.set(name_pos, name)
        sheet.setAlias(value_pos, alias)
        sheet.set(value_pos, value)
        return

class GenerateSketches():
    """ 
    TODO 
    """

    def GetResources(self):
        """ 
        TODO 
        """
        return {"Pixmap"  : "My_Command_Icon", # the name of a svg file available in the resources
                "Accel"   : "Shift+S", # a default shortcut (optional)
                "MenuText": "Add high-level sketches",
                "ToolTip" : "sketches"}
    def Activated(self):
        """ 
        TODO 
        """

        App.Console.PrintMessage('Generating sketches\n')

        doc=App.activeDocument()

        dimensions = App.ActiveDocument.getObject("Dimensions")

        length = dimensions.get('length')
        width = dimensions.get('width')
        height = dimensions.get('height')
        stairs_width = dimensions.get('staircase_width')
        side_width = dimensions.get('side_width')
        step_sink = dimensions.get('step_sink')
        wall_offset = dimensions.get('step_overlay')
        step_overlay = dimensions.get('wall_offset')
        last_step_width = dimensions.get('last_step_width')
        first_step_dist = dimensions.get('first_step_dist')

        # Top view
        sketch_top = doc.addObject("Sketcher::SketchObject", "Top_view")
        sketch_top.Placement = App.Placement(App.Vector(0.000000, 0.000000, height), App.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
        sketch_top.MapMode = "Deactivated"

        (geo_list, con_list) = self.createRectangle()
        (tb, tl, tt, tr) = sketch_top.addGeometry(geo_list,False)
        sketch_top.addConstraint(con_list)
        conw = sketch_top.addConstraint(Sketcher.Constraint('DistanceX',tt,1,tt,2, width))
        conl = sketch_top.addConstraint(Sketcher.Constraint('DistanceY', tl, 1, tl, 2, length))
        sketch_top.addConstraint(Sketcher.Constraint('Coincident',-1,1,tl,1))

        sketch_top.setExpression(f'Constraints[{conw}]', u'Dimensions.width')
        sketch_top.setExpression(f'Constraints[{conl}]', u'Dimensions.length')

        offset = 4
        (geo_list, con_list) = self.createRectangle(offset=offset)
        (tsi1b, tsi1l, tsi1t, tsi1r) = sketch_top.addGeometry(geo_list,False)
        sketch_top.addConstraint(con_list)
        conw = sketch_top.addConstraint(Sketcher.Constraint('DistanceX',tsi1t,1, tsi1t,2, side_width))
        sketch_top.addConstraint(Sketcher.Constraint('DistanceX',-1,1,tsi1b, 2, wall_offset))
        sketch_top.addConstraint(Sketcher.Constraint('PointOnObject',tsi1b,1, tb))
        sketch_top.addConstraint(Sketcher.Constraint('PointOnObject',tsi1t,1, tt))

        offset = 8
        (geo_list, con_list) = self.createRectangle(offset=offset)
        (tsi2b, tsi2l, tsi2t, tsi2r) = sketch_top.addGeometry(geo_list,False)
        sketch_top.addConstraint(con_list)
        conw = sketch_top.addConstraint(Sketcher.Constraint('DistanceX',tsi2t,1, tsi2t,2, side_width))
        sketch_top.addConstraint(Sketcher.Constraint('DistanceX',-1,1,tsi2b, 1, wall_offset+stairs_width))
        sketch_top.addConstraint(Sketcher.Constraint('PointOnObject',tsi2b,1, tb))
        sketch_top.addConstraint(Sketcher.Constraint('PointOnObject',tsi2t,1, tt))

        num_of_stairs = math.floor(height.Value/200)
        step_width = (length.Value-last_step_width.Value-first_step_dist.Value)/(num_of_stairs-1)
        print(num_of_stairs)
        print(step_width)
        for i in range(0,num_of_stairs):
            offset = 12 + 4*i
            if i==num_of_stairs-1: # last step
                (geo_list, con_list) = self.createRectangle(x=App.Units.Quantity(stairs_width-2*(side_width-step_sink)), y=App.Units.Quantity(last_step_width.Value), offset=offset, originx=App.Units.Quantity(wall_offset+side_width-step_sink), originy=App.Units.Quantity(first_step_dist.Value)+i*App.Units.Quantity(step_width))
            else:
                (geo_list, con_list) = self.createRectangle(x=App.Units.Quantity(stairs_width-2*(side_width-step_sink)), y=App.Units.Quantity(step_width+step_overlay.Value), offset=offset, originx=App.Units.Quantity(wall_offset+side_width-step_sink), originy=App.Units.Quantity(first_step_dist.Value)+i*App.Units.Quantity(step_width))
            sketch_top.addGeometry(geo_list,False)
            sketch_top.addConstraint(con_list)

        # Side view
        sketchLeft = doc.addObject("Sketcher::SketchObject", "Left_side")
        sketchLeft.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000), App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        sketchLeft.MapMode = "Deactivated"

        (geo_list, con_list) = self.createRectangle()
        con_list.append(Sketcher.Constraint('DistanceX',2,1,2,2, length))
        con_list.append(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, App.Units.Quantity('-1.0 dm')))
        con_list.append(Sketcher.Constraint('Coincident',-1,1,1,1))
        sketchLeft.addGeometry(geo_list,False)
        sketchLeft.addConstraint(con_list)
        del geo_list, con_list
        doc.recompute()

    def IsActive(self):
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True

    def createRectangle(self, x=App.Units.Quantity('10.0 mm'), y=App.Units.Quantity('10.0 mm'), originx=App.Units.Quantity('0.0 mm'), originy=App.Units.Quantity('0.0 mm'), offset=0):
        """
        TODO 
        """
        V1 = App.Vector(originx, originy, 0)
        V2 = App.Vector(originx, originy+y, 0)
        V3 = App.Vector(originx+x, originy+y, 0)
        V4 = App.Vector(originx+x, originy, 0)

        geo_list = []
        geo_list.append(Part.LineSegment(V1, V2))
        geo_list.append(Part.LineSegment(V2, V3))
        geo_list.append(Part.LineSegment(V3, V4))
        geo_list.append(Part.LineSegment(V4, V1))

        con_list = []
        con_list.append(Sketcher.Constraint('Coincident',0+offset,2,1+offset,1))
        con_list.append(Sketcher.Constraint('Coincident',1+offset,2,2+offset,1))
        con_list.append(Sketcher.Constraint('Coincident',2+offset,2,3+offset,1))
        con_list.append(Sketcher.Constraint('Coincident',3+offset,2,0+offset,1))
        con_list.append(Sketcher.Constraint('Horizontal',0+offset))
        con_list.append(Sketcher.Constraint('Horizontal',2+offset))
        con_list.append(Sketcher.Constraint('Vertical',1+offset))
        con_list.append(Sketcher.Constraint('Vertical',3+offset))

        return geo_list, con_list


FreeCADGui.addCommand("Create part", CreatePart())
FreeCADGui.addCommand("Create dimensions", GenerateSpreadsheet())
FreeCADGui.addCommand("Create sketches", GenerateSketches())
