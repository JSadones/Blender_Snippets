bl_info = {
    "name": "External Data Manager",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > External Data",
    "description": "Manage external data in your Blender projects",
    "category": "Development",
}

import bpy
import os
import json

class ExternalDataPanel(bpy.types.Panel):
    """Creates a Panel in the Sidebar of the 3D View"""
    bl_label = "External Data"
    bl_idname = "VIEW3D_PT_external_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "External Data"

    def draw(self, context):
        layout = self.layout

        # Read the data from the external file
        data = read_data()

        # Display the data in the UI
        for key, value in data.items():
            row = layout.row()
            row.label(text=key)
            row.label(text=value)
            #row.prop(value, "name", text="")

class LoadExternalDataOperator(bpy.types.Operator):
    """Load external data from a JSON file"""
    bl_idname = "external_data.load"
    bl_label = "Load External Data"

    def execute(self, context):
        # Read the data from the external file
        data = read_data()

        # Set the properties in the Blender scene
        for key, value in data.items():
            context.scene[key] = value

        return {'FINISHED'}

class SaveExternalDataOperator(bpy.types.Operator):
    """Save external data to a JSON file"""
    bl_idname = "external_data.save"
    bl_label = "Save External Data"

    def execute(self, context):
        # Get the data from the Blender scene
        data = {}
        for key in context.scene.keys():
            if not key.startswith("_"):
                data[key] = context.scene[key]

        # Write the data to the external file
        with open(get_file_path(), 'w') as f:
            json.dump(data, f, indent=4)

        return {'FINISHED'}

def read_data():
    # Get the file path of the external file
    file_path = get_file_path()

    # Read the data from the external file
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data

def get_file_path():
    # Get the file path of the external file
    project_path = bpy.path.abspath('//')
    file_name = 'external_data.json'
    file_path = os.path.join(project_path, file_name)

    return file_path

def register():
    bpy.utils.register_class(ExternalDataPanel)
    bpy.utils.register_class(LoadExternalDataOperator)
    bpy.utils.register_class(SaveExternalDataOperator)

def unregister():
    bpy.utils.unregister_class(ExternalDataPanel)
    bpy.utils.unregister_class(LoadExternalDataOperator)
    bpy.utils.unregister_class(SaveExternalDataOperator)

if __name__ == "__main__":
    register()
