from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior
from kivy.metrics import dp, sp

import math
import os
import random

import RPi.GPIO as GPIO

# Configuration
BUZZER_PIN = 18

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)


def start_buzzer(freq, duty=50):
    buzzer_pwm.ChangeFrequency(freq)
    buzzer_pwm.start(duty)


def stop_buzzer():
    buzzer_pwm.stop()


def cleanup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    stop_buzzer()


class RespiratoryComponent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(190)

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
            padding=[dp(24), dp(16), dp(24), dp(620)],
        )
        self.add_widget(content_layout)

        # Left section: text content
        left_layout = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(220)
        )
        roboto_bold_path = os.path.join("assets", "Roboto-Bold.ttf")
        title_label = Label(
            text="[b]Respiratory Rate(RR):[/b]",
            markup=True,
            size_hint=(1, None),
            padding=[dp(80), dp(0), dp(0), dp(0)],
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
            width=dp(120),
            padding=(dp(20), 0, dp(50), dp(30)),
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
            orientation="horizontal", spacing=dp(8), padding=[0, 0, dp(80), 0]
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
            source="assets/rr.png",
            size_hint=(None, None),
            size=(dp(89), dp(87)),
            pos_hint={"x": 0.01, "top": 0.95},
        )
        self.add_widget(self.icon)

        # Data buffer
        self.data_buffer = self.generate_waveform()
        Clock.schedule_interval(self.update_data, 0.05)  # 20 FPS

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def generate_waveform(self):
        waveform = []
        cycles = 5  # total breathing cycles (each cycle = inhale + exhale)

        for cycle in range(cycles):
            for i in range(40):  # 40 samples per cycle (2 seconds at 20 FPS)
                t = i / 40.0
                # Smooth sinusoidal wave for breathing
                val = 16 + math.sin(t * 2 * math.pi) * 4  # peak-to-peak: 16
                waveform.append(val)

        return waveform

    def update_data(self, dt):
        # Scroll data
        self.data_buffer = self.data_buffer[1:] + [self.data_buffer[0]]
        new_val = int(self.data_buffer[-1])
        self.value_label.text = str(new_val)
        self.max_label.text = str(int(max(self.data_buffer)))
        self.min_label.text = str(int(min(self.data_buffer)))
        self.update_graph()

    def update_graph(self, *args):
        self.graph_widget.canvas.clear()
        with self.graph_widget.canvas:
            Color(126 / 255, 255 / 255, 236 / 255, 1)
            width = self.graph_widget.width
            height = self.graph_widget.height + dp(120)
            x0 = self.graph_widget.x
            y0 = self.graph_widget.y + dp(420)
            baseline = y0 + height * 0.4  # centered vertically
            amplitude = height * 0.4  # breathing wave needs large amplitude

            n = len(self.data_buffer)
            points = []
            for i, val in enumerate(self.data_buffer):
                x = x0 + i * (width / n)
                y = baseline + ((val - 100) / 10) * amplitude
                points.extend([x, y])

            Line(points=points, width=dp(2))


