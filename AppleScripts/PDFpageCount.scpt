FasdUAS 1.101.10   ��   ��    k             l     ��������  ��  ��        l     	���� 	 r      
  
 m     ����   o      ���� 0 fcount fCount��  ��        l    ����  r        J    ����    o      ���� 0 
folderlist 
folderList��  ��        l  	  ����  r   	     J   	 ����    o      ���� 0 filelist fileList��  ��        l    ����  r        m    ����    o      ����  0 totalpagecount totalPageCount��  ��        l    ����  r        m    ����    o      ����  0 totalfilecount totalFileCount��  ��       !   l   � "���� " O    � # $ # k    � % %  & ' & I   ������
�� .miscactvnull��� ��� null��  ��   '  ( ) ( r     C * + * n     ? , - , 4   : ?�� .
�� 
cfol . m   ; > / / � 0 0  O C R s - n     : 1 2 1 4   5 :�� 3
�� 
cfol 3 m   6 9 4 4 � 5 5  s a n s p a p e r 2 n     5 6 7 6 4   2 5�� 8
�� 
cfol 8 m   3 4 9 9 � : :  S c r i p t s 7 n     2 ; < ; 4   / 2�� =
�� 
cfol = m   0 1 > > � ? ?  D r o p b o x < n     / @ A @ 4   , /�� B
�� 
cfol B m   - . C C � D D  S c a n B u s i n e s s A n     , E F E 4   ) ,�� G
�� 
cfol G m   * + H H � I I  W o r k F n     ) J K J 4   & )�� L
�� 
cfol L m   ' ( M M � N N  s e t h c h a s e K n     & O P O 4   # &�� Q
�� 
cfol Q m   $ % R R � S S 
 U s e r s P 1     #��
�� 
sdsk + o      ���� 0 topf topF )  T U T s   D P V W V n   D M X Y X 1   I M��
�� 
pnam Y l  D I Z���� Z n   D I [ \ [ 2   G I��
�� 
cfol \ o   D G���� 0 topf topF��  ��   W o      ���� 0 
folderlist 
folderList U  ] ^ ] l  Q Q�� _ `��   _ ' !display dialog folderList as text    ` � a a B d i s p l a y   d i a l o g   f o l d e r L i s t   a s   t e x t ^  b c b l   Q Q�� d e��   d1+
	repeat with x from 1 to fCount		set fName to folder (item x of folderList) of topF		set fileCount to count of files in fName		set totalFileCount to (totalFileCount + fileCount)		--(*		set fileList to name of every file in fName		repeat with y in fileList			--set y to item 2 of fileList
			    e � f fV 
 	 r e p e a t   w i t h   x   f r o m   1   t o   f C o u n t  	 	 s e t   f N a m e   t o   f o l d e r   ( i t e m   x   o f   f o l d e r L i s t )   o f   t o p F  	 	 s e t   f i l e C o u n t   t o   c o u n t   o f   f i l e s   i n   f N a m e  	 	 s e t   t o t a l F i l e C o u n t   t o   ( t o t a l F i l e C o u n t   +   f i l e C o u n t )  	 	 - - ( *  	 	 s e t   f i l e L i s t   t o   n a m e   o f   e v e r y   f i l e   i n   f N a m e  	 	 r e p e a t   w i t h   y   i n   f i l e L i s t  	 	 	 - - s e t   y   t o   i t e m   2   o f   f i l e L i s t 
 	 	 	 c  g h g O   Q � i j i k   W � k k  l m l I  W e�� n��
�� .aevtodocnull  �    alis n n  W a o p o 4   Z a�� q
�� 
file q o   ] `���� 0 y   p o   W Z���� 0 fname fName��   m  r s r r   f p t u t 4  f l�� v
�� 
cwin v m   j k����  u o      ���� 0 topw topW s  w x w r   q ~ y z y I  q z�� {��
�� .corecnte****       **** { 2  q v��
�� 
page��   z o      ���� 0 pcount pCount x  | } | I   �������
�� .CAROcldcnull��� ��� null��  ��   }  ~�� ~ r   � �  �  l  � � ����� � [   � � � � � o   � �����  0 totalpagecount totalPageCount � o   � ����� 0 pcount pCount��  ��   � o      ����  0 totalpagecount totalPageCount��   j m   Q T � �                                                                                  CARO   alis    �  MacOSX                     ȡhH+   �K�Adobe Acrobat Pro.app                                           �V��p        ����  	                Adobe Acrobat X Pro     ȡ�N      ��X     �K� ��   �  CMacOSX:Applications:Adobe:Adobe Acrobat X Pro:Adobe Acrobat Pro.app   ,  A d o b e   A c r o b a t   P r o . a p p    M a c O S X  <Applications/Adobe/Adobe Acrobat X Pro/Adobe Acrobat Pro.app  / ��   h  � � � l  � ��� � ���   �  
end repeat    � � � �  e n d   r e p e a t �  � � � l  � ��� � ���   �  *)    � � � �  * ) �  ��� � l  � ��� � ���   �  
end repeat    � � � �  e n d   r e p e a t��   $ m     � ��                                                                                  MACS   alis    `  MacOSX                     ȡhH+     �
Finder.app                                                       s��Z�$        ����  	                CoreServices    ȡ�N      �Z�t       �   Q   P  -MacOSX:System:Library:CoreServices:Finder.app    
 F i n d e r . a p p    M a c O S X  &System/Library/CoreServices/Finder.app  / ��  ��  ��   !  � � � l  � � ����� � I  � ��� ���
�� .sysodlogaskr        TEXT � o   � �����  0 totalpagecount totalPageCount��  ��  ��   �  ��� � l  � � ����� � I  � ��� ���
�� .sysodlogaskr        TEXT � o   � �����  0 totalfilecount totalFileCount��  ��  ��  ��       �� � ���   � ��
�� .aevtoappnull  �   � **** � �� ����� � ���
�� .aevtoappnull  �   � **** � k     � � �   � �   � �   � �   � �   � �    � �  � � �  �����  ��  ��   �   �  ������������ ������� R M H C > 9 4 /���� ������������������������� �� 0 fcount fCount�� 0 
folderlist 
folderList�� 0 filelist fileList��  0 totalpagecount totalPageCount��  0 totalfilecount totalFileCount
�� .miscactvnull��� ��� null
�� 
sdsk
�� 
cfol�� 0 topf topF
�� 
pnam�� 0 fname fName
�� 
file�� 0 y  
�� .aevtodocnull  �    alis
�� 
cwin�� 0 topw topW
�� 
page
�� .corecnte****       ****�� 0 pcount pCount
�� .CAROcldcnull��� ��� null
�� .sysodlogaskr        TEXT�� ��E�OjvE�OjvE�OjE�OjE�O� w*j O*�,��/��/��/��/��/��/�a /�a /E` O_ �-a ,EQ�Oa  7_ a _ /j O*a k/E` O*a -j E` O*j O�_ E�UOPUO�j O�j ascr  ��ޭ