FasdUAS 1.101.10   ��   ��    k             l     ��  ��     property countDone : 0     � 	 	 , p r o p e r t y   c o u n t D o n e   :   0   
  
 l     ��������  ��  ��        l     ��  ��     set countDone to 0     �   $ s e t   c o u n t D o n e   t o   0      l     ��  ��    W Qset {folderCount, folderList} to ProcessFolder(application "Microsoft Entourage")     �   � s e t   { f o l d e r C o u n t ,   f o l d e r L i s t }   t o   P r o c e s s F o l d e r ( a p p l i c a t i o n   " M i c r o s o f t   E n t o u r a g e " )      l     ��  ��    P Jdisplay dialog "Deleted " & delCount & " messages from " & folderCount & �     �   � d i s p l a y   d i a l o g   " D e l e t e d   "   &   d e l C o u n t   &   "   m e s s a g e s   f r o m   "   &   f o l d e r C o u n t   &   �      l     ��  ��      	" folders" buttons {"Ok"}     �   4 	 "   f o l d e r s "   b u t t o n s   { " O k " }     !   l     "���� " r      # $ # J     ����   $ o      ����  0 foldernamelist folderNameList��  ��   !  % & % l     ��������  ��  ��   &  ' ( ' l     �� ) *��   )  delegated account!    * � + + $ d e l e g a t e d   a c c o u n t ! (  , - , l     ��������  ��  ��   -  . / . l  � 0���� 0 O   � 1 2 1 k   	� 3 3  4 5 4 r   	  6 7 6 l  	  8���� 8 n   	  9 : 9 2   ��
