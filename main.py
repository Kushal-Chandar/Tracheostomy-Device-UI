from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.uix.button import Button
import math
import random

class ResponsiveComponent(BoxLayout):
    """Base class for responsive components"""
    def __init__(self, title="Component", bg_color=(0.15, 0.15, 0.15, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(10)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.title = title
        self.bg_color = bg_color
        
        # Create background
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Border
            Color(0.3, 0.3, 0.3, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
            
        self.bind(pos=self.update_bg, size=self.update_bg)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)

class RespiratoryComponent(ResponsiveComponent):
    """Respiratory Rate Component"""
    def __init__(self, **kwargs):
        super().__init__(title="Respiratory Rate", bg_color=(0.1, 0.15, 0.2, 1), **kwargs)
        
        # Left side - Value display
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        
        # Icon placeholder
        icon_widget = Widget(size_hint_y=0.4)
        with icon_widget.canvas:
            Color(0.3, 0.7, 1, 1)  # Light blue
            self.icon_circle = Ellipse(size=(dp(40), dp(40)))
        icon_widget.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='RESPIRATORY\nRATE',
            font_size=sp(12),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='center',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value
        self.value_label = Label(
            text='24',
            font_size=sp(36),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        )
        
        value_layout.add_widget(icon_widget)
        value_layout.add_widget(title_label)
        value_layout.add_widget(self.value_label)
        
        # Right side - Graph
        self.graph_widget = Widget()
        with self.graph_widget.canvas:
            Color(0.3, 0.7, 1, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)
        
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)
        
        # Animation
        Clock.schedule_interval(self.update_data, 0.1)
        
    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(20)
        center_y = widget.y + widget.height / 2 - dp(20)
        self.icon_circle.pos = (center_x, center_y)
        
    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return
            
        # Generate sine wave for respiratory pattern
        points = []
        for i in range(0, int(self.graph_widget.width - dp(20)), 4):
            x = self.graph_widget.x + dp(10) + i
            y = (self.graph_widget.y + self.graph_widget.height/2 + 
                 math.sin(i * 0.02) * self.graph_widget.height/4)
            points.extend([x, y])
            
        if len(points) > 2:
            self.graph_line.points = points
            
    def update_data(self, dt):
        # Simulate changing respiratory rate
        new_value = 22 + random.randint(-2, 4)
        self.value_label.text = str(new_value)

class CO2Component(ResponsiveComponent):
    """CO2 Level Component"""
    def __init__(self, **kwargs):
        super().__init__(title="CO2 Level", bg_color=(0.15, 0.2, 0.1, 1), **kwargs)
        
        # Left side - Value display
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        
        # Icon placeholder
        icon_widget = Widget(size_hint_y=0.4)
        with icon_widget.canvas:
            Color(0.5, 1, 0.3, 1)  # Light green
            self.icon_rect = Rectangle(size=(dp(40), dp(30)))
        icon_widget.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='ETCO2\nLEVEL',
            font_size=sp(12),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='center',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value
        self.value_label = Label(
            text='42',
            font_size=sp(36),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        )
        
        value_layout.add_widget(icon_widget)
        value_layout.add_widget(title_label)
        value_layout.add_widget(self.value_label)
        
        # Right side - Graph (square wave pattern)
        self.graph_widget = Widget()
        with self.graph_widget.canvas:
            Color(0.5, 1, 0.3, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)
        
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)
        
        Clock.schedule_interval(self.update_data, 0.2)
        
    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(20)
        center_y = widget.y + widget.height / 2 - dp(15)
        self.icon_rect.pos = (center_x, center_y)
        
    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return
            
        # Generate square wave pattern
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
        super().__init__(title="SpO2", bg_color=(0.2, 0.1, 0.15, 1), **kwargs)
        
        # Left side - Value display
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        
        # Icon placeholder
        icon_widget = Widget(size_hint_y=0.4)
        with icon_widget.canvas:
            Color(1, 0.4, 0.4, 1)  # Light red
            self.icon_circle = Ellipse(size=(dp(35), dp(35)))
        icon_widget.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='SPO2\nSATURATION',
            font_size=sp(12),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='center',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value with percentage
        self.value_label = Label(
            text='92%',
            font_size=sp(36),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        )
        
        value_layout.add_widget(icon_widget)
        value_layout.add_widget(title_label)
        value_layout.add_widget(self.value_label)
        
        # Right side - Pulse wave
        self.graph_widget = Widget()
        with self.graph_widget.canvas:
            Color(1, 0.4, 0.4, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)
        
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)
        
        Clock.schedule_interval(self.update_data, 0.15)
        
    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(17.5)
        center_y = widget.y + widget.height / 2 - dp(17.5)
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
                    y = base_y + (j / (pulse_width * 0.1)) * self.graph_widget.height * 0.3
                elif j < pulse_width * 0.2:  # Peak
                    y = base_y + self.graph_widget.height * 0.3
                elif j < pulse_width * 0.4:  # Falling edge
                    y = base_y + self.graph_widget.height * 0.3 * (1 - (j - pulse_width * 0.2) / (pulse_width * 0.2))
                else:  # Baseline
                    y = base_y
                    
                points.extend([x, y])
                
        if len(points) > 2:
            self.graph_line.points = points
            
    def update_data(self, dt):
        new_value = 90 + random.randint(-2, 5)
        self.value_label.text = f'{new_value}%'

