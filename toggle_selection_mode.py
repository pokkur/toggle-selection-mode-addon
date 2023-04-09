bl_info = {
    "name": "Toggle Selection Mode",
    "author": "pokkur",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Toolbar > Toggle Selection Mode",
    "description": "Toggle between vertex, edge, and face selection modes",
    "category": "Mesh",
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty

class ToggleSelectionModeOperator(Operator):
    bl_idname = "mesh.toggle_selection_mode"
    bl_label = "Toggle Selection Mode"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        current_mode = context.tool_settings.mesh_select_mode[:]
        # Vertex to Edge
        if current_mode == (True, False, False):
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            context.workspace.status_text_set("Edge Select")
        # Edge to Face
        elif current_mode == (False, True, False):
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            context.workspace.status_text_set("Face Select")
        # Face to Vertex
        elif current_mode == (False, False, True):
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            context.workspace.status_text_set("Vertex Select")
        return {'FINISHED'}

class ToggleSelectionModePreferences(AddonPreferences):
    bl_idname = __name__
    keymap: StringProperty(
        name="Keymap",
        default="SPACE",
        description="Key used to toggle selection mode"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "keymap")

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    keymap = bpy.context.preferences.addons[__name__].preferences.keymap

    if kc:
        km = kc.keymaps.new(name="Mesh", space_type='EMPTY', region_type='WINDOW')
        kmi = km.keymap_items.new(ToggleSelectionModeOperator.bl_idname, keymap, 'PRESS')

def unregister_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    keymap = bpy.context.preferences.addons[__name__].preferences.keymap

    if kc:
        km = kc.keymaps["Mesh"]
        for kmi in km.keymap_items:
            if kmi.idname == ToggleSelectionModeOperator.bl_idname:
                km.keymap_items.remove(kmi)

def register():
    bpy.utils.register_class(ToggleSelectionModeOperator)
    bpy.utils.register_class(ToggleSelectionModePreferences)
    register_keymaps()

def unregister():
    unregister_keymaps()
    bpy.utils.unregister_class(ToggleSelectionModeOperator)
    bpy.utils.unregister_class(ToggleSelectionModePreferences)

if __name__ == "__main__":
    register()
