from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Widget, Button, PopUpDialog, ListBox, \
    RadioButtons
from asciimatics.effects import Print, Scroll
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
        raise NextScene()

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


class FinalFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen,
                                        int(screen.height * 2 // 3),
                                        int(screen.width * 2 // 3),
                                        data=form_data,
                                        has_shadow=True,
                                        name="My Form")
        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        self._reset_button = Button("Reset", self._reset)
        layout.add_widget(TextBox(5,
                            label="My First Box:",
                            name="TA",
                            on_change=self._on_change), 1)
        layout.add_widget(
            Text(label="Alpha:",
                 name="TB",
                 on_change=self._on_change,
                 validator="^[a-zA-Z]*$"), 1)
        layout.add_widget(
            Text(label="Number:",
                 name="TC",
                 on_change=self._on_change,
                 validator="^[0-9]*$"), 1)
        layout.add_widget(
            Text(label="Email:",
                 name="TD",
                 on_change=self._on_change,
                 validator=self._check_email), 1)
        layout.add_widget(Divider(height=2), 1)
        layout.add_widget(Label("Group 2:"), 1)
        layout.add_widget(RadioButtons([("Option 1", 1),
                                        ("Option 2", 2),
                                        ("Option 3", 3)],
                                       label="A Longer Selection:",
                                       name="Things",
                                       on_change=self._on_change), 1)
        layout.add_widget(CheckBox("Field 1",
                                   label="A very silly long name for fields:",
                                   name="CA",
                                   on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 2", name="CB", on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 3", name="CC", on_change=self._on_change), 1)
        layout.add_widget(Divider(height=3), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in form_data or form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

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
        NextScene()


# a button what sound to use
# save midi
# number of voices
# play button

class FinalFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         int(screen.height),
                         int(screen.width),
                         data=form_data,
                         has_shadow=True,
                         name="PyPadberg")
        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("Whatchawannado. YOU MUST DECIDE NOW. THE CLOCK IS TICKING", height=3, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())

        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(RadioButtons([("1", 1),
                                        ("2", 2),
                                        ("3", 3)],
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
        layout2.add_widget(Button("Play", self._play), 0)
        layout2.add_widget(Button("Save", self._save), 1)
        layout2.add_widget(Button("Make Another", self._make_another), 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        # layout2.add_widget(Button("Submit", self._submit), 1)
        # self._reset_button = Button("Reset", self._reset)
        # layout2.add_widget(self._reset_button, 0)

        layout.add_widget(Label("Group 1:"), 1)
        layout.add_widget(TextBox(5,
                                  label="My First Box:",
                                  name="TA",
                                  on_change=self._on_change), 1)
        layout.add_widget(
            Text(label="Alpha:",
                 name="TB",
                 on_change=self._on_change,
                 validator="^[a-zA-Z]*$"), 1)
        layout.add_widget(
            Text(label="Number:",
                 name="TC",
                 on_change=self._on_change,
                 validator="^[0-9]*$"), 1)
        layout.add_widget(
            Text(label="Email:",
                 name="TD",
                 on_change=self._on_change,
                 validator=self._check_email), 1)
        layout.add_widget(Divider(height=2), 1)
        layout.add_widget(Label("Group 2:"), 1)
        layout.add_widget(RadioButtons([("Option 1", 1),
                                        ("Option 2", 2),
                                        ("Option 3", 3)],
                                       label="A Longer Selection:",
                                       name="Things",
                                       on_change=self._on_change), 1)
        layout.add_widget(CheckBox("Field 1",
                                   label="A very silly long name for fields:",
                                   name="CA",
                                   on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 2", name="CB", on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 3", name="CC", on_change=self._on_change), 1)
        layout.add_widget(Divider(height=3), 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in form_data or form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

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
        banner_pos = (screen.width - 100) // 2 + 1
        static_image = [
            Print(screen,
                  ColourImageFile(screen, "ibm1620.jpg", screen.height, uni=screen.unicode_aware),
                  y=0,
                  speed=1,
                  stop_frame=(21 + screen.height)*2),
            Print(screen,
                  FigletText("PyPadberg", "banner"),
                  screen.height - 8, x=banner_pos,
                  colour=Screen.COLOUR_BLACK,
                  bg=Screen.COLOUR_BLACK,
                  speed=1),
            Print(screen,
                  FigletText("PyPadberg", "banner"),
                  screen.height - 9, x=(banner_pos + 1),
                  colour=Screen.COLOUR_WHITE,
                  bg=Screen.COLOUR_WHITE,
                  speed=1),
        ]
        scenes.append(Scene(static_image, name="intro2"))
        scenes.append(Scene([TextFormFrame(screen)], -1, name="main"))
        scenes.append(Scene([ProcessingFrame(screen)], -1, name="display_processing"))
        screen.play(scenes, stop_on_resize=True, start_scene=scene)

    def run(self):
        last_scene = None
        while True:
            try:
                Screen.wrapper(self._seq, catch_interrupt=False, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
