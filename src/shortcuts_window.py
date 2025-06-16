import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from localization import *

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
                <property name="action-name">app.open-wiki</property>\
                <property name="accelerator">F1</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.save-config</property>\
                <property name="accelerator">&lt;primary&gt;&amp;s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.import-config</property>\
                <property name="accelerator">&lt;primary&gt;&amp;i</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.m_sync_with_key</property>\
                <property name="accelerator">&lt;primary&gt;&amp;m</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.shortcuts</property>\
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
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.ms-dialog</property>\
                <property name="accelerator">&lt;primary&gt;&lt;shift&gt;&amp;m</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.items-dialog</property>\
                <property name="accelerator">&lt;primary&gt;&lt;shift&gt;&amp;i</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.set-dialog</property>\
                <property name="accelerator">&lt;primary&gt;&lt;shift&gt;&amp;s</property>\
              </object>\
            </child>\
            <child>\
              <object class="GtkShortcutsShortcut">\
                <property name="title" translatable="true" context="ShortcutsWindow">%s</property>\
                <property name="action-name">app.cloud-dialog</property>\
                <property name="accelerator">&lt;primary&gt;&lt;shift&gt;&amp;c</property>\
              </object>\
            </child>\
          </object>\
        </child>\
      </object>\
    </child>\
  </template>\
</interface>' % (_["open_wiki"], _["save_config"], _["import_from_file"], _["sync_manually"], _["keyboard_shortcuts"], _["quit"], _["more_options"], _["items_for_archive"], _["set_up_sync_file"], _["connect_cloud_storage"])

# Load the shortcuts window
@Gtk.Template(string=SHORTCUTS_WINDOW)
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
