FasdUAS 1.101.10   ��   ��    k             l     ��  ��    O ISTART ON "Goto Sheet", next sheet is sheet with conditional starting A13      � 	 	 � S T A R T   O N   " G o t o   S h e e t " ,   n e x t   s h e e t   i s   s h e e t   w i t h   c o n d i t i o n a l   s t a r t i n g   A 1 3     
  
 l     ��  ��    B <(=IF((AND(B13>1,SUM(A3:A12)=0,B13<>"")),1,(IF(B13="",2,"")))     �   x ( = I F ( ( A N D ( B 1 3 > 1 , S U M ( A 3 : A 1 2 ) = 0 , B 1 3 < > " " ) ) , 1 , ( I F ( B 1 3 = " " , 2 , " " ) ) )      l     ��  ��    $ cursor starts at B2 on sheet 1     �   < c u r s o r   s t a r t s   a t   B 2   o n   s h e e t   1      l     ��  ��     116 page up     �    1 1 6   p a g e   u p      l     ��  ��     121 page down     �    1 2 1   p a g e   d o w n      l     ��   !��      115 home    ! � " "  1 1 5   h o m e   # $ # l     �� % &��   %   117 delete (not backspace)    & � ' ' 4 1 1 7   d e l e t e   ( n o t   b a c k s p a c e ) $  ( ) ( l     ��������  ��  ��   )  * + * l     �� , -��   ,  pageCount()    - � . .  p a g e C o u n t ( ) +  / 0 / l     1���� 1 I     �������� "0 setupacrowindow setupAcroWindow��  ��  ��  ��   0  2 3 2 l     �� 4 5��   4  setupPyWindow()    5 � 6 6  s e t u p P y W i n d o w ( ) 3  7 8 7 l     �� 9 :��   9  setupTermWin()    : � ; ;  s e t u p T e r m W i n ( ) 8  < = < l     �� > ?��   >  
nextPage()    ? � @ @  n e x t P a g e ( ) =  A B A l     �� C D��   C  setupIDLE()    D � E E  s e t u p I D L E ( ) B  F G F l     �� H I��   H  
boldText()    I � J J  b o l d T e x t ( ) G  K L K l     �� M N��   M  runOCR()    N � O O  r u n O C R ( ) L  P Q P l     �� R S��   R  
doScript()    S � T T  d o S c r i p t ( ) Q  U V U l     �� W X��   W  
gotoPage()    X � Y Y  g o t o P a g e ( ) V  Z [ Z l     �� \ ]��   \  insertPages()    ] � ^ ^  i n s e r t P a g e s ( ) [  _ ` _ l     ��������  ��  ��   `  a b a l     �� c d��   c $ copyPDFtoNotebook(repeatCount)    d � e e < c o p y P D F t o N o t e b o o k ( r e p e a t C o u n t ) b  f g f l     �� h i��   h / )renameNotebookTitles(chapter,repeatCount)    i � j j R r e n a m e N o t e b o o k T i t l e s ( c h a p t e r , r e p e a t C o u n t ) g  k l k l     ��������  ��  ��   l  m n m l     ��������  ��  ��   n  o p o l     ��������  ��  ��   p  q r q i      s t s I      �������� "0 setupacrowindow setupAcroWindow��  ��   t O     $ u v u k    # w w  x y x l    �� z {��   z��		tell application "Adobe Acrobat Professional"			activate			set test to document 1			set test2 to page 2 of test			set test3 to trim box of test2			set test4 to bounds of test2			set test5 to bounds of test			get properties			get document						get page properties			--set test to active doc			--display dialog test			(*			set bounds of active doc to {47, 44, 875, 896}			set topW to PDF Window of active doc			set pageType to page layout			set zoom type of topW to {no vary}			set the zoom factor of topW to {70}			delay 0.25
			*)		end tell		tell process "Acrobat"			--get properties of page			--get properties						--set test to every property of document 1			--set test to properties of window 1			--display dialog test			tell window 1				--get properties				--set position to {47, 22}			end tell			tell document 1				--get properties			end tell					end tell
		    { � | |  	 	 t e l l   a p p l i c a t i o n   " A d o b e   A c r o b a t   P r o f e s s i o n a l "  	 	 	 a c t i v a t e  	 	 	 s e t   t e s t   t o   d o c u m e n t   1  	 	 	 s e t   t e s t 2   t o   p a g e   2   o f   t e s t  	 	 	 s e t   t e s t 3   t o   t r i m   b o x   o f   t e s t 2  	 	 	 s e t   t e s t 4   t o   b o u n d s   o f   t e s t 2  	 	 	 s e t   t e s t 5   t o   b o u n d s   o f   t e s t  	 	 	 g e t   p r o p e r t i e s  	 	 	 g e t   d o c u m e n t  	 	 	  	 	 	 g e t   p a g e   p r o p e r t i e s  	 	 	 - - s e t   t e s t   t o   a c t i v e   d o c  	 	 	 - - d i s p l a y   d i a l o g   t e s t  	 	 	 ( *  	 	 	 s e t   b o u n d s   o f   a c t i v e   d o c   t o   { 4 7 ,   4 4 ,   8 7 5 ,   8 9 6 }  	 	 	 s e t   t o p W   t o   P D F   W i n d o w   o f   a c t i v e   d o c  	 	 	 s e t   p a g e T y p e   t o   p a g e   l a y o u t  	 	 	 s e t   z o o m   t y p e   o f   t o p W   t o   { n o   v a r y }  	 	 	 s e t   t h e   z o o m   f a c t o r   o f   t o p W   t o   { 7 0 }  	 	 	 d e l a y   0 . 2 5 
 	 	 	 * )  	 	 e n d   t e l l  	 	 t e l l   p r o c e s s   " A c r o b a t "  	 	 	 - - g e t   p r o p e r t i e s   o f   p a g e  	 	 	 - - g e t   p r o p e r t i e s  	 	 	  	 	 	 - - s e t   t e s t   t o   e v e r y   p r o p e r t y   o f   d o c u m e n t   1  	 	 	 - - s e t   t e s t   t o   p r o p e r t i e s   o f   w i n d o w   1  	 	 	 - - d i s p l a y   d i a l o g   t e s t  	 	 	 t e l l   w i n d o w   1  	 	 	 	 - - g e t   p r o p e r t i e s  	 	 	 	 - - s e t   p o s i t i o n   t o   { 4 7 ,   2 2 }  	 	 	 e n d   t e l l  	 	 	 t e l l   d o c u m e n t   1  	 	 	 	 - - g e t   p r o p e r t i e s  	 	 	 e n d   t e l l  	 	 	  	 	 e n d   t e l l 
 	 	 y  }�� } O    # ~  ~ k    " � �  � � � I   ������
