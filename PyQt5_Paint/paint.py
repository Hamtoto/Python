from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
import sys
from PyQt5.QtWidgets import QToolBar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "그림판"
        top = 200
        left = 200
        width = 1400
        height = 800

        icon = "PyQt5_Paint/img/web.png"
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))


        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 5
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.drawType = "pen"

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("파일")
        brushSize = mainMenu.addMenu("팬 사이즈")
        brushColor = mainMenu.addMenu("색상")
        drawType = mainMenu.addMenu("그리기 타입")

        saveAction = QAction(QIcon("PyQt5_Paint/img/save.png"), "저장",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)
        
        clearAction = QAction(QIcon("PyQt5_Paint/img/delete.png"), "초기화", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
        
        threepxAction = QAction("3px", self)
        brushSize.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePixel)

        fivepxAction = QAction("5px", self)
        brushSize.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePixel)

        sevenpxAction = QAction("7px", self)
        brushSize.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPixel)

        ninepxAction = QAction("10px", self)
        brushSize.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePixel)

        blackAction = QAction(QIcon("PyQt5_Paint/img/black.png"), "검정색", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor)

        blueAction = QAction(QIcon("PyQt5_Paint/img/blue.png"), "파란색", self)
        blueAction.setShortcut("Ctrl+U")
        brushColor.addAction(blueAction)
        blueAction.triggered.connect(self.blueColor)

        whitekAction = QAction(QIcon("PyQt5_Paint/img/white.png"), "하얀색", self)
        whitekAction.setShortcut("Ctrl+W")
        brushColor.addAction(whitekAction)
        whitekAction.triggered.connect(self.whiteColor)

        redAction = QAction(QIcon("PyQt5_Paint/img/red.png"), "빨강색", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.redColor)

        greenAction = QAction(QIcon("PyQt5_Paint/img/green.png"), "초록색", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)

        yellowAction = QAction(QIcon("PyQt5_Paint/img/yellow.png"), "노란색", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor)

        penAction = QAction(QIcon("PyQt5_Paint/img/pen.png"), "펜", self)
        drawType.addAction(penAction)
        penAction.triggered.connect(self.penDraw)

        rectAction = QAction(QIcon("PyQt5_Paint/img/rectangle.png"), "사각형", self)
        drawType.addAction(rectAction)
        rectAction.triggered.connect(self.rectDraw)

        circleAction = QAction(QIcon("PyQt5_Paint/img/circle.png"), "원", self)
        drawType.addAction(circleAction)
        circleAction.triggered.connect(self.circleDraw)

        lineAction = QAction(QIcon("PyQt5_Paint/img/line.png"), "선", self)
        drawType.addAction(lineAction)
        lineAction.triggered.connect(self.lineDraw)

        triangleAction = QAction(QIcon("PyQt5_Paint/img/triangle.png"), "삼각형", self)
        drawType.addAction(triangleAction)
        triangleAction.triggered.connect(self.triangleDraw)

        self.statusBar()
        self.toolbar = self.addToolBar('파일 툴바')
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(clearAction)
        
        ColorToolBar = QToolBar("색상툴바", self)
        self.addToolBar(Qt.LeftToolBarArea, ColorToolBar)
        ColorToolBar.addAction(blackAction)
        ColorToolBar.addAction(whitekAction)
        ColorToolBar.addAction(redAction)
        ColorToolBar.addAction(greenAction)
        ColorToolBar.addAction(blueAction)
        ColorToolBar.addAction(yellowAction)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.imageTemp = self.image.copy()

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            if self.drawType == "pen":
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()    
            else:    
                painter.end()
                self.image = self.imageTemp.copy()
                painter = QPainter(self.image)
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.drawType == "rectangle":
                    painter.drawRect(self.lastPoint.x(), self.lastPoint.y(), event.pos().x() - self.lastPoint.x(), event.pos().y() - self.lastPoint.y())
                elif self.drawType == "circle":
                    painter.drawEllipse(self.lastPoint.x(), self.lastPoint.y(), event.pos().x() - self.lastPoint.x(), event.pos().y() - self.lastPoint.y())
                elif self.drawType == "line":
                    painter.drawLine(self.lastPoint, event.pos())
                elif self.drawType == "triangle":
                    points = [self.lastPoint, QPoint(event.pos().x(), self.lastPoint.y()), event.pos()]
                    painter.drawPolygon(*points)
            painter.end()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image, self.image.rect() )

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def threePixel(self):
        self.brushSize = 3

    def fivePixel(self):
        self.brushSize = 5

    def sevenPixel(self):
        self.brushSize = 7

    def ninePixel(self):
        self.brushSize = 10

    def blackColor(self):
        self.brushColor = Qt.black
        
    def blueColor(self):
        self.brushColor = Qt.blue

    def whiteColor(self):
        self.brushColor = Qt.white

    def redColor(self):
        self.brushColor = Qt.red

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def rectDraw(self):
        self.drawType = "rectangle"

    def circleDraw(self):
        self.drawType = "circle"

    def lineDraw(self):
        self.drawType = "line"

    def triangleDraw(self):
        self.drawType = "triangle"

    def penDraw(self):
        self.drawType = "pen"

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newImage = QImage(self.width(), self.height(), QImage.Format_RGB32)
            newImage.fill(Qt.white)
            painter = QPainter(newImage)
            painter.drawImage(QPoint(), self.image)
            self.image = newImage
        QMainWindow.resizeEvent(self, event)
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()