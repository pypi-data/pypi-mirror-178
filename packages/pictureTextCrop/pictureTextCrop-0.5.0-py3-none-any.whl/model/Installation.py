#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           Installation.py
#   Language:       Python 3.0+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#

from os import environ

USER_HOME = environ['HOME']
INSTALLED_PY_MODULES    = None
ALL_PY_MODULES          = None

#   DATA_FOLDER             = environ['HOME'] + '/PycharmProjects/PictureTextCrop/model'
TEXT_EXTRACTION_DB_FILE = 'TextExtraction.db'
#   TEST_SAMPLE_FILES       = environ['HOME'] + '/PycharmProjects/PictureTextCrop/test/samples'