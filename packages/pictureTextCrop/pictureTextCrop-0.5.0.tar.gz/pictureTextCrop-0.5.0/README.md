# pictureTextCrop

Quick Start:

This application can be run by simply unzipping the source archive, pictureTextCrop.tar.gz into 
a new directory that you create to contain the application and its files.  Once unzipped, do into the
pictureTextCrop folder, and from there into its 'src' folder.  It should have the main application script in it, pictureTextCrop.py.
To start the application, execute the following on the command line:

$ python3 pictureTextCrop.py


Introduction:

This application is a simple tool which allows you to interactively extract text from image files by dragging
 from the top-left corner of a crop rectangle to the bottom-right corner.  When you release the mouse button
 the text inside the rectangle is printed to the console and a record of the conversion and its result
 is made in the SQLite3 database, TextExtraction.db, in the CropLog table.  Each record of this table
 records the date and time of the extraction in its timeStamp field, the full path to the file on your
 disk of the image file in the filePath field, the coordinates of the crop in the coordinates field, and
 the text of the crop in the text field.  The value of storing all extractions in a database table is
 simply that you can then search large numbers of images containing particular text using SQL.

 When you start the program, a folder selection dialog will appear.  Select the folder you want to look
 for images in here.  When you do, the application builds an index of all of the recognized image files
 in the folder to any depth in the folder tree.  The image formats recognized are those of the Pillow
 python imaging processing library, which includes those associated with the following file extensions:

            'apng', 'blp', 'blp1', 'blp2', 'bmp', 'dds', 'dib', 'dxt1', 'dxt3', 'dxt5', 'eps',
            'gif', 'icns', 'ico', 'im', 'jfif', 'jpeg', 'jpg', 'msp', 'pbm', 'pcx', 'pgm', 'png',
            'pnm', 'ppm', 'sgi', 'spi', 'tga', 'tiff', 'webp', 'xbm'

 The application then displays a dialog with a list of the files identified using their extensions.  use of
 MIME type recognizing software is planned for the future.  The list of files will be on the left, and in
 the right half of the dialog will be a space which shows the image selected when you click on a file
 path in the list.  The status bar shows the full path in case yours are longer than will fit in the
 space provided by the list.  The dialog can be resized to accomdate your needs.

 To extract text from an image, select the checkbox located to the left of it and click on the "Select Image Text"
 button in the button-bar at the top.  You can select multiple files and a text selection dialog will be
 stacked up for each.  Press the left mouse button at the top left of a rectangle containing the text you
 want to extract and then drag to the lower right corner.  When you release the button the extracted text
 is printed to the console and a record of the conversion and its result is made in the SQLite3 database.
 You can do this as many times as you like for each image.  A separate log record will be made for each.


Batch Mode:

If you click on the "Batch Process" button in the tool bar the application will extract all of the text from
each of the files in the folder scan list.  This process can take some time, my own trials on my ordinary
laptop resulting in a pace of about 5 or so seconds per image.  With only 100 images, the process coul
take up to 10 minutes.  The resulting extracted text will be placed into the BachMaster table in the SQLite3
database.  The fields written in each record in include the extraction TimeStamp, the FolderPath, the FileName,
the Text, and the file metadata in the Info field.  An attempt is made on each file to also get the EXIF
data, and if successful it is placed in the Exif field.  Views for reviewing the file metadata and other
components saved in convenient formats are planned.


MIME Information Collection:

Coming Soon.
