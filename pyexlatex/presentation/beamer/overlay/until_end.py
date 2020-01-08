from pyexlatex.presentation.beamer.overlay.overlay_param import OverlayParameter


class UntilEnd(OverlayParameter):
    """
    Option to be passed to Overlay that makes object exist until the end of the frame
    """

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f'{self.content}-'
