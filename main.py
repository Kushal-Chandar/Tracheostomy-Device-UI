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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import ListProperty

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

class SidebarPanel(BoxLayout):
    """Right sidebar with exact dimensions matching your design"""
    
    def __init__(self, **kwargs):
        super().__init__(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(247), dp(718)),  # Main container dimensions as specified
            spacing=dp(10),
            padding=dp(20),
            **kwargs
        )
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        
        # Top caution section
        caution_section = BoxLayout(
            size_hint=(None, None),
            size=(dp(200), dp(163)),
            pos_hint={'center_x': 0.5}
        )
        
        caution_image = Image(
            source='./assets/Group_8.png',
            size_hint=(None, None),
            size=(dp(200), dp(163)),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        caution_section.add_widget(caution_image)
        self.add_widget(caution_section)
        
        # Spacer between sections
        self.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Status section container (holds all three status items)
        status_section = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(205), dp(300)),  # Reduced height from 378 to 300
            spacing=dp(15),  # Reduced spacing from 20 to 15
            pos_hint={'center_x': 0.5}
        )
        status_section.bind(pos=self.status_section_bg, size=self.status_section_bg)

        # Status items data
        status_data = [
            ('assets/Rectangle_35.png', 'Full\nBlockage'),
            ('assets/Rectangle_36.png', 'Partial\nBlockage'),
            ('assets/Rectangle_37.png', 'No\nBlockage')
        ]
        
        # Create status items
        for image_path, label_text in status_data:
            status_row = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height=dp(75),  # Reduced height from 90 to 75
                spacing=dp(15),
                padding=[dp(10), dp(10), dp(10), dp(10)]
            )
            
            status_image = Image(
                source=image_path,
                size_hint=(None, None),
                size=(dp(69), dp(63)),
                allow_stretch=True,
                keep_ratio=True
            )
            
            status_label = Label(
                text=label_text,
                font_size=dp(14),
                color=(1, 1, 1, 1),
                halign='left',
                valign='middle'
            )
            status_label.bind(size=status_label.setter('text_size'))
            
            status_row.add_widget(status_image)
            status_row.add_widget(status_label)
            status_section.add_widget(status_row)

        self.add_widget(status_section)
        
        # Spacer between status section and new rectangles
        self.add_widget(Widget(size_hint_y=None, height=dp(10)))
        
        # Rectangle 1
        rect1 = BoxLayout(
            size_hint=(None, None),
            size=(dp(205), dp(60)),
            pos_hint={'center_x': 0.5}
        )
        rect1.bind(pos=self.rect_bg, size=self.rect_bg)
        
        rect1_label = Label(
            text='Rect 1',
            font_size=dp(14),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        rect1_label.bind(size=rect1_label.setter('text_size'))
        rect1.add_widget(rect1_label)
        self.add_widget(rect1)
        
        # Small spacer between rectangles
        self.add_widget(Widget(size_hint_y=None, height=dp(10)))
        
        # Rectangle 2
        rect2 = BoxLayout(
            size_hint=(None, None),
            size=(dp(205), dp(60)),
            pos_hint={'center_x': 0.5}
        )
        rect2.bind(pos=self.rect_bg, size=self.rect_bg)
        
        rect2_label = Label(
            text='Rect 2',
            font_size=dp(14),
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        rect2_label.bind(size=rect2_label.setter('text_size'))
        rect2.add_widget(rect2_label)
        self.add_widget(rect2)
        
        # Flexible bottom spacer
        self.add_widget(Widget())

    def update_graphics(self, *args):
        """Draw the main container background and styling"""
        self.canvas.before.clear()
        with self.canvas.before:
            # --- Inset shadow simulation ---
            Color(0, 0, 0, 0.6)  # Black with 60% opacity
            RoundedRectangle(
                pos=(self.x, self.y - dp(4)),  # Offset shadow down by 4px
                size=(self.width, self.height + dp(8)),  # Slightly taller for shadow effect
                radius=[dp(28)]
            )
            
            # --- Main background ---
            Color(148/255, 155/255, 164/255, 0.25)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(28)]
            )
            
            # --- Border ---
            Color(245/255, 245/255, 245/255, 1)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(28)),
                width=dp(1)
            )

    def status_section_bg(self, instance, value):
        """Draw background for the status section with all effects"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Box shadow (drawn first, appears behind)
            Color(0, 0, 0, 0.4)
            RoundedRectangle(
                pos=(instance.x, instance.y - dp(4)),
                size=instance.size,
                radius=[dp(28)]
            )
            
            # Background with transparency
            Color(148/255, 155/255, 164/255, 0.15)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(28)]
            )
            
            # Border
            Color(234/255, 234/255, 234/255, 1)  # #EAEAEA
            Line(
                rounded_rectangle=(
                    instance.x, 
                    instance.y, 
                    instance.width, 
                    instance.height, 
                    dp(28)
                ),
                width=0.5  # 0.5px border
            )
    
    def rect_bg(self, instance, value):
        """Draw background for the rectangle sections"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Box shadow
            Color(0, 0, 0, 0.4)
            RoundedRectangle(
                pos=(instance.x, instance.y - dp(2)),
                size=instance.size,
                radius=[dp(28)]
            )
            
            # Background with transparency
            Color(148/255, 155/255, 164/255, 0.15)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(28)]
            )
            
            # Border
            Color(234/255, 234/255, 234/255, 1)
            Line(
                rounded_rectangle=(
                    instance.x, 
                    instance.y, 
                    instance.width, 
                    instance.height, 
                    dp(28)
                ),
                width=0.5
            )
class ResponsiveStackApp(App):
    def build(self):
        # Configure window
        from kivy.config import Config
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '800')
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