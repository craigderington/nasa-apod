from textual.app import App, ComposeResult
from textual.widgets import Static, LoadingIndicator
from PIL import Image
import requests
from io import BytesIO

NASA_API_KEY = ""

class APODApp(App):
    def compose(self) -> ComposeResult:
        yield Static(id="image")

    async def on_mount(self) -> None:
        # Fetch APOD data
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
        response = requests.get(url)
        data = response.json()
        loader = LoadingIndicator()
        loader.loading = True

        if data["media_type"] == "image":
            # Download image
            image_url = data["url"]
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))

            # Resize for terminal (adjust as needed)
            image = image.resize((80, 40))

            # Convert to ASCII (Textual doesn't natively render images)
            ascii_art = self.image_to_ascii(image)
            self.query_one("#image", Static).update(ascii_art)
            loader.loading = False

    def image_to_ascii(self, image: Image.Image) -> str:
        # Basic ASCII conversion (simplified)
        chars = "@#S%?*+;:,."
        image = image.convert("L")  # Grayscale
        pixels = image.getdata()
        ascii_str = ""
        width, height = image.size
        for i, pixel in enumerate(pixels):
            ascii_str += chars[pixel // 25]
            if (i + 1) % width == 0:
                ascii_str += "\n"
        return ascii_str

if __name__ == "__main__":
    app = APODApp()
    app.run()