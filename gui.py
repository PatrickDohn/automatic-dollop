import sys
from pathlib import Path

from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

APP_STYLE = """
QMainWindow {
    background-color: #F1F4F9;
}

QWidget#mainContainer {
    background-color: #F1F4F9;
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue";
}

QLabel#logo {
    font-size: 30px;
    background-color: #DCE8FF;
    border-radius: 12px;
    padding: 8px;
}

QLabel#title {
    color: #17243A;
    font-size: 23px;
    font-weight: 700;
}

QLabel#subtitle {
    color: #718096;
    font-size: 12px;
}

QFrame#settingsCard {
    background-color: #FFFFFF;
    border: 1px solid #E1E7F0;
    border-radius: 16px;
}



QLabel#sectionTitle {
    color: #25344B;
    font-size: 15px;
    font-weight: 700;
}

QLabel#description {
    color: #718096;
    font-size: 12px;
}

QLineEdit#keyEntry {
    background-color: #F8FAFC;
    border: 1px solid #DCE3ED;
    border-radius: 9px;
    padding: 0 12px;
    min-height: 44px;
    color: #25344B;
    font-size: 14px;
}

QLineEdit#keyEntry:focus {
    border: 1px solid #2865D9;
}

QLabel#statusLabel {
    color: #718096;
    font-size: 12px;
    font-weight: 600;
}

QPushButton {
    border: none;
    border-radius: 9px;
    min-height: 42px;
    padding: 0 16px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#startButton {
    background-color: #2865D9;
    color: white;
}

QPushButton#stopButton {
    background-color: #E9EEF6;
    color: #34445C;
}

QPushButton#startButton:hover {
    background-color: #1E54BD;
}

QPushButton#startButton:disabled {
    background-color: #A9BCE0;
    color: #FFFFFF;
}

QPushButton#stopButton:hover {
    background-color: #DCE4F0;
}

QPushButton#stopButton:disabled {
    color: #A0AABA;
    background-color: #F2F4F7;
}

QLabel#footer {
    color: #8A96A8;
    font-size: 11px;
}
"""


def resource_path(relative_path: str) -> Path:
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base_path / relative_path


class QuackApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quack")
        self.setFixedSize(440, 360)
        self.stopping = False

        self.listener = QProcess(self)
        # self.listener.readyReadStandardOutput.connect(self.read_output)
        # self.listener.readyReadStandardError.connect(self.read_errors)
        self.listener.finished.connect(self.listener_finished)
        self.listener.errorOccurred.connect(self.listener_error)

        self.build_ui()

    def build_ui(self):
        container = QWidget()
        container.setObjectName("mainContainer")

        outer_layout = QVBoxLayout(container)
        outer_layout.setContentsMargins(28, 26, 28, 22)
        outer_layout.setSpacing(24)

        # Header
        header = QHBoxLayout()
        header.setSpacing(14)

        logo = QLabel("🦆")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(4)

        title = QLabel("Quack")
        title.setObjectName("title")

        subtitle = QLabel("Keyboard sound effects")
        subtitle.setObjectName("subtitle")

        heading_layout.addWidget(title)
        heading_layout.addWidget(subtitle)

        header.addWidget(logo)
        header.addLayout(heading_layout)
        header.addStretch()

        outer_layout.addLayout(header)

        # Settings card
        card = QFrame()
        card.setObjectName("settingsCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 24, 22, 22)
        card_layout.setSpacing(0)

        # Section heading
        section_title = QLabel("Keyboard configuration")
        section_title.setObjectName("sectionTitle")

        description = QLabel("Choose the keys that trigger your sound.")
        description.setObjectName("description")

        card_layout.addWidget(section_title)
        card_layout.addSpacing(6)
        card_layout.addWidget(description)

        # Input
        card_layout.addSpacing(18)

        self.key_entry = QLineEdit("esc")
        self.key_entry.setObjectName("keyEntry")
        self.key_entry.setPlaceholderText("e.g. esc f8 space")
        self.key_entry.setMinimumHeight(46)

        card_layout.addWidget(self.key_entry)

        # Status
        card_layout.addSpacing(22)

        self.status_label = QLabel("● Stopped")
        self.status_label.setObjectName("statusLabel")

        card_layout.addWidget(self.status_label)

        # Buttons
        card_layout.addSpacing(16)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.start_button, 1)
        button_layout.addWidget(self.stop_button, 1)

        card_layout.addLayout(button_layout)

        outer_layout.addWidget(card)

        # Footer
        footer = QLabel("⌨  Press Ctrl + C to stop listening")
        footer.setObjectName("footer")

        outer_layout.addStretch()
        outer_layout.addWidget(footer)

        self.setCentralWidget(container)

    def start(self):
        if self.listener.state() != QProcess.ProcessState.NotRunning:
            return

        keys = self.key_entry.text().split() or ["esc"]

        listener_script = resource_path("listener.py")
        sound_file = resource_path("audio/better_quack.wav")

        self.listener.setProgram(sys.executable)
        self.listener.setArguments(
            [
                str(listener_script),
                "--sound",
                str(sound_file),
                "--keys",
                *keys,
            ]
        )

        self.listener.start()

        self.status_label.setText("Lets get quackin...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.key_entry.setEnabled(False)

    def listener_finished(self, exit_code, exit_status):
        if self.stopping:
            return

        crashed = exit_status == QProcess.ExitStatus.CrashExit

        if crashed:
            self.status_label.setText(f"Listener crashed (exit code {exit_code})")
            QMessageBox.warning(
                self,
                "Listener Crashed",
                f"The keyboard listener stopped unexpectedly.\nExit code: {exit_code}",
            )
        else:
            self.status_label.setText("Stopped")

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.key_entry.setEnabled(True)

    def listener_error(self, error):
        if error == QProcess.ProcessError.FailedToStart:
            self.status_label.setText("Could not start listener")
            QMessageBox.critical(
                self,
                "Startup Error",
                self.listener.errorString(),
            )

            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.key_entry.setEnabled(True)

    def stop(self):
        self.stopping = True

        if self.listener.state() != QProcess.ProcessState.NotRunning:
            self.listener.terminate()

            if not self.listener.waitForFinished(1500):
                self.listener.kill()
                self.listener.waitForFinished(1000)

        self.status_label.setText(" 🦆 ╾━╤デ╦︻ (•_- ) ... duck silenced")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.key_entry.setEnabled(True)

        self.stopping = False

    def closeEvent(self, event):
        self.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    window = QuackApp()
    window.setFixedSize(460, 430)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
