from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line, Ellipse, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp, sp
import math
import random

class ResponsiveComponent(BoxLayout):
    """Base class for responsive medical components"""
    def __init__(self, title="Component", bg_color=(0.15, 0.15, 0.15, 1), 
                 icon_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(15)
        self.padding = [dp(20), dp(15), dp(20), dp(15)]
        self.title = title
        self.bg_color = bg_color
        self.icon_color = icon_color
        
        # Create rounded background
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
            
        self.bind(pos=self.update_bg, size=self.update_bg)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class RespiratoryComponent(ResponsiveComponent):
    """Respiratory Rate Component"""
    def __init__(self, **kwargs):
        super().__init__(title="Respiratory Rate (RR)", 
                        bg_color=(0.08, 0.12, 0.16, 1), 
                        icon_color=(0.4, 0.8, 1, 1), **kwargs)
        
        # Left side - Icon and title
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, spacing=dp(5))
        
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
            text='Respiratory Rate (RR):',
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='bottom',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value
        self.value_label = Label(
            text='24',
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign='left',
            size_hint_y=0.6
        )
        self.value_label.bind(size=self.value_label.setter('text_size'))
        
        # Unit
        unit_label = Label(
            text='bpm',
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign='left',
            valign='top',
            size_hint_y=0.2
        )
        unit_label.bind(size=unit_label.setter('text_size'))
        
        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)
        
        # Value section
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
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
            y = (self.graph_widget.y + self.graph_widget.height/2 + 
                 math.sin(i * 0.015) * self.graph_widget.height/3)
            points.extend([x, y])
            
        if len(points) > 2:
            self.graph_line.points = points
            
    def update_data(self, dt):
        new_value = 22 + random.randint(-2, 4)
        self.value_label.text = str(new_value)

