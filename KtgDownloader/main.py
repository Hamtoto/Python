from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel, QScrollArea
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
import sys
import os
import requests
import json

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "다운로더"
        top = 200
        left = 200
        width = 1400
        height = 800
        
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        icon = "KtgDownloader\img\download.png"
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.downloadButton = QPushButton("Download", self)
        self.downloadButton.clicked.connect(self.download_file)
        self.downloadButton.setGeometry(200, 200, 200, 50)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setGeometry(200, 300, 1000, 400)

        self.label = QLabel(self.scroll)

    def download_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirName = QFileDialog.getExistingDirectory(self,"QFileDialog.getExistingDirectory()", "", options=options)
        if dirName:
            with open('C:/Users/Admin/Documents/work/python/Crawling/data.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            for item in data:
                url = item['url']
                name = item['name']

                response = requests.get(url)
                
                if response.status_code == 200:
                    file_path = os.path.join(dirName, name)
                    
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    
                    self.label.setText(self.label.text() + f'{name} 다운로드 및 저장 완료.\n')
                else:
                    self.label.setText(self.label.text() + f'{name} 다운로드 실패. 상태 코드: {response.status_code}\n')

        self.scroll.setWidget(self.label)
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
