import os
import FreeCADGui as Gui
import FreeCAD as App
from freecad.gridfinity_plus_workbench import CreateBaseplate, CreateBin 

translate=App.Qt.translate
QT_TRANSLATE_NOOP=App.Qt.QT_TRANSLATE_NOOP

ICONPATH = os.path.join(os.path.dirname(__file__), "resources//icons//")
TRANSLATIONSPATH = os.path.join(os.path.dirname(__file__), "resources", "translations")

# Add translations path
Gui.addLanguagePath(TRANSLATIONSPATH)
Gui.updateLocale()

class GridifintyPlusWorkbench(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """
    MenuText = translate("Workbench", "GridifintyPlusWorkbench")
    ToolTip = translate("Workbench", "GridifintyPlusWorkbench")
    Icon = os.path.join(ICONPATH, "layout-grid-line.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """

        App.Console.PrintMessage(translate(
            "Log",
            "Switching to gridfinity_plus_workbench") + "\n")
        
        self.list = ["CreateBaseplateCommand", "CreateBinCommand"] # a list of command names created in the line above
        self.appendToolbar("Gridfinity+ tools", self.list) # creates a new toolbar with your commands
        self.appendMenu("Gridfintiy+", self.list) # creates a new menu

    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        App.Console.PrintMessage(translate(
            "Log",
            "Workbench gridfinity_plus_workbench activated.") + "\n")

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        App.Console.PrintMessage(translate(
            "Log",
            "Workbench gridfinity_plus_workbench de-activated.") + "\n")


Gui.addWorkbench(GridifintyPlusWorkbench())
