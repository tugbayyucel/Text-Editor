import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QRegExp, QSize
import time
import about

textChanged = False
url = ""
tbchecked = True
dockchecked = True
statusbarchecked = True


class FindDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bul ve Değiştir")
        self.setGeometry(450, 250, 350, 200)
        self.arayuz()

    def arayuz(self):
        formLayout = QFormLayout(self)
        hbox = QHBoxLayout()
        txtFind = QLabel("Bul :")
        txtReplace = QLabel("Değiştir :")
        txtEmpty = QLabel("")
        self.findInput = QLineEdit()
        self.replaceInput = QLineEdit()
        self.btnFind = QPushButton("Bul")
        self.btnReplace = QPushButton("Değiştir")
        hbox.addWidget(self.btnFind)
        hbox.addWidget(self.btnReplace)
        formLayout.addRow(txtFind, self.findInput)
        formLayout.addRow(txtReplace, self.replaceInput)
        formLayout.addRow(txtEmpty, hbox)


class Pencere(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Editör")
        self.setWindowIcon(QIcon('icons/notepad.png'))
        self.setGeometry(0, 0, 800, 600)
        self.arayuz()

    def arayuz(self):
        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.editor.setFontPointSize(10)
        self.editor.textChanged.connect(self.funcTextChanged)
        self.menu()
        self.toolbar()
        self.dockbar()
        self.statusbar()

        self.show()

    def statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def funcTextChanged(self):
        global textChanged
        textChanged = True
        text = self.editor.toPlainText()
        letters = len(text)
        words = len(text.split())
        self.status_bar.showMessage("Harf Sayısı :" + str(letters) + "     Kelime Sayısı :" + str(words))

    def dockbar(self):
        self.dock = QDockWidget("Kısayollar", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockWidget = QWidget(self)
        self.dock.setWidget(self.dockWidget)
        formLayout = QFormLayout()
        #################################
        btnFind = QToolButton()
        btnFind.setIcon(QIcon('menu/find_large.png'))
        btnFind.setText("Bul")
        btnFind.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btnFind.setIconSize(QSize(50, 50))
        btnFind.setCheckable(True)
        btnFind.toggled.connect(self.find)
        #################################
        btnNew = QToolButton()
        btnNew.setIcon(QIcon('menu/new_large.png'))
        btnNew.setText("Yeni")
        btnNew.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btnNew.setIconSize(QSize(50, 50))
        btnNew.setCheckable(True)
        btnNew.toggled.connect(self.newFile)
        #################################
        btnOpen = QToolButton()
        btnOpen.setIcon(QIcon('menu/open_large.png'))
        btnOpen.setText("Aç")
        btnOpen.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btnOpen.setIconSize(QSize(50, 50))
        btnOpen.setCheckable(True)
        btnOpen.toggled.connect(self.openFile)
        #################################
        btnSave = QToolButton()
        btnSave.setIcon(QIcon('menu/save_large.png'))
        btnSave.setText("Kaydet")
        btnSave.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btnSave.setIconSize(QSize(50, 50))
        btnSave.setCheckable(True)
        btnSave.toggled.connect(self.saveFile)
        #################################
        formLayout.addRow(btnFind, btnNew)
        formLayout.addRow(btnOpen, btnSave)
        self.dockWidget.setLayout(formLayout)
        ################Dockbar Bitiş#################

    def toolbar(self):
        self.tb = self.addToolBar("Araç Çubuğu")
        self.fontFamily = QFontComboBox(self)
        self.fontFamily.currentFontChanged.connect(self.changeFont)
        self.tb.addWidget(self.fontFamily)
        self.tb.addSeparator()
        self.tb.addSeparator()
        ########################
        self.fontSize = QComboBox()
        self.tb.addWidget(self.fontSize)
        self.fontSize.setEditable(True)
        for i in range(6, 100):
            self.fontSize.addItem(str(i))
        self.fontSize.setCurrentText("12")
        self.fontSize.currentTextChanged.connect(self.changeFontSize)
        self.tb.addSeparator()
        self.tb.addSeparator()
        ##########################
        self.bold = QAction(QIcon('menu/bold.png'), "Kalın yazı", self)
        self.tb.addAction(self.bold)
        self.bold.triggered.connect(self.Bold)
        ##########################
        self.italic = QAction(QIcon('menu/italic.png'), "İtalik yazı", self)
        self.tb.addAction(self.italic)
        self.italic.triggered.connect(self.Italic)
        ##########################
        self.underline = QAction(QIcon('menu/underline.png'), "Altı çizgili yazı", self)
        self.tb.addAction(self.underline)
        self.underline.triggered.connect(self.Underline)
        self.tb.addSeparator()
        self.tb.addSeparator()
        ##########################
        self.font_color = QAction(QIcon('menu/color.png'), "Font rengi", self)
        self.tb.addAction(self.font_color)
        self.font_color.triggered.connect(self.funcFontColor)
        ##########################
        self.font_bgcolor = QAction(QIcon('menu/backcolor.png'), "Yazı arka rengi", self)
        self.tb.addAction(self.font_bgcolor)
        self.font_bgcolor.triggered.connect(self.funcFontBackColor)
        self.tb.addSeparator()
        self.tb.addSeparator()
        ##########################
        self.align_left = QAction(QIcon('menu/alignleft.png'), "Sola hizala", self)
        self.tb.addAction(self.align_left)
        self.align_left.triggered.connect(self.funcAllignLeft)
        ##########################
        self.align_right = QAction(QIcon('menu/alignright.png'), "Sağa hizala", self)
        self.tb.addAction(self.align_right)
        self.align_right.triggered.connect(self.funcAllignRight)
        ##########################
        self.align_center = QAction(QIcon('menu/aligncenter.png'), "Ortala", self)
        self.tb.addAction(self.align_center)
        self.align_center.triggered.connect(self.funcAllignCenter)
        ##########################
        self.align_justify = QAction(QIcon('menu/alignJustify.png'), "İki yana yasla", self)
        self.tb.addAction(self.align_justify)
        self.align_justify.triggered.connect(self.funcAllignJustify)
        self.tb.addSeparator()
        self.tb.addSeparator()
        ##########################
        self.bulletList = QAction(QIcon('menu/bulletlist.png'), "Madde işareti", self)
        self.tb.addAction(self.bulletList)
        self.bulletList.triggered.connect(self.funcBulletList)
        ##########################
        self.numberList = QAction(QIcon('menu/numberlist.png'), "Numara işareti", self)
        self.tb.addAction(self.numberList)
        self.numberList.triggered.connect(self.funcNumberList)

    def funcNumberList(self):
        self.editor.insertHtml("<ol><li><h3>&nbsp;</h3></li></ol>")

    def funcBulletList(self):
        self.editor.insertHtml("<ul><li><h3>&nbsp;</h3></li></ul>")

    def funcAllignLeft(self):
        self.editor.setAlignment(Qt.AlignLeft)

    def funcAllignRight(self):
        self.editor.setAlignment(Qt.AlignRight)

    def funcAllignCenter(self):
        self.editor.setAlignment(Qt.AlignCenter)

    def funcAllignJustify(self):
        self.editor.setAlignment(Qt.AlignJustify)

    def funcFontColor(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    def funcFontBackColor(self):
        bcolor = QColorDialog.getColor()
        self.editor.setTextBackgroundColor(bcolor)

    def Bold(self):
        fontWeight = self.editor.fontWeight()
        if fontWeight == 50:
            self.editor.setFontWeight(QFont.Bold)
        elif fontWeight == 75:
            self.editor.setFontWeight(QFont.Normal)

    def Italic(self):
        italic = self.editor.fontItalic()
        if italic == True:
            self.editor.setFontItalic(False)
        else:
            self.editor.setFontItalic(True)

    def Underline(self):
        underline = self.editor.fontUnderline()
        if underline == True:
            self.editor.setFontUnderline(False)
        else:
            self.editor.setFontUnderline(True)

    def changeFont(self, font):
        font = QFont(self.fontFamily.currentFont())
        self.editor.setCurrentFont(font)

    def changeFontSize(self, fontSize):
        self.editor.setFontPointSize(float(fontSize))
        ##############Toolbar Bitiş ############

    def menu(self):
        #####Ana Menu######

        menubar = self.menuBar()
        file = menubar.addMenu("Dosya")
        edit = menubar.addMenu("Düzen")
        view = menubar.addMenu("Görünüm")
        help_menu = menubar.addMenu("Yardım")
        #######Alt Menü#######
        new = QAction(QIcon('menu/new.png'), "Yeni", self)
        new.setShortcut("Alt+Insert")
        new.triggered.connect(self.newFile)
        file.addAction(new)
        ######################
        open = QAction(QIcon('menu/open.png'), "Aç", self)
        open.setShortcut("Ctrl+O")
        open.triggered.connect(self.openFile)
        file.addAction(open)
        #######################
        save = QAction(QIcon('menu/save.png'), "Kaydet", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.saveFile)
        file.addAction(save)
        #######################
        exit = QAction(QIcon('menu/exit.png'), "Çıkış", self)
        exit.setShortcut("Ctrl+Q")
        exit.triggered.connect(self.exitFile)
        file.addAction(exit)
        #######################
        undo = QAction(QIcon('menu/undo.png'), "Geri Al", self)
        undo.setShortcut("Ctrl+Z")
        undo.triggered.connect(self.undo)
        edit.addAction(undo)
        #######################
        cut = QAction(QIcon('menu/cut.png'), "Kes", self)
        cut.setShortcut("Ctrl+X")
        cut.triggered.connect(self.cut)
        edit.addAction(cut)
        #######################
        copy = QAction(QIcon('menu/copy.png'), "Kopyala", self)
        copy.setShortcut("Ctrl+C")
        copy.triggered.connect(self.copy)
        edit.addAction(copy)
        #######################
        paste = QAction(QIcon('menu/paste.png'), "Yapıştır", self)
        paste.setShortcut("Ctrl+V")
        paste.triggered.connect(self.paste)
        edit.addAction(paste)
        #######################
        find = QAction(QIcon('menu/find.png'), "Bul", self)
        find.setShortcut("Ctrl+F")
        find.triggered.connect(self.find)
        edit.addAction(find)
        #######################
        time_data = QAction(QIcon('menu/datetime.png'), "Tarih ve Zaman Ekle", self)
        time_data.setShortcut("F5")
        time_data.triggered.connect(self.time_date)
        edit.addAction(time_data)
        #######################
        statusBar = QAction("Durum Çubuğu", self, checkable=True)
        statusBar.triggered.connect(self.funcStatusBar)
        view.addAction(statusBar)
        #######################
        toolBar = QAction("Araç Çubuğu", self, checkable=True)
        toolBar.triggered.connect(self.funcToolBar)
        view.addAction(toolBar)
        #######################
        dockBar = QAction("Yerleştirme Çubuğu", self, checkable=True)
        dockBar.triggered.connect(self.funcDockBar)
        view.addAction(dockBar)
        #######################
        about_us = QAction("Hakkımızda", self)
        about_us.triggered.connect(self.about_us)
        help_menu.addAction(about_us)

    def about_us(self):
        self.help = about.Help()
        self.help.show()

    def funcStatusBar(self):
        global statusbarchecked
        if statusbarchecked == True:
            self.status_bar.hide()
            statusbarchecked = False
        else:
            self.status_bar.show()
            statusbarchecked = True

    def funcToolBar(self):
        global tbchecked
        if tbchecked == True:
            self.tb.hide()
            tbchecked = False
        else:
            self.tb.show()
            tbchecked = True

    def funcDockBar(self):
        global dockchecked
        if dockchecked == True:
            self.dock.hide()
            dockchecked = False
        else:
            self.dock.show()
            dockchecked = True

    def undo(self):
        self.editor.undo()

    def cut(self):
        self.editor.cut()

    def copy(self):
        self.editor.copy()

    def paste(self):
        self.editor.paste()

    def find(self):
        self.find = FindDialog()
        self.find.show()

        def findWords():
            global word
            word = self.find.findInput.text()
            if word != "":
                cursor = self.editor.textCursor()
                format = QTextCharFormat()
                format.setBackground(QBrush(QColor("grey")))
                regex = QRegExp(word)
                pos = 0
                index = regex.indexIn(self.editor.toPlainText(), pos)
                self.count = 0
                while (index != -1):
                    cursor.setPosition(index)
                    cursor.movePosition(QTextCursor.EndOfWord, 1)
                    cursor.mergeCharFormat(format)
                    pos = index + regex.matchedLength()
                    index = regex.indexIn(self.editor.toPlainText(), pos)
                    self.count += 1
                self.status_bar.showMessage(str(self.count) + "Sonuç bulundu")
            else:
                QMessageBox.information(self, "Uyarı!", "Alanlar boş olamaz")

        def replaceWords():
            replaceText = self.find.replaceInput.text()
            word = self.find.findInput.text()
            text = self.editor.toPlainText()
            newValue = text.replace(word, replaceText)
            self.editor.clear()
            self.editor.append(newValue)

            self.find.btnFind.clicked.connect(findWords)
            self.find.btnReplace.clicked.connect(replaceWords)

    def time_date(self):
        try:
            time_date = time.strftime("%d.%m.%Y %H:%M")
            self.editor.append(time_date)

        except:
            pass

    def newFile(self):
        try:
            global url
            url = ""
            self.editor.clear()
        except:
            pass

    def openFile(self):
        global url
        try:
            url = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Tüm Dosyalar(*);;Txt Dosyası *.txt")
            with open(url[0], 'r+', encoding='utf-8') as file:
                self.editor.clear()
                self.editor.setText(content)
        except:
            pass

    def saveFile(self):
        global url
        try:
            if textChanged == True:
                if url != "":
                    content = self.editor.toPlainText()
                    with open(url[0], 'w', encoding='utf-8') as file:
                        file.write(content)
                else:
                    url = QFileDialog.getSaveFileName(self, "Dosyayı Kaydet", "Txt Dosyası(*.txt)")
                    content2 = self.editor.toPlainText()
                    with open(url[0], 'w', encoding='utf-8') as file2:
                        file2.write(content2)
        except:
            pass

    def exitFile(self):
        global url
        try:
            if textChanged == True:
                mbox = QMessageBox.information(self, "Dikkat!", "Dosyayı Kaydetmek İstiyor musunuz?",
                                               QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)

                if mbox == QMessageBox.Save:
                    if url != "":
                        content = self.editor.toPlainText()
                        with open(url[0], 'w', encoding='utf-8') as file:
                            file.write(content)

                    else:
                        url = QFileDialog.getSaveFileName(self, "Dosyayı Kaydet", "Txt Dosyası(*.txt)")
                        content2 = self.editor.toPlainText()
                        with open(url[0], "w", encoding='utf-8') as file2:
                            file2.write(content2)

                elif mbox == QMessageBox.No:
                    qApp.quit()

            else:
                qApp.quit()

        except:
            pass

    #####################################Menü Bitiş########################################################


uygulama = QApplication(sys.argv)
pencere = Pencere()
sys.exit(uygulama.exec_())
