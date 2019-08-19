from dero.latex.models.presentation.beamer.overlay.overlay_param import OverlayParameter


class UntilEnd(OverlayParameter):

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f'{self.content}-'
