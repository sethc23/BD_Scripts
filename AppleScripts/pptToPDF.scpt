FasdUAS 1.101.10   ��   ��    k             l     ����  O       	  k     
 
     I   	������
�� .miscactvnull��� ��� null��  ��        l  
 
��  ��    � �set fName to folder "2" of folder "Copy" of folder "Pierce Library" of folder "Desktop" of folder "sethchase" of folder "Users" of startup disk     �   s e t   f N a m e   t o   f o l d e r   " 2 "   o f   f o l d e r   " C o p y "   o f   f o l d e r   " P i e r c e   L i b r a r y "   o f   f o l d e r   " D e s k t o p "   o f   f o l d e r   " s e t h c h a s e "   o f   f o l d e r   " U s e r s "   o f   s t a r t u p   d i s k      l  
 
��  ��    � zset fName to folder "MacOSX:Users:sethchase:School:Franklin Pierce:2010 - Fall:ToDo:Tech Licensing:Brunsvold_CD:Contents:"     �   � s e t   f N a m e   t o   f o l d e r   " M a c O S X : U s e r s : s e t h c h a s e : S c h o o l : F r a n k l i n   P i e r c e : 2 0 1 0   -   F a l l : T o D o : T e c h   L i c e n s i n g : B r u n s v o l d _ C D : C o n t e n t s : "      l  
 
��  ��    ) #set fileList to every file in fName     �   F s e t   f i l e L i s t   t o   e v e r y   f i l e   i n   f N a m e   ��  r   
     1   
 ��
