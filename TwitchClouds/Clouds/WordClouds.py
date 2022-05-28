import typing
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator


class ColoredCloud:
    def __init__(
            self,
            words: typing.Union[str],
            image: 'PIL.Image',
            font: typing.Union[str] = "arial.ttf",
            width: typing.Union[int] = 4000,
            height: typing.Union[int] = 4000,
            max_words: typing.Union[int] = 8000,
            max_font_size: typing.Union[int] = 100,
    ):
        self._words = words
        self._coloring = np.array(image)
        self._image_colors = ImageColorGenerator(self._coloring)
        self.wordcloud = WordCloud(
            font_path=font,
            width=width,
            height=height,
            max_words=max_words,
            mask=self._coloring,
            max_font_size=max_font_size,
            random_state=42,
            min_word_length=2
        ).generate(self._words)

        self.wordcloud.recolor(self._image_colors)

    def as_png(self, filename: typing.Union[str], path: typing.Union[str] = None):
        return self.wordcloud.to_file(f'{path}{filename}.png')
