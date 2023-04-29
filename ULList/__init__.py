import bpy
from . import ui
from . import Logger
from . import props

bl_info = {
	"name": "UL List Example",
	"description": "",
	"author": "",
	"version": (3, 0, 1),
	"blender": (3, 2, 0),
	"location": "Object > UL List Example",
	"warning": "", # used for warning icon and text in add-ons panel
	"category": ""
}

def register():
    props.register()
    ui.register()
    Logger.register()
    
def unregister():
    props.unregister()
    ui.unregister()
    Logger.unregister()