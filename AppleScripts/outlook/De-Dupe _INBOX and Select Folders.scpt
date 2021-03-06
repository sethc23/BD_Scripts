FasdUAS 1.101.10   ��   ��    k             l     ��  ��    $  Remove Duplicate Message v2.1     � 	 	 <   R e m o v e   D u p l i c a t e   M e s s a g e   v 2 . 1   
  
 l     ��  ��    < 6 An Applescript by Barry Wainwright, 15th October 2010     �   l   A n   A p p l e s c r i p t   b y   B a r r y   W a i n w r i g h t ,   1 5 t h   O c t o b e r   2 0 1 0      l     ��  ��    F @ Detects and deletes duplicate messages within a selected folder     �   �   D e t e c t s   a n d   d e l e t e s   d u p l i c a t e   m e s s a g e s   w i t h i n   a   s e l e c t e d   f o l d e r      l     ��  ��    C = works on Message-ID header - uniquely identifying duplicates     �   z   w o r k s   o n   M e s s a g e - I D   h e a d e r   -   u n i q u e l y   i d e n t i f y i n g   d u p l i c a t e s      l     ��������  ��  ��        l     ��  ��      Version History     �       V e r s i o n   H i s t o r y     !   l     �� " #��   " A ; v1.0 - 2002-03-18: First Release (For Microsoft Entourage)    # � $ $ v   v 1 . 0   -   2 0 0 2 - 0 3 - 1 8 :   F i r s t   R e l e a s e   ( F o r   M i c r o s o f t   E n t o u r a g e ) !  % & % l     �� ' (��   ' I C v2.0 - 2010-10-07: modified to work with Microsoft Outlook for Mac    ( � ) ) �   v 2 . 0   -   2 0 1 0 - 1 0 - 0 7 :   m o d i f i e d   t o   w o r k   w i t h   M i c r o s o f t   O u t l o o k   f o r   M a c &  * + * l     �� , -��   , J D v2.1 - 2010-10-15: added final dialog to summarise messages removed    - � . . �   v 2 . 1   -   2 0 1 0 - 1 0 - 1 5 :   a d d e d   f i n a l   d i a l o g   t o   s u m m a r i s e   m e s s a g e s   r e m o v e d +  / 0 / l     ��������  ��  ��   0  1 2 1 l   o 3���� 3 O    o 4 5 4 k   n 6 6  7 8 7 r    	 9 : 9 1    ��
�� 
CMgs : o      ���� 0 themessages theMessages 8  ; < ; Z   
 F = >�� ? = =   
  @ A @ o   
 ���� 0 themessages theMessages A J    ����   > Q    7 B C D B k     E E  F G F r     H I H 1    ��
