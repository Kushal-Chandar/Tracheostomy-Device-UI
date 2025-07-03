from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp, sp
import math
import random
from kivy.properties import ListProperty
import os
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButtonBehavior



class ResponsiveComponent(BoxLayout):
    """Base class for responsive medical components"""

    def __init__(
        self,
        title="Component",
        bg_color=(0.15, 0.15, 0.15, 1),
        icon_color=(1, 1, 1, 1),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = dp(15)
        self.padding = [dp(20), dp(15), dp(20), dp(15)]
        self.title = title
        self.bg_color = bg_color
        self.icon_color = icon_color

        # Create rounded background
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(8)]
            )

        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class RespiratoryComponent(ResponsiveComponent):
    """Respiratory Rate Component"""

    def __init__(self, **kwargs):
        super().__init__(
            title="Respiratory Rate (RR)",
            bg_color=(0.08, 0.12, 0.16, 1),
            icon_color=(0.4, 0.8, 1, 1),
            **kwargs,
        )

        # Left side - Icon and title
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.25, spacing=dp(5))

        # Icon widget
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            # Lungs icon representation
            self.icon_ellipse1 = Ellipse(size=(dp(15), dp(25)))
            self.icon_ellipse2 = Ellipse(size=(dp(15), dp(25)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)

        # Title
        title_label = Label(
            text="Respiratory Rate (RR):",
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign="left",
            valign="bottom",
            size_hint_y=0.3,
        )
        title_label.bind(size=title_label.setter("text_size"))

        # Value
        self.value_label = Label(
            text="24",
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign="left",
            size_hint_y=0.6,
        )
        self.value_label.bind(size=self.value_label.setter("text_size"))

        # Unit
        unit_label = Label(
            text="bpm",
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign="left",
            valign="top",
            size_hint_y=0.2,
        )
        unit_label.bind(size=unit_label.setter("text_size"))

        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)

        # Value section
        value_layout = BoxLayout(orientation="vertical", size_hint_x=0.2)
        value_layout.add_widget(self.value_label)
        value_layout.add_widget(unit_label)

        # Right side - Graph
        self.graph_widget = Widget(size_hint_x=0.55)
        with self.graph_widget.canvas:
            Color(*self.icon_color, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)

        self.add_widget(left_layout)
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)

        # Animation
        Clock.schedule_interval(self.update_data, 0.1)

    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2
        center_y = widget.y + widget.height / 2
        self.icon_ellipse1.pos = (center_x - dp(20), center_y - dp(12))
        self.icon_ellipse2.pos = (center_x + dp(5), center_y - dp(12))

    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return

        # Generate sine wave for respiratory pattern
        points = []
        for i in range(0, int(self.graph_widget.width - dp(20)), 3):
            x = self.graph_widget.x + dp(10) + i
            y = (
                self.graph_widget.y
                + self.graph_widget.height / 2
                + math.sin(i * 0.015) * self.graph_widget.height / 3
            )
            points.extend([x, y])

        if len(points) > 2:
            self.graph_line.points = points

    def update_data(self, dt):
        new_value = 22 + random.randint(-2, 4)
        self.value_label.text = str(new_value)


class CO2Component(ResponsiveComponent):
    """CO2 Level Component"""

    def __init__(self, **kwargs):
        super().__init__(
            title="ETCO2",
            bg_color=(0.08, 0.12, 0.16, 1),
            icon_color=(0.3, 1, 0.5, 1),
            **kwargs,
        )

        # Left side - Icon and title
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.25, spacing=dp(5))

        # Icon widget
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            self.co2_text = Rectangle(size=(dp(35), dp(20)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)

        # Title
        title_label = Label(
            text="ETCO2:",
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign="left",
            valign="bottom",
            size_hint_y=0.3,
        )
        title_label.bind(size=title_label.setter("text_size"))

        # Value
        self.value_label = Label(
            text="42",
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign="left",
            size_hint_y=0.6,
        )
        self.value_label.bind(size=self.value_label.setter("text_size"))

        # Unit
        unit_label = Label(
            text="mmHg",
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign="left",
            valign="top",
            size_hint_y=0.2,
        )
        unit_label.bind(size=unit_label.setter("text_size"))

        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)

        # Value section
        value_layout = BoxLayout(orientation="vertical", size_hint_x=0.2)
        value_layout.add_widget(self.value_label)
        value_layout.add_widget(unit_label)

        # Right side - Graph (square wave pattern)
        self.graph_widget = Widget(size_hint_x=0.55)
        with self.graph_widget.canvas:
            Color(*self.icon_color, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)

        self.add_widget(left_layout)
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)

        Clock.schedule_interval(self.update_data, 0.2)

    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(17)
        center_y = widget.y + widget.height / 2 - dp(10)
        self.co2_text.pos = (center_x, center_y)

    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return

        # Generate square wave pattern for CO2
        points = []
        segment_width = (self.graph_widget.width - dp(20)) / 6
        base_y = self.graph_widget.y + self.graph_widget.height * 0.3
        high_y = self.graph_widget.y + self.graph_widget.height * 0.7

        for i in range(6):
            x_start = self.graph_widget.x + dp(10) + i * segment_width
            x_mid = x_start + segment_width * 0.3
            x_end = x_start + segment_width

            if i == 0:
                points.extend([x_start, base_y])
            points.extend([x_mid, base_y, x_mid, high_y, x_end, high_y, x_end, base_y])

        if len(points) > 2:
            self.graph_line.points = points

    def update_data(self, dt):
        new_value = 40 + random.randint(-3, 6)
        self.value_label.text = str(new_value)


