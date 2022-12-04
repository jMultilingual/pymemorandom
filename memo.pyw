from PySide6.QtWidgets import (QApplication, QInputDialog, QMainWindow, QMenu, QPlainTextEdit, QLabel, QWidget, QScrollArea, QFileDialog, QComboBox,
                                QDialog, QLineEdit, QToolButton, QSpacerItem, QPushButton, QHBoxLayout, QVBoxLayout, QSpinBox,
                               QTextEdit, QMessageBox, QFontComboBox)

from PySide6.QtGui import QAction, QActionGroup, QFont, QKeySequence, QTextDocument, QTextCharFormat, QBrush, QTextCursor, QPainter
from PySide6.QtCore import Qt, QSize, QDateTime, QPoint, QUrl, QTextStream, QFile, QSaveFile, QUrl, QStringConverter, QRunnable, QProcess, QThreadPool, QEvent, QSettings

from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog
import sys

from resources import resources




INIFILE = "config.ini"
class SubExe(QRunnable):

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):

        QProcess.execute("memo.exe")
        
class FindDialog(QDialog):

    def __init__(self, doc, parent=None):

        super().__init__(parent)
        self.doc = doc
        self.extraSelections = []
        self.setWindowTitle(self.tr('検索と置換'))

        self.scrollArea = QScrollArea()
        self.collapseToolButton = QToolButton(
            text='+',
            checkable=True,
            checked = False
            )
        self.collapseToolButton.toggled[bool].connect(
            self.setMaximumHeightOfScrollArea
            )

        self.searchLineEdit = QLineEdit(
            placeholderText = self.tr('検索する'),
            clearButtonEnabled = True
            )
        self.searchLineEdit.setMinimumWidth(500)

        self.searchPushButton = QPushButton(
            parent=self.searchLineEdit,
            clicked=self.searchText
            
            )
        self.searchPushButton.resize(20, 20)
        self.searchPushButton.move(610, 1)
        self.searchPushButton.setStyleSheet(
            """QPushButton:!hover{background: transparent;}"""
            )

        self.searchForwardToolButton = QPushButton(
            text="↓",
            clicked=self.searchNext
            )
        self.searchForwardToolButton.setMaximumSize(20, 20)
        self.searchBackwardToolButton = QPushButton(
            text="↑",
            clicked=self.searchPrevious
            )
        self.searchBackwardToolButton.setMaximumSize(20, 20)
        self.searchOptionToolButton = QToolButton(text=";")

        self.searchOptionToolButtonMenu = QMenu()
        self.searchCaseSensitivelyAction = QAction(
            text=self.tr('大文字と小文字を区別する'),
            checkable=True,
            checked=False
            )
        self.searchWholeWordsAction = QAction(
            text=self.tr('単語全体を一致させる'),
            checkable=True,
            checked=False
            )
        self.searchOptionToolButtonMenu.addAction(
            self.searchCaseSensitivelyAction
            )
        self.searchOptionToolButtonMenu.addAction(
            self.searchWholeWordsAction
            )

        self.searchOptionToolButton.setStyleSheet(
            'QToolButton::menu-indicator{image: url("");}'
            )

        self.searchOptionToolButton.setPopupMode(
            QToolButton.InstantPopup
            )
        self.searchOptionToolButton.setMenu(
            self.searchOptionToolButtonMenu
            )
        self.searchCloseAction = QAction(triggered=self.close)
        self.searchCloseToolButton = QPushButton(
            text='x',
            clicked=self.close
            )
        self.searchCloseToolButton.setMaximumSize(20, 20)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.collapseToolButton)
        self.searchLayout.addWidget(self.searchLineEdit)
        self.searchLayout.addWidget(
            self.searchForwardToolButton
            )
        self.searchLayout.addWidget(
            self.searchBackwardToolButton
            )
        self.searchLayout.addWidget(
            self.searchOptionToolButton
            )
        self.searchLayout.addWidget(
            self.searchCloseToolButton
            )

        self.replaceSpacer = QSpacerItem(
            self.collapseToolButton.sizeHint().width() + 6,
            self.collapseToolButton.sizeHint().height() +6,
            )
        self.replaceLineEdit = QLineEdit(
            placeholderText=self.tr('置換する'),
            clearButtonEnabled=True
            )
        self.replaceToolButton = QToolButton(
            text=self.tr('置換'),
            clicked=self.doReplace
            )
        self.replaceAllToolButton = QToolButton(
            text=self.tr('全て置換'),
            clicked=self.doReplaceAll
            )
        self.replaceLayout = QHBoxLayout()
        self.replaceLayout.addSpacerItem(self.replaceSpacer)
        self.replaceLayout.addWidget(self.replaceLineEdit)
        self.replaceLayout.addWidget(self.replaceToolButton)
        self.replaceLayout.addWidget(self.replaceAllToolButton)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addLayout(self.searchLayout)
        self.vBoxLayout.addLayout(self.replaceLayout)

        self.areaWidget = QWidget()
        self.areaWidget.setLayout(self.vBoxLayout)

        self.scrollArea.setWidget(self.areaWidget)
        self.scrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
            )
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
            )
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setFrameShape(QScrollArea.NoFrame)
        self.scrollArea.setMaximumHeight(
                self.searchLayout.geometry().height() + 12
                )
        self.areaWidget.setMinimumWidth(800)
        self.scrollArea.setMinimumWidth(800)

        self.scrollLayout = QVBoxLayout()
        self.scrollLayout.addWidget(self.scrollArea)
        self.setLayout(self.scrollLayout)

    def setMaximumHeightOfScrollArea(self, opened):

        if opened:
            self.setTabOrder(
                             self.collapseToolButton,
                             self.searchLineEdit
                             )
            self.setTabOrder(
                             self.searchLineEdit,
                             self.replaceLineEdit
                             )
            self.setTabOrder(
                             self.replaceLineEdit,
                             self.searchForwardToolButton
                             )
            self.setTabOrder(
                             self.searchForwardToolButton,
                             self.searchBackwardToolButton
                             )
            self.setTabOrder(
                             self.searchBackwardToolButton,
                             self.searchOptionToolButton
                             )
            self.setTabOrder(
                             self.searchOptionToolButton,
                             self.searchCloseToolButton
                             )
            self.setTabOrder(
                             self.searchCloseToolButton,
                             self.replaceToolButton
                             )
            self.setTabOrder(
                            self.searchPushButton,
                            self.replaceAllToolButton
                            )
            self.setTabOrder(
                            self.replaceAllToolButton,
                            self.collapseToolButton
                            )
        else:
            self.setTabOrder(
                            self.collapseToolButton,
                            self.searchLineEdit
                            )
            self.setTabOrder(
                            self.searchLineEdit,
                            self.searchForwardToolButton
                            )
            self.setTabOrder(
                            self.searchForwardToolButton,
                            self.searchBackwardToolButton
                            )
            self.setTabOrder(
                            self.searchBackwardToolButton,
                            self.searchOptionToolButton
                            )
            self.setTabOrder(
                            self.searchOptionToolButton,
                            self.searchCloseToolButton
                            )
            self.setTabOrder(
                            self.searchCloseToolButton,
                            self.collapseToolButton
                            )
            
            
            

        height = (
            self.searchLayout.geometry().height() +
            self.searchLayout.spacing()*2 +
            self.replaceLayout.geometry().height() +
            self.searchLayout.spacing()*2
            if opened
            else self.searchLayout.geometry().height() +
            self.searchLayout.spacing()*2
            )
        self.scrollArea.setMaximumHeight(height)
        self.setMaximumHeight(self.scrollArea.minimumHeight())
        self.resize(
            self.size().width(),
            self.scrollArea.minimumHeight()
            )
        oldSize = QSize(
            self.size().width(),
            self.scrollArea.minimumHeight()
            )
        newSize = QSize(self.size().width(), height)
        self.scrollArea.setFixedHeight(height)
        self.adjustSize()

    def aside(self, tc):
        cursorRect = self.doc.parent().cursorRect(tc)
        size = cursorRect.size()
        this_geo = self.geometry()

        print(cursorRect)
        cursorPos = (
            self.doc.parent().window().geometry().topLeft()
            +
            cursorRect.topLeft()
            )
        cursorRect.setTopLeft(
            cursorPos +
            QPoint(
                0,
                self.doc.parent().window().menuBar().sizeHint().height()
                )
            )
        cursorRect.setSize(size)

        if this_geo.intersects(cursorRect):
            screen = self.doc.parent().window().screen()
            ag = screen.availableGeometry()

            left = cursorRect.left()
            right = cursorRect.right()
            top = cursorRect.top()
            bottom = cursorRect.bottom()
            extra = 50
            if right + this_geo.width() > ag.width():
                right = left - this_geo.width()
            extra -= 50
            this_geo.moveTo(right + extra, top)
            self.setGeometry(this_geo)
            

            
        
    def searchText(self):

        self.extraSelections.clear()
        self.doc.parent().setExtraSelections(
            self.extraSelectios
            )
        text = self.searchLineEdit.text()
        flags = self.flagPath()
        self.recurFindPosition(text, 0, flags)

        if not text:
            return

        if self.extraSelections:
            length = len(self.extraSelections)
            self.doc.parent().setExtraSelections(
                self.extraSelections
                )
            message = QMessageBox.warning(
                None,
                self.tr('検索結果'),
                self.tr(f"{length}件の結果が見つかりました"),
                QMessageBox.Ok
                )
        else:
            message = QMessageBox.warning(
                None,
                self.tr('何もなし'),
                self.tr(f'{text}はこれ以上見つかりませんでした'),
                QMessageBox.Ok
                )

    def searchOne(self):

        text = self.searchLineEdit.text()
        flags = self.flagPath(QTextDocument.FindFlags())
        tc = self.searchForward(text, self.doc.parent().textCursor(), flags)
        if tc.isNull():
            tc = self.searchForward(text, 0, flags)
        self.extraSelections.clear()
        if not tc.isNull():
            
            charFormat = QTextCharFormat()
            charFormat.setBackground(QBrush(Qt.gray))
            charFormat.setForeground(QBrush(Qt.white))
            extraSelection = QTextEdit.ExtraSelection()
            extraSelection.cursor = tc
            extraSelection.format = charFormat
            self.extraSelections.append(extraSelection)
        self.doc.parent().setExtraSelections(self.extraSelections)
        return tc

    
    def recurFindPosition(self, find_text, start_position, flag):

        find_tc = self.doc.find(
            find_text,
            start_position,
            flag
            )

        if not find_tc.isNull():
            charFormat = QTextCharFormat()
            charFormat.setBackground(QBrush(Qt.gray))
            charFormat.setForeground(QBrush(Qt.white))
            extraSelection = QTextEdit.ExtraSelection()
            extraSelection.cursor = find_tc
            extraSelection.format = charFormat
            self.extraSelections.append(extraSelection)
            self.recurFindPosition(find_text, find_tc, flag)

    def searchNext(self):

        text = self.searchLineEdit.text()
        if not text and not self.isVisible():

            self.exec()
            return

        flags = self.flagPath()
        tc = self.searchForward(
            text,
            self.doc.parent().textCursor(),
            flags
            )
        if tc.isNull():
            tc = self.searchForward(text, 0, flags)

        if not tc.isNull():

            self.doc.parent().setTextCursor(tc)
        self.aside(tc)
        return tc

    def searchForward(self, text, position, flags):

        tc = self.doc.find(text, position, flags)
        if tc.isNull():
            return tc

        if tc.block().isVisible():
            self.doc.parent().setTextCursor(tc)
            return tc

        return self.searchForward(text, tc, flags)

    def flagPath(self,  prev=False):
        flags = QTextDocument.FindFlags()
        
        if prev:
            flags |= QTextDocument.FindBackward

        if self.searchCaseSensitivelyAction.isChecked():
            flags |= QTextDocument.FindCaseSensitively

        if self.searchWholeWordsAction.isChecked():
            flags |= QTextDocument.FindWholeWords

        return flags

    def searchPrevious(self):

        text = self.searchLineEdit.text()
        if not text and not self.isVisible():

            self.exec()
            return

        flags = self.flagPath(True)
        tc = self.searchBackward(
            text,
            self.doc.parent().textCursor(),
            flags
            )
        if tc.isNull():
            tc = self.searchBackward(
                text,
                self.doc.characterCount(),
                flags
                )
        if not tc.isNull():
            self.doc.parent().setTextCursor(tc)
        self.aside(tc)
        return tc

    def searchBackward(self, text, position, flags):

        tc = self.doc.find(text, position, flags)

        if tc.isNull():
            return QTextCursor()

        self.doc.parent().setTextCursor(tc)
        return tc

    def doReplace(self):

        searched_text = self.searchLineEdit.text()
        replaced_text = self.replaceLineEdit.text()
        flags = self.flagPath()
        if not self.extraSelections:
            tc = self.searchOne()
            if tc.isNull():
                message = QMessageBox.warning(None,
                                           self.tr('何もなし'),
                                           self.tr(f'{searched_text}はこれ以上見つかりませんでした。'),
                                           QMessageBox.Ok)
                return

            self.extraSelections[0].cursor.insertText(replaced_text)
            self.extraSelections.clear()
            self.doc.parent().setExtraSelections([])

    def doReplaceAll(self):

        searched_text = self.searchLineEdit.text()
        replaced_text = self.replaceLineEdit.text()
        flags = self.flagPath()
        message = QMessageBox.warning(None,
                                      '置換',
                                      f"ドキュメント内の{searched_text}を{replaced_text}に変換します。よろしいですか?",
                                      QMessageBox.Ok,
                                      QMessageBox.Cancel
                                      )
        
        if message == QMessageBox.Ok:
            self.recurReplaceFindPosition(searched_text, replaced_text, 0, self.doc.characterCount(), flags)

    def recurReplaceFindPosition(self, find_text, replaced_text, start_position, end_position, flag):

        find_tc = self.doc.find(find_text, start_position, flag)
        
        if not find_tc.isNull():
            if find_tc.position() <= end_position:


                
                find_tc.insertText(replaced_text)
                

                if find_text < replaced_text:
                    end_position += len(replaced_text) - len(find_text)
                self.recurReplaceFindPosition(find_text, replaced_text, find_tc.position(), end_position, flag)

    
            
