FasdUAS 1.101.10   ��   ��    k             l     ��  ��    7 1activate application "KeyRemap4MacBook_statusbar"     � 	 	 b a c t i v a t e   a p p l i c a t i o n   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r "   
  
 l     ��  ��    5 /activate application "KeyRemap4MacBook_launchd"     �   ^ a c t i v a t e   a p p l i c a t i o n   " K e y R e m a p 4 M a c B o o k _ l a u n c h d "      l     ��  ��    &  tell application "System Events"     �   @ t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "      l     ��  ��    / )tell process "KeyRemap4MacBook_statusbar"     �   R t e l l   p r o c e s s   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r "      l     ��  ��     get properties     �    g e t   p r o p e r t i e s      l     ��   !��      end tell    ! � " "  e n d   t e l l   # $ # l     ��������  ��  ��   $  % & % l     �� ' (��   ' : 4get every attribute of menu bar item 1 of menu bar 1    ( � ) ) h g e t   e v e r y   a t t r i b u t e   o f   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1 &  * + * l     �� , -��   ,  tell process "Finder"    - � . . * t e l l   p r o c e s s   " F i n d e r " +  / 0 / l     �� 1 2��   1 B <get title of every item of menu bar 1 --item 1 of menu bar 1    2 � 3 3 x g e t   t i t l e   o f   e v e r y   i t e m   o f   m e n u   b a r   1   - - i t e m   1   o f   m e n u   b a r   1 0  4 5 4 l     �� 6 7��   6 < 6get every attribute of menu bar 1 item 1 of menu bar 1    7 � 8 8 l g e t   e v e r y   a t t r i b u t e   o f   m e n u   b a r   1   i t e m   1   o f   m e n u   b a r   1 5  9 : 9 l     �� ; <��   ;  end tell    < � = =  e n d   t e l l :  > ? > l     ��������  ��  ��   ?  @ A @ l     �� B C��   B  end tell    C � D D  e n d   t e l l A  E F E l     ��������  ��  ��   F  G H G l     �� I J��   I ] Wactivate "MacOSX:Library:org.pqrs:KeyRemap4MacBook:app:KeyRemap4MacBook_statusbar.app:"    J � K K � a c t i v a t e   " M a c O S X : L i b r a r y : o r g . p q r s : K e y R e m a p 4 M a c B o o k : a p p : K e y R e m a p 4 M a c B o o k _ s t a t u s b a r . a p p : " H  L M L l     ��������  ��  ��   M  N O N l     �� P Q��   P + %activate application "SystemUIServer"    Q � R R J a c t i v a t e   a p p l i c a t i o n   " S y s t e m U I S e r v e r " O  S T S l     �� U V��   U Z Tactivate "MacOSX:Library:org.pqrs:KeyRemap4MacBook:app:KeyRemap4MacBook_status.app:"    V � W W � a c t i v a t e   " M a c O S X : L i b r a r y : o r g . p q r s : K e y R e m a p 4 M a c B o o k : a p p : K e y R e m a p 4 M a c B o o k _ s t a t u s . a p p : " T  X Y X l      �� Z [��   Z��tell application "System Events"	get processes	tell process "KeyRemap4MacBook_launchd"		--	activate		get properties		--click		--	get actions		--	select		--click	end tell	activate "MacOSX:Library:org.pqrs:KeyRemap4MacBook:app:KeyRemap4MacBook_status.app:"	tell process "SystemUIServer"		--tell menu bar 1		--	click menu bar item 1		--end tell				-- insert GUI Scripting statements here		--get every attribute of menu bar item 1 of menu bar 1		--get every attribute of menu bar item 2 of menu bar 1		--click menu bar item 2 of menu bar 1		--get menu bar item 2 of menu bar 1		--get properties		--get value of attribute "AXChildren" of menu bar item 2 of menu bar 1		--set x to get every menu bar item of menu bar 1		--repeat with i from 1 to (count of items in x)		--get name of every menu bar item of every menu -- of menu bar item i of menu bar 1		--end repeat		--set menuBar to menu bar 1				--set x to menu bar item 1 of menu bar 1		--set y to every menu bar item of menu bar 1 --value of x		--set z to properties of item 1 of y		--tell item 1 of y		--get value of every attribute		--get properties		--end tell		--get every attribute of menu bar item 1 of x		--tell y		--repeat 3 times -- just handy for debugging		-- can only get menu items if menu dropped				--if not selected then click		--set namesOfMenuItems to name of menu items of menu 1		--display dialog namesOfMenuItems as string		--end repeat		--end tell		--get value of attribute "AXDescription" of menu bar item 7 of menu bar 1		--set menuBarItemsList to value of attribute "AXDescription" of menu bar items of menu bar		--log "|tBC"		--set theMenu to menuBar's menu bar item 2		--tell theMenu --the icon on menu bar		--	repeat 3 times -- just handy for debugging		--		-- can only get menu items if menu dropped		--		if not selected then click		--		set namesOfMenuItems to name of menu items of menu 1		--		display dialog namesOfMenuItems as string		--	end repeat		--end tell	end tellend tell
    [ � \ \�  t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 g e t   p r o c e s s e s  	 t e l l   p r o c e s s   " K e y R e m a p 4 M a c B o o k _ l a u n c h d "  	 	 - - 	 a c t i v a t e  	 	 g e t   p r o p e r t i e s  	 	 - - c l i c k  	 	 - - 	 g e t   a c t i o n s  	 	 - - 	 s e l e c t  	 	 - - c l i c k  	 e n d   t e l l  	 a c t i v a t e   " M a c O S X : L i b r a r y : o r g . p q r s : K e y R e m a p 4 M a c B o o k : a p p : K e y R e m a p 4 M a c B o o k _ s t a t u s . a p p : "  	 t e l l   p r o c e s s   " S y s t e m U I S e r v e r "  	 	 - - t e l l   m e n u   b a r   1  	 	 - - 	 c l i c k   m e n u   b a r   i t e m   1  	 	 - - e n d   t e l l  	 	  	 	 - -   i n s e r t   G U I   S c r i p t i n g   s t a t e m e n t s   h e r e  	 	 - - g e t   e v e r y   a t t r i b u t e   o f   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1  	 	 - - g e t   e v e r y   a t t r i b u t e   o f   m e n u   b a r   i t e m   2   o f   m e n u   b a r   1  	 	 - - c l i c k   m e n u   b a r   i t e m   2   o f   m e n u   b a r   1  	 	 - - g e t   m e n u   b a r   i t e m   2   o f   m e n u   b a r   1  	 	 - - g e t   p r o p e r t i e s  	 	 - - g e t   v a l u e   o f   a t t r i b u t e   " A X C h i l d r e n "   o f   m e n u   b a r   i t e m   2   o f   m e n u   b a r   1  	 	 - - s e t   x   t o   g e t   e v e r y   m e n u   b a r   i t e m   o f   m e n u   b a r   1  	 	 - - r e p e a t   w i t h   i   f r o m   1   t o   ( c o u n t   o f   i t e m s   i n   x )  	 	 - - g e t   n a m e   o f   e v e r y   m e n u   b a r   i t e m   o f   e v e r y   m e n u   - -   o f   m e n u   b a r   i t e m   i   o f   m e n u   b a r   1  	 	 - - e n d   r e p e a t  	 	 - - s e t   m e n u B a r   t o   m e n u   b a r   1  	 	  	 	 - - s e t   x   t o   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1  	 	 - - s e t   y   t o   e v e r y   m e n u   b a r   i t e m   o f   m e n u   b a r   1   - - v a l u e   o f   x  	 	 - - s e t   z   t o   p r o p e r t i e s   o f   i t e m   1   o f   y  	 	 - - t e l l   i t e m   1   o f   y  	 	 - - g e t   v a l u e   o f   e v e r y   a t t r i b u t e  	 	 - - g e t   p r o p e r t i e s  	 	 - - e n d   t e l l  	 	 - - g e t   e v e r y   a t t r i b u t e   o f   m e n u   b a r   i t e m   1   o f   x  	 	 - - t e l l   y  	 	 - - r e p e a t   3   t i m e s   - -   j u s t   h a n d y   f o r   d e b u g g i n g  	 	 - -   c a n   o n l y   g e t   m e n u   i t e m s   i f   m e n u   d r o p p e d  	 	  	 	 - - i f   n o t   s e l e c t e d   t h e n   c l i c k  	 	 - - s e t   n a m e s O f M e n u I t e m s   t o   n a m e   o f   m e n u   i t e m s   o f   m e n u   1  	 	 - - d i s p l a y   d i a l o g   n a m e s O f M e n u I t e m s   a s   s t r i n g  	 	 - - e n d   r e p e a t  	 	 - - e n d   t e l l  	 	 - - g e t   v a l u e   o f   a t t r i b u t e   " A X D e s c r i p t i o n "   o f   m e n u   b a r   i t e m   7   o f   m e n u   b a r   1  	 	 - - s e t   m e n u B a r I t e m s L i s t   t o   v a l u e   o f   a t t r i b u t e   " A X D e s c r i p t i o n "   o f   m e n u   b a r   i t e m s   o f   m e n u   b a r  	 	 - - l o g   " | t B C "  	 	 - - s e t   t h e M e n u   t o   m e n u B a r ' s   m e n u   b a r   i t e m   2  	 	 - - t e l l   t h e M e n u   - - t h e   i c o n   o n   m e n u   b a r  	 	 - - 	 r e p e a t   3   t i m e s   - -   j u s t   h a n d y   f o r   d e b u g g i n g  	 	 - - 	 	 - -   c a n   o n l y   g e t   m e n u   i t e m s   i f   m e n u   d r o p p e d  	 	 - - 	 	 i f   n o t   s e l e c t e d   t h e n   c l i c k  	 	 - - 	 	 s e t   n a m e s O f M e n u I t e m s   t o   n a m e   o f   m e n u   i t e m s   o f   m e n u   1  	 	 - - 	 	 d i s p l a y   d i a l o g   n a m e s O f M e n u I t e m s   a s   s t r i n g  	 	 - - 	 e n d   r e p e a t  	 	 - - e n d   t e l l  	 e n d   t e l l  e n d   t e l l 
 Y  ] ^ ] l     ��������  ��  ��   ^  _ ` _ l     a���� a I    �� b��
�� .sysodelanull��� ��� nmbr b m     ���� ��  ��  ��   `  c d c l     �� e f��   e 3 -tell application "KeyRemap4MacBook_statusbar"    f � g g Z t e l l   a p p l i c a t i o n   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r " d  h i h l     �� j k��   j  		activate    k � l l  	 a c t i v a t e i  m n m l     �� o p��   o  end tell    p � q q  e n d   t e l l n  r s r l     ��������  ��  ��   s  t u t l   # v���� v O    # w x w k   
 " y y  z { z l  
 
