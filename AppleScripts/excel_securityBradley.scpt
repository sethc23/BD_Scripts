FasdUAS 1.101.10   ��   ��    k             l     ��  ��    O ISTART ON "Goto Sheet", next sheet is sheet with conditional starting A13      � 	 	 � S T A R T   O N   " G o t o   S h e e t " ,   n e x t   s h e e t   i s   s h e e t   w i t h   c o n d i t i o n a l   s t a r t i n g   A 1 3     
  
 l     ��  ��    B <(=IF((AND(B13>1,SUM(A3:A12)=0,B13<>"")),1,(IF(B13="",2,"")))     �   x ( = I F ( ( A N D ( B 1 3 > 1 , S U M ( A 3 : A 1 2 ) = 0 , B 1 3 < > " " ) ) , 1 , ( I F ( B 1 3 = " " , 2 , " " ) ) )      l     ��  ��    $ cursor starts at B2 on sheet 1     �   < c u r s o r   s t a r t s   a t   B 2   o n   s h e e t   1      l     ��  ��     116 page up     �    1 1 6   p a g e   u p      l     ��  ��     121 page down     �    1 2 1   p a g e   d o w n      l     ��   !��      115 home    ! � " "  1 1 5   h o m e   # $ # l     �� % &��   %   117 delete (not backspace)    & � ' ' 4 1 1 7   d e l e t e   ( n o t   b a c k s p a c e ) $  ( ) ( l     ��������  ��  ��   )  * + * l      �� , -��   ,display dialog "How many months to generate?" default answer " "set repeat_num to text returned of resultset char_num to count of characters of repeat_numset repeat_clean to text 1 thru char_num of repeat_numset month_count to text of repeat_cleanset day_count to 182
    - � . .$  d i s p l a y   d i a l o g   " H o w   m a n y   m o n t h s   t o   g e n e r a t e ? "   d e f a u l t   a n s w e r   "   "  s e t   r e p e a t _ n u m   t o   t e x t   r e t u r n e d   o f   r e s u l t  s e t   c h a r _ n u m   t o   c o u n t   o f   c h a r a c t e r s   o f   r e p e a t _ n u m  s e t   r e p e a t _ c l e a n   t o   t e x t   1   t h r u   c h a r _ n u m   o f   r e p e a t _ n u m  s e t   m o n t h _ c o u n t   t o   t e x t   o f   r e p e a t _ c l e a n  s e t   d a y _ c o u n t   t o   1 8 2 
 +  / 0 / l     1���� 1 r      2 3 2 m     ����  3 o      ���� 0 month_count  ��  ��   0  4 5 4 l    6���� 6 r     7 8 7 m    ����  8 o      ���� 0 	month_num  ��  ��   5  9 : 9 l    ;���� ; r     < = < m    	����  = o      ���� 0 repeat_count  ��  ��   :  > ? > l    @���� @ r     A B A m    ����O B o      ���� 0 	day_count  ��  ��   ?  C D C l     �� E F��   E  (*    F � G G  ( * D  H I H l   ( J���� J Y    ( K�� L M�� K k    # N N  O P O l   �� Q R��   Q I Cset {repeat_count, day_count} to makeNewMonth(month_num, day_count)    R � S S � s e t   { r e p e a t _ c o u n t ,   d a y _ c o u n t }   t o   m a k e N e w M o n t h ( m o n t h _ n u m ,   d a y _ c o u n t ) P  T U T l   �� V W��   V  
prepare1()    W � X X  p r e p a r e 1 ( ) U  Y Z Y l   �� [ \��   [ # display dialog "transition 1"    \ � ] ] : d i s p l a y   d i a l o g   " t r a n s i t i o n   1 " Z  ^ _ ^ l   �� ` a��   `  transition1()    a � b b  t r a n s i t i o n 1 ( ) _  c d c l   �� e f��   e  display dialog "prepare2"    f � g g 2 d i s p l a y   d i a l o g   " p r e p a r e 2 " d  h i h l   �� j k��   j  
prepare2()    k � l l  p r e p a r e 2 ( ) i  m n m l   �� o p��   o   display dialog "makeTimes"    p � q q 4 d i s p l a y   d i a l o g   " m a k e T i m e s " n  r s r l   �� t u��   t ( "makeTimes(repeat_count, day_count)    u � v v D m a k e T i m e s ( r e p e a t _ c o u n t ,   d a y _ c o u n t ) s  w x w l   �� y z��   y ' !display dialog "rearrangeTimes 1"    z � { { B d i s p l a y   d i a l o g   " r e a r r a n g e T i m e s   1 " x  | } | l   ��������  ��  ��   }  ~  ~ l   ��������  ��  ��     � � � l   ! � � � � I    !�� �����  0 rearrangetimes rearrangeTimes �  � � � o    ���� 0 repeat_count   �  ��� � o    ���� 0 	day_count  ��  ��   � ; 5start on goto page, Copyedit col B, 3 line seperation    � � � � j s t a r t   o n   g o t o   p a g e ,   C o p y e d i t   c o l   B ,   3   l i n e   s e p e r a t i o n �  � � � l  " "��������  ��  ��   �  � � � l  " "�� � ���   � ( "display dialog "transfer_clean1 1"    � � � � D d i s p l a y   d i a l o g   " t r a n s f e r _ c l e a n 1   1 " �  � � � l  " "�� � ���   �  transfer_clean1()    � � � � " t r a n s f e r _ c l e a n 1 ( ) �  � � � l  " "�� � ���   � # display dialog "transition 1"    � � � � : d i s p l a y   d i a l o g   " t r a n s i t i o n   1 " �  � � � l  " "�� � ���   � ? 9transition1() --makes format of times from copyedit in A1    � � � � r t r a n s i t i o n 1 ( )   - - m a k e s   f o r m a t   o f   t i m e s   f r o m   c o p y e d i t   i n   A 1 �  � � � l  " "�� � ���   � &  display dialog "transfer_clean2"    � � � � @ d i s p l a y   d i a l o g   " t r a n s f e r _ c l e a n 2 " �  ��� � l  " "�� � ���   �  transfer_clean2()    � � � � " t r a n s f e r _ c l e a n 2 ( )��  �� 0 	month_num   L m    ����  M o    ���� 0 month_count  ��  ��  ��   I  � � � l     �� � ���   �  *)    � � � �  * ) �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   �  test()    � � � �  t e s t ( ) �  � � � i      � � � I      �������� 0 test  ��  ��   � k      � �  � � � I    �� ���
�� .miscactvnull��� ��� null � m      � �                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��   �  ��� � O     � � � O   
  � � � l   ��������  ��  ��   � 4   
 �� �
�� 
pcap � m     � � � � �  M i c r o s o f t   E x c e l � m     � ��                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��   �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   �  set row_count to 112    � � � � ( s e t   r o w _ c o u n t   t o   1 1 2 �  � � � l     �� � ���   � : 4add rows to word document, put cursor outside of row    � � � � h a d d   r o w s   t o   w o r d   d o c u m e n t ,   p u t   c u r s o r   o u t s i d e   o f   r o w �  � � � l     �� � ���   �  makeWordTable(row_count)    � � � � 0 m a k e W o r d T a b l e ( r o w _ c o u n t ) �  � � � l     ��������  ��  ��   �  � � � l     �� � ���   �  --    � � � �  - - �  � � � l     �� � ���   �  --    � � � �  - - �  � � � l     �� � ���   � 2 ,addDayNum_rearrange(repeat_count, day_count)    � � � � X a d d D a y N u m _ r e a r r a n g e ( r e p e a t _ c o u n t ,   d a y _ c o u n t ) �  � � � l     ��������  ��  ��   �  � � � l     ��������  ��  ��   �  � � � l     ��������  ��  ��   �  � � � l     ��������  ��  ��   �  � � � i     � � � I      �� �����  0 rearrangetimes rearrangeTimes �  � � � o      ���� 0 repeat_count   �  ��� � o      ���� 0 	day_count  ��  ��   � k     � �  � � � r      � � � [      � � � o     ���� 0 repeat_count   � o    ���� 0 	day_count   � o      ���� 0 	end_count   �    l    ����  ��	activate application "Microsoft Excel"	tell application "System Events"		tell application process "Microsoft Excel"			delay 0.25			key code 115 using control down			delay 0.25			key code 53			delay 0.25			key code 121 using control down			delay 0.25			key code 126			delay 0.25			key code 126			delay 0.25			key code 49 using control down			delay 0.25			key code 34 using control down			delay 0.25			key code 123			delay 0.25			key code 125		end tell	end tell
	    ��  	 a c t i v a t e   a p p l i c a t i o n   " M i c r o s o f t   E x c e l "  	 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 	 t e l l   a p p l i c a t i o n   p r o c e s s   " M i c r o s o f t   E x c e l "  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 1 5   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   5 3  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 1   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 6  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 6  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   4 9   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   3 4   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 3  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 5  	 	 e n d   t e l l  	 e n d   t e l l 
 	  l   ����   ' !setup for transition to next step    �		 B s e t u p   f o r   t r a n s i t i o n   t o   n e x t   s t e p 

 I   ����
�� .miscactvnull��� ��� null m                                                                                      XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��    O    O    k     r     m    ����   o      ���� 0 complete    l   ����   * $repeat with x from 1 to repeat_count    � H r e p e a t   w i t h   x   f r o m   1   t o   r e p e a t _ c o u n t  l    �� !��   
				move up until #1 is found
				r,r,d - copy - u,l,l
				if that copy square != tremont, then move()
				move( go up 16, or go up 
				keep moving up until 2, once 2, go down 1, count up since move start-1 (down)
				)
				otherwise, keep going 
				
				
					
				end
				   ! �""* 
 	 	 	 	 m o v e   u p   u n t i l   # 1   i s   f o u n d 
 	 	 	 	 r , r , d   -   c o p y   -   u , l , l 
 	 	 	 	 i f   t h a t   c o p y   s q u a r e   ! =   t r e m o n t ,   t h e n   m o v e ( ) 
 	 	 	 	 m o v e (   g o   u p   1 6 ,   o r   g o   u p   
 	 	 	 	 k e e p   m o v i n g   u p   u n t i l   2 ,   o n c e   2 ,   g o   d o w n   1 ,   c o u n t   u p   s i n c e   m o v e   s t a r t - 1   ( d o w n ) 
 	 	 	 	 ) 
 	 	 	 	 o t h e r w i s e ,   k e e p   g o i n g   
 	 	 	 	 
 	 	 	 	 
 	 	 	 	 	 
 	 	 	 	 e n d 
 	 	 	 	 #$# l   ��������  ��  ��  $ %&% l   ��������  ��  ��  & '(' l    ��)*��  ) � �			delay 0.15			key code 123 using control down			delay 0.15			key code 126 using control down			delay 0.15			key code 126 using control down			delay 0.15			key code 125			   * �++j  	 	 	 d e l a y   0 . 1 5  	 	 	 k e y   c o d e   1 2 3   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 1 5  	 	 	 k e y   c o d e   1 2 6   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 1 5  	 	 	 k e y   c o d e   1 2 6   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 1 5  	 	 	 k e y   c o d e   1 2 5  	 	 	( ,-, l   ����~��  �  �~  - ./. I   "�}01
�} .prcskprsnull���    utxt0 m    22 �33  c1 �|4�{
�| 
faal4 m    �z
�z eMdsKcmd�{  / 565 I  # (�y7�x
�y .sysodelanull��� ��� nmbr7 m   # $88 ?�      �x  6 9:9 r   ) 0;<; l  ) .=�w�v= I  ) .�u�t�s
�u .JonsgClp****    ��� null�t  �s  �w  �v  < o      �r�r 0 act_num  : >?> Z   1�@A�q�p@ >  1 4BCB o   1 2�o�o 0 act_num  C m   2 3DD �EE  1A k   7�FF GHG r   7 :IJI m   7 8�n�n  J o      �m�m 
0 found1  H KLK r   ; >MNM m   ; <�l�l  N o      �k�k 0 sqmoved  L OPO W   ? �QRQ k   G �SS TUT I  G L�jV�i
�j .prcskcodnull���    longV m   G H�h�h }�i  U WXW I  M R�gY�f
�g .sysodelanull��� ��� nmbrY m   M NZZ ?�      �f  X [\[ I  S Z�e]^
�e .prcskprsnull���    utxt] m   S T__ �``  c^ �da�c
�d 
faala m   U V�b
�b eMdsKcmd�c  \ bcb I  [ `�ad�`
�a .sysodelanull��� ��� nmbrd m   [ \ee ?�      �`  c fgf r   a hhih l  a fj�_�^j I  a f�]�\�[
�] .JonsgClp****    ��� null�\  �[  �_  �^  i o      �Z�Z 0 act_num  g klk I  i n�Ym�X
�Y .sysodelanull��� ��� nmbrm m   i jnn ?�      �X  l opo I  o v�Wq�V
�W .prcskcodnull���    longq m   o r�U�U 5�V  p rsr I  w |�Tt�S
�T .sysodelanull��� ��� nmbrt m   w xuu ?�      �S  s vwv r   } �xyx c   } �z{z l  } �|�R�Q| [   } �}~} o   } ~�P�P 0 sqmoved  ~ m   ~ �O�O �R  �Q  { m   � ��N
�N 
longy o      �M�M 0 sqmoved  w � Z  � ����L�K� =  � ���� o   � ��J�J 0 act_num  � m   � ��� ���  1� r   � ���� m   � ��I�I � o      �H�H 
0 found1  �L  �K  � ��G� Z   � ����F�E� =  � ���� o   � ��D�D 0 act_num  � m   � ��� ���  2� k   � ��� ��� r   � ���� m   � ��C�C � o      �B�B 
0 found1  � ��A�  S   � ��A  �F  �E  �G  R =   C F��� o   C D�@�@ 
0 found1  � m   D E�?�? P ��� Z  � ����>�=� =  � ���� o   � ��<�< 
0 found1  � m   � ��� ���  2�  S   � ��>  �=  � ��� l  � ��;���;  � " get move command true/false(   � ��� 8 g e t   m o v e   c o m m a n d   t r u e / f a l s e (� ��� I  � ��:��9
�: .prcskcodnull���    long� m   � ��8�8 }�9  � ��� I  � ��7��6
�7 .sysodelanull��� ��� nmbr� m   � ��� ?�      �6  � ��� I  � ��5��4
�5 .prcskcodnull���    long� m   � ��3�3 |�4  � ��� I  � ��2��1
�2 .sysodelanull��� ��� nmbr� m   � ��� ?�      �1  � ��� I  � ��0��/
�0 .prcskcodnull���    long� m   � ��.�. |�/  � ��� I  � ��-��,
�- .sysodelanull��� ��� nmbr� m   � ��� ?�      �,  � ��� I  � ��+��
�+ .prcskprsnull���    utxt� m   � ��� ���  c� �*��)
�* 
faal� m   � ��(
�( eMdsKcmd�)  � ��� I  � ��'��&
�' .sysodelanull��� ��� nmbr� m   � ��� ?�      �&  � ��� r   � ���� c   � ���� l  � ���%�$� I  � ��#�"�!
�# .JonsgClp****    ��� null�"  �!  �%  �$  � m   � �� 
�  
TEXT� o      �� 0 address  � ��� r   	��� n  ��� 1  �
� 
txdl� 1   �
� 
ascr� o      �� 0 tid  � ��� r  
��� m  
�� ���   � n     ��� 1  �
� 
txdl� 1  �
� 
ascr� ��� r  "��� c   ��� l ���� n  ��� 4  ��
� 
citm� m  �� � o  �� 0 address  �  �  � m  �
� 
ctxt� o      �� 0 	thesubstr 	theSubStr� ��� r  #,��� o  #$�� 0 tid  � n     ��� 1  '+�
� 
txdl� 1  $'�
� 
ascr� ��� r  -0��� m  -.�
� boovtrue� o      �� 0 movedata moveData� ��� Z 1@����� > 16��� o  12�� 0 	thesubstr 	theSubStr� m  25�� ���  T r e m o n t� r  9<��� m  9:�

�
 boovfals� o      �	�	 0 movedata moveData�  �  � ��� I AH���
� .prcskcodnull���    long� m  AD�� 5�  � ��� I IN���
� .sysodelanull��� ��� nmbr� m  IJ�� ?�      �  � � � I OV��
� .prcskcodnull���    long m  OR�� ~�     I W\� ��
�  .sysodelanull��� ��� nmbr m  WX ?�      ��    I ]d����
�� .prcskcodnull���    long m  ]`���� {��   	
	 I ej����
�� .sysodelanull��� ��� nmbr m  ef ?�      ��  
  I kr����
�� .prcskcodnull���    long m  kn���� {��    I sx����
�� .sysodelanull��� ��� nmbr m  st ?�      ��    I y�����
�� .prcskcodnull���    long m  y|���� ~��    l ������    go right 3 columns    � $ g o   r i g h t   3   c o l u m n s  U  �� k  ��   !"! I ����#$
�� .prcskcodnull���    long# m  ������ |$ ��%��
�� 
faal% m  ����
�� eMdsKsft��  " &��& I ����'��
�� .sysodelanull��� ��� nmbr' m  ��(( ?�333333��  ��   m  ������  )*) l ����+,��  +  go up num rows   , �--  g o   u p   n u m   r o w s* .��. U  ��/0/ k  ��11 232 I ����45
�� .prcskcodnull���    long4 m  ������ ~5 ��6��
�� 
faal6 m  ����
�� eMdsKsft��  3 7��7 I ����8��
�� .sysodelanull��� ��� nmbr8 m  ��99 ?�333333��  ��  0 l ��:����: \  ��;<; o  ������ 0 sqmoved  < m  ������ ��  ��  ��  �q  �p  ? =>= l ����������  ��  ��  > ?@? Z  �AB����A = ��CDC o  ������ 0 movedata moveDataD m  ����
�� boovtrueB k  �EE FGF I ����HI
�� .prcskcodnull���    longH m  ������ I ��J��
�� 
faalJ m  ����
�� eMdsKcmd��  G KLK I ����M��
�� .sysodelanull��� ��� nmbrM m  ��NN ?�      ��  L OPO U  ��QRQ k  ��SS TUT I ����V��
�� .prcskcodnull���    longV m  ������ |��  U W��W I ����X��
�� .sysodelanull��� ��� nmbrX m  ��YY ?�333333��  ��  R m  ������ P Z[Z U  �\]\ k  ^^ _`_ I ��ab
�� .prcskcodnull���    longa m  ���� ~b ��c��
�� 
faalc m  ��
�� eMdsKsft��  ` d��d I ��e��
�� .sysodelanull��� ��� nmbre m  ff ?�333333��  ��  ] l �g����g \  �hih o  ������ 0 sqmoved  i m  � ���� ��  ��  [ jkj I +��lm
�� .prcskcodnull���    longl m   ���� 	m ��n��
�� 
faaln J  !'oo pqp m  !"��
�� eMdsKcmdq r��r m  "%��
�� eMdsKctl��  ��  k sts I ,1��u��
�� .sysodelanull��� ��� nmbru m  ,-vv ?�      ��  t wxw U  2Myzy k  9H{{ |}| I 9@��~��
�� .prcskcodnull���    long~ m  9<���� {��  } �� I AH�����
�� .sysodelanull��� ��� nmbr� m  AD�� ?�333333��  ��  z m  56���� x ��� I NS�����
�� .prcskcodnull���    long� m  NO���� }��  � ��� I T[�����
�� .sysodelanull��� ��� nmbr� m  TW�� ?�333333��  � ��� U  \{��� k  cv�� ��� I cn����
�� .prcskcodnull���    long� m  cf���� ~� �����
�� 
faal� m  gj��
�� eMdsKsft��  � ���� I ov�����
�� .sysodelanull��� ��� nmbr� m  or�� ?�333333��  ��  � l _`������ o  _`���� 0 sqmoved  ��  ��  � ��� U  |���� k  ���� ��� I ������
�� .prcskcodnull���    long� m  ������ {� �����
�� 
faal� m  ����
�� eMdsKsft��  � ���� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�333333��  ��  � m  ����� � ��� I �������
�� .prcsclicuiel    ��� uiel� n  ����� 4  �����
�� 
menI� m  ���� ���  D e l e t e . . .� n  ����� 4  �����
�� 
menE� m  ������ � n  ����� 4  �����
�� 
mbri� m  ���� ���  E d i t� 4  �����
�� 
mbar� m  ������ ��  � ��� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�      ��  � ��� I �������
�� .prcsclicuiel    ��� uiel� n  ����� 4  �����
�� 
radB� m  ���� ���  S h i f t   c e l l s   u p� n  ����� 4  �����
�� 
rgrp� m  ������ � n  ����� 4  �����
�� 
sgrp� m  ���� � 4  ���~�
�~ 
cwin� m  ���� ���  D e l e t e��  � ��� I ���}��|
�} .prcsclicuiel    ��� uiel� n  ����� 4  ���{�
�{ 
butT� m  ���� ���  O K� 4  ���z�
�z 
cwin� m  ���� ���  D e l e t e�|  � ��y� U  ���� k  ��� ��� I � �x��w
�x .prcskcodnull���    long� m  ���v�v {�w  � ��u� I �t��s
�t .sysodelanull��� ��� nmbr� m  �� ?�333333�s  �u  � m  ���r�r �y  ��  ��  @ ��� r  ��� m  �q
�q boovfals� o      �p�p 0 movedata moveData� ��� l �o�n�m�o  �n  �m  � ��� l �l�k�j�l  �k  �j  � ��i� l  �h���h  ��|				if act_num is equal to "1" then					key code 124					delay 0.25					set the clipboard to end_count as text					delay 0.35					key code 9 using command down					delay 0.25					key code 48 using shift down					delay 0.25					set end_count to end_count - 1					delay 0.25					key code 123					delay 0.25					key code 63					delay 0.25				end if				--if x is equal to 1 then key code 125				delay 0.25				repeat with i from 1 to 12					key code 126					delay 0.25				end repeat				delay 0.25
							keystroke "c" using command down			delay 0.25			set act_num to (the clipboard)			delay 0.25			key code 53			delay 0.25			if act_num is not equal to "2" then				set found2 to 0				repeat until found2 = 1					key code 125					delay 0.25					keystroke "c" using command down					delay 0.25					set act_num to (the clipboard)					delay 0.25					key code 53					delay 0.25					if act_num is equal to "2" then set found2 to 1					if act_num is equal to "conditional formatted" then						key code 125						delay 0.25						key code 124						delay 0.25						set the clipboard to end_count as text						delay 0.35						key code 9 using command down						delay 0.25						key code 123						delay 0.25						key code 126						delay 0.25						set found2 to 1					end if				end repeat			end if			if act_num is equal to "2" then				delay 0.25				key code 63				delay 0.25				key code 49 using shift down				delay 0.25				key code 27 using control down				delay 0.25			end if			key code 126			delay 0.25			if found1 is equal to 1 then				if found2 is equal to 2 then exit repeat			end if			--end repeat
			   � ����  	 	 	 	 i f   a c t _ n u m   i s   e q u a l   t o   " 1 "   t h e n  	 	 	 	 	 k e y   c o d e   1 2 4  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 s e t   t h e   c l i p b o a r d   t o   e n d _ c o u n t   a s   t e x t  	 	 	 	 	 d e l a y   0 . 3 5  	 	 	 	 	 k e y   c o d e   9   u s i n g   c o m m a n d   d o w n  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 k e y   c o d e   4 8   u s i n g   s h i f t   d o w n  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 s e t   e n d _ c o u n t   t o   e n d _ c o u n t   -   1  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 k e y   c o d e   1 2 3  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 k e y   c o d e   6 3  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 e n d   i f  	 	 	 	 - - i f   x   i s   e q u a l   t o   1   t h e n   k e y   c o d e   1 2 5  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 r e p e a t   w i t h   i   f r o m   1   t o   1 2  	 	 	 	 	 k e y   c o d e   1 2 6  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 e n d   r e p e a t  	 	 	 	 d e l a y   0 . 2 5 
 	 	 	 	  	 	 	 k e y s t r o k e   " c "   u s i n g   c o m m a n d   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 s e t   a c t _ n u m   t o   ( t h e   c l i p b o a r d )  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   5 3  	 	 	 d e l a y   0 . 2 5  	 	 	 i f   a c t _ n u m   i s   n o t   e q u a l   t o   " 2 "   t h e n  	 	 	 	 s e t   f o u n d 2   t o   0  	 	 	 	 r e p e a t   u n t i l   f o u n d 2   =   1  	 	 	 	 	 k e y   c o d e   1 2 5  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 k e y s t r o k e   " c "   u s i n g   c o m m a n d   d o w n  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 s e t   a c t _ n u m   t o   ( t h e   c l i p b o a r d )  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 k e y   c o d e   5 3  	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 i f   a c t _ n u m   i s   e q u a l   t o   " 2 "   t h e n   s e t   f o u n d 2   t o   1  	 	 	 	 	 i f   a c t _ n u m   i s   e q u a l   t o   " c o n d i t i o n a l   f o r m a t t e d "   t h e n  	 	 	 	 	 	 k e y   c o d e   1 2 5  	 	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 	 k e y   c o d e   1 2 4  	 	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 	 s e t   t h e   c l i p b o a r d   t o   e n d _ c o u n t   a s   t e x t  	 	 	 	 	 	 d e l a y   0 . 3 5  	 	 	 	 	 	 k e y   c o d e   9   u s i n g   c o m m a n d   d o w n  	 	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 	 k e y   c o d e   1 2 3  	 	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 	 k e y   c o d e   1 2 6  	 	 	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 	 	 s e t   f o u n d 2   t o   1  	 	 	 	 	 e n d   i f  	 	 	 	 e n d   r e p e a t  	 	 	 e n d   i f  	 	 	 i f   a c t _ n u m   i s   e q u a l   t o   " 2 "   t h e n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   6 3  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   4 9   u s i n g   s h i f t   d o w n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 	 k e y   c o d e   2 7   u s i n g   c o n t r o l   d o w n  	 	 	 	 d e l a y   0 . 2 5  	 	 	 e n d   i f  	 	 	 k e y   c o d e   1 2 6  	 	 	 d e l a y   0 . 2 5  	 	 	 i f   f o u n d 1   i s   e q u a l   t o   1   t h e n  	 	 	 	 i f   f o u n d 2   i s   e q u a l   t o   2   t h e n   e x i t   r e p e a t  	 	 	 e n d   i f  	 	 	 - - e n d   r e p e a t 
 	 	 	�i   4    �g�
�g 
pcap� m    �� ���  M i c r o s o f t   E x c e l m    ���                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��   ��f� l �e���e  � / )use conditional to rearrange rows of days   � ��� R u s e   c o n d i t i o n a l   t o   r e a r r a n g e   r o w s   o f   d a y s�f   � ��� l     �d�c�b�d  �c  �b  � ��� l     �a�`�_�a  �`  �_  � ��� l     �^�]�\�^  �]  �\  � ��� i    ��� I      �[�Z�Y�[ 0 transition1  �Z  �Y  � k    ��� ��� I    �X �W
�X .miscactvnull��� ��� null  m                                                                                       XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  �W  �  O   � O   
� k   � 	
	 l   �V�V    (make column with format)    � 2 ( m a k e   c o l u m n   w i t h   f o r m a t )
  I   �U
�U .prcskcodnull���    long m    �T�T 1 �S�R
�S 
faal m    �Q
�Q eMdsKctl�R    I   �P�O
�P .sysodelanull��� ��� nmbr m     ?�      �O    I   &�N
�N .prcskcodnull���    long m     �M�M  �L�K
�L 
faal m   ! "�J
�J eMdsKcmd�K    I  ' ,�I�H
�I .sysodelanull��� ��� nmbr m   ' ( ?�      �H    !  I  - 2�G"�F
�G .sysodelanull��� ��� nmbr" m   - .## ?�      �F  ! $%$ I  3 A�E&�D
�E .miscslctuiel       uiel& n   3 ='(' 4   : =�C)
�C 
sgrp) m   ; <�B�B ( n   3 :*+* 4   7 :�A,
�A 
tabg, m   8 9�@�@ + 4   3 7�?-
�? 
cwin- m   5 6�>�> �D  % ./. I  B G�=0�<
�= .sysodelanull��� ��� nmbr0 m   B C11 ?�      �<  / 232 I  H O�;4�:
�; .prcskcodnull���    long4 m   H K�9�9 �:  3 565 I  P U�87�7
�8 .sysodelanull��� ��� nmbr7 m   P Q88 ?�      �7  6 9:9 I  V ]�6;�5
�6 .prcskcodnull���    long; m   V Y�4�4 �5  : <=< I  ^ c�3>�2
�3 .sysodelanull��� ��� nmbr> m   ^ _?? ?�      �2  = @A@ I  d k�1B�0
�1 .prcskcodnull���    longB m   d g�/�/ 0�0  A CDC I  l q�.E�-
�. .sysodelanull��� ��� nmbrE m   l mFF ?�      �-  D GHG I  r y�,I�+
�, .prcskcodnull���    longI m   r u�*�* 0�+  H JKJ I  z �)L�(
�) .sysodelanull��� ��� nmbrL m   z {MM ?�      �(  K NON I  � ��'P�&
�' .prcskprsnull���    utxtP m   � �QQ �RR 
 h h : m m�&  O STS I  � ��%U�$
�% .sysodelanull��� ��� nmbrU m   � �VV ?�      �$  T WXW I  � ��#Y�"
�# .prcskcodnull���    longY m   � ��!�! $�"  X Z[Z I  � �� \�
�  .sysodelanull��� ��� nmbr\ m   � �]] ?�      �  [ ^_^ I  � ��`�
� .prcskcodnull���    long` m   � ��� $�  _ aba I  � ��c�
� .sysodelanull��� ��� nmbrc m   � �dd ?�      �  b efe I  � ��g�
� .prcskcodnull���    longg m   � ��� ~�  f hih I  � ��j�
� .sysodelanull��� ��� nmbrj m   � �kk ?�      �  i lml l  � ��no�  n  )make column with format   o �pp 0 ) m a k e   c o l u m n   w i t h   f o r m a tm qrq U   � �sts l  � �uvwu k   � �xx yzy I  � ��{�
� .sysodelanull��� ��� nmbr{ m   � �|| ?�      �  z }�} I  � ��~�
� .prcskcodnull���    long~ m   � ��� |�  �  v  go right 3 times   w �   g o   r i g h t   3   t i m e st m   � ��� r ��� l  � �����  �  (make column with format)   � ��� 2 ( m a k e   c o l u m n   w i t h   f o r m a t )� ��� I  � ����
� .prcskcodnull���    long� m   � ��
�
 1� �	��
�	 
faal� m   � ��
� eMdsKctl�  � ��� I  � ����
� .sysodelanull��� ��� nmbr� m   � ��� ?�      �  � ��� I  � ����
� .prcskcodnull���    long� m   � ��� � ���
� 
faal� m   � �� 
�  eMdsKcmd�  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  ������
�� .miscslctuiel       uiel� n   � ��� 4   � ���
�� 
sgrp� m   � ����� � n   � ���� 4   � ����
�� 
tabg� m   � ����� � 4   � ����
�� 
cwin� m   � ����� ��  � ��� I 
�����
�� .sysodelanull��� ��� nmbr� m  �� ?�      ��  � ��� I �����
�� .prcskcodnull���    long� m  ���� ��  � ��� I �����
�� .sysodelanull��� ��� nmbr� m  �� ?�      ��  � ��� I  �����
�� .prcskcodnull���    long� m  ���� ��  � ��� I !&�����
�� .sysodelanull��� ��� nmbr� m  !"�� ?�      ��  � ��� I '.�����
�� .prcskcodnull���    long� m  '*���� 0��  � ��� I /4�����
�� .sysodelanull��� ��� nmbr� m  /0�� ?�      ��  � ��� I 5<�����
�� .prcskcodnull���    long� m  58���� 0��  � ��� I =B�����
�� .sysodelanull��� ��� nmbr� m  =>�� ?�      ��  � ��� I CJ�����
�� .prcskprsnull���    utxt� m  CF�� ��� 
 h h : m m��  � ��� I KP�����
�� .sysodelanull��� ��� nmbr� m  KL�� ?�      ��  � ��� I QX�����
�� .prcskcodnull���    long� m  QT���� $��  � ��� I Y^�����
�� .sysodelanull��� ��� nmbr� m  YZ�� ?�      ��  � ��� I _f�����
�� .prcskcodnull���    long� m  _b���� $��  � ��� I gl�����
�� .sysodelanull��� ��� nmbr� m  gh�� ?�      ��  � ��� I mt�����
�� .prcskcodnull���    long� m  mp���� ~��  � ��� I uz�����
�� .sysodelanull��� ��� nmbr� m  uv�� ?�      ��  � ��� l {{������  �  )make column with format   � ��� 0 ) m a k e   c o l u m n   w i t h   f o r m a t� ��� U  {���� l ������ k  ���� ��� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�      ��  � ���� I �������
�� .prcskcodnull���    long� m  ������ {��  ��  �  go left 3 times   � ���  g o   l e f t   3   t i m e s� m  ~����� � ��� l ��������  �   (jump to other 2nd column)   � ��� 4 ( j u m p   t o   o t h e r   2 n d   c o l u m n )� ��� l ��������  �  (jump back)   � �    ( j u m p   b a c k )� �� l ����������  ��  ��  ��   4   
 ��
�� 
prcs m     �  M i c r o s o f t   E x c e l m    �                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��   �� l ������   , &make right format, setup for next move    �		 L m a k e   r i g h t   f o r m a t ,   s e t u p   f o r   n e x t   m o v e��  � 

 i     I      �������� 0 prepare1  ��  ��   k     &  I    ����
�� .miscactvnull��� ��� null m                                                                                       XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��   �� O    & O   
 % k    $  I   ����
�� .sysodelanull��� ��� nmbr m     ?�      ��    I   �� 
�� .prcskcodnull���    long m    ���� y  ��!��
�� 
faal! m    ��
�� eMdsKctl��   "��" I   $��#��
�� .sysodelanull��� ��� nmbr# m     $$ ?�      ��  ��   4   
 ��%
�� 
pcap% m    && �''  M i c r o s o f t   E x c e l m    ((�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��   )*) i    +,+ I      �������� 0 prepare2  ��  ��  , k     &-- ./. I    ��0��
�� .miscactvnull��� ��� null0 m     11                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  / 2��2 O    &343 O   
 %565 k    $77 898 I   ��:��
�� .sysodelanull��� ��� nmbr: m    ;; ?�      ��  9 <=< I   ��>?
�� .prcskcodnull���    long> m    ���� t? ��@��
�� 
faal@ m    ��
�� eMdsKctl��  = A��A I   $��B��
�� .sysodelanull��� ��� nmbrB m     CC ?�      ��  ��  6 4   
 ��D
�� 
pcapD m    EE �FF  M i c r o s o f t   E x c e l4 m    GG�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  * HIH i    JKJ I      ��L���� 0 makenewmonth makeNewMonthL MNM o      ���� 0 month_count  N O��O o      ���� 0 	day_count  ��  ��  K k    �PP QRQ I    ��S��
�� .miscactvnull��� ��� nullS m     TT                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  R UVU O   �WXW O   
�YZY k   �[[ \]\ I   ��^��
�� .sysodelanull��� ��� nmbr^ m    __ ?�      ��  ] `a` I   ��bc
�� .prcskcodnull���    longb m    ���� sc ��d��
�� 
faald m    ��
�� eMdsKctl��  a efe I   $��g��
�� .sysodelanull��� ��� nmbrg m     hh ?�      ��  f iji U   % <klk k   , 7mm non I  , 1��p��
�� .prcskcodnull���    longp m   , -���� 0��  o q��q I  2 7��r��
�� .sysodelanull��� ��� nmbrr m   2 3ss ?�      ��  ��  l m   ( )���� 	j tut Y   = Wv��wx�v k   G Ryy z{z I  G L�~|�}
�~ .prcskcodnull���    long| m   G H�|�| }�}  { }�{} I  M R�z~�y
�z .sysodelanull��� ��� nmbr~ m   M N ?�      �y  �{  �� 0 i  w m   @ A�x�x x o   A B�w�w 0 month_count  �  u ��� I  X _�v��
�v .prcskprsnull���    utxt� m   X Y�� ���  c� �u��t
�u 
faal� m   Z [�s
�s eMdsKcmd�t  � ��� I  ` e�r��q
�r .sysodelanull��� ��� nmbr� m   ` a�� ?�      �q  � ��� r   f s��� l  f q��p�o� I  f q�n�m�
�n .JonsgClp****    ��� null�m  � �l��k
�l 
rtyp� m   j m�j
�j 
long�k  �p  �o  � o      �i�i 0 day_num  � ��� I  t y�h��g
�h .sysodelanull��� ��� nmbr� m   t u�� ?�      �g  � ��� r   z }��� o   z {�f�f 0 day_num  � o      �e�e 0 repeat_count  � ��� I  ~ ��d��c
�d .sysodelanull��� ��� nmbr� m   ~ �� ?�      �c  � ��� r   � ���� [   � ���� o   � ��b�b 0 	day_count  � o   � ��a�a 0 day_num  � o      �`�` 0 	day_count  � ��� I  � ��_��^
�_ .sysodelanull��� ��� nmbr� m   � ��� ?�      �^  � ��� I  � ��]��\
�] .prcskcodnull���    long� m   � ��[�[ 5�\  � ��� I  � ��Z��Y
�Z .sysodelanull��� ��� nmbr� m   � ��� ?�      �Y  � ��� I  � ��X��
�X .prcskcodnull���    long� m   � ��W�W ~� �V��U
�V 
faal� m   � ��T
�T eMdsKctl�U  � ��� I  � ��S��R
�S .sysodelanull��� ��� nmbr� m   � ��� ?�      �R  � ��� I  � ��Q��P
�Q .prcskcodnull���    long� m   � ��O�O {�P  � ��� I  � ��N��M
�N .sysodelanull��� ��� nmbr� m   � ��� ?�      �M  � ��� I  � ��L��K
�L .prcskcodnull���    long� m   � ��J�J }�K  � ��� I  � ��I��H
�I .sysodelanull��� ��� nmbr� m   � ��� ?�      �H  � ��� I  � ��G��
�G .prcskprsnull���    utxt� m   � ��� ���  c� �F��E
�F 
faal� m   � ��D
�D eMdsKcmd�E  � ��� I  � ��C��B
�C .sysodelanull��� ��� nmbr� m   � ��� ?�      �B  � ��� Y   � ���A���@� k   � ��� ��� I  � ��?��
�? .prcskcodnull���    long� m   � ��>�> }� �=��<
�= 
faal� m   � ��;
�; eMdsKsft�<  � ��:� I  � ��9��8
�9 .sysodelanull��� ��� nmbr� m   � ��� ?�      �8  �:  �A 0 i  � m   � ��7�7 � l  � ���6�5� o   � ��4�4 0 day_num  �6  �5  �@  � ��� I  � �3��
�3 .prcskprsnull���    utxt� m   � ��� ���  v� �2��1
�2 
faal� m   � ��0
�0 eMdsKcmd�1  � ��� I �/��.
�/ .sysodelanull��� ��� nmbr� m  �� ?�      �.  � ��� I 	�-��
�- .prcskcodnull���    long� m  	�,�, ~� �+��*
�+ 
faal� m  �)
�) eMdsKctl�*  � ��� I �(��'
�( .sysodelanull��� ��� nmbr� m  �� ?�      �'  � ��� I �&��%
�& .prcskcodnull���    long� m  �$�$ }�%  � ��� I $�#��"
�# .sysodelanull��� ��� nmbr� m   �� ?�      �"  � ��� I %1�!��
�! .prcskcodnull���    long� m  %&� �  }� ���
� 
faal� J  '-    m  '(�
� eMdsKctl � m  (+�
� eMdsKsft�  �  �  I 27��
� .sysodelanull��� ��� nmbr m  23 ?�      �   	 I 8A�

� .prcskprsnull���    utxt
 m  8; �  c ��
� 
faal m  <=�
� eMdsKcmd�  	  I BG��
� .sysodelanull��� ��� nmbr m  BC ?�      �    I HO�
� .prcskcodnull���    long m  HI�� s ��
� 
faal m  JK�
� eMdsKctl�    I PU��
� .sysodelanull��� ��� nmbr m  PQ ?�      �    I V[��

� .prcskcodnull���    long m  VW�	�	 }�
     I \a�!�
� .sysodelanull��� ��� nmbr! m  \]"" ?�      �    #$# I bn�%&
� .prcskprsnull���    utxt% m  be'' �((  v& �)�
� 
faal) J  fj** +,+ m  fg�
� eMdsKctl, -�- m  gh�
� eMdsKcmd�  �  $ ./. I ot� 0��
�  .sysodelanull��� ��� nmbr0 m  op11 ?�      ��  / 232 I u|��4��
�� .prcskcodnull���    long4 m  ux���� 5��  3 565 I }���7��
�� .sysodelanull��� ��� nmbr7 m  }~88 ?�      ��  6 9:9 I ����;<
�� .prcskcodnull���    long; m  ������ s< ��=��
�� 
faal= m  ����
�� eMdsKctl��  : >?> I ����@��
�� .sysodelanull��� ��� nmbr@ m  ��AA ?�      ��  ? BCB U  ��DED k  ��FF GHG I ����I��
�� .prcskcodnull���    longI m  ������ 0��  H J��J I ����K��
�� .sysodelanull��� ��� nmbrK m  ��LL ?�      ��  ��  E m  ������ C MNM I ����O��
�� .sysodelanull��� ��� nmbrO m  ��PP ?�      ��  N QRQ I ����S��
�� .prcskcodnull���    longS m  ������ }��  R TUT I ����V��
�� .sysodelanull��� ��� nmbrV m  ��WW ?�      ��  U XYX I ����Z��
�� .prcskcodnull���    longZ m  ������ }��  Y [\[ I ����]��
�� .sysodelanull��� ��� nmbr] m  ��^^ ?�      ��  \ _`_ I ����ab
�� .prcskcodnull���    longa m  ������ }b ��c��
�� 
faalc J  ��dd efe m  ����
�� eMdsKctlf g��g m  ����
�� eMdsKsft��  ��  ` hih I ����j��
�� .sysodelanull��� ��� nmbrj m  ��kk ?�      ��  i lml I ����n��
�� .prcskcodnull���    longn m  ������ u��  m opo I ����q��
�� .sysodelanull��� ��� nmbrq m  ��rr ?�      ��  p sts I ����uv
�� .prcskcodnull���    longu m  ������ sv ��w��
�� 
faalw m  ����
�� eMdsKctl��  t x��x I ����y��
�� .sysodelanull��� ��� nmbry m  ��zz ?�      ��  ��  Z 4   
 ��{
�� 
pcap{ m    || �}}  M i c r o s o f t   E x c e lX m    ~~�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  V �� L  ���� J  ���� ��� o  ������ 0 repeat_count  � ���� o  ������ 0 	day_count  ��  ��  I ��� i    ��� I      ������� 0 	maketimes 	makeTimes� ��� o      ���� 0 repeat_count  � ���� o      ���� 0 	day_count  ��  ��  � k    ��� ��� Y    ��������� k   
��� ��� l  
 
������  �   move down number in repeat   � ��� 4 m o v e   d o w n   n u m b e r   i n   r e p e a t� ��� I  
 �����
�� .miscactvnull��� ��� null� m   
 ��                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  � ���� O   ���� O   ���� k   ��� ��� I    �����
�� .sysodelanull��� ��� nmbr� m    �� ?�      ��  � ��� I  ! (����
�� .prcskcodnull���    long� m   ! "���� s� �����
�� 
faal� m   # $��
�� eMdsKctl��  � ��� I  ) .�����
�� .sysodelanull��� ��� nmbr� m   ) *�� ?�      ��  � ��� Y   / I�������� k   9 D�� ��� I  9 >�����
�� .sysodelanull��� ��� nmbr� m   9 :�� ?�      ��  � ���� I  ? D�����
�� .prcskcodnull���    long� m   ? @���� }��  ��  �� 0 j  � m   2 3���� � o   3 4���� 0 x  ��  � ��� l  J J������  �  go down to random number   � ��� 0 g o   d o w n   t o   r a n d o m   n u m b e r� ��� I  J O�����
�� .sysodelanull��� ��� nmbr� m   J K�� ?�      ��  � ��� I  P W����
�� .prcskprsnull���    utxt� m   P Q�� ���  c� �����
�� 
faal� m   R S��
�� eMdsKcmd��  � ��� I  X ]�����
�� .sysodelanull��� ��� nmbr� m   X Y�� ?�      ��  � ��� r   ^ i��� l  ^ g������ I  ^ g�����
�� .JonsgClp****    ��� null��  � �����
�� 
rtyp� m   ` c��
�� 
long��  ��  ��  � o      ���� 0 list_num  � ��� I  j o�����
�� .sysodelanull��� ��� nmbr� m   j k�� ?�      ��  � ��� I  p w�����
�� .prcskcodnull���    long� m   p s���� 5��  � ��� I  x }�����
�� .sysodelanull��� ��� nmbr� m   x y�� ?�      ��  � ��� I  ~ ������
�� .prcskcodnull���    long� m   ~ ����� |��  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  � �����
�� .prcskcodnull���    long� m   � ����� ~� �����
�� 
faal� m   � ���
�� eMdsKctl��  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  � ������
�� .prcskcodnull���    long� m   � ����� |��  � ��� I  � ����~
� .sysodelanull��� ��� nmbr� m   � ��� ?�      �~  � ��� Y   � ���}���|� k   � ��� � � I  � ��{�z
�{ .sysodelanull��� ��� nmbr m   � � ?�      �z    �y I  � ��x
�x .prcskcodnull���    long m   � ��w�w } �v�u
�v 
faal m   � ��t
�t eMdsKctl�u  �y  �} 0 i  � m   � ��s�s � l  � ��r�q o   � ��p�p 0 list_num  �r  �q  �|  � 	 l  � ��o
�o  
  go to right section    � & g o   t o   r i g h t   s e c t i o n	  I  � ��n�m
�n .sysodelanull��� ��� nmbr m   � � ?�      �m    I  � ��l�k
�l .prcskcodnull���    long m   � ��j�j |�k    Y   ��i�h k   �  I  � ��g�f
�g .sysodelanull��� ��� nmbr m   � � ?�      �f    I  � ��e !
�e .prcskcodnull���    long  m   � ��d�d  ! �c"�b
�c 
faal" m   � ��a
�a eMdsKctl�b   #$# I  � ��`%�_
�` .sysodelanull��� ��� nmbr% m   � �&& ?�      �_  $ '(' I  � ��^)�]
�^ .prcskcodnull���    long) m   � ��\�\ 0�]  ( *�[* I  ��Z+�Y
�Z .sysodelanull��� ��� nmbr+ m   � �,, ?�      �Y  �[  �i 0 i   m   � ��X�X  m   � ��W�W �h   -.- I �V/�U
�V .sysodelanull��� ��� nmbr/ m  	00 ?�      �U  . 121 I �T3�S
�T .prcskcodnull���    long3 m  �R�R {�S  2 454 I �Q6�P
�Q .sysodelanull��� ��� nmbr6 m  77 ?�      �P  5 898 I %�O:;
�O .prcskprsnull���    utxt: m  << �==  c; �N>�M
�N 
faal> m   !�L
�L eMdsKcmd�M  9 ?@? I &+�KA�J
�K .sysodelanull��� ��� nmbrA m  &'BB ?�      �J  @ CDC r  ,7EFE l ,5G�I�HG I ,5�G�FH
�G .JonsgClp****    ��� null�F  H �EI�D
�E 
rtypI m  .1�C
�C 
ctxt�D  �I  �H  F o      �B�B 0 top_time  D JKJ I 8=�AL�@
�A .sysodelanull��� ��� nmbrL m  89MM ?�      �@  K NON I >E�?P�>
�? .prcskcodnull���    longP m  >A�=�= 5�>  O QRQ Z  F&ST�<�;S H  FPUU E  FOVWV l FKX�:�9X I FK�8�7�6
�8 .JonsgClp****    ��� null�7  �6  �:  �9  W m  KNYY �ZZ  :T l S"[\][ k  S"^^ _`_ I SX�5a�4
�5 .sysodelanull��� ��� nmbra m  STbb ?�      �4  ` cdc I Y`�3e�2
�3 .prcskcodnull���    longe m  Y\�1�1 {�2  d fgf I af�0h�/
�0 .sysodelanull��� ��� nmbrh m  abii ?�      �/  g jkj I gn�.l�-
�. .prcskcodnull���    longl m  gj�,�, {�-  k mnm I ot�+o�*
�+ .sysodelanull��� ��� nmbro m  oppp ?�      �*  n qrq I u~�)st
�) .prcskcodnull���    longs m  ux�(�(  t �'u�&
�' 
faalu m  yz�%
�% eMdsKctl�&  r vwv I ��$x�#
�$ .sysodelanull��� ��� nmbrx m  �yy ?�      �#  w z{z I ���"|�!
�" .prcskcodnull���    long| m  ��� �  0�!  { }~} I ����
� .sysodelanull��� ��� nmbr m  ���� ?�      �  ~ ��� I �����
� .prcskcodnull���    long� m  ���� 0�  � ��� I �����
� .sysodelanull��� ��� nmbr� m  ���� ?�      �  � ��� I �����
� .prcskprsnull���    utxt� m  ���� ���  c� ���
� 
faal� m  ���
� eMdsKcmd�  � ��� I �����
� .sysodelanull��� ��� nmbr� m  ���� ?�      �  � ��� r  ����� l ������ I �����
� .JonsgClp****    ��� null�  � ���
� 
rtyp� m  ���
� 
ctxt�  �  �  � o      �� 0 top_time  � ��� I ���
��	
�
 .sysodelanull��� ��� nmbr� m  ���� ?�      �	  � ��� I �����
� .prcskcodnull���    long� m  ���� 5�  � ��� Z  �"����� H  ���� E  ����� l ������ I ��� ����
�  .JonsgClp****    ��� null��  ��  �  �  � m  ���� ���  :� l ����� k  ��� ��� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�      ��  � ��� I �������
�� .prcskcodnull���    long� m  ������ {��  � ��� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�      ��  � ��� I ������
�� .prcskcodnull���    long� m  ������  � �����
�� 
faal� m  ����
�� eMdsKctl��  � ��� I �������
�� .sysodelanull��� ��� nmbr� m  ���� ?�      ��  � ��� I ������
�� .prcskcodnull���    long� m  ������ 0��  � ��� l ��������  ��  ��  � ��� I 	�����
�� .sysodelanull��� ��� nmbr� m  �� ?�      ��  � ��� I 
����
�� .prcskprsnull���    utxt� m  
�� ���  c� �����
�� 
faal� m  ��
�� eMdsKcmd��  � ��� I �����
�� .sysodelanull��� ��� nmbr� m  �� ?�      ��  � ��� r  %��� l #������ I #�����
�� .JonsgClp****    ��� null��  � �����
�� 
rtyp� m  ��
�� 
ctxt��  ��  ��  � o      ���� 0 top_time  � ��� I &+�����
�� .sysodelanull��� ��� nmbr� m  &'�� ?�      ��  � ��� I ,3�����
�� .prcskcodnull���    long� m  ,/���� 5��  � ���� Z  4������� H  4>�� E  4=��� l 49������ I 49������
�� .JonsgClp****    ��� null��  ��  ��  ��  � m  9<�� ���  :� k  A�� ��� I AF�����
�� .sysodelanull��� ��� nmbr� m  AB�� ?�      ��  � ��� I GP����
�� .prcskcodnull���    long� m  GJ����  � �����
�� 
faal� m  KL��
�� eMdsKctl��  � ��� I QV�����
�� .sysodelanull��� ��� nmbr� m  QR�� ?�      ��  � ��� I W^�����
�� .prcskcodnull���    long� m  WZ���� 0��  � ��� I _d�� ��
�� .sysodelanull��� ��� nmbr  m  _` ?�      ��  �  I el����
�� .prcskcodnull���    long m  eh���� {��    I mr����
�� .sysodelanull��� ��� nmbr m  mn ?�      ��   	
	 I s|��
�� .prcskprsnull���    utxt m  sv �  c ����
�� 
faal m  wx��
�� eMdsKcmd��  
  I }�����
�� .sysodelanull��� ��� nmbr m  }~ ?�      ��    r  �� l ������ I ������
�� .JonsgClp****    ��� null��   ����
�� 
rtyp m  ����
�� 
ctxt��  ��  ��   o      ���� 0 top_time    I ������
�� .sysodelanull��� ��� nmbr m  �� ?�      ��     I ����!��
�� .prcskcodnull���    long! m  ������ 5��    "��" Z  �#$����# H  ��%% E  ��&'& l ��(����( I ��������
�� .JonsgClp****    ��� null��  ��  ��  ��  ' m  ��)) �**  :$ l �+,-+ k  �.. /0/ I ����1��
�� .sysodelanull��� ��� nmbr1 m  ��22 ?�      ��  0 343 I ����5��
�� .prcskcodnull���    long5 m  ������ {��  4 676 I ����8��
�� .sysodelanull��� ��� nmbr8 m  ��99 ?�      ��  7 :;: I ����<��
�� .prcskcodnull���    long< m  ������ {��  ; =>= I ����?��
�� .sysodelanull��� ��� nmbr? m  ��@@ ?�      ��  > ABA I ����CD
�� .prcskcodnull���    longC m  ������  D ��E��
�� 
faalE m  ����
�� eMdsKctl��  B FGF I ����H��
�� .sysodelanull��� ��� nmbrH m  ��II ?�      ��  G JKJ I ����L��
�� .prcskcodnull���    longL m  ������ 0��  K MNM I ����O��
�� .sysodelanull��� ��� nmbrO m  ��PP ?�      ��  N QRQ I ����S��
�� .prcskcodnull���    longS m  ������ 0��  R T��T Z  �UV����U H  ��WW E  ��XYX l ��Z���Z I ���~�}�|
�~ .JonsgClp****    ��� null�}  �|  ��  �  Y m  ��[[ �\\  :V l �]^_] k  �`` aba I ��{c�z
�{ .sysodelanull��� ��� nmbrc m  � dd ?�      �z  b efe I �yg�x
�y .prcskcodnull���    longg m  �w�w {�x  f hih I �vj�u
�v .sysodelanull��� ��� nmbrj m  kk ?�      �u  i lml I �tn�s
�t .prcskcodnull���    longn m  �r�r {�s  m opo I  �qq�p
�q .sysodelanull��� ��� nmbrq m  rr ?�      �p  p sts I !*�ouv
�o .prcskcodnull���    longu m  !$�n�n  v �mw�l
�m 
faalw m  %&�k
�k eMdsKctl�l  t xyx I +0�jz�i
�j .sysodelanull��� ��� nmbrz m  +,{{ ?�      �i  y |}| I 18�h~�g
�h .prcskcodnull���    long~ m  14�f�f 0�g  } � I 9>�e��d
�e .sysodelanull��� ��� nmbr� m  9:�� ?�      �d  � ��� I ?F�c��b
�c .prcskcodnull���    long� m  ?B�a�a 0�b  � ��� I GL�`��_
�` .sysodelanull��� ��� nmbr� m  GH�� ?�      �_  � ��� I MV�^��
�^ .prcskprsnull���    utxt� m  MP�� ���  c� �]��\
�] 
faal� m  QR�[
�[ eMdsKcmd�\  � ��� I W\�Z��Y
�Z .sysodelanull��� ��� nmbr� m  WX�� ?�      �Y  � ��� r  ]h��� l ]f��X�W� I ]f�V�U�
�V .JonsgClp****    ��� null�U  � �T��S
�T 
rtyp� m  _b�R
�R 
ctxt�S  �X  �W  � o      �Q�Q 0 top_time  � ��� I in�P��O
�P .sysodelanull��� ��� nmbr� m  ij�� ?�      �O  � ��� I ov�N��M
�N .prcskcodnull���    long� m  or�L�L 5�M  � ��K� Z  w���J�I� H  w��� E  w���� l w|��H�G� I w|�F�E�D
�F .JonsgClp****    ��� null�E  �D  �H  �G  � m  |�� ���  :� k  ��� ��� r  ����� m  ���C�C  � o      �B�B 0 done  � ��A� W  ���� k  �	�� ��� I ���@��?
�@ .sysodelanull��� ��� nmbr� m  ���� ?�      �?  � ��� I ���>��
�> .prcskcodnull���    long� m  ���=�=  � �<��;
�< 
faal� m  ���:
�: eMdsKctl�;  � ��� I ���9��8
�9 .sysodelanull��� ��� nmbr� m  ���� ?�      �8  � ��� I ���7��6
�7 .prcskcodnull���    long� m  ���5�5 0�6  � ��� I ���4��3
�4 .sysodelanull��� ��� nmbr� m  ���� ?�      �3  � ��� I ���2��
�2 .prcskcodnull���    long� m  ���1�1 0� �0��/
�0 
faal� m  ���.
�. eMdsKsft�/  � ��� I ���-��,
�- .sysodelanull��� ��� nmbr� m  ���� ?�      �,  � ��� I ���+��
�+ .prcskprsnull���    utxt� m  ���� ���  c� �*��)
�* 
faal� m  ���(
�( eMdsKcmd�)  � ��� I ���'��&
�' .sysodelanull��� ��� nmbr� m  ���� ?�      �&  � ��� r  ����� l ����%�$� I ���#�"�
�# .JonsgClp****    ��� null�"  � �!�� 
�! 
rtyp� m  ���
� 
ctxt�   �%  �$  � o      �� 0 top_time  � ��� I �����
� .sysodelanull��� ��� nmbr� m  ���� ?�      �  � ��� I �����
� .prcskcodnull���    long� m  ���� 5�  � ��� I �����
� .sysodelanull��� ��� nmbr� m  ���� ?�      �  � ��� Z �	����� E  ����� l ������ I �����
� .JonsgClp****    ��� null�  �  �  �  � m  ���� ���  :� r  ��� m  �� � o      �� 0 done  �  �  �  � =  ����� o  ���� 0 done  � m  ���� �A  �J  �I  �K  ^  	go over 2   _ ���  g o   o v e r   2��  ��  ��  ,  	go over 2   - ���  g o   o v e r   2��  ��  ��  ��  ��  ��  �  	go over 1   � ���  g o   o v e r   1�  �  �  \  	go over 2   ] ���  g o   o v e r   2�<  �;  R � � I ',�
�	
�
 .sysodelanull��� ��� nmbr m  '( ?�      �	     I -9�
� .prcskcodnull���    long m  -.�� } ��
� 
faal J  /5 	
	 m  /0�
� eMdsKctl
 � m  03�
� eMdsKsft�  �    I :?�� 
� .sysodelanull��� ��� nmbr m  :; ?�      �     I @K��
�� .prcskcodnull���    long m  @C���� | ����
�� 
faal m  DG��
�� eMdsKsft��    I LQ����
�� .sysodelanull��� ��� nmbr m  LM ?�      ��    I R[��
�� .prcskprsnull���    utxt m  RU �  c ����
�� 
faal m  VW��
�� eMdsKcmd��    !  I \a��"��
�� .sysodelanull��� ��� nmbr" m  \]## ?�      ��  ! $%$ I bk��&'
�� .prcskcodnull���    long& m  be���� y' ��(��
�� 
faal( m  fg��
�� eMdsKctl��  % )*) I lq��+��
�� .sysodelanull��� ��� nmbr+ m  lm,, ?�      ��  * -.- I r~��/0
�� .prcskcodnull���    long/ m  ru���� 	0 ��1��
�� 
faal1 J  vz22 343 m  vw��
�� eMdsKcmd4 5��5 m  wx��
�� eMdsKctl��  ��  . 676 I ���8��
�� .sysodelanull��� ��� nmbr8 m  �99 ?�      ��  7 :;: l ����<=��  < 3 -key code 1 using {command down, control down}   = �>> Z k e y   c o d e   1   u s i n g   { c o m m a n d   d o w n ,   c o n t r o l   d o w n }; ?@? l ����AB��  A  
delay 0.25   B �CC  d e l a y   0 . 2 5@ DED I ����FG
�� .prcskcodnull���    longF m  ������ }G ��H��
�� 
faalH m  ����
�� eMdsKctl��  E IJI I ����K��
�� .sysodelanull��� ��� nmbrK m  ��LL ?�      ��  J MNM I ����O��
�� .prcskcodnull���    longO m  ������ }��  N PQP I ����R��
�� .sysodelanull��� ��� nmbrR m  ��SS ?�      ��  Q TUT I ����V��
�� .prcskcodnull���    longV m  ������ }��  U WXW I ����Y��
�� .sysodelanull��� ��� nmbrY m  ��ZZ ?�      ��  X [��[ I ����\]
�� .prcskcodnull���    long\ m  ������ t] ��^��
�� 
faal^ m  ����
�� eMdsKctl��  ��  � 4    ��_
�� 
pcap_ m    `` �aa  M i c r o s o f t   E x c e l� m    bb�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  �� 0 x  � m    ���� � o    ���� 0 repeat_count  ��  � c��c l ����de��  d  set times and sort places   e �ff 2 s e t   t i m e s   a n d   s o r t   p l a c e s��  � ghg i    iji I      �������� 0 transfer_clean1  ��  ��  j k    /kk lml I    ��n��
�� .miscactvnull��� ��� nulln m     oo                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  m p��p O   /qrq O   
.sts k   -uu vwv I   ��xy
�� .prcskcodnull���    longx m    ���� sy ��z��
�� 
faalz m    ��
�� eMdsKctl��  w {|{ I   ��}��
�� .sysodelanull��� ��� nmbr} m    ~~ ?�      ��  | � I   $�����
�� .prcskcodnull���    long� m     ���� }��  � ��� I  % *�����
�� .sysodelanull��� ��� nmbr� m   % &�� ?�      ��  � ��� I  + 0�����
�� .prcskcodnull���    long� m   + ,���� |��  � ��� I  1 6�����
�� .sysodelanull��� ��� nmbr� m   1 2�� ?�      ��  � ��� I  7 <�����
�� .prcskcodnull���    long� m   7 8���� |��  � ��� I  = B�����
�� .sysodelanull��� ��� nmbr� m   = >�� ?�      ��  � ��� I  C J����
�� .prcskcodnull���    long� m   C D���� 1� �����
�� 
faal� m   E F��
�� eMdsKctl��  � ��� I  K P�����
�� .sysodelanull��� ��� nmbr� m   K L�� ?�      ��  � ��� I  Q X����
�� .prcskcodnull���    long� m   Q R���� "� �����
�� 
faal� m   S T��
�� eMdsKctl��  � ��� I  Y ^�����
�� .sysodelanull��� ��� nmbr� m   Y Z�� ?�      ��  � ��� I  _ d�����
�� .prcskcodnull���    long� m   _ `���� |��  � ��� I  e j�����
�� .sysodelanull��� ��� nmbr� m   e f�� ?�      ��  � ��� I  k p�����
�� .prcskcodnull���    long� m   k l���� |��  � ��� I  q v�����
�� .sysodelanull��� ��� nmbr� m   q r�� ?�      ��  � ��� I  w �����
�� .prcskcodnull���    long� m   w x���� }� �����
�� 
faal� J   y }�� ��� m   y z��
�� eMdsKctl� ���� m   z {��
�� eMdsKsft��  ��  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  � �����
�� .prcskcodnull���    long� m   � ����� {� �����
�� 
faal� m   � ���
�� eMdsKsft��  � ��� I  � ������
�� .sysodelanull��� ��� nmbr� m   � ��� ?�      ��  � ��� I  � �����
�� .prcskcodnull���    long� m   � ��� {� �~��}
�~ 
faal� m   � ��|
�| eMdsKsft�}  � ��� I  � ��{��z
�{ .sysodelanull��� ��� nmbr� m   � ��� ?�      �z  � ��� I  � ��y��
�y .prcskcodnull���    long� m   � ��x�x {� �w��v
�w 
faal� m   � ��u
�u eMdsKsft�v  � ��� I  � ��t��s
�t .sysodelanull��� ��� nmbr� m   � ��� ?�      �s  � ��� I  � ��r��
�r .prcskcodnull���    long� m   � ��q�q � �p��o
�p 
faal� m   � ��n
�n eMdsKcmd�o  � ��� I  � ��m��l
�m .sysodelanull��� ��� nmbr� m   � ��� ?�      �l  � ��� I  � ��k��
�k .prcskcodnull���    long� m   � ��j�j y� �i��h
�i 
faal� m   � ��g
�g eMdsKctl�h  � ��� I  � ��f��e
�f .sysodelanull��� ��� nmbr� m   � ��� ?�      �e  � ��� I  � ��d��
�d .prcskcodnull���    long� m   � ��c�c 	� �b��a
�b 
faal� m   � ��`
�` eMdsKcmd�a  � ��� I  � ��_��^
�_ .sysodelanull��� ��� nmbr� m   � ��]�] �^  � ��� I  � ��\��[
�\ .prcskcodnull���    long� m   � ��Z�Z 5�[  � ��� I  � ��Y��X
�Y .sysodelanull��� ��� nmbr� m   � ��� ?�      �X  � ��� I  ��W��V
�W .prcskcodnull���    long� m   � ��U�U ~�V  � 	 		  I 	�T	�S
�T .sysodelanull��� ��� nmbr	 m  		 ?�      �S  	 			 I 
�R	�Q
�R .prcskcodnull���    long	 m  
�P�P }�Q  	 			 I �O		�N
�O .sysodelanull��� ��� nmbr		 m  	
	
 ?�      �N  	 			 I �M	�L
�M .prcskcodnull���    long	 m  �K�K |�L  	 			 I !�J	�I
�J .sysodelanull��� ��� nmbr	 m  		 ?�      �I  	 			 I "'�H	�G
�H .prcskcodnull���    long	 m  "#�F�F |�G  	 	�E	 I (-�D	�C
�D .sysodelanull��� ��� nmbr	 m  ()		 ?�      �C  �E  t 4   
 �B	
�B 
pcap	 m    		 �		  M i c r o s o f t   E x c e lr m    		�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  h 			 l     �A�@�?�A  �@  �?  	 			 i     #	 	!	  I      �>�=�<�> 0 transfer_clean2  �=  �<  	! k    x	"	" 	#	$	# I    �;	%�:
�; .miscactvnull��� ��� null	% m     	&	&                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  �:  	$ 	'	(	' O   v	)	*	) O   
u	+	,	+ k   t	-	- 	.	/	. U    (	0	1	0 k    #	2	2 	3	4	3 I   �9	5�8
�9 .prcskcodnull���    long	5 m    �7�7 |�8  	4 	6�6	6 I   #�5	7�4
�5 .sysodelanull��� ��� nmbr	7 m    	8	8 ?�      �4  �6  	1 m    �3�3 	/ 	9	:	9 l  ) )�2	;	<�2  	;  leaving 6 month sheet   	< �	=	= * l e a v i n g   6   m o n t h   s h e e t	: 	>	?	> I  ) 0�1	@	A
�1 .prcskcodnull���    long	@ m   ) *�0�0 t	A �/	B�.
�/ 
faal	B m   + ,�-
�- eMdsKctl�.  	? 	C	D	C I  1 6�,	E�+
�, .sysodelanull��� ��� nmbr	E m   1 2	F	F ?�      �+  	D 	G	H	G I  7 <�*	I�)
�* .prcskcodnull���    long	I m   7 8�(�( $�)  	H 	J	K	J I  = B�'	L�&
�' .sysodelanull��� ��� nmbr	L m   = >	M	M ?�      �&  	K 	N	O	N I  C J�%	P	Q
�% .prcskcodnull���    long	P m   C D�$�$ s	Q �#	R�"
�# 
faal	R m   E F�!
�! eMdsKctl�"  	O 	S	T	S I  K P� 	U�
�  .sysodelanull��� ��� nmbr	U m   K L	V	V ?�      �  	T 	W	X	W I  Q V�	Y�
� .prcskcodnull���    long	Y m   Q R�� |�  	X 	Z	[	Z I  W \�	\�
� .sysodelanull��� ��� nmbr	\ m   W X	]	] ?�      �  	[ 	^	_	^ I  ] b�	`�
� .prcskcodnull���    long	` m   ] ^�� |�  	_ 	a	b	a I  c h�	c�
� .sysodelanull��� ��� nmbr	c m   c d	d	d ?�      �  	b 	e	f	e I  i p�	g	h
� .prcskcodnull���    long	g m   i j�� 1	h �	i�
� 
faal	i m   k l�
� eMdsKctl�  	f 	j	k	j I  q v�	l�
� .sysodelanull��� ��� nmbr	l m   q r	m	m ?�      �  	k 	n	o	n I  w ��	p	q
� .prcskcodnull���    long	p m   w x�� 	q �	r�

� 
faal	r J   y }	s	s 	t	u	t m   y z�	
�	 eMdsKctl	u 	v�	v m   z {�
� eMdsKsft�  �
  	o 	w	x	w I  � ��	y�
� .sysodelanull��� ��� nmbr	y m   � �	z	z ?�      �  	x 	{	|	{ I  � ��	}�
� .prcskcodnull���    long	} m   � ��� {�  	| 	~		~ I  � ��	�� 
� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      �   	 	�	�	� I  � ���	�	�
�� .prcskcodnull���    long	� m   � ����� 1	� ��	���
�� 
faal	� m   � ���
�� eMdsKctl��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	�	�
�� .prcskcodnull���    long	� m   � ����� 	� ��	���
�� 
faal	� J   � �	�	� 	�	�	� m   � ���
�� eMdsKctl	� 	���	� m   � ���
�� eMdsKsft��  ��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	���
�� .prcskcodnull���    long	� m   � ����� ~��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	���
�� .prcskcodnull���    long	� m   � ����� }��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	�	�
�� .prcskcodnull���    long	� m   � ����� }	� ��	���
�� 
faal	� J   � �	�	� 	�	�	� m   � ���
�� eMdsKctl	� 	���	� m   � ���
�� eMdsKsft��  ��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	�	�
�� .prcskcodnull���    long	� m   � ����� |	� ��	���
�� 
faal	� m   � ���
�� eMdsKsft��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  � ���	���
�� .prcskcodnull���    long	� m   � ����� u��  	� 	�	�	� I  � ���	���
�� .sysodelanull��� ��� nmbr	� m   � �	�	� ?�      ��  	� 	�	�	� I  ��	���
�� .prcskcodnull���    long	� m   ���� ~��  	� 	�	�	� I ��	���
�� .sysodelanull��� ��� nmbr	� m  		�	� ?�      ��  	� 	�	�	� I ��	���
�� .prcskcodnull���    long	� m  ���� }��  	� 	�	�	� I ��	���
�� .sysodelanull��� ��� nmbr	� m  	�	� ?�      ��  	� 	�	�	� l ��	�	���  	�  leaving copy edit sheet   	� �	�	� . l e a v i n g   c o p y   e d i t   s h e e t	� 	�	�	� I #��	�	�
�� .prcskcodnull���    long	� m  ���� t	� ��	���
�� 
faal	� m  ��
�� eMdsKctl��  	� 	�	�	� I $)��	���
�� .sysodelanull��� ��� nmbr	� m  $%	�	� ?�      ��  	� 	�	�	� I */��	���
�� .prcskcodnull���    long	� m  *+���� s��  	� 	�	�	� I 05��	���
�� .sysodelanull��� ��� nmbr	� m  01	�	� ?�      ��  	� 	�	�	� I 6=��	���
�� .prcskcodnull���    long	� m  69���� }��  	� 	�	�	� I >C��	���
�� .sysodelanull��� ��� nmbr	� m  >?	�	� ?�      ��  	� 	�	�	� I DP��	�	�
�� .prcskcodnull���    long	� m  DG���� }	� ��	���
�� 
faal	� J  HL	�	� 	�	�	� m  HI��
�� eMdsKctl	� 	���	� m  IJ��
�� eMdsKsft��  ��  	� 	�	�	� I QV��	���
�� .sysodelanull��� ��� nmbr	� m  QR	�	� ?�      ��  	� 	�	�	� I W^��	���
�� .prcskcodnull���    long	� m  WZ���� u��  	� 	�	�	� I _d��	���
�� .sysodelanull��� ��� nmbr	� m  _`
 
  ?�      ��  	� 


 I el��
��
�� .prcskcodnull���    long
 m  eh���� ~��  
 


 I mr��
��
�� .sysodelanull��� ��� nmbr
 m  mn

 ?�      ��  
 
��
 l ss��
	

��  
	  on goto sheet   

 �

  o n   g o t o   s h e e t��  	, 4   
 ��

�� 
pcap
 m    

 �

  M i c r o s o f t   E x c e l	* m    

�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  	( 
��
 l ww��

��  
 # transfer data to second sheet   
 �

 : t r a n s f e r   d a t a   t o   s e c o n d   s h e e t��  	 


 l     ��������  ��  ��  
 


 i   $ '


 I      ��
���� *0 adddaynum_rearrange addDayNum_rearrange
 


 o      ���� 0 repeat_count  
 
��
 o      ���� 0 	day_count  ��  ��  
 k     �

 

 
 I    ��
!��
�� .miscactvnull��� ��� null
! m     
"
"                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  
  
#
$
# O    $
%
&
% O   
 #
'
(
' k    "
)
) 
*
+
* I   ��
,��
�� .sysodelanull��� ��� nmbr
, m    
-
- ?�      ��  
+ 
.
/
. I   ��
0��
�� .prcskcodnull���    long
0 m    ���� 5��  
/ 
1��
1 I   "��
2��
�� .sysodelanull��� ��� nmbr
2 m    
3
3 ?�      ��  ��  
( 4   
 ��
4
�� 
pcap
4 m    
5
5 �
6
6  M i c r o s o f t   E x c e l
& m    
7
7�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  
$ 
8
9
8 l  % %��
:
;��  
: ' !setup for transition to next step   
; �
<
< B s e t u p   f o r   t r a n s i t i o n   t o   n e x t   s t e p
9 
=
>
= I  % *��
?��
�� .miscactvnull��� ��� null
? m   % &
@
@                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  ��  
> 
A��
A O   + �
B
C
B O   / �
D
E
D k   6 �
F
F 
G
H
G l   6 6��
I
J��  
I � �			delay 0.25			key code 124			delay 0.25			key code 49 using control down			delay 0.25			key code 34 using control down			delay 0.25			key code 126			delay 0.25			key code 126 using control down			delay 0.25			key code 125			delay 0.25   
J �
K
K�  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 4  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   4 9   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   3 4   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 6  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 6   u s i n g   c o n t r o l   d o w n  	 	 	 d e l a y   0 . 2 5  	 	 	 k e y   c o d e   1 2 5  	 	 	 d e l a y   0 . 2 5
H 
L��
L Y   6 �
M��
N
O��
M k   D �
P
P 
Q
R
Q I  D I��
S��
�� .prcskcodnull���    long
S m   D E�� |��  
R 
T
U
T I  J O�~
V�}
�~ .sysodelanull��� ��� nmbr
V m   J K
W
W ?�      �}  
U 
X
Y
X I  P W�|
Z
[
�| .prcskcodnull���    long
Z m   P Q�{�{ }
[ �z
\�y
�z 
faal
\ m   R S�x
�x eMdsKctl�y  
Y 
]
^
] I  X ]�w
_�v
�w .sysodelanull��� ��� nmbr
_ m   X Y
`
` ?�      �v  
^ 
a
b
a I  ^ c�u
c�t
�u .prcskcodnull���    long
c m   ^ _�s�s {�t  
b 
d
e
d I  d i�r
f�q
�r .sysodelanull��� ��� nmbr
f m   d e
g
g ?�      �q  
e 
h
i
h I  j o�p
j�o
�p .prcskcodnull���    long
j m   j k�n�n }�o  
i 
k
l
k I  p u�m
m�l
�m .sysodelanull��� ��� nmbr
m m   p q
n
n ?�      �l  
l 
o
p
o I  v �k
q
r
�k .prcskcodnull���    long
q m   v w�j�j 1
r �i
s�h
�i 
faal
s m   x {�g
�g eMdsKsft�h  
p 
t
u
t I  � ��f
v�e
�f .sysodelanull��� ��� nmbr
v m   � �
w
w ?�      �e  
u 
x
y
x I  � ��d
z
{
�d .prcskcodnull���    long
z m   � ��c�c 
{ �b
|�a
�b 
faal
| m   � ��`
�` eMdsKctl�a  
y 
}
~
} I  � ��_
�^
�_ .sysodelanull��� ��� nmbr
 m   � �
�
� ?�      �^  
~ 
�
�
� I  � ��]
��\
�] .prcskcodnull���    long
� m   � ��[�[ }�\  
� 
�
�
� I  � ��Z
��Y
�Z .sysodelanull��� ��� nmbr
� m   � �
�
� ?�      �Y  
� 
�
�
� I  � ��X
��W
�X .prcskcodnull���    long
� m   � ��V�V ~�W  
� 
�
�
� I  � ��U
��T
�U .sysodelanull��� ��� nmbr
� m   � �
�
� ?�ffffff�T  
� 
�
�
� I  � ��S
��R
�S .JonspClpnull���     ****
� l  � �
��Q�P
� c   � �
�
�
� o   � ��O�O 0 j  
� m   � ��N
�N 
ctxt�Q  �P  �R  
� 
�
�
� I  � ��M
��L
�M .sysodelanull��� ��� nmbr
� m   � �
�
� ?�      �L  
� 
�
�
� I  � ��K
�
�
�K .prcskcodnull���    long
� m   � ��J�J 	
� �I
��H
�I 
faal
� m   � ��G
�G eMdsKcmd�H  
� 
�
�
� I  � ��F
��E
�F .sysodelanull��� ��� nmbr
� m   � �
�
� ?�ffffff�E  
� 
�
�
� I  � ��D
��C
�D .prcskcodnull���    long
� m   � ��B�B 0�C  
� 
�
�
� I  � ��A
��@
�A .sysodelanull��� ��� nmbr
� m   � �
�
� ?�      �@  
� 
�
�
� I  � ��?
�
�
�? .prcskcodnull���    long
� m   � ��>�> 0
� �=
��<
�= 
faal
� m   � ��;
�; eMdsKsft�<  
� 
��:
� I  � ��9
��8
�9 .sysodelanull��� ��� nmbr
� m   � �
�
� ?�      �8  �:  �� 0 j  
N l  9 <
��7�6
� [   9 <
�
�
� o   9 :�5�5 0 	day_count  
� m   : ;�4�4 �7  �6  
O l  < ?
��3�2
� [   < ?
�
�
� o   < =�1�1 0 repeat_count  
� o   = >�0�0 0 	day_count  �3  �2  ��  ��  
E 4   / 3�/
�
�/ 
pcap
� m   1 2
�
� �
�
�  M i c r o s o f t   E x c e l
C m   + ,
�
��                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  
 
�
�
� l     �.�-�,�.  �-  �,  
� 
�
�
� i   ( +
�
�
� I      �+�*�)�+ 0 	addoneday 	addOneDay�*  �)  
� k     �
�
� 
�
�
� I    �(
��'
�( .miscactvnull��� ��� null
� m     
�
�                                                                                  XCEL   alis    �  Macintosh HD               �a�%H+   ��Microsoft Excel.app                                             ���v�	        ����  	                Microsoft Office 2008     �bu      �wY     ��     CMacintosh HD:Applications:Microsoft Office 2008:Microsoft Excel.app   (  M i c r o s o f t   E x c e l . a p p    M a c i n t o s h   H D  6Applications/Microsoft Office 2008/Microsoft Excel.app  / ��  �'  
� 
�
�
� O    �
�
�
� O   
 �
�
�
� k    �
�
� 
�
�
� I   �&
��%
�& .sysodelanull��� ��� nmbr
� m    
�
� ?�      �%  
� 
�
�
� I   �$
�
�
�$ .prcskprsnull���    utxt
� m    
�
� �
�
�  c
� �#
��"
�# 
faal
� m    �!
�! eMdsKcmd�"  
� 
�
�
� I   $� 
��
�  .sysodelanull��� ��� nmbr
� m     
�
� ?�      �  
� 
�
�
� r   % ,
�
�
� l  % *
���
� I  % *���
� .JonsgClp****    ��� null�  �  �  �  
� o      �� 0 list_num  
� 
�
�
� I  - 2�
��
� .sysodelanull��� ��� nmbr
� m   - .
�
� ?�      �  
� 
�
�
� I  3 8�
��
� .prcskcodnull���    long
� m   3 4�� 5�  
� 
�
�
� I  9 >�
��
� .sysodelanull��� ��� nmbr
� m   9 :
�
� ?�      �  
� 
��
� Y   ? �
��
�
��
� k   I �
�
� 
�
�
� I  I P�
�
�
� .prcskcodnull���    long
� m   I J�� }
� �
��
� 
faal
� m   K L�

�
 eMdsKctl�  
� 
�
�
� I  Q V�	
��
�	 .sysodelanull��� ��� nmbr
� m   Q R
�
� ?�      �  
� 
�
�
� r   W \
�
�
� l  W Z
���
� [   W Z
� 
� o   W X�� 0 list_num    m   X Y�� �  �  
� o      �� 0 list_num  
�  I  ] b��
� .sysodelanull��� ��� nmbr m   ] ^ ?�      �    I  c l� ��
�  .JonspClpnull���     **** c   c h	 o   c d���� 0 list_num  	 m   d g��
�� 
ctxt��   

 I  m t����
�� .sysodelanull��� ��� nmbr m   m p ?�ffffff��    I  u |����
�� .prcskcodnull���    long m   u x���� 3��    I  } �����
�� .sysodelanull��� ��� nmbr m   } � ?�ffffff��    I  � �����
�� .prcskprsnull���    utxt l  � ����� I  � �������
�� .JonsgClp****    ��� null��  ��  ��  ��  ��    I  � �����
�� .sysodelanull��� ��� nmbr m   � � ?�ffffff��    I  � �����
�� .prcskcodnull���    long m   � ����� 0��    !  I  � ���"��
�� .sysodelanull��� ��� nmbr" m   � �## ?�      ��  ! $%$ I  � ���&'
�� .prcskcodnull���    long& m   � ����� 0' ��(��
�� 
faal( m   � ���
�� eMdsKsft��  % )��) I  � ���*��
�� .sysodelanull��� ��� nmbr* m   � �++ ?�      ��  ��  � 0 k  
� m   B C���� 
� o   C D���� 0 repeat_count  �  �  
� 4   
 ��,
�� 
pcap, m    -- �..  M i c r o s o f t   E x c e l
� m    //�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  
� 0��0 l  � ���12��  1 ( "add 1 to every day starting at top   2 �33 D a d d   1   t o   e v e r y   d a y   s t a r t i n g   a t   t o p��  
� 4��4 i   , /565 I      ��7���� 0 makewordtable makeWordTable7 8��8 o      ���� 0 	row_count  ��  ��  6 k     699 :;: I    ��<��
�� .miscactvnull��� ��� null< m     ==                                                                                  MSWD   alis    �  Macintosh HD               �a�%H+   ��Microsoft Word.app                                              ���v�7        ����  	                Microsoft Office 2008     �bu      �w�     ��     BMacintosh HD:Applications:Microsoft Office 2008:Microsoft Word.app  &  M i c r o s o f t   W o r d . a p p    M a c i n t o s h   H D  5Applications/Microsoft Office 2008/Microsoft Word.app   / ��  ��  ; >��> O    6?@? O   
 5ABA U    4CDC k    /EE FGF I   ��H��
�� .sysodelanull��� ��� nmbrH m    II ?��Q����  G JKJ I   #��L��
�� .prcskcodnull���    longL m    ���� $��  K MNM I  $ )��O��
�� .sysodelanull��� ��� nmbrO m   $ %PP ?��Q����  N Q��Q I  * /��R��
�� .prcskcodnull���    longR m   * +���� {��  ��  D o    ���� 0 	row_count  B 4   
 ��S
�� 
pcapS m    TT �UU  M i c r o s o f t   W o r d@ m    VV�                                                                                  sevs   alis    �  Macintosh HD               �a�%H+     tSystem Events.app                                                ���        ����  	                CoreServices    �bu      ��C       t   0   /  :Macintosh HD:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c i n t o s h   H D  -System/Library/CoreServices/System Events.app   / ��  ��  ��       ��WXYZ[\]^_`abcd��  W ���������������������������� 0 test  ��  0 rearrangetimes rearrangeTimes�� 0 transition1  �� 0 prepare1  �� 0 prepare2  �� 0 makenewmonth makeNewMonth�� 0 	maketimes 	makeTimes�� 0 transfer_clean1  �� 0 transfer_clean2  �� *0 adddaynum_rearrange addDayNum_rearrange�� 0 	addoneday 	addOneDay�� 0 makewordtable makeWordTable
�� .aevtoappnull  �   � ****X �� �����ef���� 0 test  ��  ��  e  f  ��� ��� �
�� .miscactvnull��� ��� null
�� 
pcap�� �j O� *��/ hUUY �� �����gh����  0 rearrangetimes rearrangeTimes�� ��i�� i  ������ 0 repeat_count  �� 0 	day_count  ��  g ������������������������ 0 repeat_count  �� 0 	day_count  �� 0 	end_count  �� 0 complete  �� 0 act_num  �� 
0 found1  �� 0 sqmoved  �� 0 address  �� 0 tid  �� 0 	thesubstr 	theSubStr�� 0 movedata moveDatah 6������2������8����D����_����������������������������(�������������������������������~�
�� .miscactvnull��� ��� null
�� 
pcap
�� 
faal
�� eMdsKcmd
�� .prcskprsnull���    utxt
�� .sysodelanull��� ��� nmbr
�� .JonsgClp****    ��� null�� }
�� .prcskcodnull���    long�� 5
�� 
long�� |
�� 
TEXT
�� 
ascr
�� 
txdl
�� 
citm
�� 
ctxt�� ~�� {
�� eMdsKsft�� �� �� 	
�� eMdsKctl
�� 
mbar
�� 
mbri
�� 
menE
�� 
menI
�� .prcsclicuiel    ��� uiel
�� 
cwin
�� 
sgrp
�� 
rgrp
� 
radB
�~ 
butT����E�O�j O�
*��/jE�O���l O�j 
O*j E�O���jE�OjE�O mh�k �j O�j 
O���l O�j 
O*j E�O�j 
Oa j O�j 
O�ka &E�O�a   kE�Y hO�a   
lE�OY h[OY��O�a   Y hO�j O�j 
Oa j O�j 
Oa j O�j 
Oa ��l O�j 
O*j a &E�O_ a ,E�Oa _ a ,FO�a l/a &E�O�_ a ,FOeE�O�a  fE�Y hOa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O mkha �a  l Oa !j 
[OY��O  �kkha �a  l Oa !j 
[OY��Y hO�e Ea "��l O�j 
O a #kha j Oa !j 
[OY��O  �kkha �a  l Oa !j 
[OY��Oa $��a %lvl O�j 
O lkha j Oa !j 
[OY��O�j Oa !j 
O �kha �a  l Oa !j 
[OY��O mkha �a  l Oa !j 
[OY��O*a &k/a 'a (/a )k/a *a +/j ,O�j 
O*a -a ./a /k/a 0k/a 1a 2/j ,O*a -a 3/a 4a 5/j ,O mkha j Oa !j 
[OY��Y hOfE�OPUUOPZ �}��|�{jk�z�} 0 transition1  �|  �{  j  k �y�x�w�v�u�t�s�r�q�p�o�n�m�l�kQ�j�i�h�g�f��e
�y .miscactvnull��� ��� null
�x 
prcs�w 1
�v 
faal
�u eMdsKctl
�t .prcskcodnull���    long
�s .sysodelanull��� ��� nmbr�r 
�q eMdsKcmd
�p 
cwin
�o 
tabg
�n 
sgrp
�m .miscslctuiel       uiel�l �k 0
�j .prcskprsnull���    utxt�i $�h ~�g �f |�e {�z��j O��*��/����l O�j 
O���l O�j 
O�j 
O*�k/�k/�k/j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
O a kh�j 
Oa j [OY��O���l O�j 
O���l O�j 
O�j 
O*�k/�k/�k/j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
Oa j O�j 
O a kh�j 
Oa j [OY��OPUUOP[ �d�c�blm�a�d 0 prepare1  �c  �b  l  m �`(�_&�^�]�\�[�Z
�` .miscactvnull��� ��� null
�_ 
pcap
�^ .sysodelanull��� ��� nmbr�] y
�\ 
faal
�[ eMdsKctl
�Z .prcskcodnull���    long�a '�j O� *��/ �j O���l 
O�j UU\ �Y,�X�Wno�V�Y 0 prepare2  �X  �W  n  o 1�UG�TE;�S�R�Q�P�O
�U .miscactvnull��� ��� null
�T 
pcap
�S .sysodelanull��� ��� nmbr�R t
�Q 
faal
�P eMdsKctl
�O .prcskcodnull���    long�V '�j O� *��/ �j O���l 
O�j UU] �NK�M�Lpq�K�N 0 makenewmonth makeNewMonth�M �Jr�J r  �I�H�I 0 month_count  �H 0 	day_count  �L  p �G�F�E�D�C�G 0 month_count  �F 0 	day_count  �E 0 i  �D 0 day_num  �C 0 repeat_count  q T�B~�A|_�@�?�>�=�<�;�:�9��8�7�6�5�4�3�2�1��0��'�/�.
�B .miscactvnull��� ��� null
�A 
pcap
�@ .sysodelanull��� ��� nmbr�? s
�> 
faal
�= eMdsKctl
�< .prcskcodnull���    long�; 	�: 0�9 }
�8 eMdsKcmd
�7 .prcskprsnull���    utxt
�6 
rtyp
�5 
long
�4 .JonsgClp****    ��� null�3 5�2 ~�1 {
�0 eMdsKsft�/ �. u�K �j O��*��/��j O���l 
O�j O �kh�j 
O�j [OY��O k�kh �j 
O�j [OY��O���l O�j O*a a l E�O�j O�E�O�j O��E�O�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j O�j 
O�j Oa ��l O�j O l�kh ��a l 
O�j [OY��Oa ��l Oa j Oa ��l 
O�j O�j 
O�j O���a lvl 
O�j Oa ��l O�j O���l 
O�j O�j 
O�j Oa ���lvl O�j Oa j 
O�j O���l 
O�j O a kh�j 
O�j [OY��O�j O�j 
O�j O�j 
O�j O���a lvl 
O�j Oa j 
O�j O���l 
O�j UUO��lv^ �-��,�+st�*�- 0 	maketimes 	makeTimes�, �)u�) u  �(�'�( 0 repeat_count  �' 0 	day_count  �+  s �&�%�$�#�"�!� ��& 0 repeat_count  �% 0 	day_count  �$ 0 x  �# 0 j  �" 0 list_num  �! 0 i  �  0 top_time  � 0 done  t +��b�`�������������������<�Y����)[���
���	��
� .miscactvnull��� ��� null
� 
pcap
� .sysodelanull��� ��� nmbr� s
� 
faal
� eMdsKctl
� .prcskcodnull���    long� }
� eMdsKcmd
� .prcskprsnull���    utxt
� 
rtyp
� 
long
� .JonsgClp****    ��� null� 5� |� ~�  � 0� {
� 
ctxt
�
 eMdsKsft�	 y� 	� t�*��k�kh �j O��*��/��j O���l 
O�j O k�kh �j O�j 
[OY��O�j O���l O�j O*�a l E�O�j Oa j 
O�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j O k�kh �j O���l 
[OY��O�j Oa j 
O 1kmkh �j Oa ��l 
O�j Oa j 
O�j [OY��O�j Oa j 
O�j Oa ��l O�j O*�a l E�O�j Oa j 
O*j a ��j Oa j 
O�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j Oa j 
O�j Oa ��l O�j O*�a l E�O�j Oa j 
O*j a K�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j Oa ��l O�j O*�a l E�O�j Oa j 
O*j a ��j Oa ��l 
O�j Oa j 
O�j Oa j 
O�j Oa ��l O�j O*�a l E�O�j Oa j 
O*j a  q�j Oa j 
O�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j Oa j 
O*j a !�j Oa j 
O�j Oa j 
O�j Oa ��l 
O�j Oa j 
O�j Oa j 
O�j Oa "��l O�j O*�a l E�O�j Oa j 
O*j a # �jE�O �h�k �j Oa ��l 
O�j Oa j 
O�j Oa �a $l 
O�j Oa %��l O�j O*�a l E�O�j Oa j 
O�j O*j a & kE�Y h[OY��Y hY hY hY hY hY hO�j O���a $lvl 
O�j Oa �a $l 
O�j Oa '��l O�j Oa (��l 
O�j Oa )���lvl 
O�j O���l 
O�j O�j 
O�j O�j 
O�j Oa *��l 
UU[OY�NOP_ �j��vw�� 0 transfer_clean1  �  �  v  w o�	�	� ������~���������������������������
� .miscactvnull��� ��� null
� 
pcap�  s
�� 
faal
�� eMdsKctl
�� .prcskcodnull���    long
�� .sysodelanull��� ��� nmbr�� }�� |�� 1�� "
�� eMdsKsft�� {�� 
�� eMdsKcmd�� y�� 	�� 5�� ~�0�j O�&*��/���l O�j 
O�j O�j 
O�j O�j 
O�j O�j 
O���l O�j 
O���l O�j 
O�j O�j 
O�j O�j 
O����lvl O�j 
Oa ��l O�j 
Oa ��l O�j 
Oa ��l O�j 
Oa �a l O�j 
Oa ��l Oa j 
Oa �a l Okj 
Oa j O�j 
Oa j O�j 
O�j O�j 
O�j O�j 
O�j O�j 
UU` ��	!����xy���� 0 transfer_clean2  ��  ��  x  y 	&��
��
����	8������������������������
�� .miscactvnull��� ��� null
�� 
pcap�� |
�� .prcskcodnull���    long
�� .sysodelanull��� ��� nmbr�� t
�� 
faal
�� eMdsKctl�� $�� s�� 1
�� eMdsKsft�� {�� ~�� }�� u��y�j O�m*��/e mkh�j O�j [OY��O���l O�j O�j O�j O���l O�j O�j O�j O�j O�j O���l O�j Ol���lvl O�j Oa j O�j O���l O�j Ol���lvl O�j Oa j O�j Oa j O�j Oa ���lvl O�j O���l O�j Oa j O�j Oa j O�j Oa j O�j O���l O�j O�j O�j Oa j O�j Oa ���lvl O�j Oa j O�j Oa j O�j OPUUOPa ��
����z{���� *0 adddaynum_rearrange addDayNum_rearrange�� ��|�� |  ������ 0 repeat_count  �� 0 	day_count  ��  z �������� 0 repeat_count  �� 0 	day_count  �� 0 j  { 
"��
7��
5
-������
�������������������
�����������
�� .miscactvnull��� ��� null
�� 
pcap
�� .sysodelanull��� ��� nmbr�� 5
�� .prcskcodnull���    long�� |�� }
�� 
faal
�� eMdsKctl�� {�� 1
�� eMdsKsft�� �� ~
�� 
ctxt
�� .JonspClpnull���     ****�� 	
�� eMdsKcmd�� 0�� ��j O� *��/ �j O�j O�j UUO�j O� �*��/ � ák��kh �j O�j O���l O�j O�j O�j O�j O�j O��a l O�j Oa ��l O�j O�j O�j Oa j Oa j O�a &j O�j Oa �a l Oa j Oa j O�j Oa �a l O�j [OY�IUUb ��
�����}~���� 0 	addoneday 	addOneDay��  ��  } �������� 0 list_num  �� 0 repeat_count  �� 0 k  ~ 
���/��-
���
���������������������������
�� .miscactvnull��� ��� null
�� 
pcap
�� .sysodelanull��� ��� nmbr
�� 
faal
�� eMdsKcmd
�� .prcskprsnull���    utxt
�� .JonsgClp****    ��� null�� 5
�� .prcskcodnull���    long�� }
�� eMdsKctl
�� 
ctxt
�� .JonspClpnull���     ****�� 3�� 0
�� eMdsKsft�� ��j O� �*��/ ��j O���l 
O�j O*j E�O�j O�j O�j O {l�kh ���l O�j O�kE�O�j O�a &j Oa j Oa j Oa j O*j j 
Oa j Oa j O�j Oa �a l O�j [OY��UUOPc ��6��������� 0 makewordtable makeWordTable�� ����� �  ���� 0 	row_count  ��   ���� 0 	row_count  � 
=��V��TI��������
�� .miscactvnull��� ��� null
�� 
pcap
�� .sysodelanull��� ��� nmbr�� $
�� .prcskcodnull���    long�� {�� 7�j O� -*��/ % "�kh�j O�j O�j O�j [OY��UUd �����������
�� .aevtoappnull  �   � ****� k     (��  /��  4��  9��  >��  H����  ��  ��  � ���� 0 	month_num  � ���������������� 0 month_count  �� 0 	month_num  �� �� 0 repeat_count  ��O�� 0 	day_count  ��  0 rearrangetimes rearrangeTimes�� )kE�OkE�O�E�O�E�O k�kh  *��l+ OP[OY��ascr  ��ޭ