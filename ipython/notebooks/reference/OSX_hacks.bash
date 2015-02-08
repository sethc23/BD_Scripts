#!/usr/bin/env bash

# ~/.osx — https://mths.be/osx

# Ask for the administrator password upfront
sudo -v

# Keep-alive: update existing `sudo` time stamp until `.osx` has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

# Set highlight color to green
defaults write NSGlobalDomain AppleHighlightColor -string "0.764700 0.976500 0.568600"
# Always show scrollbars
defaults write NSGlobalDomain AppleShowScrollBars -string "Always"
# Disable the “Are you sure you want to open this application?” dialog
defaults write com.apple.LaunchServices LSQuarantine -bool false
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint2 -bool true
defaults write com.apple.print.PrintingPrefs "Quit When Finished" -bool true
# Try e.g. `cd /tmp; unidecode "\x{0000}" > cc.txt; open -e cc.txt`
#echo "Displaying ASCII control characters using caret notation in standard text views"
#defaults write NSGlobalDomain NSTextShowsControlCharacters -bool true
echo "Save to disk, rather than iCloud, by default? (y/n)"
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false
echo "Reveal IP address, hostname, OS version, etc. when clicking the clock in the login window"
sudo defaults write /Library/Preferences/com.apple.loginwindow AdminHostInfo HostName
echo "Removing duplicates in the 'Open With' menu"
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
echo "Disable smart quotes and smart dashes? (y/n)"
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
###############################################################################
# General Power and Performance modifications
###############################################################################
echo "Disable the sudden motion sensor? (it's not useful for SSDs/current MacBooks) (y/n)"
echo "Disable system-wide resume? (y/n)"
defaults write com.apple.systempreferences NSQuitAlwaysKeepsWindows -bool false
echo "Speeding up wake from sleep to 24 hours from an hour"
# http://www.cultofmac.com/221392/quick-hack-speeds-up-retina-macbooks-wake-from-sleep-os-x-tips/
sudo pmset -a standbydelay 86400
# Never go into computer sleep mode
sudo systemsetup -setcomputersleep Off > /dev/null
################################################################################
# Trackpad, mouse, keyboard, Bluetooth accessories, and input
###############################################################################
echo "Increasing sound quality for Bluetooth headphones/headsets"
defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40
# Disable the sound effects on boot
sudo nvram SystemAudioVolume=" "
echo "Enabling full keyboard access for all controls (enable Tab in modal dialogs, menu windows, etc.)"
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3
echo "Disabling press-and-hold for special keys in favor of key repeat"
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false
echo "Setting a blazingly fast keyboard repeat rate"
defaults write NSGlobalDomain KeyRepeat -int 0
echo "Disable auto-correct? (y/n)"
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false
echo "Turn off keyboard illumination when computer is not used for 5 minutes"
defaults write com.apple.BezelServices kDimTime -int 300
echo "Disable display from automatically adjusting brightness? (y/n)"
sudo defaults write /Library/Preferences/com.apple.iokit.AmbientLightSensor "Automatic Display Enabled" -bool false
echo "Disable keyboard from automatically adjusting backlight brightness in low light? (y/n)"
sudo defaults write /Library/Preferences/com.apple.iokit.AmbientLightSensor "Automatic Keyboard Enabled" -bool false
# Stop iTunes from responding to the keyboard media keys
launchctl unload -w /System/Library/LaunchAgents/com.apple.rcd.plist 2> /dev/null
###############################################################################
# Screen
###############################################################################
#echo "Requiring password immediately after sleep or screen saver begins"
#defaults write com.apple.screensaver askForPassword -int 1
#defaults write com.apple.screensaver askForPasswordDelay -int 0
echo "Where do you want screenshots to be stored? (hit ENTER if you want ~/Desktop as default)"
# Thanks https://github.com/omgmog
defaults write com.apple.screencapture location -string "/Users/admin/Desktop"
echo "What format should screenshots be saved as? (hit ENTER for PNG, options: BMP, GIF, JPG, PDF, TIFF) "
defaults write com.apple.screencapture type -string "pdf"
echo "Enabling subpixel font rendering on non-Apple LCDs"
defaults write NSGlobalDomain AppleFontSmoothing -int 2
echo "Enabling HiDPI display modes (requires restart)"
sudo defaults write /Library/Preferences/com.apple.windowserver DisplayResolutionEnabled -bool true
# Disable shadow in screenshots
defaults write com.apple.screencapture disable-shadow -bool true
###############################################################################
# Finder
###############################################################################
# Disable automatic termination of inactive apps
defaults write NSGlobalDomain NSDisableAutomaticTermination -bool true
# Disable the crash reporter
defaults write com.apple.CrashReporter DialogType -string "none"
echo "Show icons for hard drives, servers, and removable media on the desktop? (y/n)"
defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool false
echo "Show hidden files in Finder by default? (y/n)"
defaults write com.apple.Finder AppleShowAllFiles -bool true
echo "Show dotfiles in Finder by default? (y/n)"
defaults write com.apple.finder AppleShowAllFiles TRUE
echo "Show all filename extensions in Finder by default? (y/n)"
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
echo "Show status bar in Finder by default? (y/n)"
defaults write com.apple.finder ShowStatusBar -bool true
# Finder: show path bar
defaults write com.apple.finder ShowPathbar -bool true
echo "Display full POSIX path as Finder window title? (y/n)"
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
echo "Disable the warning when changing a file extension? (y/n)"
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
# When performing a search, search the current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
echo "Use column view in all Finder windows by default? (y/n)"
defaults write com.apple.finder FXPreferredViewStyle Clmv
# Remove the spring loading delay for directories
defaults write NSGlobalDomain com.apple.springing.delay -float 0
echo "Avoid creation of .DS_Store files on network volumes? (y/n)"
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.frameworks.diskimages skip-verify -bool true
defaults write com.apple.frameworks.diskimages skip-verify-locked -bool true
defaults write com.apple.frameworks.diskimages skip-verify-remote -bool true
echo "Allowing text selection in Quick Look/Preview in Finder by default"
defaults write com.apple.finder QLEnableTextSelection -bool true
echo "Enabling snap-to-grid for icons on the desktop and in other icon views"
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :FK_StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
/usr/libexec/PlistBuddy -c "Set :StandardViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist
# Finder: disable window animations and Get Info animations
defaults write com.apple.finder DisableAllAnimations -bool true
# Expand the following File Info panes:
# “General”, “Open with”, and “Sharing & Permissions”
defaults write com.apple.finder FXInfoPanesExpanded -dict \
	General -bool true \
	OpenWith -bool true \
	Privileges -bool true