class MainWindow(QMainWindow):

    UTF16BE = "UTF-16 BE"
    UTF8    = "UTF-8"
    UTF16   = "UTF-16"
    UTF16LE = "UTF-16 LE"
    UTF8BOM = "UTF-8(BOM)"
    ENCODES = {UTF16BE: QStringConverter.Utf16BE,
               UTF8:QStringConverter.Utf8,
               UTF16:QStringConverter.Utf16,
               UTF16LE:QStringConverter.Utf16LE,
               UTF8BOM:QStringConverter.Utf8}
    DECODES = {QStringConverter.Utf8: UTF8,
               QStringConverter.Utf16: UTF16,
               QStringConverter.Utf16LE: UTF16LE,
               QStringConverter.Utf16BE: UTF16BE}
    

    def __init__(self, parent=None):
        super().__init__(parent)

        
        self.filename = ""

        self.memo = Memo(self)
        
        self.setCentralWidget(self.memo)

        self.initFontDialog()
        self.initMenu()
        self.initStatusBar()

    

        self.encodeFileDialog = QFileDialog()
        self.encodeComboBox = QComboBox()
        self.encodeComboBox.addItems(
            list(MainWindow.DECODES.values())+[MainWindow.UTF8BOM]
            )
        self.encodeVBoxLayout = QVBoxLayout()
        self.encodeVBoxLayout.addWidget(self.encodeFileDialog)
        self.encodeHBoxLayout = QHBoxLayout()
        self.encodeLabel = QLabel(self.tr("エンコード:"))
        self.encodeHBoxLayout.addWidget(self.encodeLabel)
        self.encodeHBoxLayout.addWidget(self.encodeComboBox)
        self.encodeVBoxLayout.addLayout(self.encodeHBoxLayout)
        self.encodeDialog = QDialog()
        self.encodeDialog.setSizeGripEnabled(True)

        self.encodeDialog.setLayout(self.encodeVBoxLayout)
        self.encodeFileDialog.accepted.connect(
                                    self.encodeDialog.accept
                                    )
        self.encodeFileDialog.rejected.connect(self.encodeDialog.close)

    def setFont_(self, font):

        font.setPointSize(self.fontSpinBox.value())
        self.memo.document().setDefaultFont(font)

    def setFontPointSize(self, value):

        doc = self.memo.document()
        
        font = doc.defaultFont()
        font.setPointSize(value)
     
        doc.setDefaultFont(font)
        
        
    

    

    def settings(self):

        settings = QSettings(INIFILE, QSettings.IniFormat)       
  

        settings.beginGroup("Memo")
        geometry = settings.value("geometry")

      
        (self.restoreGeometry(geometry)
         if geometry is not None
         else
         self.setGeometry(500, 300, 500, 500)
         )
        
        font = settings.value("defaultFont")
    
        (
            self.memo.document().setDefaultFont(font)
            
            if font is not None
            else
            self.memo.document().setDefaultFont(QFont('Segoe UI', 10))
            
            
        )
        self.memo.zoomTo(self.memo.document().defaultFont().pointSize())
        #ステータスバー
        isStatusBarVisible = settings.value("statusBar", 1)
        self.statusBarAction.setChecked(int(isStatusBarVisible))
        #ラインウラップ
        isLineWrapVisible = settings.value("lineWrap", 1)

        self.wrapAction.setChecked(int(isLineWrapVisible))

        

        settings.endGroup()

    def showEvent(self, event):
        self.settings()
        

        super().showEvent(event)

    def closeEvent(self, event):

        if self.memo.document().isModified():
            message = QMessageBox.warning(
                None,
                '',
                f"ドキュメントは保存されていません。\n保存をして終了しますか？",
                QMessageBox.Ok,
                QMessageBox.Cancel
                )
            if message == QMessageBox.Ok:
                self.writeLog()
                self.save(False)

            elif message == QMessageBox.No:
                event.accept()
            else:
                return
        elif self.filename:
            self.oversave()
            
        s = QSettings(INIFILE, QSettings.IniFormat)
      
     
        s.beginGroup("Memo")
        s.setValue("geometry", self.saveGeometry())
        s.setValue("statusBar", str(int(self.statusBar().isVisible())))
        s.setValue("lineWrap", str(int(self.memo.lineWrapMode() == QTextEdit.WidgetWidth)))
        s.setValue("defaultFont", self.memo.document().defaultFont())
       
      
        
        
        
        s.endGroup()

        return super().closeEvent(event)
    
    def oversave(self):

        if self.filename:
            if not self.filename.endswith(".pxt"):
                self.filename += ".pxt"

            file = QSaveFile(self.filename)
            if file.open(QSaveFile.WriteOnly):

                out = QTextStream(file)
                out << self.memo.toPlainText()

                file.commit()
                self.memo.document().setModified(False)
                return True
    
    def showActions(self):

        tc = self.memo.textCursor()
        self.cutAction.setEnabled(tc.hasSelection())
        self.copyAction.setEnabled(tc.hasSelection())
        self.deleteAction.setEnabled(tc.hasSelection())
        self.pasteAction.setEnabled(self.memo.canPaste())
        self.undoAction.setEnabled(
            self.memo.document().isUndoAvailable()
            )
        self.redoAction.setEnabled(
            self.memo.document().isRedoAvailable()
            )
        self.searchAction.setEnabled(
            self.memo.document().characterCount() != 0
            )
        self.nextSearchAction.setEnabled(
            self.searchAction.isEnabled()
            )
        self.previousSearchAction.setEnabled(
            self.searchAction.isEnabled()
            )
        self.replaceAction.setEnabled(
            self.searchAction.isEnabled()
            )
        self.moveToAction.setEnabled(
            self.memo.document().blockCount() != 1
            )
        self.selectAllAction.setEnabled(
            self.memo.document().characterCount() != 0
            )
        
    def event(self, event):
        if event.type() == QEvent.StatusTip:
            self.showActions()

       
        return super().event(event)




    def writeLog(self):
        if ".LOG" in self.memo.document().firstBlock().text():
            d = QDateTime()
            lastTc = QTextCursor(self.memo.document().lastBlock())
            if lastTc.block().text():
                lastTc.movePosition(
                    QTextCursor.EndOfBlock,
                    QTextCursor.MoveAnchor)
            lastTc.insertBlock()
            c = d.currentDateTime()
            lastTc.insertText(c.toString())
            self.memo.document().setModified(True)

    def new(self):

        if self.memo.document().isModified():
            m = QMessageBox.question(
                None,
                self.tr('未保存'),
                self.tr("文書は変更されています。保存しますか？"),
                QMessageBox.Ok|
                QMessageBox.No|
                QMessageBox.Cancel)
            if m == QMessageBox.Ok:
                self.save()
            elif m == QMessageBox.No:
                pass
            elif m == QMessageBox.Cancel:
                return
        self.memo.clear()
        self.memo.document().setModified(False)
        self.filename = ""

    def saveAs(self):

        self.save(True)
        self.memo.document().setModified(False)
        
            
        
    def save(self, overSave = True):
        self.statusBar().showMessage('保存中')
        
        if self.filename and not overSave:
            print("こっち来てますよ")
            if self.oversave():
                return

        if not self.encodeFileDialog.isVisible():
            self.encodeFileDialog.setVisible(True)
            self.encodeFileDialog.setFileMode(QFileDialog.AnyFile)
            self.encodeFileDialog.selectNameFilter("Text Files(*.pxt)")
            self.encodeFileDialog.selectUrl(QUrl("home"))
            self.encodeFileDialog.setAcceptMode(
                QFileDialog.AcceptMode.AcceptSave
                )
            self.encodeFileDialog.setWindowTitle(self.tr("メモの保存"))
            self.encodeDialog.resize(1000, 500)
            if QFileDialog.Accepted == self.encodeDialog.exec():
                self.encodeFileDialog.setSizeGripEnabled(False)
                file = self.encodeFileDialog.selectedFiles()[0]
                encode = self.encodeComboBox.currentText()

                if file:
                    if not file.endswith(".pxt"):
                        file += ".pxt"
                    file = QSaveFile(file)
                    if file.open(QSaveFile.WriteOnly):
                        out = QTextStream(file)

                    out.setEncoding(self.ENCODES[encode])
                    if encode == self.UTF8BOM:
                        out.setGenerateByteOrderMark(True)
                        

                    out << self.memo.toPlainText()
                    file.commit()
                    self.memo.document().setModified(False)
                    self.statusBar().showMessage(
                                            "保存完了しました",
                                            3000
                                            )
                    return
            self.statusBar().showMessage(
                                        "保存はキャンセルしました。",
                                        3000
                                        )

    def load(self):

        self.statusBar().showMessage("読込中")
        file, _ = QFileDialog.getOpenFileName(
                                            None,
                                            self.tr("メモ帳の読込"),
                                            "home",
                                            "Files (*.pxt)"
                                            )
        if file:
            self.filename = file
            file = QFile(file)
            if file.open(QFile.ReadOnly):
                out = QTextStream(file)
                out.setAutoDetectUnicode(True)
                byteordermark = out.generateByteOrderMark()
                encode = out.encoding()
                text = out.readAll()
                self.memo.setPlainText(text)

                if byteordermark:
                    self.encodeComboBox.setCurrentText(
                                            self.UTF8BOM

                                             )
                else:
                    self.encodeComboBox.setCurrentText(
                        self.DECODES[encode]
                        )
                    
                self.encodeLabel.setText(self.tr(f"エンコード:{encode}"))
                file.close()
                self.statusBar().showMessage("読込完了しました。", 3000)
                self.memo.document().setModified(False)
                self.writeLog()
                
    def event(self, event):

        if event.type() == QEvent.StatusTip:
            self.showActions()

       

         
            
       

        return super().event(event)

    def initMenu(self):

        self.fileMenu = QMenu(self.tr('ファイル(&F)'))

        printPreviewKeySeq = QKeySequence(self.tr("Ctrl+Shift+P"))
        
        newWindowKeySeq = QKeySequence(self.tr("Ctrl+W"))

        self.newAction = QAction(self.tr('新規'), shortcut=QKeySequence.StandardKey.New, triggered=self.new)
        self.otherWindowAction = QAction(self.tr('新しいウィンドウ'), shortcut=newWindowKeySeq, triggered=self.memo.newWindow)
        self.openAction = QAction(self.tr('開く'), shortcut=QKeySequence.StandardKey.Open, triggered=self.load)
        self.saveAction = QAction(self.tr('保存'), shortcut=QKeySequence.StandardKey.Save, triggered=self.save)
        self.saveAsAction = QAction(self.tr('名前をつけて保存'), shortcut=QKeySequence.StandardKey.SaveAs, triggered=self.saveAs)
        self.printPreviewAction = QAction(self.tr('ページ設定'), shortcut=printPreviewKeySeq, triggered=self.memo.printPreview)
        self.printAction = QAction(self.tr('印刷'), shortcut=QKeySequence.StandardKey.Print, triggered=self.memo.print)
        self.closeAction = QAction(self.tr('閉じる'), shortcut=QKeySequence.StandardKey.Close, triggered=self.close)

        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.otherWindowAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printPreviewAction)
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAction)

        self.editMenu = QMenu(self.tr('編集(&E)'))

        moveToKeySeq = QKeySequence(self.tr("Alt+G"))
        insertDateToKeySeq = QKeySequence(self.tr("Ctrl+D"))
        setFontKeySeq = QKeySequence(self.tr("Alt+O"))

        self.undoAction  = QAction(self.tr('やり直し'), shortcut=QKeySequence.StandardKey.Undo, triggered=self.memo.undo)
        self.redoAction  = QAction(self.tr('元に戻す'), shortcut=QKeySequence.StandardKey.Redo, triggered=self.memo.redo)
        self.cutAction   = QAction(self.tr('切り取り'), shortcut=QKeySequence.StandardKey.Cut, triggered=self.memo.cut)
        self.copyAction  = QAction(self.tr('コピー'), shortcut=QKeySequence.StandardKey.Copy, triggered=self.memo.copy)
        self.pasteAction = QAction(self.tr('貼り付け'), shortcut=QKeySequence.StandardKey.Paste, triggered=self.memo.paste)
        self.deleteAction= QAction(self.tr('削除'), shortcut=QKeySequence.StandardKey.Delete, triggered=lambda:self.memo.textCursor().removeSelectedText())
        self.searchAction= QAction(self.tr('検索'), shortcut=QKeySequence.StandardKey.Find, triggered=self.memo.findDialog.exec)
        self.nextSearchAction = QAction(self.tr('次を検索'), shortcut=QKeySequence.StandardKey.FindNext, triggered=self.memo.findDialog.searchNext)
        self.previousSearchAction = QAction(self.tr('前を検索'), shortcut=QKeySequence.StandardKey.FindPrevious, triggered=self.memo.findDialog.searchPrevious)
        self.replaceAction = QAction(self.tr('置換'), shortcut=QKeySequence.StandardKey.Replace, triggered=self.memo.replaceDialog)
        self.moveToAction =QAction(self.tr('移動先'), shortcut= moveToKeySeq, triggered=self.memo.moveTo)
        self.selectAllAction = QAction(self.tr('全て選択'), shortcut=QKeySequence.StandardKey.SelectAll, triggered=self.memo.selectAll)
        self.dateAndTimeAction = QAction(self.tr('日付と時刻'), shortcut=insertDateToKeySeq, triggered=self.memo.insertDateTime)
        self.fontAction = QAction(self.tr('フォント'), shortcut =setFontKeySeq, triggered=self.showFontComboBox)

        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addSeparator()        
        self.editMenu.addAction(self.searchAction)
        self.editMenu.addAction(self.nextSearchAction)
        self.editMenu.addAction(self.previousSearchAction)
        self.editMenu.addAction(self.replaceAction)
        self.editMenu.addAction(self.moveToAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.selectAllAction)
        self.editMenu.addAction(self.dateAndTimeAction)        
        self.editMenu.addAction(self.fontAction)

        self.displayMenu = QMenu(self.tr('表示(&D)'))


        statusBarKeySeq = QKeySequence("Ctrl+Shift+S")
        lineWrapKeySeq = QKeySequence("Ctrl+Shift+L")

        self.zoomMenu = QMenu(self.tr('ズーム(&Z)'))
        self.zoomInAction = QAction(self.tr('拡大'), triggered=self.memo.zoomInByAction, shortcut=QKeySequence.ZoomIn)
        self.zoomOutAction = QAction(self.tr('縮小'), triggered=self.memo.zoomOutByAction,  shortcut=QKeySequence.ZoomOut)
        self.zoomBaseAction = QAction(self.tr('100%に戻す'),triggered=self.memo.zoomBaseByAction, shortcut=QKeySequence(self.tr('Ctrl+*')))
                                    

        self.statusBarAction = QAction(self.tr('ステータスバー'), shortcut=statusBarKeySeq, checkable=True, checked=True)
        self.statusBarAction.toggled[bool].connect(self.statusBar().setVisible)
        
     

        self.wrapAction = QAction(self.tr('行の端での折り返し'), shortcut=lineWrapKeySeq, checkable=True, checked=True)
        self.wrapAction.toggled.connect(lambda checked: self.memo.setLineWrapMode(QTextEdit.LineWrapMode(not self.memo.lineWrapMode().value)))
        
          
        
        
        self.displayMenu.addMenu(self.zoomMenu)
        self.zoomMenu.addAction(self.zoomInAction)
        self.zoomMenu.addAction(self.zoomOutAction)
        self.zoomMenu.addAction(self.zoomBaseAction)

        self.displayMenu.addAction(self.statusBarAction)
        self.displayMenu.addAction(self.wrapAction)



        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.editMenu)
        self.menuBar().addMenu(self.displayMenu)
      


    def initFontDialog(self):

        self.fontComboBox = QFontComboBox()
        self.fontComboBox.currentFontChanged.connect(
            self.setFont_
            )
        self.fontSpinBox = QSpinBox(minimum=1, maximum=50)
        self.fontSpinBox.valueChanged[int].connect(
            self.setFontPointSize
            )

        self.fontDialog = QDialog()
        self.fontHBoxLayout = QHBoxLayout()
        self.fontHBoxLayout.addWidget(self.fontComboBox)
        self.fontHBoxLayout.addWidget(self.fontSpinBox)
        self.fontButtonHBoxLayout = QHBoxLayout()
        self.fontOkButton = QPushButton(
                                    self.tr("OK"),
                                    clicked = self.fontDialog.accept
                                    )
        self.fontCancelButton = QPushButton(
                                    self.tr('Cancel'),
                                    clicked= self.fontDialog.reject
                                    )
        self.fontButtonHBoxLayout.addWidget(
                                    self.fontOkButton
                                    )
        self.fontButtonHBoxLayout.addWidget(
                                    self.fontCancelButton
                                    )
        self.fontVBoxLayout = QVBoxLayout()
        self.fontVBoxLayout.addLayout(self.fontHBoxLayout)
        self.fontVBoxLayout.addLayout(self.fontButtonHBoxLayout)
        self.fontDialog.setLayout(self.fontVBoxLayout)

    def showFontComboBox(self):

        self.originalFont = self.memo.document().defaultFont()
       
        self.fontSpinBox.setValue(
            self.memo.document().defaultFont().pointSize()
            )
       
        answer = self.fontDialog.exec()
        
        if answer == QDialog.Accepted:
            font = self.memo.document().defaultFont()
            font.setFamily(self.fontComboBox.currentText())
            self.memo.document().setDefaultFont(font)
            self.memo.zoomTo(self.fontSpinBox.value())
            
            
        elif answer == QDialog.Rejected:
            
            self.memo.zoomTo(self.originalFont.pointSize())
            
            
        


    def initStatusBar(self):

        self.rowAndColumnLabel = QLabel(self.tr('行 1, 列 1"'))
        self.zoomLabel = QLabel(self.tr('100%'))
        self.encodeLabel = QLabel(self.tr('Utf-8'))
        self.localeLabel = QLabel(text=self.tr("ロケール:日本語(日本)"))  

        self.statusBar().addWidget(self.rowAndColumnLabel)
        self.statusBar().addPermanentWidget(self.zoomLabel)
        self.statusBar().addPermanentWidget(self.encodeLabel)
        self.statusBar().addPermanentWidget(self.localeLabel)
        self.memo.update()

    


