from textual.app import App, RenderResult, ComposeResult
from textual import events
from textual.widget import Widget
from textual.widgets import Static, LoadingIndicator, Header, Footer, RichLog
from textual_imageview import img
from pathlib import Path
from PIL import Image
import requests
import math
from io import BytesIO
import asyncio

NASA_API_KEY = ""
IMAGE_PATH = "assets/images/M57.jpg"

class ImageViewer(Widget):
    DEFAULT_CSS = """
    ImageViewer{
        height: 100%;
        width: 100%
    }
    """

    def __init__(self, image: Image.Image):
        super().__init__()
        if not isinstance(image, Image.Image):
            raise TypeError(
                f"Expected PIL Image, but received '{type(image).__name__}' instead."
            )

        self.image = img.ImageView(image)
        self.mouse_down = False
    
    def on_show(self):
        w, h = self.size.width, self.size.height
        img_w, img_h = self.image.size

        # compute zoom such that image fits in container
        zoom_w = math.log(max(w, 1) / img_w, self.image.ZOOM_RATE)
        zoom_h = math.log((max(h, 1) * 2) / img_h, self.image.ZOOM_RATE)
        zoom = max(0, math.ceil(max(zoom_w, zoom_h)))
        self.image.set_zoom(zoom)

        # position image in center of container
        img_w, img_h = self.image.zoomed_size
        self.image.origin_position = (-round((w - img_w) / 2), -round(h - img_h / 2))
        self.image.set_container_size(w, h, maintain_center=True)
        self.refresh()
    
    def render(self) -> RenderResult:
        return self.image
    
    def on_resize(self, event: events.Resize):
        self.image.set_container_size(event.size.width, event.size.height)
        self.refresh()


class APODApp(App):    
  
    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()        
        yield ImageViewer(Image.open(IMAGE_PATH))
        yield Footer()
    
    def on_mount(self) -> None:        
        self.query_one(LoadingIndicator).remove()
    

if __name__ == "__main__":
    app = APODApp()
    app.run()