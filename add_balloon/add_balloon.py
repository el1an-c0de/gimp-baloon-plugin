#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl
from gi.repository import GObject
from gi.repository import GLib

import gettext
import json
import os
import sys

textdomain = 'add_balloon'
locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
gettext.bindtextdomain(textdomain, locale_dir)
gettext.textdomain(textdomain)
_ = gettext.gettext
def N_(message): return message

presets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'add_balloon_presets.json')

def load_presets():
    if os.path.exists(presets_path):
        try:
            with open(presets_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_presets(presets):
    with open(presets_path, 'w', encoding='utf-8') as f:
        json.dump(presets, f, indent=2, ensure_ascii=False)

class AddBalloon(Gimp.PlugIn):
    def do_set_i18n(self, procname):
        return True, textdomain, locale_dir

    def do_query_procedures(self):
        return [ "plug-in-add-balloon" ]

    def do_create_procedure(self, name):
        Gegl.init(None)

        procedure = Gimp.ImageProcedure.new(self, name,
                                       Gimp.PDBProcType.PLUGIN,
                                       self.run, None)

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask (Gimp.ProcedureSensitivityMask.DRAWABLE)

        procedure.set_menu_label(N_("Add Balloon..."))
        procedure.set_icon_name(GimpUi.ICON_GEGL)
        procedure.add_menu_path('<Image>/Select')

        procedure.set_documentation(N_("Add a text for balloon"),
                                    N_("Add a text layer with a chosen font and color inside the selection"),
                                    name)
        procedure.set_attribution("Z-UO", "Z-UO", "2022")

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if len(drawables) != 1:
            msg = _(f"Procedure '{procedure.get_name()}' only works with one drawable.")
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
        else:
            drawable = drawables[0]

        # if the active drawable is a layer mask, it isn't a direct child of
        # the image's item tree, so use the mask's owner layer instead
        if drawable.is_layer_mask():
            selected_layers = image.get_selected_layers()
            if len(selected_layers) != 1:
                msg = _(f"Select a single layer (not a layer mask) before using this plugin.")
                error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
                return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)
            layer = selected_layers[0]
        else:
            layer = drawable

        # check if selection exist
        flag, non_empty, x1, y1, x2, y2 = Gimp.Selection.bounds(image)
        if not non_empty:
            msg = _(f"The selection is empty, create a selection box and precede with the use of this plugin.")
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)

        if run_mode == Gimp.RunMode.INTERACTIVE:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gdk

            GimpUi.init("add_balloon.py")

            dialog = GimpUi.Dialog(use_header_bar=True,
                                   title=_("Add Balloon"),
                                   role="add_balloon-Python3")
            dialog.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)

            geometry = Gdk.Geometry()
            geometry.min_aspect = 0.5
            geometry.max_aspect = 1.0
            dialog.set_geometry_hints(None, geometry, Gdk.WindowHints.ASPECT)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            dialog.get_content_area().add(box)
            box.show()

            # Label text content
            label = Gtk.Label(label=_('Text:'))
            box.pack_start(label, False, False, 1)
            label.show()

            # scroll area for text
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_vexpand (True)
            scrolled.set_min_content_height(120)
            scrolled.set_min_content_width(300)
            box.pack_start(scrolled, True, True, 1)
            scrolled.show()

            # text content box
            text_content = Gtk.TextView()
            contents = 'text'
            buffer = text_content.get_buffer()
            buffer.set_text(contents, -1)
            scrolled.add(text_content)
            text_content.show()

            # Improve UI
            font_chooser = Gtk.FontChooserWidget()
            box.pack_start(font_chooser, False, False, 1)
            font_chooser.show()

            # text color
            color_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            box.pack_start(color_box, False, False, 1)
            color_box.show()

            color_label = Gtk.Label(label=_('Color:'))
            color_box.pack_start(color_label, False, False, 1)
            color_label.show()

            color_button = Gtk.ColorButton()
            color_button.set_rgba(Gdk.RGBA(0.0, 0.0, 0.0, 1.0))
            color_box.pack_start(color_button, False, False, 1)
            color_button.show()

            # text outline (stroke)
            outline_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            box.pack_start(outline_box, False, False, 1)
            outline_box.show()

            outline_check = Gtk.CheckButton(label=_("Outline"))
            outline_box.pack_start(outline_check, False, False, 1)
            outline_check.show()

            outline_color_button = Gtk.ColorButton()
            outline_color_button.set_rgba(Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            outline_color_button.set_sensitive(False)
            outline_box.pack_start(outline_color_button, False, False, 1)
            outline_color_button.show()

            outline_width_label = Gtk.Label(label=_("Width:"))
            outline_box.pack_start(outline_width_label, False, False, 1)
            outline_width_label.show()

            outline_width_spin = Gtk.SpinButton()
            outline_width_spin.set_adjustment(Gtk.Adjustment(value=2.0, lower=0.1, upper=200.0, step_increment=0.5, page_increment=5.0))
            outline_width_spin.set_digits(1)
            outline_width_spin.set_sensitive(False)
            outline_box.pack_start(outline_width_spin, False, False, 1)
            outline_width_spin.show()

            def on_outline_toggled(check):
                enabled = check.get_active()
                outline_color_button.set_sensitive(enabled)
                outline_width_spin.set_sensitive(enabled)

            outline_check.connect('toggled', on_outline_toggled)

            # presets (font + size + color templates)
            presets = load_presets()

            def refresh_preset_combo(select=None):
                preset_combo.remove_all()
                for preset_name in sorted(presets):
                    preset_combo.append_text(preset_name)
                if select is not None:
                    model = preset_combo.get_model()
                    for i, row in enumerate(model):
                        if row[0] == select:
                            preset_combo.set_active(i)
                            break

            def on_preset_selected(combo):
                name = combo.get_active_text()
                if name is None or name not in presets:
                    return
                preset = presets[name]
                font_chooser.set_font(preset['font'])
                r, g, b, a = preset['color']
                color_button.set_rgba(Gdk.RGBA(r, g, b, a))

                outline = preset.get('outline')
                outline_check.set_active(bool(outline))
                if outline:
                    orr, og, ob, oa = outline['color']
                    outline_color_button.set_rgba(Gdk.RGBA(orr, og, ob, oa))
                    outline_width_spin.set_value(outline['width'])

            def on_save_preset(button):
                name = preset_name_entry.get_text().strip()
                if not name:
                    return
                rgba = color_button.get_rgba()
                preset = {
                    'font': font_chooser.get_font(),
                    'color': [rgba.red, rgba.green, rgba.blue, rgba.alpha],
                }
                if outline_check.get_active():
                    outline_rgba = outline_color_button.get_rgba()
                    preset['outline'] = {
                        'color': [outline_rgba.red, outline_rgba.green, outline_rgba.blue, outline_rgba.alpha],
                        'width': outline_width_spin.get_value(),
                    }
                presets[name] = preset
                save_presets(presets)
                preset_name_entry.set_text('')
                refresh_preset_combo(select=name)

            def on_delete_preset(button):
                name = preset_combo.get_active_text()
                if name and name in presets:
                    del presets[name]
                    save_presets(presets)
                    refresh_preset_combo()

            preset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            box.pack_start(preset_box, False, False, 1)
            preset_box.show()

            preset_label = Gtk.Label(label=_('Template:'))
            preset_box.pack_start(preset_label, False, False, 1)
            preset_label.show()

            preset_combo = Gtk.ComboBoxText()
            refresh_preset_combo()
            preset_combo.connect('changed', on_preset_selected)
            preset_box.pack_start(preset_combo, True, True, 1)
            preset_combo.show()

            delete_preset_button = Gtk.Button(label=_("Delete"))
            delete_preset_button.connect('clicked', on_delete_preset)
            preset_box.pack_start(delete_preset_button, False, False, 1)
            delete_preset_button.show()

            save_preset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            box.pack_start(save_preset_box, False, False, 1)
            save_preset_box.show()

            preset_name_entry = Gtk.Entry()
            preset_name_entry.set_placeholder_text(_("Template name"))
            save_preset_box.pack_start(preset_name_entry, True, True, 1)
            preset_name_entry.show()

            save_preset_button = Gtk.Button(label=_("Save template"))
            save_preset_button.connect('clicked', on_save_preset)
            save_preset_box.pack_start(save_preset_button, False, False, 1)
            save_preset_button.show()

            # TODO add spinner for waiting

            while (True):
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    # TODO enable spinner and lock all other values

                    # layer position
                    position = image.get_item_position(layer)

                    # add text layer
                    buffer = text_content.get_buffer()
                    text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)

                    font_str = font_chooser.get_font()
                    font_tokens = font_str.split(' ')
                    font_size = float(font_tokens[-1])
                    font_name = ' '.join(font_tokens[:-1])

                    # GIMP's font list uses its own names (eg. "Sans-serif",
                    # "DejaVu Sans Book"), which don't always match the name
                    # given by the GTK font chooser, so fall back to a search.
                    font = Gimp.Font.get_by_name(font_name)
                    if font is None:
                        candidates = Gimp.fonts_get_list(font_name)
                        for suffix in (' Book', ' Regular', ''):
                            match = next((c for c in candidates if c.get_name() == font_name + suffix), None)
                            if match is not None:
                                font = match
                                break
                        else:
                            font = candidates[0] if candidates else Gimp.context_get_font()

                    text_layer = Gimp.TextLayer.new(image, text, font, font_size, Gimp.Unit.pixel())
                    image.insert_layer(text_layer, layer.get_parent(), position)

                    # set text color
                    rgba = color_button.get_rgba()
                    color = Gegl.Color.new("black")
                    color.set_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
                    text_layer.set_color(color)

                    # set outline (stroke), before resizing/cropping so the
                    # stroke width is included in the final bounds
                    if outline_check.get_active():
                        outline_rgba = outline_color_button.get_rgba()
                        outline_color = Gegl.Color.new("black")
                        outline_color.set_rgba(outline_rgba.red, outline_rgba.green,
                                               outline_rgba.blue, outline_rgba.alpha)
                        text_layer.set_outline(Gimp.TextOutline.STROKE_FILL)
                        text_layer.set_outline_color(outline_color)
                        text_layer.set_outline_width(outline_width_spin.get_value(), Gimp.Unit.pixel())
                    else:
                        text_layer.set_outline(Gimp.TextOutline.NONE)

                    # wrap the text inside the selection box instead of running
                    # off in a single line, and crop the layer to the actual
                    # rendered text so it can be centered precisely.
                    # Pass the text layer itself as the crop reference: a NULL
                    # reference makes GIMP use the whole flattened image to
                    # detect "empty borders", which finds none on a busy
                    # background and leaves the layer nearly uncropped.
                    text_layer.set_justification(Gimp.TextJustification.CENTER)
                    text_layer.resize(x2 - x1, y2 - y1)
                    image.set_selected_layers([text_layer])
                    image.autocrop_selected_layers(text_layer)

                    # center text layer inside the selection. Must be an
                    # absolute move: transform_translate() adds a delta to
                    # the layer's current position (which is no longer (0,0)
                    # after autocrop), so it would overshoot the center.
                    cx = (x1 + x2)/2 - text_layer.get_width()/2
                    cy = (y1 + y2)/2 - text_layer.get_height()/2
                    text_layer.set_offsets(round(cx), round(cy))


                    dialog.destroy()
                    break
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL,
                                                       GLib.Error())

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(AddBalloon.__gtype__, sys.argv)