class Memo(QTextEdit):

    def __init__(self, window, parent=None):
        super().__init__(parent)

        
        self.defaultPointSize = 10
        self._window = window
        self.doc = self.document()
        self.doc.setParent(self)
        defaultFont = self.doc.defaultFont()
        defaultFont.setPointSize(self.defaultPointSize)
        self.doc.setDefaultFont(defaultFont)
       
        self.zoomIn(10)
        self.setFont(defaultFont)

        

        self.cursorPositionChanged.connect(
                        self.statusBarUpdate
                        )
        
        self.findDialog = FindDialog(self.document())

        self.setAcceptRichText(False)

    def replaceDialog(self):
        
        self.findDialog.collapseToolButton.toggled[bool].emit(True)
        self.findDialog.collapseToolButton.setChecked(True)
        
        self.findDialog.exec()

    def insertDateTime(self):#new↓
        d = QDateTime()
        tc = self.textCursor()
        c = d.currentDateTime()
        tc.insertText(c.toString())

    def contextMenu(self, pos):
        w = self.window()
        self.ccm = QMenu()
        self.ccm.addActions(
            [w.redoAction, w.undoAction, w.cutAction,
             w.copyAction, w.pasteAction, w.deleteAction]
            )
        w.showActions()
        self.ccm.exec(self.mapToGlobal(pos))
        

    def newWindow(self):

        r = SubExe()
        QProcess.execute("memo.exe")
        
    def printPreview(self):

        printer = QPrinter()
        printPreviewDialog = QPrintPreviewDialog()
        printPreviewDialog.paintRequested[QPrinter].connect(self.paintPrint)
        printPreviewDialog.exec()

    def paintPrint(self, printer):
 
        painter = QPainter(printer)
        self.document().drawContents(painter)

    def print(self):

        printer = QPrinter()
        super().print_(printer)
        
    def moveTo(self):

        i, _ = QInputDialog.getInt(
                    None,
                    self.tr('行数'),
                    self.tr('何行目'),
                    minValue=1
                    )

        if i:
            br = self.document().findBlockByNumber(i-1)
            if not br.isValid():
                message = QMessageBox.warning(
                                None,
                                '',
                                f"メモ帳―指定行への移動\n指定した行は最大行を超えています。",
                                QMessage.Ok
                                )
                self.moveTo()
                return
            tc = self.textCursor()
            tc.setPosition(br.position())
            self.setTextCursor(tc)
            self.ensureCursorVisible()

    def wheelEvent(self, event):

        if event.modifiers() == Qt.ControlModifier and event.angleDelta().y() > 0:
            self.zoomInByAction()
            return
        elif event.modifiers() == Qt.ControlModifier and  event.angleDelta().y() < 0:
            self.zoomOutByAction()
            return

        return super().wheelEvent(event)
            
        
    def window(self):

        return self._window

    def zoomInByAction(self):
        
        if self.doc.defaultFont().pointSize()< 50:
       
            self.zoomIn(1)
            percentage = self.doc.defaultFont().pointSize()*self.defaultPointSize
            self.window().zoomLabel.setText(f"{percentage}%")

    def zoomOutByAction(self):
        if self.doc.defaultFont().pointSize() > 1:
          
            self.zoomOut(1)
            percentage = self.doc.defaultFont().pointSize()*self.defaultPointSize
            self.window().zoomLabel.setText(f"{percentage}%")

    def zoomBaseByAction(self):
        diff = 10 - self.doc.defaultFont().pointSize()
   
        self.zoomIn(diff) if diff > 0 else self.zoomOut(abs(diff))
        percentage = 100
        self.window().zoomLabel.setText(f"{percentage}%")
        
    def zoomTo(self, value):
        if 1 <= value <= 50:
            diff = value - self.doc.defaultFont().pointSize()
       
            self.zoomIn(diff) if diff > 0 else self.zoomOut(abs(diff))
            percentage = value*10
            self.window().zoomLabel.setText(f"{percentage}%")
        
    def statusBarUpdate(self):

        tc = self.textCursor()
        block = tc.block()
        blockNumber = block.blockNumber() + 1
        positionInBlock = tc.positionInBlock() + 1
        self.window().rowAndColumnLabel.setText(
            self.tr(f'行{blockNumber}, 列{positionInBlock}')
            )

        
        


def main():

    app = QApplication([])
    app.setOrganizationName("Qt User")
    app.setApplicationName("PyMemo")
    s = QSettings(INIFILE, QSettings.IniFormat)
    
 

   
    t = MainWindow()
  
    
    
    t.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
