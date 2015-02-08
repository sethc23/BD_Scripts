from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/html')
from HTML_API import getAllTag
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from API_system import renameFileZ,getFolderContents
from printToPDF import wordPrint

"""
f=open('/Users/admin/Desktop/TOC.Chrono.html','r')
x=f.read()
f.close()

z=getAllTag(x,'href')

print z[0]
print len(z)

ct=len(z)
fpath='/Users/admin/Desktop/Files'
for it in z:
	#print 'Files/'+str(ct)+it[-4:]
	#print it[6:]
	renameFileZ(fpath,it[6:],str(ct)+it[-4:],test=False)
	ct-=1
	#break
"""
#step 2
"""
fpath='/Users/admin/Desktop/Files'
z=getFolderContents(fpath)[0]
#print type(z)
#print type(z[0])

for it in z[:]:
	it=it.replace(fpath,"")
	a=it[-4:].lower()  #file extension
	b=it[1:].replace(a,"") #file name
	if a == '.doc':
		wordPrint(fpath+it,1,b+".pdf")
"""
fpath='/Users/admin/Desktop/Files'
z=getFolderContents(fpath)[0]
for it in z[:]:
	it=it.replace(fpath,"").lstrip('/')
	a=it[-4:] #file extension
	b=it.replace(a,"") #file name
	if len(b) == 1:
		c='00'+b+a
		print it
		print c
		renameFileZ(fpath,it,c,test=False)
	if len(b) == 2:
		c='0'+b+a
		print it
		print c
		renameFileZ(fpath,it,c,test=False)