###############################################################################
# Dock & Mission Control
###############################################################################
echo "Setting the icon size of Dock items to 36 pixels for optimal size/screen-realestate"
defaults write com.apple.dock tilesize -int 36
echo "Speeding up Mission Control animations and grouping windows by application"
#defaults write com.apple.dock expose-animation-duration -float 0.1
#defaults write com.apple.dock "expose-group-by-app" -bool true
# Don’t animate opening applications from the Dock
defaults write com.apple.dock launchanim -bool false
echo "Set Dock to auto-hide and remove the auto-hiding delay? (y/n)"
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0
###############################################################################
# Chrome, Safari, & WebKit
###############################################################################
# Set Safari’s home page to `about:blank` for faster loading
defaults write com.apple.Safari HomePage -string "about:blank"
echo "Privacy: Don't send search queries to Apple"
defaults write com.apple.Safari UniversalSearchEnabled -bool false
defaults write com.apple.Safari SuppressSearchSuggestions -bool true
echo "Hiding Safari's bookmarks bar by default"
defaults write com.apple.Safari ShowFavoritesBar -bool false
echo "Hiding Safari's sidebar in Top Sites"
defaults write com.apple.Safari ShowSidebarInTopSites -bool false
echo "Disabling Safari's thumbnail cache for History and Top Sites"
defaults write com.apple.Safari DebugSnapshotsUpdatePolicy -int 2
echo "Enabling Safari's debug menu"
defaults write com.apple.Safari IncludeInternalDebugMenu -bool true
echo "Making Safari's search banners default to Contains instead of Starts With"
defaults write com.apple.Safari FindOnPageMatchesWordStartsOnly -bool false
echo "Removing useless icons from Safari's bookmarks bar"
defaults write com.apple.Safari ProxiesInBookmarksBar "()"
echo "Enabling the Develop menu and the Web Inspector in Safari"
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true
defaults write com.apple.Safari "com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled" -bool true
echo "Adding a context menu item for showing the Web Inspector in web views"
defaults write NSGlobalDomain WebKitDeveloperExtras -bool true
echo "Disabling the annoying backswipe in Chrome"
defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool false
defaults write com.google.Chrome.canary AppleEnableSwipeNavigateWithScrolls -bool false
echo "Using the system-native print preview dialog in Chrome"
defaults write com.google.Chrome DisablePrintPreview -bool true
defaults write com.google.Chrome.canary DisablePrintPreview -bool true
###############################################################################
# Mail
###############################################################################
# Disable send and reply animations in Mail.app
defaults write com.apple.mail DisableReplyAnimations -bool true
defaults write com.apple.mail DisableSendAnimations -bool true
echo "Setting email addresses to copy as 'foo@example.com' instead of 'Foo Bar <foo@example.com>' in Mail.app"
defaults write com.apple.mail AddressesIncludeNameOnPasteboard -bool false
# Display emails in threaded mode, sorted by date (oldest at the top)
defaults write com.apple.mail DraftsViewerAttributes -dict-add "DisplayInThreadedMode" -string "yes"
defaults write com.apple.mail DraftsViewerAttributes -dict-add "SortedAscending" -string "yes"
defaults write com.apple.mail DraftsViewerAttributes -dict-add "SortOrder" -string "received-date"
# Disable inline attachments (just show the icons)
defaults write com.apple.mail DisableInlineAttachmentViewing -bool true
###############################################################################
# Terminal
###############################################################################
echo "Enabling UTF-8 ONLY in Terminal.app and setting the Pro theme by default"
defaults write com.apple.terminal StringEncodings -array 4
defaults write com.apple.Terminal "Default Window Settings" -string "Pro"
defaults write com.apple.Terminal "Startup Window Settings" -string "Pro"
###############################################################################
# Time Machine
###############################################################################
echo "Prevent Time Machine from prompting to use new hard drives as backup volume? (y/n)"
defaults write com.apple.TimeMachine DoNotOfferNewDisksForBackup -bool true
echo "Disable local Time Machine backups? (This can take up a ton of SSD space on <128GB SSDs) (y/n)"
hash tmutil &> /dev/null && sudo tmutil disablelocal
###############################################################################
# Messages                                                                    #
###############################################################################
echo "Disable automatic emoji substitution in Messages.app? (i.e. use plain text smileys) (y/n)"
defaults write com.apple.messageshelper.MessageController SOInputLineSettings -dict-add "automaticEmojiSubstitutionEnablediMessage" -bool false
echo "Disable smart quotes in Messages.app? (it's annoying for messages that contain code) (y/n)"
defaults write com.apple.messageshelper.MessageController SOInputLineSettings -dict-add "automaticQuoteSubstitutionEnabled" -bool false
echo "Disable continuous spell checking in Messages.app? (y/n)"
defaults write com.apple.messageshelper.MessageController SOInputLineSettings -dict-add "continuousSpellCheckingEnabled" -bool false
echo "Note that some of these changes require a logout/restart to take effect." $red
echo "Killing some open applications in order to take effect." $red
find ~/Library/Application\ Support/Dock -name "*.db" -maxdepth 1 -delete
for app in "Activity Monitor" "Address Book" "Calendar" "Contacts" "cfprefsd" \
"Dock" "Finder" "Mail" "Messages" "Safari" "SystemUIServer" \
"Terminal" "Transmission"; do
killall "${app}" > /dev/null 2>&1
###############################################################################
# Spotlight                                                                   #
###############################################################################