class CO2Component(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(190)

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
            padding=[dp(24), dp(16), dp(24), dp(422)],
        )
        self.add_widget(content_layout)

        # Left section: text content
        left_layout = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(200)
        )
        roboto_bold_path = os.path.join("assets", "Roboto-Bold.ttf")
        title_label = Label(
            text="[b]ETC02:[/b]",
            markup=True,
            size_hint=(1, None),
            padding=[dp(80), dp(0), dp(0), dp(0)],
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
            padding=(0, 0, dp(50), dp(30)),
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
            orientation="horizontal", spacing=dp(8), padding=[0, 0, dp(80), 0]
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
            source="assets/co2.png",
            size_hint=(None, None),
            size=(dp(89), dp(87)),
            pos_hint={"x": 0.01, "top": 0.95},
        )
        self.add_widget(self.icon)

        # Data buffer
        self.data_buffer = self.generate_waveform()
        Clock.schedule_interval(self.update_data, 0.05)  # 20 FPS

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def generate_waveform(
        self,
        cycles=10,
        plateau_duration=30,
        baseline_duration=10,
        upstroke_duration=10,
        downstroke_duration=8,
    ):
        """
        Generate a normal ETCO2 capnograph waveform for a number of respiratory cycles with proportional durations for each phase.

        Parameters:
        - cycles: Number of respiratory cycles to simulate.
        - plateau_duration: Duration of the alveolar plateau (Phase III) in terms of number of samples.
        - baseline_duration: Duration of the baseline phase (Phase I) in terms of number of samples.
        - upstroke_duration: Duration of the expiratory upstroke phase (Phase II) in terms of number of samples.
        - downstroke_duration: Duration of the inspiratory downstroke phase (Phase IV) in terms of number of samples.

        Returns:
        - A list representing the ETCO2 waveform (in mmHg).
        """
        waveform = []

        for cycle in range(cycles):  # Each cycle represents one breath
            # Phase I – Baseline (0-5 mmHg)
            for _ in range(baseline_duration):  # Baseline duration adjustable
                waveform.append(2)  # Low CO2 level during baseline (0–5 mmHg)

            # Phase II – Expiratory upstroke (5 → 35 mmHg)
            for i in range(
                upstroke_duration
            ):  # Exhalation increase from 5 mmHg to 35 mmHg
                val = 5 + (
                    i * (30 / upstroke_duration)
                )  # Gradual increase in CO2 concentration
                waveform.append(val)

            # Phase III – Alveolar plateau (35–45 mmHg) – Now with adjustable duration
            plateau_value = (
                40  # Alveolar plateau typically around 40 mmHg, can vary between 35-45
            )
            for _ in range(plateau_duration):  # Extended plateau phase
                waveform.append(plateau_value)  # Constant value for alveolar CO2

            # Phase IV – Inspiratory downstroke (45 → 0 mmHg)
            for i in range(
                downstroke_duration
            ):  # Rapid decrease in CO2 as inspiration begins
                val = 45 - (i * (45 / downstroke_duration))  # Drop from 45 to baseline
                waveform.append(val)

            for _ in range(baseline_duration):  # Return to baseline
                waveform.append(2)  # Small return to the baseline CO2 level

        return waveform

    def update_data(self, dt):
        # Scroll data
        self.data_buffer = self.data_buffer[1:] + [self.data_buffer[0]]
        new_val = int(self.data_buffer[-1])
        self.value_label.text = str(new_val)
        self.max_label.text = str(int(max(self.data_buffer)))
        self.min_label.text = str(int(min(self.data_buffer)))
        self.update_graph()

    def update_graph(self, *args):
        self.graph_widget.canvas.clear()
        with self.graph_widget.canvas:
            Color(126 / 255, 255 / 255, 236 / 255, 1)
            width = self.graph_widget.width
            height = self.graph_widget.height + dp(90)
            x0 = self.graph_widget.x
            y0 = self.graph_widget.y + dp(190)
            baseline = y0 + height * 0.75  # higher baseline
            amplitude = height * 0.25

            n = len(self.data_buffer)
            points = []
            for i, val in enumerate(self.data_buffer):
                x = x0 + i * (width / n)
                y = baseline + ((val - 100) / 10) * amplitude
                points.extend([x, y])

            Line(points=points, width=dp(2))