class CO2Component(ResponsiveComponent):
    """CO2 Level Component"""
    def __init__(self, **kwargs):
        super().__init__(title="ETCO2", 
                        bg_color=(0.08, 0.12, 0.16, 1), 
                        icon_color=(0.3, 1, 0.5, 1), **kwargs)
        
        # Left side - Icon and title
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, spacing=dp(5))
        
        # Icon widget
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            self.co2_text = Rectangle(size=(dp(35), dp(20)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='ETCO2:',
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='bottom',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value
        self.value_label = Label(
            text='42',
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign='left',
            size_hint_y=0.6
        )
        self.value_label.bind(size=self.value_label.setter('text_size'))
        
        # Unit
        unit_label = Label(
            text='mmHg',
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign='left',
            valign='top',
            size_hint_y=0.2
        )
        unit_label.bind(size=unit_label.setter('text_size'))
        
        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)
        
        # Value section
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
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
        super().__init__(title="SPO2", 
                        bg_color=(0.08, 0.12, 0.16, 1), 
                        icon_color=(0.9, 0.4, 0.9, 1), **kwargs)
        
        # Left side - Icon and title
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, spacing=dp(5))
        
        # Icon widget
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            self.icon_circle = Ellipse(size=(dp(30), dp(30)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='SPO2:',
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='bottom',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value with percentage
        self.value_label = Label(
            text='92',
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign='left',
            size_hint_y=0.6
        )
        self.value_label.bind(size=self.value_label.setter('text_size'))
        
        # Unit
        unit_label = Label(
            text='%',
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign='left',
            valign='top',
            size_hint_y=0.2
        )
        unit_label.bind(size=unit_label.setter('text_size'))
        
        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)
        
        # Value section
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
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
        self.value_label.text = str(new_value)

class HeartRateComponent(ResponsiveComponent):
    """Heart Rate Component"""
    def __init__(self, **kwargs):
        super().__init__(title="Heart Rate", 
                        bg_color=(0.08, 0.12, 0.16, 1), 
                        icon_color=(0.3, 1, 0.3, 1), **kwargs)
        
        # Left side - Icon and title
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, spacing=dp(5))
        
        # Icon widget (heart shape)
        icon_container = Widget(size_hint_y=0.4)
        with icon_container.canvas:
            Color(*self.icon_color)
            self.icon_heart = Ellipse(size=(dp(20), dp(20)))
            self.icon_heart2 = Ellipse(size=(dp(20), dp(20)))
        icon_container.bind(size=self.update_icon_pos, pos=self.update_icon_pos)
        
        # Title
        title_label = Label(
            text='Heart rate (HR):',
            font_size=sp(11),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='bottom',
            size_hint_y=0.3
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Value
        self.value_label = Label(
            text='98',
            font_size=sp(48),
            color=(1, 1, 1, 1),
            bold=True,
            halign='left',
            size_hint_y=0.6
        )
        self.value_label.bind(size=self.value_label.setter('text_size'))
        
        # Unit
        unit_label = Label(
            text='bpm',
            font_size=sp(12),
            color=(0.5, 0.5, 0.5, 1),
            halign='left',
            valign='top',
            size_hint_y=0.2
        )
        unit_label.bind(size=unit_label.setter('text_size'))
        
        left_layout.add_widget(icon_container)
        left_layout.add_widget(title_label)
        
        # Value section
        value_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
        value_layout.add_widget(self.value_label)
        value_layout.add_widget(unit_label)
        
        # Right side - ECG pattern
        self.graph_widget = Widget(size_hint_x=0.55)
        with self.graph_widget.canvas:
            Color(*self.icon_color, 0.8)
            self.graph_line = Line(width=2)
        self.graph_widget.bind(size=self.update_graph, pos=self.update_graph)
        
        self.add_widget(left_layout)
        self.add_widget(value_layout)
        self.add_widget(self.graph_widget)
        
        Clock.schedule_interval(self.update_data, 0.6)
        
    def update_icon_pos(self, widget, *args):
        center_x = widget.x + widget.width / 2 - dp(10)
        center_y = widget.y + widget.height / 2 - dp(10)
        # Simple heart shape with two circles
        self.icon_heart.pos = (center_x - dp(8), center_y + dp(3))
        self.icon_heart2.pos = (center_x + dp(8), center_y + dp(3))
        
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
                (0, 0), (0.1, 0.2), (0.2, 0), (0.3, 0),
                (0.35, -0.3), (0.4, 1), (0.45, -0.5), (0.5, 0),
                (0.6, 0), (0.7, 0.3), (0.8, 0), (1, 0)
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

class AlertButton(Button):
    """Custom alert button with proper styling"""
    def __init__(self, alert_type="warning", **kwargs):
        super().__init__(**kwargs)
        self.alert_type = alert_type
        self.size_hint_y = None
        self.height = dp(60)
        
        # Remove default button styling
        self.background_color = (0, 0, 0, 0)
        
        # Colors based on alert type
        colors = {
            "critical": (0.9, 0.1, 0.1, 1),
            "warning": (1, 0.5, 0.1, 1),
            "normal": (0.3, 0.3, 0.3, 1),
            "info": (0.2, 0.6, 0.9, 1)
        }
        
        self.alert_color = colors.get(alert_type, colors["normal"])
        
        with self.canvas.before:
            Color(*self.alert_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
            
        self.bind(pos=self.update_bg, size=self.update_bg)
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class SidebarPanel(BoxLayout):
    """Right sidebar with alert buttons"""
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint_x=None, width=dp(120), 
                        spacing=dp(10), padding=dp(10), **kwargs)
        
        # Background
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Critical Alert
        critical_btn = AlertButton(
            text="!",
            font_size=sp(24),
            color=(1, 1, 1, 1),
            alert_type="critical"
        )
        
        # Status indicators
        status_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # Full Blockage
        full_Blockage = AlertButton(
            text="Full\nBlockage",
            font_size=sp(10),
            color=(1, 1, 1, 1),
            alert_type="critical",
            halign="center"
        )
        full_Blockage.text_size = (dp(100), None)
        
        # Partial Blockage
        partial_Blockage = AlertButton(
            text="Partial\nBlockage",
            font_size=sp(10),
            color=(1, 1, 1, 1),
            alert_type="normal",
            halign="center"
        )
        partial_Blockage.text_size = (dp(100), None)
        
        # No Blockage
        no_Blockage = AlertButton(
            text="No\nBlockage",
            font_size=sp(10),
            color=(1, 1, 1, 1),
            alert_type="info",
            halign="center"
        )
        no_Blockage.text_size = (dp(100), None)
        
        self.add_widget(critical_btn)
        self.add_widget(Widget(size_hint_y=0.2))  # Spacer
        self.add_widget(full_Blockage)
        self.add_widget(partial_Blockage)
        self.add_widget(no_Blockage)
        self.add_widget(Widget())  # Flexible spacer
        
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class ResponsiveStackApp(App):
    def build(self):
        # Configure window
        from kivy.config import Config
        Config.set('graphics', 'width', '900')
        Config.set('graphics', 'height', '500')
        Config.set('graphics', 'resizable', True)
        
        # Main horizontal container
        root = BoxLayout(orientation='horizontal', spacing=dp(10), padding=dp(10))
        
        # Dark background
        with root.canvas.before:
            Color(0.02, 0.02, 0.02, 1)
            self.bg = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self._update_bg, pos=self._update_bg)
        
        # Left side - Medical components
        components_layout = BoxLayout(orientation='vertical', spacing=dp(8))
        
        # Create 4 components
        components = [
            RespiratoryComponent(size_hint_y=0.25),
            CO2Component(size_hint_y=0.25),
            SpO2Component(size_hint_y=0.25),
            HeartRateComponent(size_hint_y=0.25)
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

if __name__ == '__main__':
    ResponsiveStackApp().run()