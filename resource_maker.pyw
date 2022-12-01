# -*- coding: utf-8 -*-

import os
from PySide6.QtGui import QTextDocument, QTextCursor
from PySide6.QtCore import QFile, QIODevice, QDir, QTextStream, QCoreApplication

def make_block(textStream, _dir, prefix, extensions):

    template = "\t\t<file>{}</file>\r\n"
    entryLists = _dir.entryList()
    
    lists = [l for l in entryLists if l.endswith(extensions)]
    
    
    textStream << f"\t<qresource prefix='{prefix}'>\r\n"    
    for i in lists:        
        a = template.format(i)
        textStream << a
    textStream << "\t</qresource>\r\n"
    
    
def main():
    
    d_str = os.getcwd()
    _dir = QDir(d_str)
    s = _dir.toNativeSeparators(os.path.join(d_str, "resources.qrc"))
    file = QFile(s)    
    z = file.open(QIODevice.ReadWrite)
    textStream = QTextStream(file)
    textStream << "<RCC>\r\n"
    make_block(textStream, _dir, 'images', (".png", ".jpg", ".gif"))
    make_block(textStream, _dir, 'fonts', ('.otf', '.ttf'))
    make_block(textStream, _dir, 'translations', ('.qm'))
    make_block(textStream, _dir, 'stylesheets', ('.qss'))
    
    textStream << "</RCC>"
    file.close()
if __name__ == "__main__":
    main()
    
