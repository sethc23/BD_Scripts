FasdUAS 1.101.10   ��   ��    k             l     ��  ��    # say "Kind of a pain, I know."     � 	 	 : s a y   " K i n d   o f   a   p a i n ,   I   k n o w . "   
  
 l      ��  ��   MGtell application "Microsoft Word"	activate		set findRange to find object of selection	clear formatting findRange -- clear any previous formatting used in a find operation	set forward of findRange to true -- find forward	set style of findRange to "List Bullet" -- the style to look for		tell findRange		set gotIt to execute find find text "" -- do the search w/o matching any text	end tell		if gotIt is true then -- if a match was found		copy object selection -- copy it to the clipboard		set mySelection to (the clipboard) -- then put clipboard into a variable		set myOffset to �			(get selection information selection information type �				(horizontal position relative to page)) -- now put selection info into a variable				display dialog mySelection & return & (myOffset as text) -- then display it	end ifend tell
     �  �  t e l l   a p p l i c a t i o n   " M i c r o s o f t   W o r d "  	 a c t i v a t e  	  	 s e t   f i n d R a n g e   t o   f i n d   o b j e c t   o f   s e l e c t i o n  	 c l e a r   f o r m a t t i n g   f i n d R a n g e   - -   c l e a r   a n y   p r e v i o u s   f o r m a t t i n g   u s e d   i n   a   f i n d   o p e r a t i o n  	 s e t   f o r w a r d   o f   f i n d R a n g e   t o   t r u e   - -   f i n d   f o r w a r d  	 s e t   s t y l e   o f   f i n d R a n g e   t o   " L i s t   B u l l e t "   - -   t h e   s t y l e   t o   l o o k   f o r  	  	 t e l l   f i n d R a n g e  	 	 s e t   g o t I t   t o   e x e c u t e   f i n d   f i n d   t e x t   " "   - -   d o   t h e   s e a r c h   w / o   m a t c h i n g   a n y   t e x t  	 e n d   t e l l  	  	 i f   g o t I t   i s   t r u e   t h e n   - -   i f   a   m a t c h   w a s   f o u n d  	 	 c o p y   o b j e c t   s e l e c t i o n   - -   c o p y   i t   t o   t h e   c l i p b o a r d  	 	 s e t   m y S e l e c t i o n   t o   ( t h e   c l i p b o a r d )   - -   t h e n   p u t   c l i p b o a r d   i n t o   a   v a r i a b l e  	 	 s e t   m y O f f s e t   t o   �  	 	 	 ( g e t   s e l e c t i o n   i n f o r m a t i o n   s e l e c t i o n   i n f o r m a t i o n   t y p e   �  	 	 	 	 ( h o r i z o n t a l   p o s i t i o n   r e l a t i v e   t o   p a g e ) )   - -   n o w   p u t   s e l e c t i o n   i n f o   i n t o   a   v a r i a b l e  	 	  	 	 d i s p l a y   d i a l o g   m y S e l e c t i o n   &   r e t u r n   &   ( m y O f f s e t   a s   t e x t )   - -   t h e n   d i s p l a y   i t  	 e n d   i f  e n d   t e l l 
      l     ��������  ��  ��        l    � ����  O     �    k    �       I   	������
�� .miscactvnull��� ��� null��  ��        r   
     n   
     m    ��
�� 
WSoj  1   
 ��
