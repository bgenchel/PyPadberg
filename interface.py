from asciimatics.widgets import Frame, Text, TextBox, Layout, Label, Divider, Widget, Button, PopUpDialog, ListBox, \
    RadioButtons
from asciimatics.effects import Print, Scroll, Julia
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
import sys

from padberg import Padberg

LABEL_DISCR = ["\nThis is a python implementation of Harriet Padberg's 1963 Thesis,",
               "\n\"Computer Composed Canon and Free Fugue\".\n",
               "Enter a body of text below, and the program will convert it into serialist garbage."]

PADBERG = Padberg()

class TextFormFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         int(screen.height),
                         int(screen.width),
                         has_shadow=True,
                         title="PyPadberg")

        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\n".join(LABEL_DISCR), height=8, align="^"), 1)

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
        raise NextScene("text_entry")

    def _submit(self):
        self.save(validate=True)
        PADBERG.process_text(self.data["IT"][0])
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


class ProcessingFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                        int(screen.height),
                        int(screen.width),
                        on_load=self._reload_list,
                        hover_focus=True,
                        can_scroll=False,
                        title="PyPadberg")

        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\nProcessing Logs", height=3, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())
        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            PADBERG.get_summary(),
            name="processing-log",
            add_scroll_bar=True,
        )
        layout = Layout([1, 15, 1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view, 1)

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Continue", self._continue), 1)

        self.fix()
        # self._on_pick()

    def _reload_list(self, new_value=None):
        self._list_view.options = PADBERG.get_summary()
        self._list_view.value = new_value

    def _continue(self):
        raise NextScene()


# a button what sound to use
# save midi
# number of voices
# play button
form_data = {'sound_choice': "one",
             'num_voices': 1}

class FinalFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                        int(screen.height * 2 // 3),
                        int(screen.width * 2 // 3),
                        data=form_data,
                        has_shadow=True,
                        title="PyPadberg")
        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("Whatchawannado. YOU MUST DECIDE NOW. THE CLOCK IS TICKING", height=3, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())

        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(RadioButtons([("one", "one"),
                                        ("two", "two"),
                                        ("three", "three")],
                                       label="Choose a Sound:",
                                       name="sound_choice",
                                       on_change=self._on_change), 1)

        layout.add_widget(RadioButtons([("1", 1), ("2", 2), ("3", 3), ("4", 4)],
                                       label="How Many Voices?:",
                                       name="num_voices",
                                       on_change=self._on_change), 1)

        layout_div_2 = Layout([100])
        self.add_layout(layout_div_2)
        layout_div_2.add_widget(Divider())

        layout_buttons = Layout([1, 1, 1, 1])
        self.add_layout(layout_buttons)
        layout_buttons.add_widget(Button("Play", self._play), 0)
        layout_buttons.add_widget(Button("Save", self._save), 1)
        layout_buttons.add_widget(Button("Make Another", self._make_another), 2)
        layout_buttons.add_widget(Button("Quit", self._quit), 3)
        # layout2.add_widget(Button("Submit", self._submit), 1)
        # self._reset_button = Button("Reset", self._reset)
        # layout2.add_widget(self._reset_button, 0)
        self.save()
        self.fix()

    def _on_change(self):
        self.save()

    def _play(self):
        import pdb
        pdb.set_trace()
        PADBERG.play(self.data["sound_choice"], self.data["num_voices"])

    def _save(self):
        self.pud = PopUpDialog(self._screen, "Save Your Creation (MIDI)", ["Save", "Cancel"], on_close=self._saveit)
        layout = Layout([1, 18, 1])
        self.pud.add_layout(layout)
        layout.add_widget(Text(label="Filename (no ext):", name="fname", on_change=self._on_change))
        self._scene.add_effect(self.pud)
        PADBERG.save()


    def _saveit(self):
        if self.pud.data["fname"][0]:
            PADBERG.save(title=self.pud.data["fname"][0])
        else:
            PADBERG.save()

    def _make_another(self):
        raise NextScene("text_entry")

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

    def _seq(self, screen, scene):
        scenes = []
        # banner_pos = (screen.width - 100) // 2 + 20
        # static_image = [
        #     Print(screen,
        #           ColourImageFile(screen, "ibm1620.jpg", screen.height, uni=screen.unicode_aware),
        #           y=0,
        #           speed=1,
        #           stop_frame=(21 + screen.height)*2),
        #     Print(screen,
        #           FigletText("PyPadberg", "banner"),
        #           screen.height - 8, x=banner_pos,
        #           colour=Screen.COLOUR_BLACK,
        #           bg=Screen.COLOUR_BLACK,
        #           speed=1),
        #     Print(screen,
        #           FigletText("PyPadberg", "banner"),
        #           screen.height - 9, x=(banner_pos + 1),
        #           colour=Screen.COLOUR_WHITE,
        #           bg=Screen.COLOUR_WHITE,
        #           speed=1),
        # ]
        # scenes.append(Scene(static_image, name="intro2"))
        scenes.append(Scene([TextFormFrame(screen)], -1, name="text_entry"))
        scenes.append(Scene([ProcessingFrame(screen)], -1, name="display_processing"))
        final_frame = [Julia(screen), FinalFrame(screen)]
        scenes.append(Scene(final_frame, -1, name="end_menu"))
        screen.play(scenes, stop_on_resize=True, start_scene=scene)

    def run(self):
        last_scene = None
        while True:
            try:
                Screen.wrapper(self._seq, catch_interrupt=False, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
