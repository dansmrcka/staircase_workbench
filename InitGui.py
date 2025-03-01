import FreeCAD
import FreeCADGui


class Staircase (Workbench):
    """This function is executed when the workbench is first activated. """

    import os
    import empty
    path = os.path.dirname(empty.__file__)
    iconPath = os.path.join(path, "icons")

    MenuText = "Staircase workbench"
    ToolTip = "Testing"
    Icon = os.path.join(iconPath, "workbench.svg")

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        import commands  # import here all the needed files that create your FreeCAD commands
        self.list = ["Create dimensions", "Create sketches", "Create part", "Cut stairs", "Create drawings", "reset"]  # a list of command names created in the line above
        self.appendToolbar("Stair toolbar", self.list)  # creates a new toolbar with your commands
        self.appendMenu("Stairs", self.list)  # creates a new menu
        # self.appendMenu(["An existing Menu", "My submenu"], self.list)  # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        print('activating Staircase workbench')
        import commands
        from importlib import reload
        reload(commands)
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands", self.list)  # add commands to the context menu

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(Staircase())
