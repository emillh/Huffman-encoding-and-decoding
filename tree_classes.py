class internal_node():
    """
    Denne klasse er til at vise indre knuder i Huffmantræer, som skal være tomme.
    """
    def _init__(self):
        self.left = None
        self.right = None

class leaf_node():
    def __init__(self, data) -> None:
        self.data = data