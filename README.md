# Quest Beast Sync

This application synchronizes your BeastSaber bookmarks with your Beat Saber custom levels. This app was initially created for myself due to SyncSaber not being up to date, but I expanded upon it for the learning experience (I don't recommend writing an app in Python), it's simplicity, and for a feature I wanted (that was not available using SyncSaber).

![Android Build](https://github.com/KyujuuAlpha/Quest-Beast-Sync/actions/workflows/build-android.yml/badge.svg)

## Features

- Beast Saber bookmark syncing
- Multi-User syncing support (with playlist separation)

## Known Bugs
- Text deletion in the user input field is broken because of Android.  A workaround is to select the existing text and type over it.

## Usage

1. Open the application under the `Unknown Sources` section on your Quest.
2. Set the username to whatever BeastSaber user's bookmarks you want to synchronize (this does not delete local levels).  For multiple users, separate the usernames using commas.  For example: `user1,user2,user3`
3. Click `Synchronize` and wait
4. Open Beat Saber to play!

## Installation

The recommended installation method is by sideloading the APK through SideQuest.  Please follow the instructions on the SideQuest [download page](https://sidequestvr.com/download) if you don't have it installed already.

1. First download the latest APK from the `Actions` tab on this Github page
2. Follow [these instructions](https://learn.adafruit.com/sideloading-on-oculus-quest/install-and-use-sidequest#install-a-custom-apk-3051314-9) on how to sideload the downloaded APK through SideQuest

## License

Quest Beast Sync is released under the MIT License terms.  Please refer to the LICENSE file.

## Credits
- [Kivy](https://kivy.org/#home)
- [KivyMD](https://github.com/kivymd/KivyMD)
- [buildozer-action](https://github.com/ArtemSBulgakov/buildozer-action)
