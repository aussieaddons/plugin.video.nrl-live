#NRL Digital Pass addon for Kodi

##Requirements

You will need a Telstra NRL Digital Pass to use this add-on. Most Telstra Mobile customers are eligble for a free subscription with their plan. Please see their [website](https://www.telstra.com.au/tv-movies-music/sport/sports-offer-eoi) for details.

##How to install

UPDATE: NRL Live is now available from the Catch Up TV AU repository located [here](https://github.com/xbmc-catchuptv-au/repo). Head on over and follow the instructions to install the repo, then install the add-on. 

##Settings

You will need to enter your Telstra ID credentials. You can use your username or email address in the username field.

The plugin has two streaming modes which can be set in the add-on's settings - Apple's http live streaming (HLS) and Adobe's http dynamic streaming (HDS). HLS has a lower maximum quality, HDS is higher. The trade off is that you can seek freely through the video with HLS whereas HDS you can't. Pausing seems to be fine though, at least for short periods of time. For live videos only HLS is available in this add-on, which doesn't matter as the live HDS stream offers the same bitrates anyway.

The live streaming bitrates reflect an average bitrate only, you should ideally have twice the bandwidth available to ensure buffer free viewing.

Live streams are broadcast with a black border encoded into the video. This is how Telstra/NRL have it set up on their end. Fortunately Kodi can deal with this by zooming the video. This setting is found in the video settings accessed from the on screen display. A zoom of 1.23 seems to be the sweet spot.


##Issues

Please let me know of any errors by opening an [issues](https://github.com/glennguy/plugin.video.nrl-live/issues) ticket. It would be great if you could attach a Kodi debug log file as well.