�� 
cFld : 4   	 �� ;
�� 
cFld ; m     < < � = =  S a v e d   E m a i l��  ��   7 o      ���� 0 subfolderlist subFolderList 5  > ? > l   �� @ A��   @ $ FIRST ITERATION OF ALL FOLDERS    A � B B < F I R S T   I T E R A T I O N   O F   A L L   F O L D E R S ?  C D C Y    E�� F G�� E l  " H I J H k   " K K  L M L r   " . N O N l  " , P���� P n   " , Q R Q 4   & ,�� S
�� 
cFld S 1   ' +��
�� 
ID   R n  " & T U T 4   # &�� V
�� 
cobj V m   $ %����  U o   " #���� 0 subfolderlist subFolderList��  ��   O o      ���� 0 folderid folderID M  W X W l  / /�� Y Z��   Y - 'set folderID to item i of subFolderList    Z � [ [ N s e t   f o l d e r I D   t o   i t e m   i   o f   s u b F o l d e r L i s t X  \ ] \ l  / /�� ^ _��   ^ 5 /set MsgListA to subject of messages in folderID    _ � ` ` ^ s e t   M s g L i s t A   t o   s u b j e c t   o f   m e s s a g e s   i n   f o l d e r I D ]  a b a l  / /�� c d��   c  set DupeSubjectList to {}    d � e e 2 s e t   D u p e S u b j e c t L i s t   t o   { } b  f g f Y   / � h�� i j�� h k   ? � k k  l m l r   ? G n o n n   ? E p q p 1   C E��
�� 
subj q 4   ? C�� r
�� 
msg  r m   A B����>� o o      ���� 0 
msgsubject 
MsgSubject m  s t s r   H P u v u n   H N w x w 1   L N��
�� 
rTim x n  H L y z y 4   I L�� {
�� 
msg  { o   J K���� 0 j   z o   H I���� 0 folderid folderID v o      ���� 0 datereceived dateReceived t  | } | Z   Q o ~ ���� ~ E  Q T � � � o   Q R���� 0 msglista MsgListA � o   R S���� 0 
msgsubject 
MsgSubject  k   W k � �  � � � r   W c � � � n   W _ � � � 1   [ _��
�� 
pidx � n  W [ � � � 4   X [�� �
�� 
cobj � o   Y Z���� 0 
msgsubject 
MsgSubject � o   W X���� 0 msglista MsgListA � o      ���� 0 	listindex 	listIndex �  ��� � I  d k�� ���
�� .sysodlogaskr        TEXT � o   d g���� 0 	listindex 	listIndex��  ��  ��  ��   }  � � � l  p p�� � ���   � 3 -then set end of DupeSubjectList to MsgSubject    � � � � Z t h e n   s e t   e n d   o f   D u p e S u b j e c t L i s t   t o   M s g S u b j e c t �  � � � r   p } � � � I  p y�� � �
�� .corecnte****       **** � 2  p s��
�� 
msg  � �� ����� 0 
msgsubject 
MsgSubject � m   t u��
�� boovtrue��   � o      ���� 0 subjectcount SubjectCount �  � � � I  ~ ��� ���
�� .sysodlogaskr        TEXT � o   ~ ����� 0 subjectcount SubjectCount��   �  � � � Z  � � � ����� � H   � � � � E  � � � � � o   � ����� 0 msglista MsgListA � o   � ����� 0 
msgsubject 
MsgSubject � r   � � � � � o   � ����� 0 
msgsubject 
MsgSubject � n       � � �  ;   � � � o   � ����� 0 msglista MsgListA��  ��   �  ��� � l  � ���������  ��  ��  ��  �� 0 j   i m   2 3����  j I  3 :�� ���
�� .corecnte****       **** � n  3 6 � � � 2  4 6��
�� 
msg  � o   3 4���� 0 folderid folderID��  ��   g  � � � l  � ��� � ���   � , &display dialog DupeSubjectList as text    � � � � L d i s p l a y   d i a l o g   D u p e S u b j e c t L i s t   a s   t e x t �  � � � Y   � � ��� � ��� � k   � � � �  � � � l  � ��� � ���   � C =set DupeMsg to message of subject (item k in DupeSubjectList)    � � � � z s e t   D u p e M s g   t o   m e s s a g e   o f   s u b j e c t   ( i t e m   k   i n   D u p e S u b j e c t L i s t ) �  � � � r   � � � � � n   � � � � � 1   � ���
�� 
pMHd � o   � ����� 0 msgid MsgID � o      ���� 0 	msgheader 	MsgHeader �  � � � r   � � � � � m   � � � � � � �  M e s s a g e - � n      � � � 1   � ���
�� 
txdl � 1   � ���
�� 
ascr �  � � � r   � � � � � n   � � � � � 4   � ��� �
�� 
citm � m   � �����  � o   � ����� 0 	msgheader 	MsgHeader � o      ���� 0 temp   �  � � � r   � � � � � o   � ���
�� 
ret  � n      � � � 1   � ���
�� 
txdl � 1   � ���
�� 
ascr �  ��� � r   � � � � � n   � � � � � 7 � ��� � �
�� 
ctxt � m   � �����  � m   � ������� � n   � � � � � 4   � ��� �
�� 
citm � m   � �����  � o   � ����� 0 temp   � o      ���� 0 theid theID��  �� 0 k   � m   � �����  � I  � ��� ���
�� .corecnte****       **** � n  � � � � � 2  � ���
�� 
cobj � o   � ����� "0 dupesubjectlist DupeSubjectList��  ��   �  ��� � l   ��������  ��  ��  ��   I  count is 12    J � � �  c o u n t   i s   1 2�� 0 i   F m    ����  G I   �� ���
�� .corecnte****       **** � n    � � � 2   ��
�� 
cobj � o    ���� 0 subfolderlist subFolderList��  ��   D  � � � l ��~�}�  �~  �}   �  � � � l �|�{�z�|  �{  �z   �  � � � l �y � ��y   � &  SECOND ITERATION OF ALL MESSAGES    � � � � @ S E C O N D   I T E R A T I O N   O F   A L L   M E S S A G E S �  � � � l �x � ��x   � [ Uget titles for all messages, any messages with same title, add ID to investigate list    � � � � � g e t   t i t l e s   f o r   a l l   m e s s a g e s ,   a n y   m e s s a g e s   w i t h   s a m e   t i t l e ,   a d d   I D   t o   i n v e s t i g a t e   l i s t �  � � � l �w � ��w   � / )set MsgSubject to message 1 of item 1 in     � � � � R s e t   M s g S u b j e c t   t o   m e s s a g e   1   o f   i t e m   1   i n   �  � � � l �v�u�t�v  �u  �t   �  � � � r     n   4  �s
�s 
msg  m  �r�r Q n  4  �q
�q 
cobj m  	
�p�p  o  �o�o 0 subfolderlist subFolderList o      �n�n 0 msgid MsgID � 	 r   

 n   1  �m
�m 
pMHd o  �l�l 0 msgid MsgID o      �k�k 0 	msgheader 	MsgHeader	  r  !, m  !$ �  M e s s a g e - n      1  '+�j
�j 
txdl 1  $'�i
�i 
ascr  r  -9 n  -5 4  05�h
�h 
citm m  34�g�g  o  -0�f�f 0 	msgheader 	MsgHeader o      �e�e 0 temp    r  :E  o  :=�d
�d 
ret   n     !"! 1  @D�c
�c 
txdl" 1  =@�b
�b 
ascr #$# r  F`%&% n  F\'(' 7N\�a)*
�a 
ctxt) m  TX�`�` * m  Y[�_�_��( n  FN+,+ 4  IN�^-
�^ 
citm- m  LM�]�] , o  FI�\�\ 0 temp  & o      �[�[ 0 theid theID$ ./. l aa�Z�Y�X�Z  �Y  �X  / 010 l aa�W�V�U�W  �V  �U  1 232 l aa�T�S�R�T  �S  �R  3 454 I ah�Q6�P
�Q .sysodlogaskr        TEXT6 o  ad�O�O 0 theid theID�P  5 787 l ii�N�M�L�N  �M  �L  8 9:9 r  iv;<; n  ir=>= 4  mr�K?
�K 
msg ? m  nq�J�J R> n im@A@ 4  jm�IB
�I 
cobjB m  kl�H�H A o  ij�G�G 0 subfolderlist subFolderList< o      �F�F 0 msgid2 MsgID2: CDC l ww�EEF�E  E $ set uniqueID2 to theID(MsgID2)   F �GG < s e t   u n i q u e I D 2   t o   t h e I D ( M s g I D 2 )D HIH l ww�DJK�D  J  display dialog uniqueID2   K �LL 0 d i s p l a y   d i a l o g   u n i q u e I D 2I MNM l ww�COP�C  O  set messageCount to 0   P �QQ * s e t   m e s s a g e C o u n t   t o   0N RSR l ww�BTU�B  T  set delCount to 0   U �VV " s e t   d e l C o u n t   t o   0S WXW l ww�AYZ�A  Y 2 ,	if (count of folders of theFolder) > 0 then   Z �[[ X 	 i f   ( c o u n t   o f   f o l d e r s   o f   t h e F o l d e r )   >   0   t h e nX \]\ l ww�@^_�@  ^ $ repeat with f in subFolderList   _ �`` < r e p e a t   w i t h   f   i n   s u b F o l d e r L i s t] aba l ww�?�>�=�?  �>  �=  b cdc l ww�<ef�<  e ! 			set dc to my delDupes(f)   f �gg 6 	 	 	 s e t   d c   t o   m y   d e l D u p e s ( f )d hih l ww�;jk�;  j &  			set delCount to delCount + dc   k �ll @ 	 	 	 s e t   d e l C o u n t   t o   d e l C o u n t   +   d ci mnm l ww�:op�:  o , &			set {mc, fc} to my ProcessFolder(f)   p �qq L 	 	 	 s e t   { m c ,   f c }   t o   m y   P r o c e s s F o l d e r ( f )n rsr l ww�9tu�9  t , &			set folderCount to folderCount + fc   u �vv L 	 	 	 s e t   f o l d e r C o u n t   t o   f o l d e r C o u n t   +   f cs wxw l ww�8yz�8  y F @			set messageCount to messageCount + (count messages of f) + mc   z �{{ � 	 	 	 s e t   m e s s a g e C o u n t   t o   m e s s a g e C o u n t   +   ( c o u n t   m e s s a g e s   o f   f )   +   m cx |}| l ww�7~�7  ~  
end repeat    ���  e n d   r e p e a t} ��� l ww�6���6  �  	end if   � ���  	 e n d   i f� ��� l ww�5�4�3�5  �4  �3  � ��2� L  w��� J  w�� ��� o  wz�1�1 0 foldercount folderCount� ��0� o  z}�/�/ 0 
folderlist 
folderList�0  �2   2 m    ��                                                                                  OPIM   alis    �  Macintosh HD               �a�%H+   ��Microsoft Entourage.app                                         �%�v�&        ����  	                Microsoft Office 2008     �bu      �v�v     ��     GMacintosh HD:Applications:Microsoft Office 2008:Microsoft Entourage.app   0  M i c r o s o f t   E n t o u r a g e . a p p    M a c i n t o s h   H D  :Applications/Microsoft Office 2008/Microsoft Entourage.app  / ��  ��  ��   / ��� l     �.�-�,�.  �-  �,  � ��� l     �+���+  � ! display dialog test as text   � ��� 6 d i s p l a y   d i a l o g   t e s t   a s   t e x t� ��� l     �*���*  �  display dialog folderList   � ��� 2 d i s p l a y   d i a l o g   f o l d e r L i s t� ��)� l     �(�'�&�(  �'  �&  �)       �%���%  � �$
�$ .aevtoappnull  �   � ****� �#��"�!��� 
�# .aevtoappnull  �   � ****� k    ���   ��  .��  �"  �!  � ���� 0 i  � 0 j  � 0 k  � '��� <����������������
�	��� ������� ���������������  0 foldernamelist folderNameList
� 
cFld� 0 subfolderlist subFolderList
� 
cobj
� .corecnte****       ****
� 
ID  � 0 folderid folderID
� 
msg �>�
� 
subj� 0 
msgsubject 
MsgSubject
� 
rTim� 0 datereceived dateReceived� 0 msglista MsgListA
� 
pidx� 0 	listindex 	listIndex
� .sysodlogaskr        TEXT�
 0 subjectcount SubjectCount�	 "0 dupesubjectlist DupeSubjectList� 0 msgid MsgID
� 
pMHd� 0 	msgheader 	MsgHeader
� 
ascr
� 
txdl
� 
citm� 0 temp  
� 
ret 
�  
ctxt�� �� 0 theid theID�� Q�� R�� 0 msgid2 MsgID2�� 0 foldercount folderCount�� 0 
folderlist 
folderList� �jvE�O�y*��/�-E�O �k��-j kh  ��k/�*�,E/E�O lk��-j kh *��/�,E�O��/�,E�O�� ���/a ,E` O_ j Y hO*�-�el E` O_ j O�� 	��6FY hOP[OY��O ak_ �-j kh _ a ,E` Oa _ a ,FO_ a l/E` O_ _ a ,FO_ a k/[a \[Za \Zi2E`  [OY��OP[OY�O��k/�a !/E` O_ a ,E` Oa "_ a ,FO_ a l/E` O_ _ a ,FO_ a k/[a \[Za \Zi2E`  O_  j O��k/�a #/E` $O_ %_ &lvUascr  ��ޭ