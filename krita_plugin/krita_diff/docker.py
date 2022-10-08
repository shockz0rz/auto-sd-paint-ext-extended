from krita import DockWidget, QPushButton, QTabWidget, QVBoxLayout, QWidget

from .pages import (ConfigTabWidget, Img2ImgTabWidget, InpaintTabWidget,
                    SDCommonWidget, Txt2ImgTabWidget, UpscaleTabWidget)
from .script import STATE_INIT, STATE_READY, script
from .widgets import QLabel


class SDPluginDocker(DockWidget):
    def __init__(self, *args, **kwargs):
        super(SDPluginDocker, self).__init__(*args, **kwargs)
        self.setWindowTitle("SD Plugin")
        self.create_interfaces()
        self.update_remote_config()
        self.update_interfaces()
        self.connect_interfaces()
        self.setWidget(self.widget)

    def create_interfaces(self):
        self.quick_widget = SDCommonWidget()
        self.txt2img_widget = Txt2ImgTabWidget()
        self.img2img_widget = Img2ImgTabWidget()
        self.inpaint_widget = InpaintTabWidget()
        self.upscale_widget = UpscaleTabWidget()
        self.config_widget = ConfigTabWidget(self.update_interfaces)

        self.refresh_btn = QPushButton("Refresh Available Options")

        tabs = QTabWidget()
        tabs.addTab(self.txt2img_widget, "Txt2Img")
        tabs.addTab(self.img2img_widget, "Img2Img")
        tabs.addTab(self.inpaint_widget, "Inpaint")
        tabs.addTab(self.upscale_widget, "Upscale")
        tabs.addTab(self.config_widget, "Config")

        # TODO: this is a hacky and lazy approach
        status_bar = QLabel()
        script.set_status_callback(lambda s: status_bar.setText(f"<b>Status:</b> {s}"))
        script.set_status(STATE_INIT)

        layout = QVBoxLayout()
        layout.addWidget(status_bar)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.quick_widget)
        layout.addWidget(tabs)
        layout.addStretch()

        self.widget = QWidget(self)
        self.widget.setLayout(layout)

    def update_interfaces(self):
        self.quick_widget.cfg_init()
        self.txt2img_widget.cfg_init()
        self.img2img_widget.cfg_init()
        self.inpaint_widget.cfg_init()
        self.upscale_widget.cfg_init()
        self.config_widget.cfg_init()

    def connect_interfaces(self):
        self.quick_widget.cfg_connect()
        self.txt2img_widget.cfg_connect()
        self.img2img_widget.cfg_connect()
        self.inpaint_widget.cfg_connect()
        self.upscale_widget.cfg_connect()
        self.config_widget.cfg_connect()

        self.refresh_btn.released.connect(self.update_remote_config)

    def update_remote_config(self):
        script.update_config()
        self.update_interfaces()
        script.set_status(STATE_READY)

    def canvasChanged(self, canvas):
        pass