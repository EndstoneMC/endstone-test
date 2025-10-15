import numpy as np
from endstone import Player
from endstone.map import MapCanvas, MapRenderer, MapView
from PIL.Image import Image, Resampling


class ImageRenderer(MapRenderer):
    def __init__(self, image: Image):
        MapRenderer.__init__(self)
        self.image = image.convert("RGBA")
        self.image.thumbnail((128, 128), Resampling.LANCZOS)

    def render(self, view: MapView, canvas: MapCanvas, player: Player) -> None:
        print("render!!!")
        canvas.draw_image(0, 0, np.array(self.image))
