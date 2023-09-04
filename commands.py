import math
import re

import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher


class GenerateSpreadsheet():
    """
    Generates spreadsheet
    """
    def GetResources(self):
        """
        TODO
        """
        return {"Pixmap": "My_Command_Icon",  # the name of a svg file available in the resources
                "MenuText": "Add table",
                "ToolTip": "table"}

    def Activated(self):
        """
        TODO
        """

        doc = App.activeDocument()
        sheet = doc.addObject("Spreadsheet::Sheet", "Dimensions")
        sheet.Label = "Dimensions"
        sheet.set('A1', 'General')

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
        self.add_table_element(sheet, 'Stair thickness', 'B12', '3cm', 'stair_thick')

        App.Console.PrintMessage('Generated dimensions spreadsheet\n')
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
        value_pos = chr(ord(reg[0]) + 1) + reg[1]

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
        return {"Pixmap": "My_Command_Icon",  # the name of a svg file available in the resources
                "Accel": "Shift+S",  # a default shortcut (optional)
                "MenuText": "Add high-level sketches",
                "ToolTip": "sketches"}

    def Activated(self):
        """
        TODO
        """
        App.Console.PrintMessage('Generating sketches\n')

        doc = App.activeDocument()

        group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Sketches")

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
        stair_thick = dimensions.get('stair_thick')

        # general parameters
        num_of_stairs = math.floor(height.Value / 200)  # find optimal height
        step_width = (length.Value - last_step_width.Value - first_step_dist.Value) / (num_of_stairs - 1)
        step_height = math.floor(height.Value / num_of_stairs)

        print("Number of stairs: %d, height between steps %f" % (num_of_stairs, step_height))

        # Top view
        aux_top = App.ActiveDocument.addObject("Sketcher::SketchObject", "aux_top")
        aux_top.Placement = App.Placement(App.Vector(0.000000, 0.000000, height), App.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
        aux_top.MapMode = "Deactivated"

        (geo_list, con_list) = self.create_rectangle()
        (tb, tl, tt, _) = aux_top.addGeometry(geo_list, False)
        aux_top.addConstraint(con_list)
        conw = aux_top.addConstraint(Sketcher.Constraint('DistanceX', tt, 1, tt, 2, width))
        conl = aux_top.addConstraint(Sketcher.Constraint('DistanceY', tl, 1, tl, 2, length))
        aux_top.addConstraint(Sketcher.Constraint('Coincident', -1, 1, tl, 1))

        aux_top.setExpression(f'Constraints[{conw}]', 'Dimensions.width')
        aux_top.setExpression(f'Constraints[{conl}]', 'Dimensions.length')

        offset = 4
        (geo_list, con_list) = self.create_rectangle(offset=offset)
        (tsi1b, _, tsi1t, _) = aux_top.addGeometry(geo_list, False)
        aux_top.addConstraint(con_list)
        conw = aux_top.addConstraint(Sketcher.Constraint('DistanceX', tsi1t, 1, tsi1t, 2, side_width))
        aux_top.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, tsi1b, 2, wall_offset))
        aux_top.addConstraint(Sketcher.Constraint('PointOnObject', tsi1b, 1, tb))
        aux_top.addConstraint(Sketcher.Constraint('PointOnObject', tsi1t, 1, tt))

        offset = 8
        (geo_list, con_list) = self.create_rectangle(offset=offset)
        (tsi2b, _, tsi2t, _) = aux_top.addGeometry(geo_list, False)
        aux_top.addConstraint(con_list)
        conw = aux_top.addConstraint(Sketcher.Constraint('DistanceX', tsi2t, 1, tsi2t, 2, side_width))
        aux_top.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, tsi2b, 1, wall_offset + stairs_width))
        aux_top.addConstraint(Sketcher.Constraint('PointOnObject', tsi2b, 1, tb))
        aux_top.addConstraint(Sketcher.Constraint('PointOnObject', tsi2t, 1, tt))

        group.addObject(aux_top)

        for i in range(0, num_of_stairs):
            offset = 0
            name = "stair_" + str(i)
            sketch = App.ActiveDocument.addObject("Sketcher::SketchObject", name)
            sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, (i + 1) * step_height), App.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
            sketch.MapMode = "Deactivated"
            if i == num_of_stairs - 1:  # last step
                (geo_list, con_list) = self.create_rectangle(x=App.Units.Quantity(stairs_width - 2 * (side_width - step_sink)), y=App.Units.Quantity(last_step_width.Value), offset=offset, originx=App.Units.Quantity(wall_offset + side_width - step_sink), originy=App.Units.Quantity(first_step_dist.Value) + i * App.Units.Quantity(step_width))
            else:
                (geo_list, con_list) = self.create_rectangle(x=App.Units.Quantity(stairs_width - 2 * (side_width - step_sink)), y=App.Units.Quantity(step_width + step_overlay.Value), offset=offset, originx=App.Units.Quantity(wall_offset + side_width - step_sink), originy=App.Units.Quantity(first_step_dist.Value) + i * App.Units.Quantity(step_width))
            sketch.addGeometry(geo_list, False)
            sketch.addConstraint(con_list)

            group.addObject(sketch)

        # Side view
        aux_left = App.ActiveDocument.addObject("Sketcher::SketchObject", "aux_side")
        aux_left.Placement = App.Placement(App.Vector(wall_offset, 0.000000, 0.000000), App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        aux_left.MapMode = "Deactivated"

        # floor
        (geo_list, con_list) = self.create_rectangle()
        con_list.append(Sketcher.Constraint('DistanceX', 2, 1, 2, 2, length))
        con_list.append(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, App.Units.Quantity('-1.0 dm')))
        con_list.append(Sketcher.Constraint('Coincident', -1, 1, 1, 1))
        aux_left.addGeometry(geo_list, False)
        aux_left.addConstraint(con_list)

        # create stairs
        for i in range(0, num_of_stairs):
            offset = 4 + 4 * i
            if i == num_of_stairs - 1:  # last step
                (geo_list, con_list) = self.create_rectangle(x=App.Units.Quantity(last_step_width.Value), y=App.Units.Quantity(stair_thick.Value), offset=offset, originx=App.Units.Quantity(first_step_dist.Value + i * step_width), originy=App.Units.Quantity((i + 1) * step_height - stair_thick.Value))
            else:
                (geo_list, con_list) = self.create_rectangle(x=App.Units.Quantity(step_width + step_overlay.Value), y=App.Units.Quantity(stair_thick.Value), offset=offset, originx=App.Units.Quantity(first_step_dist.Value + i * step_width), originy=App.Units.Quantity((i + 1) * step_height - stair_thick.Value))
            aux_left.addGeometry(geo_list, False)
            aux_left.addConstraint(con_list)

        group.addObject(aux_left)

        # create sides - polyline
        side_0 = App.ActiveDocument.addObject("Sketcher::SketchObject", "side_0")
        side_0.Placement = App.Placement(App.Vector(wall_offset, 0.000000, 0.000000), App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        side_0.MapMode = "Deactivated"

        (geo_list, con_list) = self.create_side(length.Value, height.Value, step_height, step_width, last_step_width.Value)
        side_0.addGeometry(geo_list, False)
        side_0.addConstraint(con_list)

        group.addObject(side_0)

        side_1 = App.ActiveDocument.addObject("Sketcher::SketchObject", "side_1")
        side_1.Placement = App.Placement(App.Vector(wall_offset + stairs_width, 0.000000, 0.000000), App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        side_1.MapMode = "Deactivated"

        (geo_list, con_list) = self.create_side(length.Value, height.Value, step_height, step_width, last_step_width.Value)
        side_1.addGeometry(geo_list, False)
        side_1.addConstraint(con_list)

        group.addObject(side_1)
        del geo_list, con_list

        doc.recompute()

    def IsActive(self):
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True

    def create_rectangle(self, x=App.Units.Quantity('10.0 mm'), y=App.Units.Quantity('10.0 mm'), originx=App.Units.Quantity('0.0 mm'), originy=App.Units.Quantity('0.0 mm'), offset=0):
        """
        TODO
        """
        V1 = App.Vector(originx, originy, 0)
        V2 = App.Vector(originx, originy + y, 0)
        V3 = App.Vector(originx + x, originy + y, 0)
        V4 = App.Vector(originx + x, originy, 0)

        geo_list = []
        geo_list.append(Part.LineSegment(V1, V2))
        geo_list.append(Part.LineSegment(V2, V3))
        geo_list.append(Part.LineSegment(V3, V4))
        geo_list.append(Part.LineSegment(V4, V1))

        con_list = []
        con_list.append(Sketcher.Constraint('Coincident', 0 + offset, 2, 1 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 1 + offset, 2, 2 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 2 + offset, 2, 3 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 3 + offset, 2, 0 + offset, 1))
        con_list.append(Sketcher.Constraint('Horizontal', 0 + offset))
        con_list.append(Sketcher.Constraint('Horizontal', 2 + offset))
        con_list.append(Sketcher.Constraint('Vertical', 1 + offset))
        con_list.append(Sketcher.Constraint('Vertical', 3 + offset))

        return geo_list, con_list

    def create_side(self, length, height, step_height, step_width, last_step_width, offset=0):
        """
        TODO
        """
        V1 = App.Vector(0, 0, 0)
        V2 = App.Vector(0, 1.5 * step_height, 0)
        V3 = App.Vector(length - 1.5 * last_step_width, height + 40, 0)
        V4 = App.Vector(length, height + 40, 0)
        V5 = App.Vector(length, height + 40 - 2 * step_height, 0)
        V6 = App.Vector(step_width, 0, 0)

        geo_list = []
        geo_list.append(Part.LineSegment(V1, V2))
        geo_list.append(Part.LineSegment(V2, V3))
        geo_list.append(Part.LineSegment(V3, V4))
        geo_list.append(Part.LineSegment(V4, V5))
        geo_list.append(Part.LineSegment(V5, V6))
        geo_list.append(Part.LineSegment(V6, V1))

        con_list = []

        con_list.append(Sketcher.Constraint('Coincident', 0 + offset, 2, 1 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 1 + offset, 2, 2 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 2 + offset, 2, 3 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 3 + offset, 2, 4 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 4 + offset, 2, 5 + offset, 1))
        con_list.append(Sketcher.Constraint('Coincident', 5 + offset, 2, 0 + offset, 1))

        return geo_list, con_list


class CreatePart():
    """
    Create
    """

    def GetResources(self):
        """
        TODO
        """
        return {"Pixmap": "My_Command_Icon",  # the name of a svg file available in the resources
                "MenuText": "Testing object",
                "ToolTip": "Create random object"}

    def Activated(self):
        """
        TODO
        """
        doc = App.activeDocument()
        group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Model")
        dimensions = App.ActiveDocument.getObject("Dimensions")

        stair_thick = dimensions.get('stair_thick')
        side_width = dimensions.get('side_width')
        num_of_stairs = 10

        sides = []
        for i in range(0, 2):
            name = "side_" + str(i)

            side = App.ActiveDocument.addObject('Part::Extrusion', name + "_bd")
            side.Base = App.ActiveDocument.getObject(name)
            side.DirMode = "Normal"
            side.DirLink = None
            if i == 0:
                side.LengthFwd = side_width
            else:
                side.LengthFwd = -side_width

            side.LengthRev = 0.000000000000000
            side.Solid = True
            side.Reversed = False
            side.Symmetric = False
            side.TaperAngle = 0.000000000000000
            side.TaperAngleRev = 0.000000000000000

            group.addObject(side)
            sides.append(name + "_bd")

        for i in range(0, num_of_stairs):
            name = "stair_" + str(i)

            stair = App.ActiveDocument.addObject('Part::Extrusion', name + "_bd")
            stair.Base = App.ActiveDocument.getObject(name)
            stair.DirMode = "Normal"
            stair.DirLink = None
            stair.LengthFwd = -stair_thick
            stair.LengthRev = 0.000000000000000
            stair.Solid = True
            stair.Reversed = False
            stair.Symmetric = False
            stair.TaperAngle = 0.000000000000000
            stair.TaperAngleRev = 0.000000000000000

            group.addObject(stair)

        doc.recompute()

        App.Console.PrintMessage('Done!\n')

    def IsActive(self):
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True


class CutStairs():
    """
    Cut
    """

    def GetResources(self):
        """
        TODO
        """
        return {"Pixmap": "My_Command_Icon",  # the name of a svg file available in the resources
                "MenuText": "Testing object",
                "ToolTip": "Create random object"}

    def Activated(self):
        """
        TODO
        """
        doc = App.activeDocument()
        group = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Cuts")
        # dimensions = App.ActiveDocument.getObject("Dimensions")

        num_of_stairs = 10

        for i in range(0, num_of_stairs):
            name = "stair_" + str(i)
            cut1 = App.activeDocument().addObject("Part::Cut", "side_0_bd" + str(i))
            if i == 0:
                cut1.Base = eval("App.activeDocument()." + "side_0_bd")
            else:
                cut1.Base = eval("App.activeDocument()." + "side_0_bd" + str(i - 1))
            cut1.Tool = eval("App.activeDocument()." + name + "_bd")
            # eval("Gui.ActiveDocument." + name + "_bd" + ".Visibility=True")

        group.addObject(cut1)
        doc.recompute()

        App.Console.PrintMessage('Cutting stairs done!\n')

    def IsActive(self):
        """
        Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True


Gui.addCommand("Create dimensions", GenerateSpreadsheet())
Gui.addCommand("Create sketches", GenerateSketches())
Gui.addCommand("Create part", CreatePart())
Gui.addCommand("Cut stairs", CutStairs())
