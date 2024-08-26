import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from localization import _

SHORTCUTS_WINDOW = '<?xml version="1.0" encoding="UTF-8"?>\
<interface>\
  <requires lib="gtk" version="4.0"/>\
  <template class="ShortcutsWindow" parent="GtkShortcutsWindow">\
    <property name="modal">true</property>\
    <child>\
      <object class="GtkShortcutsSection">\
        <property name="section-name">shortcuts</property>\
        <property name="max-height">10</property>\
        <child>\
          <object class="GtkShortcutsGroup">\
            <property name="title" translatable="true" context="ShortcutsWindow"></property>\
           <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.about</property>\
                <property name="accelerator">F1</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.shortcuts-window</property>\
                <property name="accelerator">&lt;primary&gt;&amp;s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.sync</property>\
                <property name="accelerator">&lt;primary&gt;&amp;question</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.quit</property>\
                <property name="accelerator">&lt;primary&gt;&amp;q</property>\
              </object>\
            </child>\
          </object>\
        </child>\
      </object>\
    </child>\
  </template>\
</interface>' % (_["about_app"], _["sync_manually"], _["keyboard_shortcuts"], _["quit"])

# Load the shortcuts window
@Gtk.Template(string=SHORTCUTS_WINDOW) # from shortcuts_window.py
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