# Hide Spotlight tray-icon (and subsequent helper)
#sudo chmod 600 /System/Library/CoreServices/Search.bundle/Contents/MacOS/Search
# Disable Spotlight indexing for any volume that gets mounted and has not yet
# been indexed before.
# Use `sudo mdutil -i off "/Volumes/foo"` to stop indexing any volume.
sudo defaults write /.Spotlight-V100/VolumeConfiguration Exclusions -array "/Volumes"
# Change indexing order and disable some search results
# Yosemite-specific search results (remove them if your are using OS X 10.9 or older):
# 	MENU_DEFINITION
# 	MENU_CONVERSION
# 	MENU_EXPRESSION
# 	MENU_SPOTLIGHT_SUGGESTIONS (send search queries to Apple)
# 	MENU_WEBSEARCH             (send search queries to Apple)
# 	MENU_OTHER
#defaults write com.apple.spotlight orderedItems -array \
#	'{"enabled" = 1;"name" = "APPLICATIONS";}' \
#	'{"enabled" = 1;"name" = "SYSTEM_PREFS";}' \
#	'{"enabled" = 1;"name" = "DIRECTORIES";}' \
#	'{"enabled" = 1;"name" = "PDF";}' \
#	'{"enabled" = 1;"name" = "FONTS";}' \
#	'{"enabled" = 0;"name" = "DOCUMENTS";}' \
#	'{"enabled" = 0;"name" = "MESSAGES";}' \
#	'{"enabled" = 0;"name" = "CONTACT";}' \
#	'{"enabled" = 0;"name" = "EVENT_TODO";}' \
#	'{"enabled" = 0;"name" = "IMAGES";}' \
#	'{"enabled" = 0;"name" = "BOOKMARKS";}' \
#	'{"enabled" = 0;"name" = "MUSIC";}' \
#	'{"enabled" = 0;"name" = "MOVIES";}' \
#	'{"enabled" = 0;"name" = "PRESENTATIONS";}' \
#	'{"enabled" = 0;"name" = "SPREADSHEETS";}' \
#	'{"enabled" = 0;"name" = "SOURCE";}' \
#	'{"enabled" = 0;"name" = "MENU_DEFINITION";}' \
#	'{"enabled" = 0;"name" = "MENU_OTHER";}' \
#	'{"enabled" = 0;"name" = "MENU_CONVERSION";}' \
#	'{"enabled" = 0;"name" = "MENU_EXPRESSION";}' \
#	'{"enabled" = 0;"name" = "MENU_WEBSEARCH";}' \
#	'{"enabled" = 0;"name" = "MENU_SPOTLIGHT_SUGGESTIONS";}'
# Load new settings before rebuilding the index
#killall mds > /dev/null 2>&1
# Make sure indexing is enabled for the main volume
#sudo mdutil -i on / > /dev/null
# Rebuild the index from scratch
#sudo mdutil -E / > /dev/null
###############################################################################
# Activity Monitor                                                            #
###############################################################################

