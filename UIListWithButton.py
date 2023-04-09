import bpy
import collections
import json


def select_current_selset(self, context):
    """Selection"""
    if len(context.scene.sj_sel_set_items) is 0:
        return None

    index = int(self.selection_set_dplist)
    obj_list = json.loads(
        context.scene.sj_sel_set_items[index].object_list,
        object_pairs_hook=collections.OrderedDict)

    if len(obj_list) is 0:
        return None

    bpy.ops.object.select_all(action='DESELECT')
    for obj in obj_list:
        if bpy.context.scene.objects.get(obj):
            bpy.data.objects[obj].select_set(True)

    if bpy.context.scene.objects.get(obj_list[0]):
        context.view_layer.objects.active = bpy.data.objects[obj_list[0]]
    return None


def get_selection_list_items(scene, context):
    """Get a list of selection sets"""
    items = []
    for i, item in enumerate(context.scene.sj_sel_set_items, 0):
        items.append((str(i), item.set_name, ''))

    if len(items) is 0:
        items.append(('0', 'Selection Set Empty.', ''))

    return items


def get_sel_set_item_name(self):
    return self["set_name"]


def set_sel_set_item_name(self, value):
    self["set_name"] = value
    current_names = [i.set_name for i in bpy.context.scene.sj_sel_set_items]
    current_names.remove(value)
    new_name = value
    cnt = 1
    while new_name in current_names:
        new_name = '{}.{:03d}'.format(new_name.split('.')[0], cnt)
        cnt = cnt + 1
    self["set_name"] = new_name
    return None


class SJSelectionSetItem(bpy.types.PropertyGroup):
    """Selection set collection item"""

    set_name: bpy.props.StringProperty(
        default="SelectionSet",
        name="Selection set name",
        get=get_sel_set_item_name,
        set=set_sel_set_item_name
    )
    object_list: bpy.props.StringProperty(
        name="Objects in set",
        description="",
        default="")


class SJSelectionSetProperties(bpy.types.PropertyGroup):
    """Define custom properties"""
    bl_label = ""

    selection_set_dplist: bpy.props.EnumProperty(
        items=get_selection_list_items,
        name="Selection Set",
        description="Select objects from the Selected Set",
        update=select_current_selset
    )


class SJSelectionSetAddItem(bpy.types.Operator):
    """Add new selection set"""
    bl_idname = "sj_selection_set.add_selset"
    bl_label = ""
    bl_description = "Add new Selection Set from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """"""
        if len(bpy.context.selected_objects) is 0:
            msg = 'Please Select any object.'

            def draw(self, context):
                self.layout.label(text=msg)

            bpy.context.window_manager.popup_menu(draw, title="Info", icon="INFO")
            self.report({'INFO'}, msg)
            return {'FINISHED'}
        new_item = context.scene.sj_sel_set_items.add()

        current_names = [i.set_name for i in context.scene.sj_sel_set_items]
        new_name = 'SelectionSet'
        cnt = 1
        while new_name in current_names:
            new_name = 'SelectionSet.{:03d}'.format(cnt)
            cnt = cnt + 1
        new_item.set_name = new_name

        index = len(context.scene.sj_sel_set_items) - 1
        context.scene.sj_sel_set_item_index = index
        context.scene.sj_sel_set_props.selection_set_dplist = str(index)

        obj_list = [obj.name for obj in bpy.context.selected_objects]
        new_item.object_list = json.dumps(obj_list)

        get_selection_list_items(self, context)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}


class SJSelectionSetSelect(bpy.types.Operator):
    r"""Select objects in selected set"""
    bl_idname = "sj_selection_set.select"
    bl_label = ""
    bl_description = "Select objects in selected set"

    index: bpy.props.IntProperty(name="Objects in set", default=0)

    @classmethod
    def poll(cls, context):
        return context.scene.sj_sel_set_items

    def execute(self, context):
        r""""""
        obj_list = json.loads(
            context.scene.sj_sel_set_items[self.index].object_list,
            object_pairs_hook=collections.OrderedDict)

        if len(obj_list) is 0:
            return {'FINISHED'}

        bpy.ops.object.select_all(action='DESELECT')

        for obj in obj_list:
            if bpy.context.scene.objects.get(obj):
                bpy.data.objects[obj].select_set(True)

        if context.scene.objects.get(obj_list[0]):
            context.view_layer.objects.active = bpy.data.objects[obj_list[0]]
        return {'FINISHED'}


########### UI ##########

class SJSelectionSetEditList(bpy.types.UIList):
    r""""""

    def draw_item(
            self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = 'OBJECT_HIDDEN'

        layout.prop(item, "set_name", text="", emboss=False, icon=custom_icon)
        op = layout.operator("sj_selection_set.select", icon="RESTRICT_SELECT_OFF")
        op.index = index


class SJSelectionSetListPanel(bpy.types.Panel):
    """UI"""
    bl_label = "Selection Set List"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "SJT"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        sub_row = row.row(align=True)
        sub_row.operator("sj_selection_set.add_selset", text="New Selection Set")
        layout.separator(factor=0.5)

        row = layout.row()
        row.template_list("SJSelectionSetEditList", "Sel Set List", context.scene, "sj_sel_set_items", context.scene,
                          "sj_sel_set_item_index", rows=1)


classes = (
    SJSelectionSetItem,
    SJSelectionSetProperties,
    SJSelectionSetAddItem,
    SJSelectionSetSelect,
    SJSelectionSetEditList,
    SJSelectionSetListPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sj_sel_set_props = bpy.props.PointerProperty(type=SJSelectionSetProperties)
    bpy.types.Scene.sj_sel_set_items = bpy.props.CollectionProperty(type=SJSelectionSetItem)
    bpy.types.Scene.sj_sel_set_item_index = bpy.props.IntProperty(name="Objects in set", default=0)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sj_sel_set_props
    del bpy.types.Object.action_list_index


if __name__ == "__main__":
    register()