#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           pictureTextCrop.py
#   Language:       Python 3.0+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#
from os import environ
from sys import argv
from sqlite3 import connect

from PySide6.QtCore import QCoreApplication, Qt, QRect
from PySide6.QtWidgets import QApplication, QFileDialog

from model.Installation import TEXT_EXTRACTION_DB_FILE
from view.Images import ImageManager

MODULE_NAME    = "Images"
INSTALLING      = False
TESTING         = True
DEBUG           = False


if __name__ == '__main__':
    #   Initialize the database:
    pictureTextDB = connect(TEXT_EXTRACTION_DB_FILE)
    cursor = pictureTextDB.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "BatchMaster" (
                        "rowId"	INTEGER NOT NULL UNIQUE,
                        "TimeStamp"	TEXT NOT NULL,
                        "FolderPath"	TEXT NOT NULL,
                        "FileName"	TEXT NOT NULL,
                        "Text"	TEXT NOT NULL,
                        "Info"	BLOB NOT NULL,
                        "Exif"	BLOB NOT NULL,
                        "MIME_info"	BLOB,
                        PRIMARY KEY("rowId" AUTOINCREMENT))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS "CropLog" (
                        "rowId"	INTEGER NOT NULL UNIQUE,
                        "timeStamp"	TEXT NOT NULL,
                        "filePath"	TEXT NOT NULL,
                        "coordinates"	BLOB NOT NULL,
                        "text"	TEXT NOT NULL,
                        PRIMARY KEY("rowId" AUTOINCREMENT))""")

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    #   Choice of the extension set should be made with the command line.
    #   dialog = ImageManager(config={'imageFileFolder': folderPath, 'scanType': 'list', 'extSet': "Pixmap"})
    app = QApplication(argv)
    if len(argv) > 1 and argv[1] in ('Pillow, "PixMap'):
        compatibility = argv[1]
    else:
        compatibility = 'Pillow'

    print("Starting PictureTextCrop.py to process images compatible with:\t" + compatibility)

    fileDialog = QFileDialog(parent=None, directory=environ['HOME'])
    #   fileDialog.setFileMode(QFileDialog.FileMode.Directory)
    #   fileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    fileDialog.setOption(QFileDialog.Option.ShowDirsOnly)
    fileDialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    fileDialog.setOption(QFileDialog.Option.DontResolveSymlinks)
    fileDialog.setOption(QFileDialog.Option.ReadOnly)
    fileDialog.exec()
    selections = fileDialog.selectedFiles()
    if TESTING:
        print(str(selections))
    folderPath = selections[0]
    #   To make the tool load only filed in the folder you select without traversing all folders under it,
    #   set config['scanType'] to 'list' rather than 'walk'.  'walk' will cause the folder scan to
    #   include all subfolders recursively.
    dialog = ImageManager(config={'imageFileFolder': folderPath, 'scanType': 'walk', 'extSet': compatibility})
    dialog.setGeometry(QRect(100, 50, 1200, 500))
    dialog.setWindowTitle(MODULE_NAME)
    dialog.show()
    app.exec()
