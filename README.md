#NRL Digital Pass addon for Kodi

## Updated for 2017 season. This addon supports both paid subscriptions through nrl.com and the free Telstra NRL Footy Pass. In-app subscriptions through the App Store/Google Play are not supported.

##Requirements

You will need a Telstra NRL Digital Pass to use this add-on. Most Telstra Mobile customers are eligble for a free subscription with their plan. Please see their [website](https://www.telstra.com.au/tv-movies-music/sports-offer) for details.

##How to install

NRL Live is available from the Catch Up TV AU repository located [here](https://github.com/xbmc-catchuptv-au/repo). Head on over and follow the instructions to install the repo, then install the add-on. 

##Settings

You will need to enter your Telstra ID credentials. For the free Telstra customer offer, you will need to have an eligible mobile service linked to your Telstra ID. Further information available [here](http://hub.telstra.com.au/sp2017-nrl-app).

The plugin has two replay streaming modes which can be set in the add-on's settings - Apple's http live streaming (HLS) and Adobe's http dynamic streaming (HDS). HLS has a lower maximum quality, HDS is higher. The trade off is that you can seek freely through the video with HLS whereas HDS you can't. Pausing seems to be fine though, at least for short periods of time. For live videos only HLS is available in this add-on, which doesn't matter as the live HDS stream offers the same bitrates anyway.

The live streaming bitrates reflect an average bitrate only, you should ideally have twice the bandwidth available to ensure buffer free viewing.

Live streams are broadcast with a black border encoded into the video. This is how Telstra/NRL have it set up on their end. Fortunately Kodi can deal with this by zooming the video. This setting is found in the video settings accessed from the on screen display. A zoom of 1.23 seems to be the sweet spot.


##Issues

Please let me know of any errors by opening an [issues](https://github.com/glennguy/plugin.video.nrl-live/issues) ticket. It would be great if you could attach a Kodi debug log file as well.