class SpO2Component(ResponsiveComponent):
    """SpO2 Component"""

    def __init__(self, **kwargs):
        super().__init__(
            title="SPO2",
            bg_color=(0.08, 0.12, 0.16, 1),
            icon_color=(0.9, 0.4, 0.9, 1),
            **kwargs,
        )

        # Left side - Icon and title
        left_layout = BoxLayout(orientation="vertical", size_hint_x=0.25, spacing=dp(5))

        # Icon widget
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            self.icon_circle = Ellipse(size=(dp(30), dp(30)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)

        # Title
        title_label = Label(
            text="SPO2:",
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign="left",
            valign="bottom",
            size_hint_y=0.3,
        )
        title_label.bind(size=title_label.setter("text_size"))

        # Value with percentage
        self.value_label = Label(
            text="92",
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign="left",
            size_hint_y=0.6,
        )
        self.value_label.bind(size=self.value_label.setter("text_size"))

        # Unit
        unit_label = Label(
            text="%",
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign="left",
            valign="top",
            size_hint_y=0.2,
        )
        unit_label.bind(size=unit_label.setter("text_size"))

        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)

        # Value section
        value_layout = BoxLayout(orientation="vertical", size_hint_x=0.2)
        value_layout.add_widget(self.value_label)
        value_layout.add_widget(unit_label)

        # Right side - Pulse wave
        self.graph_widget = Widget(size_hint_x=0.55)
        with self.graph_widget.canvas:
            Color(*self.icon_color, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)

        self.add_widget(left_layout)
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)

        Clock.schedule_interval(self.update_data, 0.15)

    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(15)
        center_y = widget.y + widget.height / 2 - dp(15)
        self.icon_circle.pos = (center_x, center_y)

    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return

        # Generate pulse wave pattern
        points = []
        pulse_width = (self.graph_widget.width - dp(20)) / 4
        base_y = self.graph_widget.y + self.graph_widget.height * 0.4

        for i in range(4):
            x_start = self.graph_widget.x + dp(10) + i * pulse_width

            # Pulse pattern points
            for j in range(int(pulse_width)):
                x = x_start + j
                if j < pulse_width * 0.1:  # Rising edge
                    y = (
                        base_y
                        + (j / (pulse_width * 0.1)) * self.graph_widget.height * 0.3
                    )
                elif j < pulse_width * 0.2:  # Peak
                    y = base_y + self.graph_widget.height * 0.3
                elif j < pulse_width * 0.4:  # Falling edge
                    y = base_y + self.graph_widget.height * 0.3 * (
                        1 - (j - pulse_width * 0.2) / (pulse_width * 0.2)
                    )
                else:  # Baseline
                    y = base_y

                points.extend([x, y])

        if len(points) > 2:
            self.graph_line.points = points

    def update_data(self, dt):
        new_value = 90 + random.randint(-2, 5)
        self.value_label.text = str(new_value)