�� | }��   |  get every process    } � ~ ~ " g e t   e v e r y   p r o c e s s {   �  l  
 
�� � ���   � / )tell process "KeyRemap4MacBook_statusbar"    � � � � R t e l l   p r o c e s s   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r " �  � � � l  
 
�� � ���   �  get properties    � � � �  g e t   p r o p e r t i e s �  � � � l  
 
�� � ���   �  end tell    � � � �  e n d   t e l l �  � � � l  
 
��������  ��  ��   �  � � � l  
 
�� � ���   � R Lget value of attribute "AXFrontmost" of process "KeyRemap4MacBook_statusbar"    � � � � � g e t   v a l u e   o f   a t t r i b u t e   " A X F r o n t m o s t "   o f   p r o c e s s   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r " �  � � � l  
 
��������  ��  ��   �  � � � l  
 
��������  ��  ��   �  � � � O   
   � � � k     � �  � � � r     � � � 4   �� �
�� 
popB � m    ����  � o      ���� 0 	thebutton 	theButton �  � � � I   �� ���
�� .prcsclicuiel    ��� uiel � o    ���� 0 	thebutton 	theButton��   �  � � � l   �� � ���   � ( "set attribute "AXPress" to "press"    � � � � D s e t   a t t r i b u t e   " A X P r e s s "   t o   " p r e s s " �  � � � l   �� � ���   � 3 -get every attribute -- bar item of menu bar 1    � � � � Z g e t   e v e r y   a t t r i b u t e   - -   b a r   i t e m   o f   m e n u   b a r   1 �  � � � l   �� � ���   � " get value of every attribute    � � � � 8 g e t   v a l u e   o f   e v e r y   a t t r i b u t e �  � � � l   �� � ���   � / )click button "KeyRemap4MacBook_statusbar"    � � � � R c l i c k   b u t t o n   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r " �  � � � l   �� � ���   � , &set x to value of attribute "AXHidden"    � � � � L s e t   x   t o   v a l u e   o f   a t t r i b u t e   " A X H i d d e n " �  � � � l   �� � ���   �  set frontmost to true    � � � � * s e t   f r o n t m o s t   t o   t r u e �  � � � l   �� � ���   � D >click menu bar item "KeyRemap4MacBook_statusbar" of menu bar 1    � � � � | c l i c k   m e n u   b a r   i t e m   " K e y R e m a p 4 M a c B o o k _ s t a t u s b a r "   o f   m e n u   b a r   1 �  ��� � l   �� � ���   � &  keystroke "o" using command down    � � � � @ k e y s t r o k e   " o "   u s i n g   c o m m a n d   d o w n��   � 4   
 �� �
