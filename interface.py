from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Widget, Button, PopUpDialog
from asciimatics.effects import Print, Scroll
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
import sys

from padberg import Padberg

LABEL_DISCR = ["This is a python implementation of Harriet Padberg's 1963 Thesis,",
               "\"Computer Composed Canon and Free Fugue\".",
               "Enter a body of text below, and the program will convert it into serialist garbage."]

class TextFormFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         int(screen.height),
                         int(screen.width),
                         has_shadow=True,
                         title="PyPadberg")

        layout_discr = Layout([1, 18, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\n".join(LABEL_DISCR), height=5, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())

        layout_textbox = Layout([1, 18, 1], fill_frame=True)
        self.add_layout(layout_textbox)
        layout_textbox.add_widget(TextBox(Widget.FILL_FRAME, name="IT", label="Write Something!", 
            on_change=self._on_change), 1)

        layout_div_2 = Layout([100])
        self.add_layout(layout_div_2)
        layout_div_2.add_widget(Divider())

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        self._reset_button = Button("Reset", self._reset)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("Submit", self._submit), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)

        self.fix()

    def _on_change(self):
        self.save()
        # changed = False
        # for key, value in self.data.items():
        #     if key not in form_data or form_data[key] != value:
        #         changed = True
        #         break
        # self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene()

    def _submit(self):
        self.save(validate=True)
        self.text = self.data["IT"]
        raise NextScene()

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


class Interface:

    def __init__(self):
        pass
    
    def _designation(self, screen, scene):
        scenes = []
        effects = [
            Print(screen,
                  ColourImageFile(screen, "ibm1620.jpg", screen.height,
                                  uni=screen.unicode_aware),
                  screen.height,
                  speed=1,
                  stop_frame=(21 + screen.height)*2),
            Scroll(screen, 3)
        ]
        scenes.append(Scene(effects))
        scenes.append(Scene([TextFormFrame(screen)], -1))
        screen.play(scenes, stop_on_resize=True, start_scene=scene)

    def run(self):
        last_scene = None
        while True:
            try:
                Screen.wrapper(self._designation, catch_interrupt=False, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
