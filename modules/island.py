import os
from os import truncate
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.button import Button
from fabric.widgets.stack import Stack
from fabric.widgets.eventbox import EventBox
from fabric.widgets.x11 import X11Window as Window
from fabric.utils.helpers import FormattedString, truncate
from modules.corners import MyCorner
from gi.repository import GLib, Gdk
import modules.icons as icons
#from modules.power import PowerMenu
#from modules.rofi import Rofi
#from modules.dashboard import Dashboard
from utils.i3 import ActiveWindows

class Island(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="island",
            layer="top",
            geometry="top",
            type_hint="normal",
            margin="-8px -4px -8px -4px",
            keyboard_mode="none",
            visible=True,
            all_visible=True,
        )
        
        # self.power = PowerMenu(island=self)
        # self.rofi = Rofi(notch=self)
        # self.dashboard = Dashboard(notch=self)
        
        self.active_windows = ActiveWindows()
        
        self.compact_stack = Stack(
            name="island-compact-stack",
            v_expand=True,
            h_expand=True,
            transition_type="slide-up-down",
            transition_duration=100,
            children=[
                self.active_windows
            ]
        )

        self.compact = EventBox(
            name="island-compact",
            visible=True,
            child=self.compact_stack
        )
        
        self.compact.connect("enter-notify-event", self.on_button_enter)
        self.compact.connect("leave-notify-event", self.on_button_leave)
        self.compact.connect("button-press-event", lambda *_: self.open("dashboard"))
        
        self.stack = Stack(
            name="island-content",
            v_expand=True,
            h_expand=True,
            transition_type="crossfade",
            transition_duration=100,
            children=[
                self.compact,
                # self.power,
                # self.rofi,
                # self.dashboard
            ]
        )

        self.corner_left = Box(
            name="island-corner-left",
            orientation="v",
            children=[
                MyCorner("top-right"),
                Box(),
            ]
        )

        self.corner_right = Box(
            name="island-corner-right",
            orientation="v",
            children=[
                MyCorner("top-left"),
                Box(),
            ]
        )

        self.island_box = CenterBox(
            name="island-box",
            orientation="h",
            h_align="center",
            v_align="center",
            start_children=Box(
                children=[
                    self.corner_left,
                ],
            ),
            center_children=self.stack,
            end_children=Box(
                children=[
                    self.corner_right,
                ]
            )
        )

        self.add(self.island_box)
        self.hidden = False
        
        self.show_all()
        
        self.add_keybinding("Escape", lambda *_: self.close_island())
        
    def on_button_enter(self, widget, event):
        window = widget.get_window()
        if window:
            window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))

    def on_button_leave(self, widget, event):
        window = widget.get_window()
        if window:
            window.set_cursor(None)
           
    def open(self, widget):
        #self.set_keyboard_mode("exclusive")
        
        if self.hidden:
            self.island_box.remove_style_class("hidden")
            self.island_box.add_style_class("hideshow")
            
        widgets = {
            "power": self.power,
            "rofi": self.rofi,
            "dashboard": self.dashboard
        }
        
        for style in widgets.keys():
            self.stack.remove_style_class(style)
        for w in widgets.values():
            w.remove_style_class("open")
            
        if widget in widgets:
            self.stack.add_style_class(widget)
            self.stack.set_visible_child(widgets[widget])
            widgets[widget].add_style_class("open")
            
            if widget == "rofi":
                self.rofi.open_launcher()
                self.rofi.search_entry.set_text("")
                self.rofi.search_entry.grab_focus()

            # if widget == "dashboard" and self.dashboard.stack.get_visible_child() != self.dashboard.stack.get_children()[0]:
            #     self.dashboard.stack.set_visible_child(self.dashboard.stack.get_children()[0])
        else:
            self.stack.set_visible_child(self.dashboard)
        
    def close(self):
        #self.set_keyboard_mode("none")
        self.rofi.launcher_box.remove(self.rofi.scrolled_window)

        if self.hidden:
            self.island_box.remove_style_class("hideshow")
            self.island_box.add_style_class("hidden")

        for widget in [self.power, self.rofi, self.dashboard]:
             widget.remove_style_class("open")
        for style in ["power", "rofi", "dashboard"]:
            self.stack.remove_style_class(style)
            
        self.stack.set_visible_child(self.compact)
        
    def toggle_hidden(self):
        self.hidden = not self.hidden
        if self.hidden:
            self.island_box.add_style_class("hidden")
        else:
            self.island_box.remove_style_class("hidden")

    