�� .miscactvnull��� ��� null��  ��   �  � � � e     � � n     � � � 1    ��
�� 
PDFW � n     � � � m    ��
�� 
PDFP � 4    �� �
�� 
docu � m    ����  �  � � � l   ��������  ��  ��   �  ��� � I   "�� � �
�� .coreclosnull���     obj  � 4    �� �
�� 
docu � m    ����  � �� ���
�� 
savo � m    ��
�� savono  ��  ��    m     � ��                                                                                  PDFp  alis    F  MacOSX                     ����H+    4PDFpenPro.app                                                   K U�[��        ����  	                Applications    ��      �[�5      4  !MacOSX:Applications:PDFpenPro.app     P D F p e n P r o . a p p    M a c O S X  Applications/PDFpenPro.app  / ��  ��   v m      � ��                                                                                  sevs  alis    |  MacOSX                     ����H+    -System Events.app                                               5�Ǚ@�        ����  	                CoreServices    ��      Ǚ�,      -   �   �  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��   r  � � � l     ��������  ��  ��   �  � � � i     � � � I      �������� 0 insertpages insertPages��  ��   � O      � � � k     � �  � � � I   	������
�� .miscactvnull��� ��� null��  ��   �  � � � l  
 
�� � ���   � � �insert pages of document after 3 from "/Users/sethchase/Work/ScanBusiness/Dropbox/Scripts/sanspaper/scans/Box8Scan54DS2.pdf" starting with 1 and 1 number of pages    � � � �D i n s e r t   p a g e s   o f   d o c u m e n t   a f t e r   3   f r o m   " / U s e r s / s e t h c h a s e / W o r k / S c a n B u s i n e s s / D r o p b o x / S c r i p t s / s a n s p a p e r / s c a n s / B o x 8 S c a n 5 4 D S 2 . p d f "   s t a r t i n g   w i t h   1   a n d   1   n u m b e r   o f   p a g e s �  � � � r   
  � � � c   
  � � � m   
  � � � � � � M a c O S X : U s e r s : s e t h c h a s e : W o r k : S c a n B u s i n e s s : D r o p b o x : S c r i p t s : A c r o J S : p a g e N u m b e r . t x t � m    ��
�� 
alis � o      ���� 0 ascriptpath aScriptPath �  � � � I   ���� �
�� .miscdoscnull��� ��� utxt��   � �� ���
�� 
file � o    ���� 0 ascriptpath aScriptPath��   �  � � � l   �� � ���   �VPdo script "var pageIndex = 0; var filePath = "/Users/sethchase/Work/ScanBusiness/Dropbox/Scripts/sanspaper/scans/Box8Scan54DS2.pdf"; var Start = "0"; var End = "0"; function insertThis(pageIndex,filePath,Start,End){this.insertPages({nPage: pageIndex,cPath: filePath,nStart: Start,nEnd: End})}; insertThis(pageIndex,filePath,Start,End);"    � � � �� d o   s c r i p t   " v a r   p a g e I n d e x   =   0 ;   v a r   f i l e P a t h   =   " / U s e r s / s e t h c h a s e / W o r k / S c a n B u s i n e s s / D r o p b o x / S c r i p t s / s a n s p a p e r / s c a n s / B o x 8 S c a n 5 4 D S 2 . p d f " ;   v a r   S t a r t   =   " 0 " ;   v a r   E n d   =   " 0 " ;   f u n c t i o n   i n s e r t T h i s ( p a g e I n d e x , f i l e P a t h , S t a r t , E n d ) { t h i s . i n s e r t P a g e s ( { n P a g e :   p a g e I n d e x , c P a t h :   f i l e P a t h , n S t a r t :   S t a r t , n E n d :   E n d } ) } ;   i n s e r t T h i s ( p a g e I n d e x , f i l e P a t h , S t a r t , E n d ) ; " �  � � � r     � � � m     � � � � � � / U s e r s / s e t h c h a s e / W o r k / S c a n B u s i n e s s / D r o p b o x / S c r i p t s / s a n s p a p e r / s c a n s / B o x 8 S c a n 5 4 D S 2 . p d f � o      ���� 0 fromfilepath fromFilePath �  � � � l   �� � ���   � ] Wdo script "this.insertPages({nPage: 1,cPath: " & fromFilePath & ",nStart: 1,nEnd: 2});"    � � � � � d o   s c r i p t   " t h i s . i n s e r t P a g e s ( { n P a g e :   1 , c P a t h :   "   &   f r o m F i l e P a t h   &   " , n S t a r t :   1 , n E n d :   2 } ) ; " �  � � � l   �� � ���   � " tell window to goto page  10    � � � � 8 t e l l   w i n d o w   t o   g o t o   p a g e     1 0 �  ��� � l   �� � ���   � $ do script "this.pageNum = 10;"    � � � � < d o   s c r i p t   " t h i s . p a g e N u m   =   1 0 ; "��   � m      � �6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��   �  � � � l     ��������  ��  ��   �  � � � i     � � � I      �������� 0 gotopage gotoPage��  ��   � l     � � � � O      � � � k     � �  � � � I   	������
�� .miscactvnull��� ��� null��  ��   �  � � � l  
 
�� � ���   �  tell window    � � � �  t e l l   w i n d o w �  � � � l  
 
�� � ���   �  set page of window to 10    � � � � 0 s e t   p a g e   o f   w i n d o w   t o   1 0 �  � � � l  
 
�� � ���   �  make page "10"    � � � �  m a k e   p a g e   " 1 0 " �  � � � l  
 
�� � ���   � # tell window 1 to make page 10    � � � � : t e l l   w i n d o w   1   t o   m a k e   p a g e   1 0 �  ��� � l  
 
�� � ���   �  end tell    � � � �  e n d   t e l l��   � m      � �6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��   �  NOT WORK    � � � �  N O T   W O R K �  � � � l     ��������  ��  ��   �  � � � l      �� � ���   ���on renameNotebookTitles(chapter, repeatCount)	activate application "NoteBook.app"	tell application "System Events"		tell process "Notebook"			repeat with i from 1 to repeatCount				delay 0.15				key code 0				delay 0.15				key code 115 using shift down				delay 0.15				set typeText to chapter & "." & (i + 0)				set the clipboard to (typeText as text)				delay 0.15				key code 9 using command down				delay 0.25				key code 36				delay 0.2				key code 125				delay 0.15			end repeat		end tell	end tellend renameNotebookTitleson copyPDFtoNotebook(repeatCount)	repeat repeatCount times		activate application "Adobe Acrobat Professional"		tell application "System Events"			tell process "Acrobat"				delay 0.15				key code 0 using command down				delay 0.25				key code 8 using command down				delay 0.25				key code 124				delay 0.15			end tell		end tell		activate application "NoteBook.app"		tell application "System Events"			tell process "Notebook"				delay 0.15				key code 45 using {shift down, command down}				delay 0.5				key code 36				delay 0.25				key code 9 using command down				delay 0.3				key code 11 using command down				delay 0.2			end tell		end tell	end repeatend copyPDFtoNotebook
    � � � �	�  o n   r e n a m e N o t e b o o k T i t l e s ( c h a p t e r ,   r e p e a t C o u n t )  	 a c t i v a t e   a p p l i c a t i o n   " N o t e B o o k . a p p "  	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 t e l l   p r o c e s s   " N o t e b o o k "  	 	 	 r e p e a t   w i t h   i   f r o m   1   t o   r e p e a t C o u n t  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 k e y   c o d e   0  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 k e y   c o d e   1 1 5   u s i n g   s h i f t   d o w n  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 s e t   t y p e T e x t   t o   c h a p t e r   &   " . "   &   ( i   +   0 )  	 	 	 	 s e t   t h e   c l i p b o a r d   t o   ( t y p e T e x t   a s   t e x t )  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 k e y   c o d e   9   u s i n g   c o m m a n d   d o w n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   3 6  	 	 	 	 d e l a y   0 . 2  	 	 	 	 k e y   c o d e   1 2 5  	 	 	 	 d e l a y   0 . 1 5  	 	 	 e n d   r e p e a t  	 	 e n d   t e l l  	 e n d   t e l l  e n d   r e n a m e N o t e b o o k T i t l e s  o n   c o p y P D F t o N o t e b o o k ( r e p e a t C o u n t )  	 r e p e a t   r e p e a t C o u n t   t i m e s  	 	 a c t i v a t e   a p p l i c a t i o n   " A d o b e   A c r o b a t   P r o f e s s i o n a l "  	 	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 	 t e l l   p r o c e s s   " A c r o b a t "  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 k e y   c o d e   0   u s i n g   c o m m a n d   d o w n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   8   u s i n g   c o m m a n d   d o w n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   1 2 4  	 	 	 	 d e l a y   0 . 1 5  	 	 	 e n d   t e l l  	 	 e n d   t e l l  	 	 a c t i v a t e   a p p l i c a t i o n   " N o t e B o o k . a p p "  	 	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 	 t e l l   p r o c e s s   " N o t e b o o k "  	 	 	 	 d e l a y   0 . 1 5  	 	 	 	 k e y   c o d e   4 5   u s i n g   { s h i f t   d o w n ,   c o m m a n d   d o w n }  	 	 	 	 d e l a y   0 . 5  	 	 	 	 k e y   c o d e   3 6  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   9   u s i n g   c o m m a n d   d o w n  	 	 	 	 d e l a y   0 . 3  	 	 	 	 k e y   c o d e   1 1   u s i n g   c o m m a n d   d o w n  	 	 	 	 d e l a y   0 . 2  	 	 	 e n d   t e l l  	 	 e n d   t e l l  	 e n d   r e p e a t  e n d   c o p y P D F t o N o t e b o o k  
 �  � � � l     ��������  ��  ��   �  � � � i     � � � I      �������� 0 setuptermwin setupTermWin��  ��   � O      �  � O     k      I   ������
�� .miscactvnull��� ��� null��  ��    r    	 n    

 1    ��
�� 
pbnd 4   ��
�� 
cwin m    ���� 	 o      ���� 0 x   �� l   ����   8 2set bounds of front window to {880, 25, 1440, 627}    � d s e t   b o u n d s   o f   f r o n t   w i n d o w   t o   { 8 8 0 ,   2 5 ,   1 4 4 0 ,   6 2 7 }��   m    �                                                                                      @ alis    X  MacOSX                     ����H+    5Terminal.app                                                     ZǙ/�        ����  	                	Utilities     ��      ǙvL      5  4  *MacOSX:Applications:Utilities:Terminal.app    T e r m i n a l . a p p    M a c O S X  #Applications/Utilities/Terminal.app   / ��    m     �                                                                                  sevs  alis    |  MacOSX                     ����H+    -System Events.app                                               5�Ǚ@�        ����  	                CoreServices    ��      Ǚ�,      -   �   �  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��   �  l     ��������  ��  ��    i     I      �������� 0 doscript doScript��  ��   O      k      I   	������
�� .miscactvnull��� ��� null��  ��    l  
 
� !�    U Oset aScriptPath to ("Macintosh HD:Users:sethchase:Desktop:jsTest.txt" as alias)   ! �"" � s e t   a S c r i p t P a t h   t o   ( " M a c i n t o s h   H D : U s e r s : s e t h c h a s e : D e s k t o p : j s T e s t . t x t "   a s   a l i a s ) #$# l  
 
�~%&�~  %   do script file aScriptPath   & �'' 4 d o   s c r i p t   f i l e   a S c r i p t P a t h$ ()( l  
 
�}*+�}  *XRdo script "/Applications/Adobe/Adobe Acrobat X Pro/Adobe Acrobat Pro.app').do_script(u'var pageIndex = 0; var filePath = \"/Users/sethchase/Work/ScanBusiness/Dropbox/Scripts/sanspaper/scans/Box8Scan54DS2.pdf\"; function insertThis(pageIndex,filePath){this.insertPages({nPage: pageIndex,cPath: filePath})}; insertThis(pageIndex,filePath);"   + �,,� d o   s c r i p t   " / A p p l i c a t i o n s / A d o b e / A d o b e   A c r o b a t   X   P r o / A d o b e   A c r o b a t   P r o . a p p ' ) . d o _ s c r i p t ( u ' v a r   p a g e I n d e x   =   0 ;   v a r   f i l e P a t h   =   \ " / U s e r s / s e t h c h a s e / W o r k / S c a n B u s i n e s s / D r o p b o x / S c r i p t s / s a n s p a p e r / s c a n s / B o x 8 S c a n 5 4 D S 2 . p d f \ " ;   f u n c t i o n   i n s e r t T h i s ( p a g e I n d e x , f i l e P a t h ) { t h i s . i n s e r t P a g e s ( { n P a g e :   p a g e I n d e x , c P a t h :   f i l e P a t h } ) } ;   i n s e r t T h i s ( p a g e I n d e x , f i l e P a t h ) ; ") -.- l  
 