class HeartRateComponent(ResponsiveComponent):
    """Heart Rate Component"""
    def __init__(self, **kwargs):
        super().__init__(title="Heart Rate", bg_color=(0.2, 0.15, 0.1, 1), **kwargs)
        
        # Left side - Value display
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        
        # Icon placeholder (heart shape approximation)
        icon_widget = Widget(size_hint_y=0.4)
        with icon_widget.canvas:
            Color(1, 0.6, 0.2, 1)  # Orange
            self.icon_heart = Ellipse(size=(dp(25), dp(25)))
            self.icon_heart2 = Ellipse(size=(dp(25), dp(25)))
        icon_widget.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='HEART\nRATE',
            font_size=sp(12),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='center',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value with BPM
        self.value_label = Label(
            text='98',
            font_size=sp(36),
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        )
        
        value_layout.add_widget(icon_widget)
        value_layout.add_widget(title_label)
        value_layout.add_widget(self.value_label)
        
        # Right side - ECG pattern
        self.graph_widget = Widget()
        with self.graph_widget.canvas:
            Color(1, 0.6, 0.2, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)
        
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)
        
        Clock.schedule_interval(self.update_data, 0.6)  # Slower for heart rate
        
    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(12.5)
        center_y = widget.y + widget.height / 2 - dp(12.5)
        # Simple heart shape with two circles
        self.icon_heart.pos = (center_x - dp(8), center_y + dp(5))
        self.icon_heart2.pos = (center_x + dp(8), center_y + dp(5))
        
    def update_graph(self, *args):
        if self.graph_widget.width < 100:
            return
            
        # Generate ECG pattern
        points = []
        beat_width = (self.graph_widget.width - dp(20)) / 3
        baseline_y = self.graph_widget.y + self.graph_widget.height / 2
        
        for i in range(3):
            x_start = self.graph_widget.x + dp(10) + i * beat_width
            
            # ECG pattern: P-QRS-T
            beat_points = [
                (0, 0), (0.1, 0.2), (0.2, 0), (0.3, 0),  # P wave
                (0.35, -0.3), (0.4, 1), (0.45, -0.5), (0.5, 0),  # QRS complex
                (0.6, 0), (0.7, 0.3), (0.8, 0), (1, 0)  # T wave
            ]
            
            for j, (x_ratio, y_ratio) in enumerate(beat_points):
                x = x_start + x_ratio * beat_width
                y = baseline_y + y_ratio * self.graph_widget.height * 0.2
                points.extend([x, y])
                
        if len(points) > 2:
            self.graph_line.points = points
            
    def update_data(self, dt):
        new_value = 95 + random.randint(-5, 8)
        self.value_label.text = str(new_value)

class ResponsiveStackApp(App):
    def build(self):
        # Configure for 800x480 display
        from kivy.config import Config
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        Config.set('graphics', 'resizable', True)  # Set to False for production
        
        # Main container
        root = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        
        # Black background
        with root.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_bg, pos=self._update_bg)
        
        # Create 4 components with equal height distribution
        components = [
            RespiratoryComponent(size_hint_y=0.25),
            CO2Component(size_hint_y=0.25),
            SpO2Component(size_hint_y=0.25),
            HeartRateComponent(size_hint_y=0.25)
        ]
        
        for component in components:
            root.add_widget(component)
            
        return root
    
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

if __name__ == '__main__':
    ResponsiveStackApp().run()