�� 
prcs � m     � � � � � 4 K e y R e m a p 4 M a c B o o k _ s t a t u s b a r �  � � � l  ! !��������  ��  ��   �  ��� � l   ! !�� � ���   ��{	tell process "KeyRemap4MacBook_launchd"		set frontmost to true		activate		get menu bar items of menu bar 1		control - (click menu bar item 1 of menu bar 1)		tell menu bar item "KeyRemap4MacBook_launchd" of menu bar 1			get actions			perform action "AXPress"		end tell		tell menu bar item 1 of menu bar 1 -- whose value of attribute "AXDescription" is "spaces menu extra")			--get actions			--perform action "AXPress"			--delay 0.2			--perform action "AXPress" of menu item favouriteSpace of menu 1		end tell		(*		get attributes		get value of every attribute		click menu bar item 1 of menu bar 1		select menu bar item 1 of menu bar 1		activate menu bar item 1 of menu bar 1		*)		--tell menu bar 1		--tell menu bar item 1		--tell menu 1		--tell menu item 1		--tell menu 1		--get menu bar		--end tell		--end tell		--end tell		--end tell		--end tell	end tell
	    � � � ��  	 t e l l   p r o c e s s   " K e y R e m a p 4 M a c B o o k _ l a u n c h d "  	 	 s e t   f r o n t m o s t   t o   t r u e  	 	 a c t i v a t e  	 	 g e t   m e n u   b a r   i t e m s   o f   m e n u   b a r   1  	 	 c o n t r o l   -   ( c l i c k   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1 )  	 	 t e l l   m e n u   b a r   i t e m   " K e y R e m a p 4 M a c B o o k _ l a u n c h d "   o f   m e n u   b a r   1  	 	 	 g e t   a c t i o n s  	 	 	 p e r f o r m   a c t i o n   " A X P r e s s "  	 	 e n d   t e l l  	 	 t e l l   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1   - -   w h o s e   v a l u e   o f   a t t r i b u t e   " A X D e s c r i p t i o n "   i s   " s p a c e s   m e n u   e x t r a " )  	 	 	 - - g e t   a c t i o n s  	 	 	 - - p e r f o r m   a c t i o n   " A X P r e s s "  	 	 	 - - d e l a y   0 . 2  	 	 	 - - p e r f o r m   a c t i o n   " A X P r e s s "   o f   m e n u   i t e m   f a v o u r i t e S p a c e   o f   m e n u   1  	 	 e n d   t e l l  	 	 ( *  	 	 g e t   a t t r i b u t e s  	 	 g e t   v a l u e   o f   e v e r y   a t t r i b u t e  	 	 c l i c k   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1  	 	 s e l e c t   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1  	 	 a c t i v a t e   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1  	 	 * )  	 	 - - t e l l   m e n u   b a r   1  	 	 - - t e l l   m e n u   b a r   i t e m   1  	 	 - - t e l l   m e n u   1  	 	 - - t e l l   m e n u   i t e m   1  	 	 - - t e l l   m e n u   1  	 	 - - g e t   m e n u   b a r  	 	 - - e n d   t e l l  	 	 - - e n d   t e l l  	 	 - - e n d   t e l l  	 	 - - e n d   t e l l  	 	 - - e n d   t e l l  	 e n d   t e l l 
 	��   x m     � ��                                                                                  sevs   alis    |  MacOSX                     ȡhH+     �System Events.app                                                ���        ����  	                CoreServices    ȡ�N      ��C       �   Q   P  4MacOSX:System:Library:CoreServices:System Events.app  $  S y s t e m   E v e n t s . a p p    M a c O S X  -System/Library/CoreServices/System Events.app   / ��  ��  ��   u  � � � l     �� � ���   �  get every UI element    � � � � ( g e t   e v e r y   U I   e l e m e n t �  � � � l     �� � ���   �  select UI element 14    � � � � ( s e l e c t   U I   e l e m e n t   1 4 �  � � � l     �� � ���   �  get UI elements enabled    � � � � . g e t   U I   e l e m e n t s   e n a b l e d �  � � � l      �� � ���   �;5tell application "System Events"	tell process "SystemUIServer"		tell menu bar item 1 of menu bar 1 -- whose value of attribute "AXDescription" is "spaces menu extra")			perform action "AXPress"			delay 0.2			--perform action "AXPress" of menu item favouriteSpace of menu 1		end tell	end tellend tell
    � � � �j  t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 t e l l   p r o c e s s   " S y s t e m U I S e r v e r "  	 	 t e l l   m e n u   b a r   i t e m   1   o f   m e n u   b a r   1   - -   w h o s e   v a l u e   o f   a t t r i b u t e   " A X D e s c r i p t i o n "   i s   " s p a c e s   m e n u   e x t r a " )  	 	 	 p e r f o r m   a c t i o n   " A X P r e s s "  	 	 	 d e l a y   0 . 2  	 	 	 - - p e r f o r m   a c t i o n   " A X P r e s s "   o f   m e n u   i t e m   f a v o u r i t e S p a c e   o f   m e n u   1  	 	 e n d   t e l l  	 e n d   t e l l  e n d   t e l l 
 �  � � � l     ��������  ��  ��   �  ��� � l      �� � ���   �lf