# Show the main window when launching Activity Monitor
defaults write com.apple.ActivityMonitor OpenMainWindow -bool true

# Visualize CPU usage in the Activity Monitor Dock icon
defaults write com.apple.ActivityMonitor IconType -int 5

# Show all processes in Activity Monitor
defaults write com.apple.ActivityMonitor ShowCategory -int 0

# Sort Activity Monitor results by CPU usage
defaults write com.apple.ActivityMonitor SortColumn -string "CPUUsage"
defaults write com.apple.ActivityMonitor SortDirection -int 0
###############################################################################
# Address Book, Dashboard, iCal, TextEdit, and Disk Utility                   #
###############################################################################

# Enable the debug menu in Address Book
defaults write com.apple.addressbook ABShowDebugMenu -bool true

# Enable Dashboard dev mode (allows keeping widgets on the desktop)
defaults write com.apple.dashboard devmode -bool true

# Enable the debug menu in iCal (pre-10.8)
defaults write com.apple.iCal IncludeDebugMenu -bool true

# Use plain text mode for new TextEdit documents
defaults write com.apple.TextEdit RichText -int 0
# Open and save files as UTF-8 in TextEdit
defaults write com.apple.TextEdit PlainTextEncoding -int 4
defaults write com.apple.TextEdit PlainTextEncodingForWrite -int 4

# Enable the debug menu in Disk Utility
defaults write com.apple.DiskUtility DUDebugMenuEnabled -bool true
defaults write com.apple.DiskUtility advanced-image-options -bool true
###############################################################################
# Mac App Store                                                               #
###############################################################################

# Enable the WebKit Developer Tools in the Mac App Store
defaults write com.apple.appstore WebKitDeveloperExtras -bool true

# Enable Debug Menu in the Mac App Store
defaults write com.apple.appstore ShowDebugMenu -bool true
###############################################################################
# Google Chrome & Google Chrome Canary                                        #
###############################################################################

# Allow installing user scripts via GitHub Gist or Userscripts.org
defaults write com.google.Chrome ExtensionInstallSources -array "https://gist.githubusercontent.com/" "http://userscripts.org/*"
defaults write com.google.Chrome.canary ExtensionInstallSources -array "https://gist.githubusercontent.com/" "http://userscripts.org/*"

# Disable the all too sensitive backswipe
defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool false
defaults write com.google.Chrome.canary AppleEnableSwipeNavigateWithScrolls -bool false