import sys
import os
import threading
import requests
import zipfile
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import (
    QFont, QLinearGradient, QPalette, QColor, QBrush, QPainter, QPen
)
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QMessageBox, QVBoxLayout, QGraphicsDropShadowEffect
)

class GlowButton(QPushButton):
    def __init__(self, text, parent=None, click_action=None):
        super().__init__(text, parent)
        self.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #002244, stop:1 #0044ff
                );
                border: none;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0044ff, stop:1 #00aaff
                );
            }
            QPushButton:pressed {
                background-color: #0033aa;
            }
        """)

        # Neon blue glow effect
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setColor(QColor("#00aaff"))
        self.effect.setBlurRadius(30)
        self.effect.setOffset(0, 0)
        self.setGraphicsEffect(self.effect)

        # Animated pulsing glow
        self._glow_anim = QPropertyAnimation(self.effect, b"blurRadius")
        self._glow_anim.setDuration(1000)
        self._glow_anim.setLoopCount(-1)
        self._glow_anim.setStartValue(20)
        self._glow_anim.setEndValue(35)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._glow_anim.start()

        if click_action:
            self.clicked.connect(click_action)


class TanSilkingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tan Silking The Song")
        self.setFixedSize(480, 360)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self._setup_ui()
        self._apply_fade_in_animation()
        self._setup_glow_outline_animation()
        self._setup_title_glow_animation()

    # --- UI Setup ---
    def _setup_ui(self):
        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#000000"))
        gradient.setColorAt(1.0, QColor("#001133"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title with glow
        self.title = QLabel("Tan Silking The Song")
        self.title.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #00aaff; margin-bottom: 25px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.title_glow = QGraphicsDropShadowEffect(self)
        self.title_glow.setColor(QColor("#00aaff"))
        self.title_glow.setBlurRadius(25)
        self.title_glow.setOffset(0, 0)
        self.title.setGraphicsEffect(self.title_glow)

        # Button holder
        self.button_holder = QWidget()
        self.button_layout = QVBoxLayout(self.button_holder)
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button_holder)

        # Get Started button
        self.get_started_btn = GlowButton("Get Started", click_action=self.on_get_started_click)
        self.button_layout.addWidget(self.get_started_btn)

        # Footer
        self.discord_label = QLabel("Discord: Tan_12931")
        self.discord_label.setFont(QFont("Roboto", 9))
        self.discord_label.setStyleSheet("color: #888888; margin-top: 25px;")
        self.discord_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.discord_label)

    # --- Fade-in on startup ---
    def _apply_fade_in_animation(self):
        self.setWindowOpacity(0)
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_anim.setDuration(1200)
        self.fade_in_anim.setStartValue(0)
        self.fade_in_anim.setEndValue(1)
        self.fade_in_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in_anim.start()

    # --- Title glow animation ---
    def _setup_title_glow_animation(self):
        self.title_anim = QPropertyAnimation(self.title_glow, b"blurRadius")
        self.title_anim.setDuration(1500)
        self.title_anim.setLoopCount(-1)
        self.title_anim.setStartValue(10)
        self.title_anim.setEndValue(40)
        self.title_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.title_anim.start()

    # --- Neon border animation ---
    def _setup_glow_outline_animation(self):
        self.glow_intensity = 0.4
        self.glow_increasing = True
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_glow)
        self.timer.start(40)

    def _update_glow(self):
        step = 0.02
        if self.glow_increasing:
            self.glow_intensity += step
            if self.glow_intensity >= 1.0:
                self.glow_increasing = False
        else:
            self.glow_intensity -= step
            if self.glow_intensity <= 0.4:
                self.glow_increasing = True
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(0, 170, 255, int(80 * self.glow_intensity))
        pen = QPen(color, 6)
        painter.setPen(pen)
        rect = self.rect().adjusted(3, 3, -3, -3)
        painter.drawRoundedRect(rect, 15, 15)

    # --- Transitions ---
    def fade_transition(self, old_widget, new_widget):
        if old_widget:
            old_widget.setVisible(False)
        if new_widget:
            new_widget.setVisible(True)
            new_widget.setGraphicsEffect(None)
            new_widget.setWindowOpacity(0)
            anim = QPropertyAnimation(new_widget, b"windowOpacity")
            anim.setDuration(600)
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.start()

    # --- Button flow logic ---
    def on_get_started_click(self):
        self.fade_transition(self.get_started_btn, None)
        self.button_layout.removeWidget(self.get_started_btn)
        self.get_started_btn.deleteLater()
        QTimer.singleShot(400, self.show_download_button)

    def show_download_button(self):
        self.download_btn = GlowButton(
            "Download BepinEx5 With Config Manager", click_action=self.on_download_click
        )
        self.button_layout.addWidget(self.download_btn)
        self.fade_transition(None, self.download_btn)

    def on_download_click(self):
        self.download_btn.setEnabled(False)
        threading.Thread(target=self.download_bepinex5, daemon=True).start()

    def download_bepinex5(self):
        url = "https://supporter-files.nexus-cdn.com/6933/7/BepInEx_win_x64_5.4.23.2-with-ConfigurationManager-7-5-4-23-2-1732141657.zip?md5=cTxxUiQ2OgiDswjVYcf0IQ&expires=1760927138&user_id=188515161"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            download_path = os.path.join(os.path.expanduser("~"), "Downloads", "BepInEx.zip")
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            self.download_path = download_path
            QTimer.singleShot(0, self.show_extract_button)
        except Exception as e:
            self.show_error(f"Download failed: {e}")
            self.download_btn.setEnabled(True)

    def show_extract_button(self):
        self.download_btn.hide()
        self.extract_btn = GlowButton(
            "Select Directory Where Silksong Is Downloaded",
            click_action=self.on_extract_click
        )
        self.button_layout.addWidget(self.extract_btn)
        self.fade_transition(None, self.extract_btn)

    def on_extract_click(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Silksong Directory")
        if directory:
            threading.Thread(target=self.extract_zip, args=(directory,), daemon=True).start()

    def extract_zip(self, target_directory):
        try:
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(target_directory)
            QTimer.singleShot(0, lambda: QMessageBox.information(
                self, "Congratulations",
                "Congratulations! You just downloaded BepInEx5 easily with the help of Tan."
            ))
            self.extract_btn.hide()
        except Exception as e:
            self.show_error(f"Extraction failed: {e}")

    def show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TanSilkingApp()
    window.show()
    sys.exit(app.exec())