tell application "System Events"	tell application process "SystemUIServer"		get value of every menu bar item of menu bar 1
       tell (get first menu bar item of menu bar 1 whose value of attribute "AXDescription" is "text input menu extra")
           set currentKeyboard to its value
           perform action "AXPress"
		repeat until (menu 1 exists)
               delay 0.2
           end repeat
           set menuItems to name of menu items of menu 1
           repeat with i from 1 to (count menuItems)
               if (item i of menuItems is currentKeyboard) then
                   set n to i + 1
                   if (item n of menuItems is missing value) then set n to 1
                   perform action "AXPress" of (menu item n of menu 1)
                   exit repeat
               end if
           end repeat
       end tell	end tellend tell
    � � � �� 
 t e l l   a p p l i c a t i o n   " S y s t e m   E v e n t s "  	 t e l l   a p p l i c a t i o n   p r o c e s s   " S y s t e m U I S e r v e r "  	 	 g e t   v a l u e   o f   e v e r y   m e n u   b a r   i t e m   o f   m e n u   b a r   1 
               t e l l   ( g e t   f i r s t   m e n u   b a r   i t e m   o f   m e n u   b a r   1   w h o s e   v a l u e   o f   a t t r i b u t e   " A X D e s c r i p t i o n "   i s   " t e x t   i n p u t   m e n u   e x t r a " ) 
                       s e t   c u r r e n t K e y b o a r d   t o   i t s   v a l u e 
                       p e r f o r m   a c t i o n   " A X P r e s s " 
 	 	 r e p e a t   u n t i l   ( m e n u   1   e x i s t s ) 
                               d e l a y   0 . 2 
                       e n d   r e p e a t 
                       s e t   m e n u I t e m s   t o   n a m e   o f   m e n u   i t e m s   o f   m e n u   1 
                       r e p e a t   w i t h   i   f r o m   1   t o   ( c o u n t   m e n u I t e m s ) 
                               i f   ( i t e m   i   o f   m e n u I t e m s   i s   c u r r e n t K e y b o a r d )   t h e n 
                                       s e t   n   t o   i   +   1 
                                       i f   ( i t e m   n   o f   m e n u I t e m s   i s   m i s s i n g   v a l u e )   t h e n   s e t   n   t o   1 
                                       p e r f o r m   a c t i o n   " A X P r e s s "   o f   ( m e n u   i t e m   n   o f   m e n u   1 ) 
                                       e x i t   r e p e a t 
                               e n d   i f 
                       e n d   r e p e a t 
               e n d   t e l l  	 e n d   t e l l  e n d   t e l l 
��       �� � ���   � ��
�� .aevtoappnull  �   � **** � �� ����� � ���
�� .aevtoappnull  �   � **** � k     # � �  _ � �  t����  ��  ��   �   � �� ��� �������
�� .sysodelanull��� ��� nmbr
�� 
prcs
�� 
popB�� 0 	thebutton 	theButton
�� .prcsclicuiel    ��� uiel�� $mj  O� *��/ *�k/E�O�j OPUOPUascr  ��ޭ