class HeartRateComponent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(180)

        # Background rectangle
        with self.canvas.before:
            Color(148 / 255, 155 / 255, 164 / 255, 0.20)
            self.bg_rect = RoundedRectangle(
                size=self.size, pos=self.pos, radius=[(28, 28)] * 4
            )
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # Main horizontal content container
        content_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            padding=[dp(24), dp(16), dp(24), dp(16)],
        )
        self.add_widget(content_layout)

        # Left section: text content
        left_layout = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(160)
        )
        roboto_bold_path = os.path.join("assets", "Roboto-Bold.ttf")
        title_label = Label(
            text="[b]Heart rate (HR) :[/b]",
            markup=True,
            size_hint=(None, None),
            size=(dp(275), dp(200)),
            color=(126 / 255, 255 / 255, 236 / 255, 1),
            font_name=roboto_bold_path
            if os.path.exists(roboto_bold_path)
            else "Roboto",
            font_size=14,
            halign="left",
            valign="middle",
        )
        title_label.bind(size=title_label.setter("text_size"))

        value_row = BoxLayout(
            orientation="horizontal", spacing=dp(8), size_hint=(1, None), height=dp(38)
        )
        self.value_label = Label(
            text="98",
            font_size=sp(72),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(275), dp(130)),
            halign="right",
            valign="middle",
        )
        self.value_label.bind(size=self.value_label.setter("text_size"))

        value_row.add_widget(self.value_label)

        left_layout.add_widget(title_label)
        left_layout.add_widget(value_row)

        # Graph widget
        self.graph_widget = Widget(size_hint_y=0.80)
        with self.graph_widget.canvas:
            Color(126 / 255, 255 / 255, 236 / 255, 1)
            self.graph_line = Line(width=dp(1.5))
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)

        # Min/Max vertical layout aligned with graph
        min_max_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, 1),
            width=dp(150),
            padding=(dp(50), 0, dp(50), dp(30)),
        )
        self.max_label = Label(
            text="--",
            font_size=sp(16),
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height=dp(90),
            halign="left",
            valign="middle",
        )
        self.max_label.bind(size=self.max_label.setter("text_size"))

        self.min_label = Label(
            text="--",
            font_size=sp(16),
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height=dp(20),
            halign="left",
            valign="middle",
        )
        self.min_label.bind(size=self.min_label.setter("text_size"))

        min_max_layout.add_widget(self.max_label)
        min_max_layout.add_widget(self.min_label)
        graph_layout = BoxLayout(
            orientation="horizontal", spacing=dp(8), padding=[0, 0, dp(90), 0]
        )

        # Set the graph widget to take less horizontal space
        self.graph_widget.size_hint = (0.5, 1)

        # Reorder: min/max comes first (on the left), then the graph
        graph_layout.add_widget(min_max_layout)
        graph_layout.add_widget(self.graph_widget)

        # Add to content layout
        content_layout.add_widget(left_layout)
        content_layout.add_widget(graph_layout)

        # Top-left Icon
        self.icon = Image(
            source="assets/hr.png",
            size_hint=(None, None),
            size=(dp(89), dp(87)),
            pos_hint={"x": 0.01, "top": 0.95},
        )
        self.add_widget(self.icon)

        # Data buffer for dynamic waveform
        self.data_buffer = [random.randint(90, 110) for _ in range(60)]
        self.max_val = max(self.data_buffer)
        self.min_val = min(self.data_buffer)

        Clock.schedule_interval(self.update_data, 0.6)

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_graph(self, *args):
        width = self.graph_widget.width
        height = self.graph_widget.height
        x0 = self.graph_widget.x
        y0 = self.graph_widget.y
        points = []
        baseline = y0 + height * 0.5
        amplitude = height * 0.35

        n = len(self.data_buffer)
        for i, val in enumerate(self.data_buffer):
            x = x0 + i * (width / n)
            y = baseline + ((val - 100) / 10) * amplitude
            points.extend([x, y])
        self.graph_line.points = points

    def update_data(self, dt):
        new_value = 95 + random.randint(-5, 8)
        self.data_buffer.append(new_value)
        if len(self.data_buffer) > 30:
            self.data_buffer.pop(0)
        self.max_val = max(self.data_buffer)
        self.min_val = min(self.data_buffer)
        self.value_label.text = str(new_value)
        self.max_label.text = f"{self.max_val}"
        self.min_label.text = f"{self.min_val}"
        self.update_graph()