�� 
sele  o      ���� 0 	textrange 	textRange       r     ! " ! n     # $ # 1    ��
�� 
1650 $ 1    ��
�� 
sele " o      ���� 0 x      % & % r      ' ( ' n     ) * ) 4    �� +
�� 
cpar + m    ����  * o    ���� 0 x   ( o      ���� 0 mywords myWords &  , - , l  ! !�� . /��   . &  set  selection object to myWords    / � 0 0 @ s e t     s e l e c t i o n   o b j e c t   t o   m y W o r d s -  1 2 1 r   ! ( 3 4 3 n   ! & 5 6 5 1   $ &��
�� 
1650 6 1   ! $��
�� 
sele 4 o      ���� 0 l   2  7 8 7 r   ) 0 9 : 9 n   ) . ; < ; 1   , .��
�� 
wFnO < 1   ) ,��
�� 
sele : o      ���� 0 y   8  = > = r   1 6 ? @ ? n   1 4 A B A 1   2 4��
�� 
pALL B o   1 2���� 0 y   @ o      ���� 0 z   >  C D C r   7 @ E F E n   7 < G H G 2  : <��
�� 
cwor H 1   7 :��
�� 
sele F o      ���� 0 j   D  I J I r   A N K L K n   A J M N M m   F J��
�� 
w137 N n   A F O P O 2   D F��
�� 
cwor P o   A D���� 0 j   L o      ���� 0 k   J  Q R Q l  O O�� S T��   S  ---get tab position    T � U U & - - - g e t   t a b   p o s i t i o n R  V W V I  O \�� X Y
�� .sWRDWgRiutxt      7 WSoj X 1   O R��
�� 
sele Y �� Z��
�� 
wIfT Z m   U X��
�� e266� ��   W  [ \ [ l  ] ]��������  ��  ��   \  ] ^ ] l  ] ]�� _ `��   _ 	 ---    ` � a a  - - - ^  b c b l  ] ]��������  ��  ��   c  d e d l  ] ]��������  ��  ��   e  f g f l  ] ]�� h i��   h  set y to paragraph 1 of x    i � j j 2 s e t   y   t o   p a r a g r a p h   1   o f   x g  k l k l  ] ]�� m n��   m ! get properties of selection    n � o o 6 g e t   p r o p e r t i e s   o f   s e l e c t i o n l  p q p l  ] ]�� r s��   r ' !set x to font object of selection    s � t t B s e t   x   t o   f o n t   o b j e c t   o f   s e l e c t i o n q  u v u l  ] ]�� w x��   w  set y to properties of x    x � y y 0 s e t   y   t o   p r o p e r t i e s   o f   x v  z { z l   ] ]�� | }��   |��	tell text object of document 1		set active line of line numbering of page setup of it to true		set restart mode of line numbering of page setup of it �			to restart continuous		set {r, a} to {active line, restart mode} of line numbering �			of page setup of it		--> {true, restart continuous}		--set lineNum to get selection information (text object of paragraph 1)			end tell
	    } � ~ ~
  	 t e l l   t e x t   o b j e c t   o f   d o c u m e n t   1  	 	 s e t   a c t i v e   l i n e   o f   l i n e   n u m b e r i n g   o f   p a g e   s e t u p   o f   i t   t o   t r u e  	 	 s e t   r e s t a r t   m o d e   o f   l i n e   n u m b e r i n g   o f   p a g e   s e t u p   o f   i t   �  	 	 	 t o   r e s t a r t   c o n t i n u o u s  	 	 s e t   { r ,   a }   t o   { a c t i v e   l i n e ,   r e s t a r t   m o d e }   o f   l i n e   n u m b e r i n g   �  	 	 	 o f   p a g e   s e t u p   o f   i t  	 	 - - >   { t r u e ,   r e s t a r t   c o n t i n u o u s }  	 	 - - s e t   l i n e N u m   t o   g e t   s e l e c t i o n   i n f o r m a t i o n   ( t e x t   o b j e c t   o f   p a r a g r a p h   1 )  	 	  	 e n d   t e l l 
 	 {   �  l  ] ]��������  ��  ��   �  � � � l  ] ]�� � ���   � ' !set x to paragraph 1 of textRange    � � � � B s e t   x   t o   p a r a g r a p h   1   o f   t e x t R a n g e �  � � � l  ] ]�� � ���   �  get text range of x    � � � � & g e t   t e x t   r a n g e   o f   x �  � � � l  ] ]�� � ���   �  (*    � � � �  ( * �  � � � l  ] ]�� � ���   � &  set myWords to paragraph 11 of x    � � � � @ s e t   m y W o r d s   t o   p a r a g r a p h   1 1   o f   x �  � � � l  ] ]�� � ���   � ? 9> {"The", "time", "has", "come", "the", "walrus", "said"}    � � � � r >   { " T h e " ,   " t i m e " ,   " h a s " ,   " c o m e " ,   " t h e " ,   " w a l r u s " ,   " s a i d " } �  � � � l  ] ]�� � ���   � - ' Now coerce that list back to a string:    � � � � N   N o w   c o e r c e   t h a t   l i s t   b a c k   t o   a   s t r i n g : �  � � � l  ] ]�� � ���   � 9 3myWords as string --> "Thetimehascomethewalrussaid"    � � � � f m y W o r d s   a s   s t r i n g   - - >   " T h e t i m e h a s c o m e t h e w a l r u s s a i d " �  � � � l  ] ]�� � ���   � M G That is squished together because no text "" is put between the items.    � � � � �   T h a t   i s   s q u i s h e d   t o g e t h e r   b e c a u s e   n o   t e x t   " "   i s   p u t   b e t w e e n   t h e   i t e m s . �  � � � l  ] ]�� � ���   � G A but if we set the AppleScript's text item delimiters to space...    � � � � �   b u t   i f   w e   s e t   t h e   A p p l e S c r i p t ' s   t e x t   i t e m   d e l i m i t e r s   t o   s p a c e . . . �  � � � r   ] h � � � 1   ] `��
�� 
tab  � n      � � � 1   c g��
�� 
txdl � 1   ` c��
�� 
ascr �  � � � r   i r � � � c   i n � � � o   i j���� 0 mywords myWords � m   j m��
�� 
TEXT � o      ���� 0 mw MW �  � � � l  s ~ � � � � r   s ~ � � � m   s v � � � � �   � n      � � � 1   y }��
�� 
txdl � 1   v y��
�� 
ascr �   ALWAYS SET THEM BACK    � � � � *   A L W A Y S   S E T   T H E M   B A C K �  � � � l   � � � � � I   ��� ���
�� .sysodlogaskr        TEXT � o    ����� 0 mw MW��   � + %> "The time has come the walrus said"    � � � � J >   " T h e   t i m e   h a s   c o m e   t h e   w a l r u s   s a i d " �  � � � l  � ��� � ���   �  *)    � � � �  * ) �  � � � l  � ��� � ���   � - 'set x to range information of textRange    � � � � N s e t   x   t o   r a n g e   i n f o r m a t i o n   o f   t e x t R a n g e �  � � � l  � ��� � ���   � ) #get selection information selection    � � � � F g e t   s e l e c t i o n   i n f o r m a t i o n   s e l e c t i o n �  � � � l  � ��� � ���   �  tell selection    � � � �  t e l l   s e l e c t i o n �  � � � l  � ��� � ���   �  get selection information    � � � � 2 g e t   s e l e c t i o n   i n f o r m a t i o n �  � � � l  � ��� � ���   � $ set x to selection of window 1    � � � � < s e t   x   t o   s e l e c t i o n   o f   w i n d o w   1 �  � � � l  � ��� � ���   � $ set y to selection object of x    � � � � < s e t   y   t o   s e l e c t i o n   o b j e c t   o f   x �  � � � l  � ��� � ���   �  end tell    � � � �  e n d   t e l l �  ��� � l  � ��� � ���   � $ get selection information of x    � � � � < g e t   s e l e c t i o n   i n f o r m a t i o n   o f   x��    m      � ��                                                                                  MSWD  alis    �  MacOSX                     ����H+   
hyMicrosoft Word.app                                              
�
Ț�        ����  	                Microsoft Office 2011     ��      Ț�R     
hy  4  <MacOSX:Applications:Microsoft Office 2011:Microsoft Word.app  &  M i c r o s o f t   W o r d . a p p    M a c O S X  5Applications/Microsoft Office 2011/Microsoft Word.app   / ��  ��  ��     � � � l     �� � ���   � &  tell application "System Events"    � � � � @ t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s " �  �  � l     ����   # tell process "Microsoft Word"    � : t e l l   p r o c e s s   " M i c r o s o f t   W o r d "   l     ����    	set x to  selection type    � 2 	 s e t   x   t o     s e l e c t i o n   t y p e 	
	 l     ����    end tell    �  e n d   t e l l
  l     ����    end tell    �  e n d   t e l l  l     ��������  ��  ��   �� l      ����  ��

