from zipfile import *

f = ZipFile('images.zip', 'w', ZIP_DEFLATED)

# f.write('cpp.png')
# f.write('C#.svg')
# f.write('java.png')
# f.write('js.png')
# f.write('python.jpeg')

f.close()