class SpO2Component(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(190)

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
            padding=[dp(24), dp(16), dp(24), dp(224)],
        )
        self.add_widget(content_layout)

        # Left section: text content
        left_layout = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(200)
        )
        roboto_bold_path = os.path.join("assets", "Roboto-Bold.ttf")
        title_label = Label(
            text="[b]SPO2:[/b]",
            markup=True,
            size_hint=(1, None),
            padding=[dp(80), dp(0), dp(0), dp(0)],
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
            padding=(0, 0, dp(50), dp(30)),
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
            orientation="horizontal", spacing=dp(8), padding=[0, 0, dp(80), 0]
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
            source="assets/o2.png",
            size_hint=(None, None),
            size=(dp(89), dp(87)),
            pos_hint={"x": 0.01, "top": 0.95},
        )
        self.add_widget(self.icon)

        # Data buffer
        self.data_buffer = self.generate_waveform()
        Clock.schedule_interval(self.update_data, 0.5)  # 20 FPS

    def _update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def generate_waveform(self):
        # Emulate SpO2 waveform: smooth sine-like peaks
        waveform = []
        for i in range(200):
            t = i / 20.0
            y = math.sin(t * math.pi * 2) * 2  # sine wave
            y += math.exp(-(((t % 1) * 10 - 5) ** 2) / 6) * 5  # pulse peak
            waveform.append(94 + y)
        return waveform

    def update_data(self, dt):
        # Scroll data
        self.data_buffer = self.data_buffer[1:] + [self.data_buffer[0]]
        new_val = int(self.data_buffer[-1])
        self.value_label.text = str(new_val)
        self.max_label.text = str(int(max(self.data_buffer)))
        self.min_label.text = str(int(min(self.data_buffer)))
        self.update_graph()

    def update_graph(self, *args):
        self.graph_widget.canvas.clear()
        with self.graph_widget.canvas:
            Color(126 / 255, 255 / 255, 236 / 255, 1)
            width = self.graph_widget.width
            height = self.graph_widget.height + dp(100)
            x0 = self.graph_widget.x
            y0 = self.graph_widget.y + dp(10)
            baseline = y0 + height * 1
            amplitude = height * 1.2

            n = len(self.data_buffer)
            points = []
            for i, val in enumerate(self.data_buffer):
                x = x0 + i * (width / n)
                y = baseline + ((val - 100) / 10) * amplitude
                points.extend([x, y])

            Line(points=points, width=dp(2))


class HeartRateComponent(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(190)

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
            padding=[dp(24), dp(16), dp(24), dp(26)],
        )
        self.add_widget(content_layout)

        # Left section: text content
        left_layout = BoxLayout(
            orientation="vertical", spacing=dp(4), size_hint_x=None, width=dp(200)
        )
        roboto_bold_path = os.path.join("assets", "Roboto-Bold.ttf")
        title_label = Label(
            text="[b]Heart rate (HR) :[/b]",
            markup=True,
            size_hint=(1, None),
            padding=[dp(80), dp(0), dp(0), dp(0)],
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
            padding=(dp(0), 0, dp(50), dp(30)),
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
            orientation="horizontal", spacing=dp(8), padding=[0, 0, dp(80), 0]
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
        self.data_buffer = [random.randint(80, 100) for _ in range(60)]
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
        baseline = y0 + height * 0.8
        amplitude = height * 0.35

        n = len(self.data_buffer)
        for i, val in enumerate(self.data_buffer):
            x = x0 + i * (width / n)
            y = baseline + ((val - 100) / 10) * amplitude
            points.extend([x, y])
        self.graph_line.points = points

    def update_data(self, dt):
        new_value = 85 + random.randint(-5, 8)
        self.data_buffer.append(new_value)
        if len(self.data_buffer) > 30:
            self.data_buffer.pop(0)
        self.max_val = max(self.data_buffer)
        self.min_val = min(self.data_buffer)
        self.value_label.text = str(new_value)
        self.max_label.text = f"{self.max_val}"
        self.min_label.text = f"{self.min_val}"
        self.update_graph()


# Make image behave like a button
class ClickableImage(ButtonBehavior, Image):
    pass


class ColorBlock(ButtonBehavior, Widget):
    def __init__(
        self,
        color=(1, 1, 1, 1),
        border_color=None,
        corner_radius=20,
        border_width=1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.color = color
        self.border_color = border_color or color
        self.corner_radius = corner_radius
        self.border_width = border_width
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(self.corner_radius)]
            )
            Color(*self.border_color)
            Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(self.corner_radius),
                ),
                width=self.border_width,
            )