read text,
	delay.append
	text.append
return delay,text


set to record,
say each line, using different delay for sentences, paragraphs, new lines varying levels of pauses.
stop recording
increase speed 50%
lower pitch 50%
export as MP3


select all
select all paragraphs
check indents
select indent


slow with decreasing indents
slow down with underline, bold, italic, all caps, larger than 12 font
slow down between at periods, commas, semicolons, colons, multiple dashes

    �� 
 
 r e a d   t e x t , 
 	 d e l a y . a p p e n d 
 	 t e x t . a p p e n d 
 r e t u r n   d e l a y , t e x t 
 
 
 s e t   t o   r e c o r d , 
 s a y   e a c h   l i n e ,   u s i n g   d i f f e r e n t   d e l a y   f o r   s e n t e n c e s ,   p a r a g r a p h s ,   n e w   l i n e s   v a r y i n g   l e v e l s   o f   p a u s e s . 
 s t o p   r e c o r d i n g 
 i n c r e a s e   s p e e d   5 0 % 
 l o w e r   p i t c h   5 0 % 
 e x p o r t   a s   M P 3 
 
 
 s e l e c t   a l l 
 s e l e c t   a l l   p a r a g r a p h s 
 c h e c k   i n d e n t s 
 s e l e c t   i n d e n t 
 
 
 s l o w   w i t h   d e c r e a s i n g   i n d e n t s 
 s l o w   d o w n   w i t h   u n d e r l i n e ,   b o l d ,   i t a l i c ,   a l l   c a p s ,   l a r g e r   t h a n   1 2   f o n t 
 s l o w   d o w n   b e t w e e n   a t   p e r i o d s ,   c o m m a s ,   s e m i c o l o n s ,   c o l o n s ,   m u l t i p l e   d a s h e s 
 
��       ����   ��
�� .aevtoappnull  �   � **** ��������
�� .aevtoappnull  �   � **** k     �  ����  ��  ��      �����������������������������������������~�}�|�{�z�y ��x
�� .miscactvnull��� ��� null
�� 
sele
�� 
WSoj�� 0 	textrange 	textRange
�� 
1650�� 0 x  
�� 
cpar�� �� 0 mywords myWords�� 0 l  
�� 
wFnO�� 0 y  
�� 
pALL�� 0 z  
�� 
cwor�� 0 j  
�� 
w137�� 0 k  
�� 
wIfT
� e266� 
�~ .sWRDWgRiutxt      7 WSoj
�} 
tab 
�| 
ascr
�{ 
txdl
�z 
TEXT�y 0 mw MW
�x .sysodlogaskr        TEXT�� �� �*j O*�,�,E�O*�,�,E�O���/E�O*�,�,E�O*�,�,E�O��,E�O*�,�-E` O_ �-a ,E` O*�,a a l O_ _ a ,FO�a &E` Oa _ a ,FO_ j OPU ascr  ��ޭ