class SidebarPanel(BoxLayout):
    """Right sidebar with updated layout and switches"""

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint=(None, 1),  
            width=dp(300),        
            spacing=dp(10),
            padding=dp(20),
            **kwargs,
        )
        self.bind(pos=self.update_graphics, size=self.update_graphics)

        # Top caution section
        caution_section = BoxLayout(
            size_hint=(None, None), size=(dp(300), dp(263)), pos_hint={"center_x": 0.5}
        )
        caution_image = Image(
            source="./assets/Group_8.png",
            size_hint=(None, None),
            size=(dp(300), dp(263)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        caution_section.add_widget(caution_image)
        self.add_widget(caution_section)

        self.add_widget(Widget(size_hint_y=None, height=dp(20)))

        status_section = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(260), dp(240)),
            spacing=dp(10),
            pos_hint={"center_x": 0.5},
        )
        status_section.bind(pos=self.status_section_bg, size=self.status_section_bg)

        status_data = [
            ("assets/Rectangle_35.png", "Full\nBlockage"),
            ("assets/Rectangle_36.png", "Partial\nBlockage"),
            ("assets/Rectangle_37.png", "No\nBlockage"),
        ]

        for image_path, label_text in status_data:
            status_row = BoxLayout(
                orientation="horizontal",
                size_hint=(1, None),
                height=dp(65),
                spacing=dp(10),
                padding=[dp(10), dp(5), dp(10), dp(5)],
            )
            status_image = Image(
                source=image_path,
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                allow_stretch=True,
                keep_ratio=True,
            )
            status_label = Label(
                text=label_text,
                font_size=dp(14),
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle",
            )
            status_label.bind(size=status_label.setter("text_size"))
            status_row.add_widget(status_image)
            status_row.add_widget(status_label)
            status_section.add_widget(status_row)

        self.add_widget(status_section)
        self.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Toggle switches
        self.add_widget(self.create_toggle("Saline"))
        self.add_widget(Widget(size_hint_y=None, height=dp(10)))
        self.add_widget(self.create_toggle("Suction"))
        self.add_widget(Widget())

    def create_toggle(self, label_text):
        toggle_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(dp(205), dp(60)),
            spacing=dp(10),
            pos_hint={"center_x": 0.5},
            padding=[dp(10), dp(10), dp(10), dp(10)],
        )

        label = Label(
            text=f"{label_text}: OFF",
            font_size=dp(14),
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))

        toggle_button = Button(
            text="OFF",
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            background_normal="",
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
        )

        def toggle_state(instance):
            if instance.text == "OFF":
                instance.text = "ON"
                instance.background_color = (0, 0.7, 0.3, 1)
                label.text = f"{label_text}: ON"
            else:
                instance.text = "OFF"
                instance.background_color = (0.5, 0.5, 0.5, 1)
                label.text = f"{label_text}: OFF"

        toggle_button.bind(on_press=toggle_state)

        toggle_layout.add_widget(label)
        toggle_layout.add_widget(toggle_button)
        return toggle_layout

    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.6)
            RoundedRectangle(
                pos=(self.x, self.y - dp(4)),
                size=(self.width, self.height + dp(8)),
                radius=[dp(28)],
            )
            Color(148 / 255, 155 / 255, 164 / 255, 0.25)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(28)])
            Color(245 / 255, 245 / 255, 245 / 255, 1)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(28)),
                width=dp(1),
            )

    def status_section_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 0.4)
            RoundedRectangle(
                pos=(instance.x, instance.y - dp(4)),
                size=instance.size,
                radius=[dp(28)],
            )
            Color(148 / 255, 155 / 255, 164 / 255, 0.15)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(28)])
            Color(234 / 255, 234 / 255, 234 / 255, 1)
            Line(
                rounded_rectangle=(
                    instance.x,
                    instance.y,
                    instance.width,
                    instance.height,
                    dp(28),
                ),
                width=0.5,
            )



class ResponsiveStackApp(App):
    def build(self):
        # Configure window
        from kivy.config import Config

        Config.set("graphics", "width", "1280")
        Config.set("graphics", "height", "800")
        Config.set("graphics", "resizable", True)

        # Main horizontal container
        root = BoxLayout(orientation="horizontal", spacing=dp(10), padding=dp(10))

        # Dark background

        with root.canvas.before:
            Color(11 / 255, 15 / 255, 26 / 255, 1)  # This is #0B0F1A in RGB
            self.bg = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_bg, pos=self._update_bg)

        # Left side - Medical components
        components_layout = BoxLayout(orientation="vertical", spacing=dp(8))

        # Create 4 components
        components = [
            RespiratoryComponent(size_hint_y=0.25),
            CO2Component(size_hint_y=0.25),
            SpO2Component(size_hint_y=0.25),
            HeartRateComponent(size_hint_y=0.25),
        ]

        for component in components:
            components_layout.add_widget(component)

        # Right side - Alert sidebar
        sidebar = SidebarPanel()

        root.add_widget(components_layout)
        root.add_widget(sidebar)

        return root

    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size


if __name__ == "__main__":
    ResponsiveStackApp().run()