�|/0�|  / " tell window to goto page  10   0 �11 8 t e l l   w i n d o w   t o   g o t o   p a g e     1 0. 2�{2 I  
 �z3�y
�z .miscdoscnull��� ��� utxt3 m   
 44 �55 $ t h i s . p a g e N u m   =   1 0 ;�y  �{   m     666                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��   787 l     �x�w�v�x  �w  �v  8 9:9 l     �u�t�s�u  �t  �s  : ;<; i    =>= I      �r�q�p�r 0 runocr runOCR�q  �p  > k     �?? @A@ r     BCB m     �o�o C o      �n�n 0 fcount fCountA DED r    FGF J    �m�m  G o      �l�l 0 
folderlist 
folderListE HIH r   	 JKJ J   	 �k�k  K o      �j�j 0 filelist fileListI LML r    NON m    �i�i  O o      �h�h  0 totalpagecount totalPageCountM P�gP O    �QRQ k    �SS TUT I   �f�e�d
�f .miscactvnull��� ��� null�e  �d  U VWV l   �cXY�c  X � �set fName to folder "2" of folder "Copy" of folder "Pierce Library" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk   Y �ZZ s e t   f N a m e   t o   f o l d e r   " 2 "   o f   f o l d e r   " C o p y "   o f   f o l d e r   " P i e r c e   L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s kW [\[ l   �b]^�b  ] � �set fName to folder "Week9" of folder "Archives" of folder "Reports" of folder "PierceLibrary" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk   ^ �__T s e t   f N a m e   t o   f o l d e r   " W e e k 9 "   o f   f o l d e r   " A r c h i v e s "   o f   f o l d e r   " R e p o r t s "   o f   f o l d e r   " P i e r c e L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s k\ `a` r    0bcb n    .ded 4   + .�af
�a 
cfolf m   , -gg �hh  8e n    +iji 4   ( +�`k
�` 
cfolk m   ) *ll �mm  P i e r c e L i b r a r yj n    (non 4   % (�_p
�_ 
cfolp m   & 'qq �rr  D e s k t o po n    %sts 4   " %�^u
�^ 
cfolu m   # $vv �ww  s e t h c h a s et n    "xyx 4    "�]z
�] 
cfolz m     !{{ �|| 
 U s e r sy 1    �\
�\ 
sdskc o      �[�[ 0 fname fNamea }~} l  1 1�Z��Z   . (set fileCount to count of files in fName   � ��� P s e t   f i l e C o u n t   t o   c o u n t   o f   f i l e s   i n   f N a m e~ ��� r   1 6��� n  1 4��� 2   2 4�Y
�Y 
file� o   1 2�X�X 0 fname fName� o      �W�W 0 filelist fileList� ��� X   7 ���V�� k   G ��� ��� O   G Z��� k   K Y�� ��� I  K P�U��T
�U .aevtodocnull  �    alis� o   K L�S�S 0 y  �T  � ��R� r   Q Y��� 4  Q W�Q�
�Q 
cwin� m   U V�P�P � o      �O�O 0 topw topW�R  � m   G H��6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��  � ��� I  [ `�N��M
�N .miscactvnull��� ��� null� m   [ \��6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��  �M  � ��� O   a ���� O   g ���� k   r ��� ��� I  r ��L��K
�L .prcsclicuiel    ��� uiel� n   r ���� 4   � ��J�
�J 
menI� m   � ��� ��� 6 R e c o g n i z e   T e x t   U s i n g   O C R . . .� n   r ���� 4   � ��I�
�I 
menE� m   � ��H�H � n   r ���� 4   � ��G�
�G 
menI� m   � ��� ��� ( O C R   T e x t   R e c o g n i t i o n� n   r ���� 4    ��F�
�F 
menE� m   � ��E�E � n   r ��� 4   x �D�
�D 
mbri� m   { ~�� ���  D o c u m e n t� 4   r x�C�
�C 
mbar� m   v w�B�B �K  � ��A� I  � ��@��?
�@ .prcsclicuiel    ��� uiel� n   � ���� 4   � ��>�
�> 
butT� m   � ��� ���  O K� 4   � ��=�
�= 
cwin� m   � ��� ���  R e c o g n i z e   T e x t�?  �A  � 4   g o�<�
�< 
prcs� m   k n�� ���  A c r o b a t� m   a d���                                                                                  sevs  alis    |  MacOSX                     ����H+    -System Events.app                                               5�Ǚ@�        ����  	                CoreServices    ��      Ǚ�,      -   �   �  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��  � ��� l   � ��;���;  � � �			tell application "System Events"				tell process "Acrobat"					click menu item "Save" of menu 1 of menu bar item "File" of menu bar 1				end tell			end tell
			   � ���P  	 	 	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 	 	 t e l l   p r o c e s s   " A c r o b a t "  	 	 	 	 	 c l i c k   m e n u   i t e m   " S a v e "   o f   m e n u   1   o f   m e n u   b a r   i t e m   " F i l e "   o f   m e n u   b a r   1  	 	 	 	 e n d   t e l l  	 	 	 e n d   t e l l 
 	 	 	� ��� O   � ���� k   � ��� ��� t   � ���� k   � ��� ��� I  � ��:�9�8
�: .miscactvnull��� ��� null�9  �8  � ��7� I  � ��6��5
�6 .coresavenull        obj � l  � ���4�3� 4  � ��2�
�2 
docu� m   � ��1�1 �4  �3  �5  �7  � m   � ��0�0   ��� ��/� I  � ��.��-
�. .coreclosnull���     obj � l  � ���,�+� 4  � ��*�
�* 
docu� m   � ��)�) �,  �+  �-  �/  � m   � ���6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��  � ��(� l  � ��'�&�%�'  �&  �%  �(  �V 0 y  � o   : ;�$�$ 0 filelist fileList� ��#� l  � ��"���"  �  
end repeat   � ���  e n d   r e p e a t�#  R m    ���                                                                                  MACS  alis    `  MacOSX                     ����H+    -
Finder.app                                                       ��ǟ[�        ����  	                CoreServices    ��      ǟ��      -   �   �  -MacOSX:System:Library:CoreServices:Finder.app    
 F i n d e r . a p p    M a c O S X  &System/Library/CoreServices/Finder.app  / ��  �g  < ��� l     �!� ��!  �   �  � ��� l     ����  �  �  � ��� l      ����  ���on boldText()	tell application "Adobe Acrobat Professional" to activate	tell application "System Events"		tell process "Acrobat"			delay 0.25			keystroke "a" using command down			delay 0.25			keystroke "c" using command down			delay 0.25		end tell	end tell	tell application "Tex-Edit Plus.app"		activate		�event miscpast� the (the clipboard)		set textLines to lines of window 1		set styleLines to uniform styles of lines of window 1		set styleText to ""		repeat with i from 1 to (count of items in textLines)			set {text style info:styleType} to {text style info:on styles} of (item i of styleLines)			if styleType is not equal to {plain} then				set styleText to (styleText & ((item i of textLines) as text))			end if		end repeat		set selection to styleText		�event TXEDREPL� window 1 given �class SRst�:"^c", �class SRwi�:" "		set styleText to selection		set the clipboard to styleText	end tellend boldText   � ���T  o n   b o l d T e x t ( )  	 t e l l   a p p l i c a t i o n   " A d o b e   A c r o b a t   P r o f e s s i o n a l "   t o   a c t i v a t e  	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 t e l l   p r o c e s s   " A c r o b a t "  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y s t r o k e   " a "   u s i n g   c o m m a n d   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y s t r o k e   " c "   u s i n g   c o m m a n d   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 e n d   t e l l  	 e n d   t e l l  	 t e l l   a p p l i c a t i o n   " T e x - E d i t   P l u s . a p p "  	 	 a c t i v a t e  	 	 � e v e n t   m i s c p a s t �   t h e   ( t h e   c l i p b o a r d )  	 	 s e t   t e x t L i n e s   t o   l i n e s   o f   w i n d o w   1  	 	 s e t   s t y l e L i n e s   t o   u n i f o r m   s t y l e s   o f   l i n e s   o f   w i n d o w   1  	 	 s e t   s t y l e T e x t   t o   " "  	 	 r e p e a t   w i t h   i   f r o m   1   t o   ( c o u n t   o f   i t e m s   i n   t e x t L i n e s )  	 	 	 s e t   { t e x t   s t y l e   i n f o : s t y l e T y p e }   t o   { t e x t   s t y l e   i n f o : o n   s t y l e s }   o f   ( i t e m   i   o f   s t y l e L i n e s )  	 	 	 i f   s t y l e T y p e   i s   n o t   e q u a l   t o   { p l a i n }   t h e n  	 	 	 	 s e t   s t y l e T e x t   t o   ( s t y l e T e x t   &   ( ( i t e m   i   o f   t e x t L i n e s )   a s   t e x t ) )  	 	 	 e n d   i f  	 	 e n d   r e p e a t  	 	 s e t   s e l e c t i o n   t o   s t y l e T e x t  	 	 � e v e n t   T X E D R E P L �   w i n d o w   1   g i v e n   � c l a s s   S R s t � : " ^ c " ,   � c l a s s   S R w i � : "   "  	 	 s e t   s t y l e T e x t   t o   s e l e c t i o n  	 	 s e t   t h e   c l i p b o a r d   t o   s t y l e T e x t  	 e n d   t e l l  e n d   b o l d T e x t � ��� i    ��� I      ���� 0 nextpage nextPage�  �  � O     )��� O    (��� k    '�� ��� O       I   ���
� .miscactvnull��� ��� null�  �   m    6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��  �  I   ��
� .sysodelanull��� ��� nmbr m     ?�      �    I   !�	�
� .prcskcodnull���    long	 m    �� |�   
�
 I  " '��
� .sysodelanull��� ��� nmbr m   " # ?�      �  �  � 4    �
� 
pcap m     �  A c r o b a t� m     �                                                                                  sevs  alis    |  MacOSX                     ����H+    -System Events.app                                               5�Ǚ@�        ����  	                CoreServices    ��      Ǚ�,      -   �   �  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��  �  l     ��
�	�  �
  �	    l     ����  �  �    l     ����  �  �    i     I      ��� � 0 setuppywindow setupPyWindow�  �    k     8  O     6 k    5   !"! r    #$# n    %&% 1    ��
�� 
prsz& n    '(' 4    ��)
�� 
cwin) m   	 
** �++  P y t h o n   S h e l l( 4    ��,
�� 
pcap, m    -- �..  I D L E$ o      ���� 0 x  " /0/ r    121 J    33 454 m    ����s5 6��6 m    ���� ��  2 n      787 1    ��
�� 
posn8 n    9:9 4    ��;
�� 
uiel; m    << �==  P y t h o n   S h e l l: 4    ��>
�� 
pcap> m    ?? �@@  I D L E0 A��A r    5BCB J    %DD EFE m     ����sF GHG m     !����nH IJI m   ! "���� J K��K m   " #����,��  C n      LML 1   0 4��
�� 
pbndM n   % 0NON 4   + 0��P
�� 
cwinP m   , /QQ �RR  P y t h o n   S h e l lO 4   % +��S
�� 
prcsS m   ' *TT �UU  I D L E��   m     VV�                                                                                  sevs  alis    |  MacOSX                     ����H+    -System Events.app                                               5�Ǚ@�        ����  	                CoreServices    ��      Ǚ�,      -   �   �  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��   W��W l   7 7��XY��  X	tell application "System Events"		set y to name of every window		activate application "Finder"		tell process "IDLE"			set x to name of every window			repeat with j in x				if (j as text) is "Python Shell" then					set windowTitle to j					click menu item "Python Shell" of menu 1 of menu bar item "Window" of menu bar 1					set size of window windowTitle to {527, 300}				end if				if (j as text) is "*Python Shell*" then					set windowTitle to j					click menu item "Python Shell" of menu 1 of menu bar item "Window" of menu bar 1					set size of window windowTitle to {527, 300}				end if			end repeat		end tell		tell application process "IDLE"			set position of window windowTitle to {883, 25}			--set size of window 1 to {527, 602}		end tell	end tell
	   Y �ZZ  	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 s e t   y   t o   n a m e   o f   e v e r y   w i n d o w  	 	 a c t i v a t e   a p p l i c a t i o n   " F i n d e r "  	 	 t e l l   p r o c e s s   " I D L E "  	 	 	 s e t   x   t o   n a m e   o f   e v e r y   w i n d o w  	 	 	 r e p e a t   w i t h   j   i n   x  	 	 	 	 i f   ( j   a s   t e x t )   i s   " P y t h o n   S h e l l "   t h e n  	 	 	 	 	 s e t   w i n d o w T i t l e   t o   j  	 	 	 	 	 c l i c k   m e n u   i t e m   " P y t h o n   S h e l l "   o f   m e n u   1   o f   m e n u   b a r   i t e m   " W i n d o w "   o f   m e n u   b a r   1  	 	 	 	 	 s e t   s i z e   o f   w i n d o w   w i n d o w T i t l e   t o   { 5 2 7 ,   3 0 0 }  	 	 	 	 e n d   i f  	 	 	 	 i f   ( j   a s   t e x t )   i s   " * P y t h o n   S h e l l * "   t h e n  	 	 	 	 	 s e t   w i n d o w T i t l e   t o   j  	 	 	 	 	 c l i c k   m e n u   i t e m   " P y t h o n   S h e l l "   o f   m e n u   1   o f   m e n u   b a r   i t e m   " W i n d o w "   o f   m e n u   b a r   1  	 	 	 	 	 s e t   s i z e   o f   w i n d o w   w i n d o w T i t l e   t o   { 5 2 7 ,   3 0 0 }  	 	 	 	 e n d   i f  	 	 	 e n d   r e p e a t  	 	 e n d   t e l l  	 	 t e l l   a p p l i c a t i o n   p r o c e s s   " I D L E "  	 	 	 s e t   p o s i t i o n   o f   w i n d o w   w i n d o w T i t l e   t o   { 8 8 3 ,   2 5 }  	 	 	 - - s e t   s i z e   o f   w i n d o w   1   t o   { 5 2 7 ,   6 0 2 }  	 	 e n d   t e l l  	 e n d   t e l l 
 	��   [\[ l     ��������  ��  ��  \ ]^] i     #_`_ I      �������� 0 	pagecount 	pageCount��  ��  ` k     {aa bcb r     ded m     ���� e o      ���� 0 fcount fCountc fgf r    hih J    ����  i o      ���� 0 
folderlist 
folderListg jkj r   	 lml J   	 ����  m o      ���� 0 filelist fileListk non r    pqp m    ����  q o      ����  0 totalpagecount totalPageCounto rsr O    utut k    tvv wxw I   ������
�� .miscactvnull��� ��� null��  ��  x yzy l   ��������  ��  ��  z {|{ l   ��}~��  } � �set fName to folder "2" of folder "Copy" of folder "Pierce Library" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk   ~ � s e t   f N a m e   t o   f o l d e r   " 2 "   o f   f o l d e r   " C o p y "   o f   f o l d e r   " P i e r c e   L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s k| ��� l   ������  � � �set fName to folder "Week4" of folder "Archives" of folder "Reports" of folder "PierceLibrary" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk   � ���T s e t   f N a m e   t o   f o l d e r   " W e e k 4 "   o f   f o l d e r   " A r c h i v e s "   o f   f o l d e r   " R e p o r t s "   o f   f o l d e r   " P i e r c e L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s k� ��� r    -��� n    +��� 4   ( +���
�� 
cfol� m   ) *�� ��� 
 T e s t 1� n    (��� 4   % (���
�� 
cfol� m   & '�� ���  D e s k t o p� n    %��� 4   " %���
�� 
cfol� m   # $�� ���  s e t h c h a s e� n    "��� 4    "���
�� 
cfol� m     !�� ��� 
 U s e r s� 1    ��
�� 
sdsk� o      ���� 0 fname fName� ��� l  . .������  � � �set fName to folder "extracted" of folder "Pierce Library" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk   � ��� s e t   f N a m e   t o   f o l d e r   " e x t r a c t e d "   o f   f o l d e r   " P i e r c e   L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s k� ��� l  . .������  � . (set fileCount to count of files in fName   � ��� P s e t   f i l e C o u n t   t o   c o u n t   o f   f i l e s   i n   f N a m e� ��� l  . .��������  ��  ��  � ��� r   . 3��� n  . 1��� 2   / 1��
�� 
file� o   . /���� 0 fname fName� o      ���� 0 filelist fileList� ��� l  4 4��������  ��  ��  � ��� X   4 r����� O   D m��� k   H l�� ��� I  H M�����
�� .aevtodocnull  �    alis� o   H I���� 0 y  ��  � ��� r   N T��� 4  N R���
�� 
cwin� m   P Q���� � o      ���� 0 topw topW� ��� r   U `��� I  U ^�����
�� .corecnte****       ****� 2   U Z��
�� 
page��  � o      ���� 0 pcount pCount� ��� I  a f������
�� .CAROcldcnull��� ��� null��  ��  � ���� r   g l��� l  g j������ [   g j��� o   g h����  0 totalpagecount totalPageCount� o   h i���� 0 pcount pCount��  ��  � o      ����  0 totalpagecount totalPageCount��  � m   D E��6                                                                                  CARO  alis    �  MacOSX                     ����H+   jAdobe Acrobat Professional.app                                  �#�d�        ����  	                Adobe Acrobat 8 Professional    ��      �dS2     j  4  OMacOSX:Applications:Adobe Acrobat 8 Professional:Adobe Acrobat Professional.app   >  A d o b e   A c r o b a t   P r o f e s s i o n a l . a p p    M a c O S X  HApplications/Adobe Acrobat 8 Professional/Adobe Acrobat Professional.app  / ��  �� 0 y  � o   7 8���� 0 filelist fileList� ��� l  s s������  �  
end repeat   � ���  e n d   r e p e a t� ���� l  s s��������  ��  ��  ��  u m    ���                                                                                  MACS  alis    `  MacOSX                     ����H+    -
Finder.app                                                       ��ǟ[�        ����  	                CoreServices    ��      ǟ��      -   �   �  -MacOSX:System:Library:CoreServices:Finder.app    
 F i n d e r . a p p    M a c O S X  &System/Library/CoreServices/Finder.app  / ��  s ���� I  v {�����
�� .sysodlogaskr        TEXT� o   v w����  0 totalpagecount totalPageCount��  ��  ^ ��� l     ��������  ��  ��  � ���� l     ��������  ��  ��  ��       ���������������  � 
���������������������� "0 setupacrowindow setupAcroWindow�� 0 insertpages insertPages�� 0 gotopage gotoPage�� 0 setuptermwin setupTermWin�� 0 doscript doScript�� 0 runocr runOCR�� 0 nextpage nextPage�� 0 setuppywindow setupPyWindow�� 0 	pagecount 	pageCount
�� .aevtoappnull  �   � ****� �� t���������� "0 setupacrowindow setupAcroWindow��  ��  �  � 	 � ���������������
�� .miscactvnull��� ��� null
�� 
docu
�� 
PDFP
�� 
PDFW
�� 
savo
�� savono  
�� .coreclosnull���     obj �� %� !� *j O*�k/�,�,EO*�k/��l UU� �� ����������� 0 insertpages insertPages��  ��  � ������ 0 ascriptpath aScriptPath�� 0 fromfilepath fromFilePath�  ��� ������ �
�� .miscactvnull��� ��� null
�� 
alis
�� 
file
� .miscdoscnull��� ��� utxt�� � *j O��&E�O*�l O�E�OPU� �~ ��}�|���{�~ 0 gotopage gotoPage�}  �|  �  �  ��z
�z .miscactvnull��� ��� null�{ � 	*j OPU� �y ��x�w���v�y 0 setuptermwin setupTermWin�x  �w  � �u�u 0 x  � �t�s�r
�t .miscactvnull��� ��� null
�s 
cwin
�r 
pbnd�v � � *j O*�k/�,E�OPUU� �q�p�o���n�q 0 doscript doScript�p  �o  �  � 6�m4�l
�m .miscactvnull��� ��� null
�l .miscdoscnull��� ��� utxt�n � *j O�j U� �k>�j�i���h�k 0 runocr runOCR�j  �i  � �g�f�e�d�c�b�a�g 0 fcount fCount�f 0 
folderlist 
folderList�e 0 filelist fileList�d  0 totalpagecount totalPageCount�c 0 fname fName�b 0 y  �a 0 topw topW� #�`��_�^�]{vqlg�\�[�Z�Y��X�W��V��U�T��S�R���Q��P��O�N�M�L�` 
�_ .miscactvnull��� ��� null
�^ 
sdsk
�] 
cfol
�\ 
file
�[ 
kocl
�Z 
cobj
�Y .corecnte****       ****
�X .aevtodocnull  �    alis
�W 
cwin
�V 
prcs
�U 
mbar
�T 
mbri
�S 
menE
�R 
menI
�Q .prcsclicuiel    ��� uiel
�P 
butT�O   ��
�N 
docu
�M .coresavenull        obj 
�L .coreclosnull���     obj �h ��E�OjvE�OjvE�OjE�O� �*j O*�,��/��/��/��/��/E�O��-E�O ��[��l kh � �j O*a k/E�UO�j Oa  K*a a / ?*a k/a a /a k/a a /a k/a a /j O*a a /a a /j UUO� "a n*j O*a  k/j !oO*a  k/j "UOP[OY�hOPU� �K��J�I���H�K 0 nextpage nextPage�J  �I  �  � 	�G�F�E�D�C
�G 
pcap
�F .miscactvnull��� ��� null
�E .sysodelanull��� ��� nmbr�D |
�C .prcskcodnull���    long�H *� &*��/ � *j UO�j O�j O�j UU� �B�A�@���?�B 0 setuppywindow setupPyWindow�A  �@  � �>�> 0 x  � V�=-�<*�;�:�9?�8<�7�6�5�4�3TQ�2
�= 
pcap
�< 
cwin
�; 
prsz�:s�9 
�8 
uiel
�7 
posn�6n�5,�4 
�3 
prcs
�2 
pbnd�? 9� 3*��/��/�,E�O��lv*��/��/�,FO�����v*�a /�a /a ,FUOP� �1`�0�/���.�1 0 	pagecount 	pageCount�0  �/  � �-�,�+�*�)�(�'�&�- 0 fcount fCount�, 0 
folderlist 
folderList�+ 0 filelist fileList�*  0 totalpagecount totalPageCount�) 0 fname fName�( 0 y  �' 0 topw topW�& 0 pcount pCount� �%��$�#�"�����!� ���������% 
�$ .miscactvnull��� ��� null
�# 
sdsk
�" 
cfol
�! 
file
�  
kocl
� 
cobj
� .corecnte****       ****
� .aevtodocnull  �    alis
� 
cwin
� 
page
� .CAROcldcnull��� ��� null
� .sysodlogaskr        TEXT�. |�E�OjvE�OjvE�OjE�O� `*j O*�,��/��/��/��/E�O��-E�O =�[��l kh � &�j O*�k/E�O*a -j E�O*j O��E�U[OY��OPUO�j � �������
� .aevtoappnull  �   � ****� k     ��  /��  �  �  �  � �� "0 setupacrowindow setupAcroWindow� *j+   ascr  ��ޭ