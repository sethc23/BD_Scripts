import os

base_dir = '/Users/admin/Desktop'
desktop_files = os.listdir(base_dir)

for item in desktop_files:
    if os.path.isdir(base_dir + '/' + item):
        pass
    else:
        if item.find('.txt') != -1:
            f = open(base_dir + '/' + item, 'r')
            x = f.read()
            f.close()
            x = x.replace('\xff\xfe', '')
            x = x.replace('\x00', '')
            if x.find('Name\tArtist\tComposer') == 0:
                f = open(base_dir + '/' + item, 'w')              
                x = x.replace(':', '/')
                x = x.replace('MacOSX/', 'F:/')
                f.write(x)
                f.close()
            