class SectionCard(BoxLayout):
    """
    A card with a light-gray rounded background and white border.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(148 / 255, 155 / 255, 164 / 255, 0.15)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
            Color(245 / 255, 245 / 255, 245 / 255, 1)
            self._border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(20)),
                width=1,
            )
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(20),
        )


class SidebarPanel(BoxLayout):
    def __init__(self, status_callback=None, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint=(None, 1),
            width=dp(280),
            **kwargs,
        )

        # panel background + border
        with self.canvas.before:
            Color(148 / 255, 155 / 255, 164 / 255, 0.25)
            self._panel_bg = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[dp(28)]
            )
            Color(245 / 255, 245 / 255, 245 / 255, 1)
            self._panel_border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(28)),
                width=1,
            )
        self.bind(pos=self._upd_panel, size=self._upd_panel)
        self.buzzer_event = None  # will hold the schedule interval
        self._buzzer_stop_ev = None  # will hold the one-time stop callback

        # state & callback
        self.status_callback = status_callback or (lambda label, path: None)
        self.status_blocks = []
        self.active_status = (0.30, 0.73, 0.15, 1)
        self.current_image_path = "assets/no.png"
        self.blink_event = None
        self.blink_state = True

        # build sections
        self._build_caution_card()
        self._build_status_card()
        self._build_toggle_card()

        # default highlight = "No blockage"
        if self.status_blocks:
            blk = self.status_blocks[2]
            blk.color = self.active_status
            blk.border_color = self.active_status
            blk.update_canvas()

        self.buzzer_event = None

    def _upd_panel(self, *args):
        self._panel_bg.pos = self.pos
        self._panel_bg.size = self.size
        self._panel_border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(28),
        )

    # ——— Caution Icon Section ———
    def _build_caution_card(self):
        card = SectionCard(size_hint=(1, None), height=dp(200))
        rl = RelativeLayout()
        img = Image(
            source=self.current_image_path,
            size_hint=(None, None),
            size=(dp(156), dp(156)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        rl.add_widget(img)
        card.add_widget(rl)
        self._caution_image = img
        self.add_widget(card)

    # ——— Status Selection Section ———
    def _build_status_card(self):
        card = SectionCard(
            orientation="vertical",
            spacing=dp(20),
            padding=[dp(40), dp(15), dp(15), dp(30)],
            size_hint=(None, None),
            height=dp(295),
            width=dp(231),
        )
        status_data = [
            ("Full\nblockage", (0.78, 0.17, 0.17, 1), "assets/full.png"),
            ("Partial\nblockage", (0.82, 0.73, 0.41, 1), "assets/partial.png"),
            ("No\nblockage", (0.30, 0.73, 0.15, 1), "assets/no.png"),
        ]
        for text, col, img_path in status_data:
            row = BoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                size_hint_y=None,
                height=dp(65),
            )
            block = ColorBlock(
                color=(0, 0, 0, 0),
                border_color=col,
                size_hint=(None, None),
                size=(dp(73), dp(67)),
                corner_radius=20,
            )
            block.bind(
                on_press=lambda inst,
                lt=text,
                bc=col,
                ip=img_path: self._on_status_press(inst, lt, bc, ip)
            )
            self.status_blocks.append(block)

            lbl = Label(
                text=text,
                font_name="assets/Roboto-Bold.ttf",
                font_size=dp(14),
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle",
            )
            lbl.bind(size=lbl.setter("text_size"))

            row.add_widget(block)
            row.add_widget(lbl)
            card.add_widget(row)

        # wrap in left-margin container
        wrapper = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=dp(295)
        )
        wrapper.add_widget(Widget(size_hint_x=None, width=dp(5)))
        wrapper.add_widget(card)
        wrapper.add_widget(Widget(size_hint_x=None, height=dp(10)))
        self.add_widget(wrapper)

    def _on_status_press(self, inst, label_text, bc, img_path):
        for b in self.status_blocks:
            b.color = (0, 0, 0, 0)
            b.border_color = b.border_color
            b.update_canvas()
        inst.color = bc
        inst.border_color = bc
        inst.update_canvas()
        self.active_status = bc
        self._set_caution_image(img_path)
        self.status_callback(label_text, img_path)

        # cancel any existing buzzer schedules
        if self.buzzer_event:
            Clock.unschedule(self.buzzer_event)
            self.buzzer_event = None
        if self._buzzer_stop_ev:
            Clock.unschedule(self._buzzer_stop_ev)
            self._buzzer_stop_ev = None
        stop_buzzer()

        # start new pattern
        if label_text.startswith("Full"):
            # every 0.6s, start a 0.3s 330Hz beep
            self.buzzer_event = Clock.schedule_interval(self._full_cycle, 0.6)
            # kick off the first immediately
            self._full_cycle(0)
        elif label_text.startswith("Partial"):
            # every 1.8s, start a 0.9s 440Hz beep
            self.buzzer_event = Clock.schedule_interval(self._partial_cycle, 1.8)
            self._partial_cycle(0)
        else:
            # No blockage → ensure silent
            # cleanup()
            stop_buzzer()

    def _full_cycle(self, dt):
        # start 330Hz beep, then schedule its stop in 0.3s
        start_buzzer(330)
        # cancel any pending stop, then schedule a fresh one
        if self._buzzer_stop_ev:
            Clock.unschedule(self._buzzer_stop_ev)
        self._buzzer_stop_ev = Clock.schedule_once(lambda dt: stop_buzzer(), 0.3)

    def _partial_cycle(self, dt):
        # start 440Hz beep, then stop in 0.9s
        start_buzzer(440)
        if self._buzzer_stop_ev:
            Clock.unschedule(self._buzzer_stop_ev)
        self._buzzer_stop_ev = Clock.schedule_once(lambda dt: stop_buzzer(), 0.9)

    # ——— Two Toggles at Bottom ———
    def _build_toggle_card(self):
        container = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(183),
        )
        for label_text in ("Suction", "Saline"):
            card = SectionCard(
                orientation="vertical",
                spacing=dp(10),
                padding=dp(16),
                size_hint=(None, None),
                width=dp(105),
                height=dp(183),
            )
            lbl = Label(
                text=f"{label_text}\nOFF",
                font_name="assets/Roboto-Bold.ttf",
                font_size=dp(13),
                color=(1, 1, 1, 0.8),
                size_hint=(1, None),
                height=dp(50),
                halign="center",
                valign="middle",
            )
            lbl.bind(size=lbl.setter("text_size"))

            toggle = ColorBlock(
                color=(0.2, 0.3, 0.2, 1),
                border_color=(0.2, 0.3, 0.2, 1),
                corner_radius=12,
                size_hint=(None, None),
                size=(dp(72), dp(35)),
            )
            toggle.bind(
                on_press=lambda inst, lb=lbl, lt=label_text: self._toggle_switch(
                    inst, lb, lt
                )
            )

            card.add_widget(lbl)
            card.add_widget(toggle)
            card.add_widget(Widget(size_hint_y=None, height=dp(15)))
            container.add_widget(card)

        # wrap in left-margin container
        wrapper = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=dp(183)
        )
        wrapper.add_widget(Widget(size_hint_x=None, width=dp(5)))
        wrapper.add_widget(container)
        wrapper.add_widget(Widget(size_hint_x=1))
        self.add_widget(wrapper)

    def _toggle_switch(self, inst, lbl, lt):
        if lbl.text.endswith("OFF"):
            inst.color = (0.23, 0.84, 0.07, 1)
            inst.border_color = (0.23, 0.84, 0.07, 1)
            lbl.text = f"{lt}\nON"
        else:
            inst.color = (0.2, 0.3, 0.2, 1)
            inst.border_color = (0.2, 0.3, 0.2, 1)
            lbl.text = f"{lt}\nOFF"
        inst.update_canvas()

    def _set_caution_image(self, path):
        img = self._caution_image
        img.source = path
        img.opacity = 1
        img.reload()
        if self.blink_event:
            self.blink_event.cancel()
            self.blink_event = None
        if "full" in path or "partial" in path:
            self.blink_state = True
            interval = 0.3 if "full" in path else 0.9
            self.blink_event = Clock.schedule_interval(self._blink, interval)

    def _blink(self, dt):
        self.blink_state = not self.blink_state
        self._caution_image.opacity = 1 if self.blink_state else 0


class ResponsiveStackApp(App):
    def build(self):
        # Configure window
        from kivy.config import Config

        Config.set("graphics", "borderless", "1")
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