�� 
SeFo I o      ���� 0 	thefolder 	theFolder G  J�� J r     K L K o    ���� 0 	thefolder 	theFolder L o      ���� 0 mb  ��   C R      ������
�� .ascrerr ****      � ****��  ��   D k   % 7 M M  N O N I  % 2�� P Q
�� .sysodlogaskr        TEXT P m   % & R R � S S � I n   t h e   f o l d e r   l i s t i n g ,   p l e a s e   s e l e c t   t h e   f o l d e r   y o u   w a n t   t o   b e   s c a n n e d   f o r   d u p l i c a t e s Q �� T U
�� 
disp T m   ' (��
�� stic     U �� V W
�� 
btns V J   ) , X X  Y�� Y m   ) * Z Z � [ [  Q u i t��   W �� \��
�� 
dflt \ m   - .���� ��   O  ]�� ] L   3 7 ^ ^ m   3 6��������  ��   ? r   : F _ ` _ n   : D a b a m   @ D��
�� 
cFld b n   : @ c d c 4   ; @�� e
�� 
cobj e m   > ?����  d o   : ;���� 0 themessages theMessages ` o      ���� 0 mb   <  f g f r   G P h i h n   G L j k j 1   H L��
�� 
pnam k o   G H���� 0 mb   i o      ���� 0 thename theName g  l m l l  Q Q�� n o��   n < 6say "Removing duplicates from mail folder: " & theName    o � p p l s a y   " R e m o v i n g   d u p l i c a t e s   f r o m   m a i l   f o l d e r :   "   &   t h e N a m e m  q r q r   Q ^ s t s I  Q Z�� u��
�� .corecnte****       **** u n   Q V v w v 2  R V��
�� 
msg  w o   Q R���� 0 mb  ��   t o      ���� 0 y   r  x y x l  _ _�� z {��   z - 'say "Number of messages to check, " & y    { � | | N s a y   " N u m b e r   o f   m e s s a g e s   t o   c h e c k ,   "   &   y y  } ~ } r   _ e  �  J   _ a����   � o      ���� 0 idlist IDlist ~  � � � Y   f( ��� � � � � k   r# � �  � � � Q   r � � � � � k   u � � �  � � � r   u � � � � l  u � ����� � e   u � � � n   u � � � � 1   { ��
�� 
pMHd � n   u { � � � 4   v {�� �
�� 
msg  � o   y z���� 0 x   � o   u v���� 0 mb  ��  ��   � o      ���� 0 
theheaders 
theHeaders �  � � � r   � � � � � J   � � � �  ��� � b   � � � � � o   � ���
�� 
ret  � m   � � � � � � �  M e s s a g e -��   � n      � � � 1   � ���
�� 
txdl � 1   � ���
�� 
ascr �  � � � r   � � � � � n   � � � � � 4   � ��� �
�� 
citm � m   � �����  � o   � ����� 0 
theheaders 
theHeaders � o      ���� 0 temp   �  � � � r   � � � � � J   � � � �  ��� � o   � ���
�� 
ret ��   � n      � � � 1   � ���
�� 
txdl � 1   � ���
�� 
ascr �  ��� � r   � � � � � n   � � � � � 7 � ��� � �
�� 
ctxt � m   � �����  � m   � ������� � n   � � � � � 4   � ��� �
�� 
citm � m   � �����  � o   � ����� 0 temp   � o      ���� 0 theid theId��   � R      ������
�� .ascrerr ****      � ****��  ��   � r   � � � � � m   � � � � � � �   � o      ���� 0 theid theId �  � � � Z   � � � ��� � E  � � � � � n  � � � � � o   � ����� 0 idlist IDlist �  f   � � � o   � ����� 0 theid theId � I  � ��� ���
�� .coredelonull���     obj  � n   � � � � � 4   � ��� �
�� 
msg  � o   � ����� 0 x   � o   � ����� 0 mb  ��   �  � � � >   � � � � � o   � ����� 0 theid theId � m   � � � � � � �   �  ��� � s   � � � � o   ����� 0 theid theId � n       � � �  ;   � o  ���� 0 idlist IDlist��  ��   �  ��� � Z # � ����� � =   � � � `   � � � o  ���� 0 x   � m  ���� d � m  ����   � I �� ���
�� .sysottosnull���     TEXT � b   � � � m   � � � � �   � o  ���� 0 x  ��  ��  ��  ��  �� 0 x   � o   i l���� 0 y   � m   l m����  � m   m n������ �  � � � r  ): � � � \  )6 � � � o  ),���� 0 y   � l ,5 ����� � I ,5�� ���
�� .corecnte****       **** � n  ,1 � � � 2 -1��
�� 
msg  � o  ,-���� 0 mb  ��  ��  ��   � o      ���� 0 removedcount removedCount �  � � � l ;;�� � ���   �  if removedCount is 0 then    � � � � 2 i f   r e m o v e d C o u n t   i s   0   t h e n �  � � � l ;;�� � ���   � - '	say "Finished. No duplicates detected"    � � � � N 	 s a y   " F i n i s h e d .   N o   d u p l i c a t e s   d e t e c t e d " �  � � � l ;;�� � ���   � 
 else    � � � �  e l s e �  �  � l ;;����   > 8	say "Finished. " & removedCount & " duplicates removed"    � p 	 s a y   " F i n i s h e d .   "   &   r e m o v e d C o u n t   &   "   d u p l i c a t e s   r e m o v e d "   l ;;����    end if    �  e n d   i f 	
	 I ;`��
�� .sysodlogaskr        TEXT b  ;R b  ;N b  ;J b  ;F b  ;B m  ;> �   o  >A���� 0 y   m  BE � "   m e s s a g e s   c h e c k e d o  FI�
� 
ret  o  JM�~�~ 0 removedcount removedCount m  NQ � "   m e s s a g e s   r e m o v e d �}
�} 
btns J  SX  �|  m  SV!! �""  O K�|   �{#�z
�{ 
dflt# m  YZ�y�y �z  
 $�x$ r  an%&% J  af'' (�w( m  ad)) �**  �w  & n     +,+ 1  im�v
�v 
txdl, 1  fi�u
�u 
ascr�x   5 m     --�                                                                                  OPIM  alis    �  MacOSX                     ����H+   
hyMicrosoft Outlook.app                                           
��Ț�        ����  	                Microsoft Office 2011     ��      Ț�F     
hy  4  ?MacOSX:Applications:Microsoft Office 2011:Microsoft Outlook.app   ,  M i c r o s o f t   O u t l o o k . a p p    M a c O S X  8Applications/Microsoft Office 2011/Microsoft Outlook.app  / ��  ��  ��   2 .�t. l     �s�r�q�s  �r  �q  �t       �p/0�p  / �o
�o .aevtoappnull  �   � ****0 �n1�m�l23�k
�n .aevtoappnull  �   � ****1 k    o44  1�j�j  �m  �l  2 �i�i 0 x  3 1-�h�g�f�e�d�c�b R�a�`�_ Z�^�]�\�[�Z�Y�X�W�V�U�T�S�R�Q�P ��O�N�M�L�K�J�I ��H ��G ��F�E!�D)
�h 
CMgs�g 0 themessages theMessages
�f 
SeFo�e 0 	thefolder 	theFolder�d 0 mb  �c  �b  
�a 
disp
�` stic    
�_ 
btns
�^ 
dflt�] 
�\ .sysodlogaskr        TEXT�[��
�Z 
cobj
�Y 
cFld
�X 
pnam�W 0 thename theName
�V 
msg 
�U .corecnte****       ****�T 0 y  �S 0 idlist IDlist
�R 
pMHd�Q 0 
theheaders 
theHeaders
�P 
ret 
�O 
ascr
�N 
txdl
�M 
citm�L 0 temp  
�K 
ctxt�J �I 0 theid theId
�H .coredelonull���     obj �G d
�F .sysottosnull���     TEXT�E 0 removedcount removedCount�D �kp�l*�,E�O�jv  + *�,E�O�E�W X  �����kv�k� Oa Y �a k/a ,E�O�a ,E` O�a -j E` OjvE` O �_ kih   \�a �/a ,EE` O_ a %kv_ a ,FO_ a l/E`  O_ kv_ a ,FO_  a k/[a !\[Za "\Zi2E` #W X  a $E` #O)a ,_ # �a �/j %Y _ #a & _ #_ 6GY hO�a '#j  a (�%j )Y h[OY�IO_ �a -j E` *Oa +_ %a ,%_ %_ *%a -%�a .kv�ka / Oa 0kv_ a ,FUascr  ��ޭ