FasdUAS 1.101.10   ��   ��    k             l     ����  I    �� ��
�� .miscactvnull��� ��� null  m      	 	�                                                                                  sfri   alis    :  MacOSX                     ȡhH+     �
Safari.app                                                      ���u3�        ����  	                Applications    ȡ�N      �uz?       �  MacOSX:Applications:Safari.app   
 S a f a r i . a p p    M a c O S X  Applications/Safari.app   / ��  ��  ��  ��     
  
 l     ��������  ��  ��        l     ��  ��     openWestlaw()     �    o p e n W e s t l a w ( )      l     ��  ��     gotoStart()     �    g o t o S t a r t ( )      l     ��������  ��  ��        l     ��������  ��  ��        l     ��������  ��  ��        l      ��  ��   tell application "Safari"	delay 1
	--before submit, get url
		--if url still same, wait
		--if url different, then do readyState check	repeat until ((do JavaScript "document.readyState" in document 1) is "complete")		delay 0.25	end repeat	display dialog "ready"end tell     �    *  t e l l   a p p l i c a t i o n   " S a f a r i "  	 d e l a y   1 
 	 - - b e f o r e   s u b m i t ,   g e t   u r l 
 	 	 - - i f   u r l   s t i l l   s a m e ,   w a i t 
 	 	 - - i f   u r l   d i f f e r e n t ,   t h e n   d o   r e a d y S t a t e   c h e c k  	 r e p e a t   u n t i l   ( ( d o   J a v a S c r i p t   " d o c u m e n t . r e a d y S t a t e "   i n   d o c u m e n t   1 )   i s   " c o m p l e t e " )  	 	 d e l a y   0 . 2 5  	 e n d   r e p e a t  	 d i s p l a y   d i a l o g   " r e a d y "  e n d   t e l l    ! " ! l     ��������  ��  ��   "  # $ # l     ��������  ��  ��   $  % & % l     ��������  ��  ��   &  ' ( ' l      �� ) *��   ) � �tell application "Safari"	tell document 1		set jav to "document.getElementById('mLayout_ctl00_mTocTree_ctl00_mContentRegion').innerHTML;"		do JavaScript jav	end tellend tell
    * � + +h  t e l l   a p p l i c a t i o n   " S a f a r i "  	 t e l l   d o c u m e n t   1  	 	 s e t   j a v   t o   " d o c u m e n t . g e t E l e m e n t B y I d ( ' m L a y o u t _ c t l 0 0 _ m T o c T r e e _ c t l 0 0 _ m C o n t e n t R e g i o n ' ) . i n n e r H T M L ; "  	 	 d o   J a v a S c r i p t   j a v  	 e n d   t e l l  e n d   t e l l 
 (  , - , l     ��������  ��  ��   -  . / . i      0 1 0 I      �������� 0 openwestlaw openWestlaw��  ��   1 O      2 3 2 O     4 5 4 r     6 7 6 K     8 8 �� 9��
�� 
pURL 9 m     : : � ; ; , h t t p : / / w w w . w e s t l a w . c o m��   7 n       < = < 1    ��
�� 
pALL = 4    �� >
�� 
bTab > m    ����  5 4    �� ?
�� 
cwin ? m    ����  3 m      @ @�                                                                                  sfri   alis    :  MacOSX                     ȡhH+     �
Safari.app                                                      ���u3�        ����  	                Applications    ȡ�N      �uz?       �  MacOSX:Applications:Safari.app   
 S a f a r i . a p p    M a c O S X  Applications/Safari.app   / ��   /  A B A l     ��������  ��  ��   B  C�� C i     D E D I      �������� 0 	gotostart 	gotoStart��  ��   E O      F G F O     H I H k     J J  K L K r     M N M m     O O � P P h t t p : / / w e b 2 . w e s t l a w . c o m / t o c / d e f a u l t . w l ? p b c = 4 B F 3 F C B E & s c d b = P A T L A W F & s e r v i c e = T O C & a c t i o n = C o l l a p s e T r e e & f n = _ t o p & s v = S p l i t & i t e m k e y = I 9 7 5 d c 1 e 0 e a 3 5 1 1 d 8 9 7 0 f f c 4 1 8 8 1 6 5 5 9 b & i f m = N o t S e t & a p = I 9 7 5 d c 1 e 0 e a 3 5 1 1 d 8 9 7 0 f f c 4 1 8 8 1 6 5 5 9 b & a b b r = P A T L A W F & r s = W L W 1 0 . 0 8 & v r = 2 . 0 & r p = / t o c / d e f a u l t . w l & m t = 4 4 N o      ���� 0 gotourl gotoUrl L  Q�� Q r     R S R K     T T �� U��
�� 
pURL U o    ���� 0 gotourl gotoUrl��   S n       V W V 1    ��
�� 
pALL W 4    �� X
�� 
bTab X m    ���� ��   I 4    �� Y
�� 
cwin Y m    ����  G m      Z Z�                                                                                  sfri   alis    :  MacOSX                     ȡhH+     �
Safari.app                                                      ���u3�        ����  	                Applications    ȡ�N      �uz?       �  MacOSX:Applications:Safari.app   
 S a f a r i . a p p    M a c O S X  Applications/Safari.app   / ��  ��       �� [ \ ] ^��   [ �������� 0 openwestlaw openWestlaw�� 0 	gotostart 	gotoStart
�� .aevtoappnull  �   � **** \ �� 1���� _ `���� 0 openwestlaw openWestlaw��  ��   _   `  @���� :����
�� 
cwin
�� 
pURL
�� 
bTab
�� 
pALL�� � *�k/ ��l*�k/�,FUU ] �� E���� a b���� 0 	gotostart 	gotoStart��  ��   a ���� 0 gotourl gotoUrl b  Z�� O������
�� 
cwin
�� 
pURL
�� 
bTab
�� 
pALL�� � *�k/ �E�O�l*�k/�,FUU ^ �� c���� d e��
�� .aevtoappnull  �   � **** c k      f f  ����  ��  ��   d   e  	��
�� .miscactvnull��� ��� null�� �j ascr  ��ޭ