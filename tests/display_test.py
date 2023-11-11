from wand.display import display
from wand.image import Image


from unittest.mock import patch, Mock
import tempfile


def test_should_display_psuedo_image():
    path = tempfile.mktemp(suffix=".png")

    with Image(width=10, height=10, pseudo="xc:white", format="png") as img:
        with patch("tempfile.mktemp") as mock_tempfile:
            mock_tempfile.return_value = path

            display(img)

            mock_tempfile.assert_called_once_with(suffix=".png")