�� 
sele  o      ���� 0 filelist fileList��   	 m       �                                                                                  MACS   alis    `  MacOSX                     ȡhH+     �
Finder.app                                                       s��Z�$        ����  	                CoreServices    ȡ�N      �Z�t       �   Q   P  -MacOSX:System:Library:CoreServices:Finder.app    
 F i n d e r . a p p    M a c O S X  &System/Library/CoreServices/Finder.app  / ��  ��  ��       !   l     ��������  ��  ��   !  " # " l     �� $ %��   $ # set test to count of fileList    % � & & : s e t   t e s t   t o   c o u n t   o f   f i l e L i s t #  ' ( ' l     ��������  ��  ��   (  ) * ) l    +���� + I    �� ,���� 0 ppttopdf pptToPDF ,  -�� - o    ���� 0 filelist fileList��  ��  ��  ��   *  . / . l     �� 0 1��   0  wordToPDF(fileList)    1 � 2 2 & w o r d T o P D F ( f i l e L i s t ) /  3 4 3 l     ��������  ��  ��   4  5 6 5 i      7 8 7 I      �� 9���� 0 ppttopdf pptToPDF 9  :�� : o      ���� 0 filelist fileList��  ��   8 X    Q ;�� < ; k   L = =  > ? > r     @ A @ c     B C B n     D E D 1    ��
�� 
pnam E o    ���� 0 xs   C m    ��
�� 
ctxt A o      ���� 0 filename fileName ?  F G F r    / H I H c    - J K J l   + L���� L n    + M N M 7   +�� O P
�� 
cha  O m    ����  P l    * Q���� Q \     * R S R l  ! ( T���� T I  ! (�� U��
�� .corecnte****       **** U n  ! $ V W V 2  " $��
�� 
cha  W o   ! "���� 0 filename fileName��  ��  ��   S m   ( )���� ��  ��   N o    ���� 0 filename fileName��  ��   K m   + ,��
�� 
TEXT I o      ���� 0 filename fileName G  X Y X O   0 O Z [ Z k   4 N \ \  ] ^ ] I  4 9������
�� .miscactvnull��� ��� null��  ��   ^  _ ` _ I  : ?�� a��
�� .aevtodocnull  �    alis a o   : ;���� 0 xs  ��   `  b c b t   @ H d e d I  B G������
�� .miscactvnull��� ��� null��  ��   e m   @ A����   �� c  f�� f I  I N������
�� .miscactvnull��� ��� null��  ��  ��   [ m   0 1 g g
                                                                                  PPT3   alis    �  MacOSX                     ȡhH+    /Microsoft PowerPoint.app                                        -���ؗ        ����  	                Microsoft Office 2008     ȡ�N      ���      /   �  BMacOSX:Applications:Microsoft Office 2008:Microsoft PowerPoint.app  2  M i c r o s o f t   P o w e r P o i n t . a p p    M a c O S X  ;Applications/Microsoft Office 2008/Microsoft PowerPoint.app   / ��   Y  h i h O   P$ j k j O   T# l m l k   [" n n  o p o I  [ h�� q r
�� .prcskcodnull���    long q m   [ \���� # r �� s��
�� 
faal s J   _ d t t  u�� u m   _ b��
�� eMdsKcmd��  ��   p  v w v I  i p�� x��
�� .sysodelanull��� ��� nmbr x m   i l y y ?�      ��   w  z { z I  q ��� |��
�� .prcsclicuiel    ��� uiel | n   q ~ } ~ } 4   y ~�� 
�� 
popB  m   | }����  ~ 4   q y�� �
�� 
cwin � m   u x � � � � � 
 P r i n t��   {  � � � I  � ��� ���
�� .sysodelanull��� ��� nmbr � m   � � � � ?�      ��   �  � � � I  � ��� ���
�� .prcsclicuiel    ��� uiel � n   � � � � � 4   � ��� �
�� 
menI � m   � � � � � � � 8 H a n d o u t s   ( 2   s l i d e s   p e r   p a g e ) � n   � � � � � 4   � ��� �
�� 
menE � m   � �����  � n   � � � � � 4   � ��� �
�� 
popB � m   � �����  � 4   � ��� �
�� 
cwin � m   � � � � � � � 
 P r i n t��   �  � � � I  � ��� ���
�� .sysodelanull��� ��� nmbr � m   � � � � ?�      ��   �  � � � I  � ��� ���
�� .prcsclicuiel    ��� uiel � n   � � � � � 4   � ��� �
�� 
menB � m   � � � � � � �  P D F � 4   � ��� �
�� 
cwin � m   � � � � � � � 
 P r i n t��   �  � � � I  � ��� ���
�� .sysodelanull��� ��� nmbr � m   � � � � ?�      ��   �  � � � I  � ��� ���
�� .prcsclicuiel    ��� uiel � n   � � � � � 4   � ��� �
�� 
menI � m   � � � � � � �  S a v e   a s   P D F & � n   � � � � � 4   � ��� �
�� 
menE � m   � �����  � n   � � � � � 4   � ��� �
�� 
menB � m   � � � � � � �  P D F � 4   � ��� �
�� 
cwin � m   � � � � � � � 
 P r i n t��   �  � � � I  � ��� ���
�� .sysodelanull��� ��� nmbr � m   � ����� ��   �  � � � r   � � � � o   � ����� 0 filename fileName � n       � � � 1  ��
�� 
valL � n   � � � � 4   ��� �
�� 
txtf � m   � ����  � 4   � ��� �
�� 
cwin � m   � � � � � � �  S a v e �  � � � I �� ���
�� .prcsclicuiel    ��� uiel � n   � � � 4  �� �
�� 
butT � m   � � � � �  S a v e � 4  �� �
�� 
cwin � m   � � � � �  S a v e��   �  ��� � I "�� ���
�� .sysodelanull��� ��� nmbr � m   � � ?�      ��  ��   m 4   T X�� �
�� 
prcs � m   V W � � � � � ( M i c r o s o f t   P o w e r P o i n t k m   P Q � ��                                                                                  sevs   alis    |  MacOSX                     ȡhH+     �System Events.app                                                ���        ����  	                CoreServices    ȡ�N      ��C       �   Q   P  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��   i  ��� � O  %L � � � k  )K � �  � � � t  )1 � � � I +0������
�� .miscactvnull��� ��� null��  ��   � m  )*����   �� �  � � � I 27����~
�� .miscactvnull��� ��� null�  �~   �  ��} � I 8K�| � �
�| .coreclosnull���    obj  � 4  8A�{ �
�{ 
pptP � l <@ ��z�y � n  <@ � � � 1  =?�x
�x 
pnam � o  <=�w�w 0 xs  �z  �y   � �v ��u
�v 
savo � m  DG�t
�t savono  �u  �}   � m  %& � �
                                                                                  PPT3   alis    �  MacOSX                     ȡhH+    /Microsoft PowerPoint.app                                        -���ؗ        ����  	                Microsoft Office 2008     ȡ�N      ���      /   �  BMacOSX:Applications:Microsoft Office 2008:Microsoft PowerPoint.app  2  M i c r o s o f t   P o w e r P o i n t . a p p    M a c O S X  ;Applications/Microsoft Office 2008/Microsoft PowerPoint.app   / ��  ��  �� 0 xs   < o    �s�s 0 filelist fileList 6  � � � l     �r�q�p�r  �q  �p   �  � � � i     � � � I      �o ��n�o 0 	wordtopdf 	wordToPDF �  ��m � o      �l�l 0 filelist fileList�m  �n   � X     � ��k � � k    � � �  � � � O    " �  � k    !  I   �j�i�h
�j .miscactvnull��� ��� null�i  �h   �g I   !�f�e
�f .aevtodocnull  �    alis c     o    �d�d 0 x   m    �c
�c 
TEXT�e  �g    m    �                                                                                  MSWD   alis    �  MacOSX                     ȡhH+    /Microsoft Word.app                                              0=��ؗ        ����  	                Microsoft Office 2008     ȡ�N      ���      /   �  <MacOSX:Applications:Microsoft Office 2008:Microsoft Word.app  &  M i c r o s o f t   W o r d . a p p    M a c O S X  5Applications/Microsoft Office 2008/Microsoft Word.app   / ��   � 	
	 O   # � O   ' � k   . �  I  . 7�b
�b .prcskcodnull���    long m   . /�a�a # �`�_
�` 
faal J   0 3 �^ m   0 1�]
�] eMdsKcmd�^  �_    I  8 =�\�[
�\ .sysodelanull��� ��� nmbr m   8 9 ?�      �[    I  > Q�Z�Y
�Z .prcsclicuiel    ��� uiel n   > M 4   F M�X 
�X 
menB  m   I L!! �""  P D F 4   > F�W#
�W 
cwin# m   B E$$ �%% 
 P r i n t�Y   &'& I  R Y�V(�U
�V .sysodelanull��� ��� nmbr( m   R U)) ?�      �U  ' *+* I  Z y�T,�S
�T .prcsclicuiel    ��� uiel, n   Z u-.- 4   n u�R/
�R 
menI/ m   q t00 �11  S a v e   a s   P D F &. n   Z n232 4   i n�Q4
�Q 
menE4 m   l m�P�P 3 n   Z i565 4   b i�O7
�O 
menB7 m   e h88 �99  P D F6 4   Z b�N:
�N 
cwin: m   ^ a;; �<< 
 P r i n t�S  + =>= I  z �M?�L
�M .sysodelanull��� ��� nmbr? m   z {�K�K �L  > @A@ I  � ��JB�I
�J .miscslctuiel       uielB n   � �CDC 4   � ��HE
�H 
txtfE m   � ��G�G D 4   � ��FF
�F 
cwinF m   � �GG �HH  S a v e�I  A IJI I  � ��EK�D
�E .sysodelanull��� ��� nmbrK m   � �LL ?�      �D  J MNM I  � ��CO�B
�C .prcsclicuiel    ��� uielO n   � �PQP 4   � ��AR
�A 
butTR m   � �SS �TT  S a v eQ 4   � ��@U
�@ 
cwinU m   � �VV �WW  S a v e�B  N X�?X I  � ��>Y�=
�> .sysodelanull��� ��� nmbrY m   � �ZZ ?�      �=  �?   4   ' +�<[
�< 
prcs[ m   ) *\\ �]]  W o r d m   # $^^�                                                                                  sevs   alis    |  MacOSX                     ȡhH+     �System Events.app                                                ���        ����  	                CoreServices    ȡ�N      ��C       �   Q   P  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��  
 _�;_ O   � �`a` k   � �bb cdc t   � �efe I  � ��:�9�8
�: .miscactvnull��� ��� null�9  �8  f m   � ��7�7   ��d g�6g I  � ��5h�4
�5 .coreclosnull���    obj h l  � �i�3�2i 4  � ��1j
�1 
docuj m   � ��0�0 �3  �2  �4  �6  a m   � �kk�                                                                                  MSWD   alis    �  MacOSX                     ȡhH+    /Microsoft Word.app                                              0=��ؗ        ����  	                Microsoft Office 2008     ȡ�N      ���      /   �  <MacOSX:Applications:Microsoft Office 2008:Microsoft Word.app  &  M i c r o s o f t   W o r d . a p p    M a c O S X  5Applications/Microsoft Office 2008/Microsoft Word.app   / ��  �;  �k 0 x   � o    �/�/ 0 filelist fileList � lml l     �.�-�,�.  �-  �,  m non l     �+�*�)�+  �*  �)  o pqp l     �(�'�&�(  �'  �&  q r�%r l     �$�#�"�$  �#  �"  �%       �!stuv�!  s � ���  0 ppttopdf pptToPDF� 0 	wordtopdf 	wordToPDF
� .aevtoappnull  �   � ****t � 8��wx�� 0 ppttopdf pptToPDF� �y� y  �� 0 filelist fileList�  w ���� 0 filelist fileList� 0 xs  � 0 filename fileNamex .�������� g���
 ��	 ����� y�� ��� � �� �� � ��� � � � � ����� ��� ���������
� 
kocl
� 
cobj
� .corecnte****       ****
� 
pnam
� 
ctxt
� 
cha � 
� 
TEXT
� .miscactvnull��� ��� null
� .aevtodocnull  �    alis�
   ��
�	 
prcs� #
� 
faal
� eMdsKcmd
� .prcskcodnull���    long
� .sysodelanull��� ��� nmbr
� 
cwin
� 
popB
� .prcsclicuiel    ��� uiel
�  
menE
�� 
menI
�� 
menB
�� 
txtf
�� 
valL
�� 
butT
�� 
pptP
�� 
savo
�� savono  
�� .coreclosnull���    obj �RP�[��l kh ��,�&E�O�[�\[Zk\Z��-j �2�&E�O� *j 	O�j 
O�n*j 	oO*j 	UO� �*��/ ��a a kvl Oa j O*a a /a m/j Oa j O*a a /a m/a k/a a /j Oa j O*a a /a a  /j Oa j O*a a !/a a "/a k/a a #/j Okj O�*a a $/a %k/a &,FO*a a '/a (a )/j Oa j UUO� $�n*j 	oO*j 	O*a *��,E/a +a ,l -U[OY��u �� �����z{���� 0 	wordtopdf 	wordToPDF�� ��|�� |  ���� 0 filelist fileList��  z ������ 0 filelist fileList�� 0 x  { $������������^��\������������$��!��);8����0G����V��S������
�� 
kocl
�� 
cobj
�� .corecnte****       ****
�� .miscactvnull��� ��� null
�� 
TEXT
�� .aevtodocnull  �    alis
�� 
prcs�� #
�� 
faal
�� eMdsKcmd
�� .prcskcodnull���    long
�� .sysodelanull��� ��� nmbr
�� 
cwin
�� 
menB
�� .prcsclicuiel    ��� uiel
�� 
menE
�� 
menI
�� 
txtf
�� .miscslctuiel       uiel
�� 
butT��   ��
�� 
docu
�� .coreclosnull���    obj �� � Ԡ[��l kh � *j O��&j UO� �*��/ ����kvl O�j O*a a /a a /j Oa j O*a a /a a /a k/a a /j Okj O*a a /a k/j Oa j O*a a /a a  /j O�j UUO� a !n*j oO*a "k/j #U[OY�:v ��}����~��
�� .aevtoappnull  �   � ****} k     ��  ��  )����  ��  ��  ~    ��������
�� .miscactvnull��� ��� null
�� 
sele�� 0 filelist fileList�� 0 ppttopdf pptToPDF�� � *j O*�,E�UO*�k+ ascr  ��ޭ