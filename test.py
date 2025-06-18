import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QColorDialog
from PySide6.QtGui import QPixmap, QPainter, QColor, QImage
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Color Change Demo")

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Load the original image
        self.original_pixmap = QPixmap("assets/sortify horz2.png")  # Replace with your image path

        # Create label to display image
        self.image_label = QLabel()
        self.image_label.setPixmap(self.original_pixmap)

        # Create color change button
        self.color_button = QPushButton("Change Color")
        self.color_button.clicked.connect(self.change_color)

        # Add widgets to layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.color_button)

    def colorize_image(self, image, color):
        """
        Colorize image while preserving alpha channel and brightness variations
        """
        # Convert QPixmap to QImage for pixel manipulation
        if isinstance(image, QPixmap):
            image = image.toImage()

        # Create output image
        colored = QImage(image.size(), QImage.Format_ARGB32)

        for x in range(image.width()):
            for y in range(image.height()):
                pixel = image.pixel(x, y)
                # Get alpha value (transparency)
                alpha = (pixel >> 24) & 0xff
                # Get grayscale value (using standard luminance formula)
                gray = QColor(pixel).lightness()
                # Create new color with original alpha and brightness
                new_color = QColor(color)
                # Adjust the color's brightness based on original pixel brightness
                h, s, v = new_color.hue(), new_color.saturation(), gray
                new_color.setHsv(h, s, v)
                # Set alpha
                new_color.setAlpha(alpha)
                # Set pixel in output image
                colored.setPixel(x, y, new_color.rgba())

        return QPixmap.fromImage(colored)

    def change_color(self):
        # Open color picker
        color = QColorDialog.getColor(Qt.white, self, "Choose Color")

        if color.isValid():
            # Apply color to image
            colored_pixmap = self.colorize_image(self.original_pixmap, color)
            self.image_label.setPixmap(colored_pixmap)

    def apply_color_overlay(self, pixmap, color):
        """
        Alternative simpler method that applies a color overlay
        Note: This method is faster but less sophisticated
        """
        result = QPixmap(pixmap.size())
        result.fill(Qt.transparent)

        painter = QPainter(result)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(result.rect(), color)
        painter.end()

        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())