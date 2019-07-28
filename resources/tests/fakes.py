# coding=utf-8
MATCH_XML = u"""<?xml version="1.0" encoding="utf-8"?>
<Media>
  <MediaSection Heading="">
    <Item Type="V" Featured="true">
      <Id>68647</Id>
      <Title>Full Match Replay: Dragons v Storm - Round 16, 2019</Title>
      <Description>NRL Telstra Premiership 2019 Round 16 Dragons v Storm Full Match Replay</Description>
      <Category>MATCH REPLAYS</Category>
      <Length>5463</Length>
      <Date>7/5/2019 • 9:49 AM</Date>
      <Timestamp>2019-07-04T23:49:59Z</Timestamp>
      <Video Type="O" Id="hnNTc0aTE6G5VpOAtrF3KOFl4FoWSbc3" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285947?center=0.5%2C0.5&amp;preset=nrlapp-tile-large</FullImageUrl>
      <LiveEvent>false</LiveEvent>
      <LiveNow>false</LiveNow>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68519</Id>
      <Title>Full Match Replay: Bulldogs v Sharks - Round 15, 2019</Title>
      <Description>NRL Telstra Premiership 2019 Round 15 Bulldogs v Sharks Full Match Replay</Description>
      <Category>MATCH REPLAYS</Category>
      <Length>5883</Length>
      <Date>7/1/2019 • 6:00 AM</Date>
      <Timestamp>2019-06-30T20:00:40Z</Timestamp>
      <Video Type="O" Id="RwZWEzaTE6_ZxjKaAi-hKASa7V3k-U5E" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285354?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
      <LiveEvent>false</LiveEvent>
      <LiveNow>false</LiveNow>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68517</Id>
      <Title>Full Match Replay: Warriors v Panthers - Round 15, 2019</Title>
      <Description>NRL Telstra Premiership 2019 Round 15 Warriors v Panthers Full Match Replay</Description>
      <Category>MATCH REPLAYS</Category>
      <Length>6641</Length>
      <Date>7/1/2019 • 4:00 AM</Date>
      <Timestamp>2019-06-30T18:00:41Z</Timestamp>
      <Video Type="O" Id="tjOWEzaTE6l1jrdVKy0ZRD1RYy1tBrry" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285345?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
      <LiveEvent>false</LiveEvent>
      <LiveNow>false</LiveNow>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68476</Id>
      <Title>Full Match Replay: Eels v Raiders - Round 15, 2019</Title>
      <Description>NRL Telstra Premiership 2019 Round 15 Eels v Raiders Full Match Replay</Description>
      <Category>MATCH REPLAYS</Category>
      <Length>6040</Length>
      <Date>6/30/2019 • 9:30 AM</Date>
      <Timestamp>2019-06-29T23:30:31Z</Timestamp>
      <Video Type="O" Id="dqMzczaTE6NEQEFwkIxYwXK5_S_T7498" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285180?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
      <LiveEvent>false</LiveEvent>
      <LiveNow>false</LiveNow>
    </Item>
  </MediaSection>
</Media>"""

SCORE_XML = u"""<?xml version="1.0" encoding="utf-8"?>
<Scores>
  <Day Name="THU 4 JUL 2019" MoreHeading="GO TO DRAW" MoreUrl="yc://feature/SCORES/">
    <Game Id="20191111610">
      <Timestamp>2019-07-04T09:50:00Z</Timestamp>
      <GameState>Full Time</GameState>
      <PercentComplete>1</PercentComplete>
      <HomeTeam TriCode="SGI" Id="500022" City="St George-Illawarra" Name="Dragons" FullName="St George-Illawarra Dragons" Record="10th" LastResults="LWL" Score="14" />
      <AwayTeam TriCode="MEL" Id="500021" City="Melbourne" Name="Storm" FullName="Melbourne Storm" Record="1st" LastResults="WWW" Score="16" />
    </Game>
  </Day>
  <Day Name="FRI 5 JUL 2019">
    <Game Id="20191111620">
      <Timestamp>2019-07-05T09:55:00Z</Timestamp>
      <GameState>Scheduled</GameState>
      <PercentComplete>0</PercentComplete>
      <HomeTeam TriCode="WST" Id="500023" City="" Name="Wests Tigers" FullName="Wests Tigers" Record="9th" LastResults="WWL" Score="" />
      <AwayTeam TriCode="SYD" Id="500001" City="Sydney" Name="Roosters" FullName="Sydney Roosters" Record="3rd" LastResults="LWL" Score="" />
    </Game>
  </Day>
  <Day Name="SAT 6 JUL 2019">
    <Game Id="20191111630">
      <Timestamp>2019-07-06T09:35:00Z</Timestamp>
      <GameState>Scheduled</GameState>
      <PercentComplete>0</PercentComplete>
      <HomeTeam TriCode="NEW" Id="500003" City="Newcastle" Name="Knights" FullName="Newcastle Knights" Record="5th" LastResults="WLW" Score="" />
      <AwayTeam TriCode="WAR" Id="500032" City="New Zealand" Name="Warriors" FullName="New Zealand Warriors" Record="12th" LastResults="LWL" Score="" />
    </Game>
  </Day>
  <Day Name="SUN 7 JUL 2019">
    <Game Id="20191111640">
      <Timestamp>2019-07-07T06:05:00Z</Timestamp>
      <GameState>Scheduled</GameState>
      <PercentComplete>0</PercentComplete>
      <HomeTeam TriCode="CRO" Id="500028" City="Cronulla-Sutherland" Name="Sharks" FullName="Cronulla-Sutherland Sharks" Record="7th" LastResults="LLW" Score="" />
      <AwayTeam TriCode="BRI" Id="500011" City="Brisbane" Name="Broncos" FullName="Brisbane Broncos" Record="14th" LastResults="LLL" Score="" />
    </Game>
  </Day>
</Scores>"""

VIDEO_XML = u"""<?xml version="1.0" encoding="utf-8"?>
<Media>
  <MediaSection Heading="LATEST MEDIA">
    <Item Type="V" Featured="true">
      <Id>68703</Id>
      <Title>2019: Touch Premiership: Knights v Broncos</Title>
      <Description>Coverage of the NRL Touch Football match between the Knights and Broncos from McDonald Jones Stadium.</Description>
      <Timestamp>2019-07-06T05:05:00Z</Timestamp>
      <Video Type="O" Id="UyeWc0aTE60tc7S_L6RV4ZuwP1CQ6tds" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://nrlliveimageprod.blob.core.windows.net/keyimage/436?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68704</Id>
      <Title>Long lost dogs back in the same pack</Title>
      <Description>Dale Finucane and David Klemmer talk about reuniting in the Blues line up ahead of their clash against the Maroons on Wednesday night.</Description>
      <Timestamp>2019-07-06T04:00:41Z</Timestamp>
      <Video Type="O" Id="U2M2I0aTE6ffHSiGnF4AjYtcEDzkbIcb" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285784?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68618</Id>
      <Title>Knights v Warriors - Round 16</Title>
      <Description>Sam Squiers and Jamie Soward preview Newcastle Knights v New Zealand Warriors</Description>
      <Timestamp>2019-07-06T03:00:41Z</Timestamp>
      <Video Type="O" Id="5wdTM0aTE6s8nR9HYi3a6Mv9eEpvQnv6" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285624?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68701</Id>
      <Title>Tetevano charged for tackle on Brooks</Title>
      <Description>Zane Tetevano has been charged by the match review committee for this tackle on Luke Brooks during the first half at Bankwest Stadium</Description>
      <Timestamp>2019-07-06T02:40:34Z</Timestamp>
      <Video Type="O" Id="5iaGM0aTE6m2dQFcTU8dG8otlz2IAGWY" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285915?center=0.367%2C0.52&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68700</Id>
      <Title>Papalii: I let the State down in Origin II</Title>
      <Description>Maroons prop Josh Papalii will be out to write the wrongs from Queensland’s 32-point loss in Origin II, in the series decider next Wednesday night</Description>
      <Timestamp>2019-07-06T02:26:21Z</Timestamp>
      <Video Type="O" Id="1sbmc0aTE6v-w-7izv-_5ch2tP4ojgeY" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285802?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="true">
      <Id>68699</Id>
      <Title>Seibold denies dumping Boyd rumours as baby Broncos emerge</Title>
      <Description>Broncos coach Anthony Seibold says Brisbane will field the most inexperienced team in the club’s history against the Sharks, while hitting back at suggestions he has considered dropping skipper Darius Boyd</Description>
      <Timestamp>2019-07-06T02:06:41Z</Timestamp>
      <Video Type="O" Id="9ubGc0aTE6zXvBVDDUnEJI4Wn5bRFPUq" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285801?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68696</Id>
      <Title>Extended Highlights: Wests Tigers v Roosters</Title>
      <Description>The Wests Tigers and Roosters do battle at Bankwest Stadium during round 16 of the 2019 NRL Telstra Premiership</Description>
      <Timestamp>2019-07-06T00:01:02Z</Timestamp>
      <Video Type="O" Id="t5YmQ0aTE6mXjNp_5a95oxHuGbq6GUKw" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285797?center=0.316%2C0.498&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68695</Id>
      <Title>Full Match Replay: Wests Tigers v Roosters - Round 16, 2019</Title>
      <Description>NRL Telstra Premiership 2019 Round 16 Wests Tigers v Roosters Full Match Replay</Description>
      <Timestamp>2019-07-06T00:01:02Z</Timestamp>
      <Video Type="O" Id="13OWQ0aTE6Mg9lDUNKVQAK9YaUAhNvXp" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285796?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68688</Id>
      <Title>Roosters: Round 16</Title>
      <Description>Trent Robinson chats to the media after his team's round 16 game against the Wests Tigers</Description>
      <Timestamp>2019-07-05T12:51:54Z</Timestamp>
      <Video Type="O" Id="RjNWQ0aTE6kCOxa4M_HBFftdgDklar1z" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=286044?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
    <Item Type="V" Featured="false">
      <Id>68687</Id>
      <Title>Wests Tigers: Round 16</Title>
      <Description>Michael Maguire chats to the media after his team's round 16 game against the Roosters</Description>
      <Timestamp>2019-07-05T12:50:44Z</Timestamp>
      <Video Type="O" Id="R5NWQ0aTE6SlATfuKhlYu1AuvBCLygs1" PCode="BjZ2oyOsA0g9SvHHgrgYMEu0p1j1" />
      <FullImageUrl>https://www.nrl.com/remote.axd?https://flex.nrl.ooflex.net/keyframedownloadcontroller?id=285906?center=0.5%2C0.5&amp;preset=nrlapp-tile-medium</FullImageUrl>
    </Item>
  </MediaSection>
</Media>"""

HOME_XML = u"""<?xml version="1.0" encoding="utf-8"?>
<Home>
  <HeadlineItems>
    <Item Type="BoxScore" Id="12345" />
    <Item Type="BoxScore" Id="45678" Default="true" />
    <Item Type="Media" Id="98765" />
  </HeadlineItems>
</Home>"""

BOX_XML = u"""<?xml version="1.0" encoding="utf-8"?>
<Boxscore>
  <Id>12345</Id>
  <LiveVideo>
     <Item Type="V" Featured="false">
      <Id>LIVE_2735</Id>
      <Title>Wests Magpies v Bears LIVE</Title>
      <Timestamp>2019-07-07T03:00:00Z</Timestamp>
      <Video Type="O" Id="M3bjJyZDE6sP74YyKfBlYm_0pSY1yws3" HevcId="JsbWk4ZjE616b91YV7wtrJ7eS7DUlUMp" PCode="p3ZWsyOiMLEluThqwB_eQUFngsCZ" />
      <FullImageUrl />
    </Item>
  </LiveVideo>
</Boxscore>"""

COMPLETED_MATCH_ID = '20191111610'

FAKE_VIDEO_ATTRS = {
    'video_id': '12345',
    'thumb': 'https://foo.com/bar.jpg',
    'title': 'FooBar',
    'live': True,
    'time': '2019-07-07T03:00:00Z',
    'desc': 'Game of foo vs bar',
    'dummy': 'None',
    'link_id': 'None'
}

FAKE_VIDEO_URL = '&desc=Game of foo vs bar&dummy=None&link_id=None&live=True&thumb=https%3A%2F%2Ffoo.com%2Fbar.jpg&time=2019-07-07T03:00:00Z&title=FooBar&video_id=12345'

EMBED_TOKEN_XML = u"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SubscriptionVideoTokenResponse>
  <VideoToken>http://foobar.com/video</VideoToken>
</SubscriptionVideoTokenResponse>"""

AUTH_JSON = u"""{  
   "debug_data":{  
      "server_latency":"21.919",
      "request_id":"domU-12-31-39-0B-D2-11_1346804527_57",
      "user_info":{  
         "ip_address":"204.124.203.201",
         "continent":"NORTH AMERICA",
         "country":"US",
         "request_timestamp":"1346804527",
         "language":"en-us",
         "device":"html5",
         "timezone":-7,
         "domain":"www.ooyala.com"
      }
   },
   "signature":"0pobcTRSLoiSZchrMI7Aeoub05/OKRIavq36BgW74lU=",
   "authorization_data":{  
      "44azdwNDpSWUvfd8F30d55tXY0YH9njH":{  
         "authorized":true,
         "message":"authorized",
         "code":"0",
         "request_timestamp":"1346804527",
         "retry":null,
         "streams":[  
            {  
               "delivery_type":"hls",
               "url":{  
                  "data":"aHR0cDovL3BsYXllci5vb3lhbGEuY29tL3BsYXllci9pcGhvbmUvNDRhemR3TkRwU1dVdmZkOEYzMGQ1NXRYWTBZSDluakgubTN1OA==",
                  "format":"encoded",
                  "token_expire":"1460744544"
               }
            }
         ]
      }
   }
}"""

AUTH_JSON_FAILED = u"""{
    "user_info": {
        "domain": "www.nrl.com",
        "request_timestamp": "1506446434",
        "country": "US",
        "device": "html5",
        "timezone": -7.0,
        "ip_address": "60.254.143.223",
        "continent": "NORTH AMERICA"
    },
    "debug_data": {
        "user_info": {
            "request_timestamp": "1506446434"
        },
        "provider_enabled_ssl": false,
        "server_latency": "4.55821",
        "provider_not_use_cookies": false,
        "request_id": "056f8e85ecf16432a258f1defaef816b"
    },
    "authorization_data": {
        "44azdwNDpSWUvfd8F30d55tXY0YH9njH": {
            "restrict_devices": false,
            "retry": null,
            "authorized": false,
            "synd_rule_failures": null,
            "request_timestamp": "1506446434",
            "code": "3",
            "message": "unauthorized location",
            "require_heartbeat": false
        }
    },
    "signature": "wTddCV+8s/ZyBZZ24GuJNNSXOVIfL/pP2PU/ir5uuo="
}"""


M3U8_URL = 'http://player.ooyala.com/player/iphone/44azdwNDpSWUvfd8F30d55tXY0YH9njH.m3u8'
VIDEO_ID = '44azdwNDpSWUvfd8F30d55tXY0YH9njH'



# telstra_auth

FAKE_XSRF_COOKIE = b'XSRF-TOKEN=foobar; path=/; secure'
FAKE_BPSESSION_COOKIE = b'BPSESSION=AQICapYHjH4f; Domain=telstra.com.au; Path=/; HttpOnly; Secure'

FAKE_UUID = [
    'e8485af7-fe81-4064-bfb0-fdafbf68db33',
    'cea23fb2-ab9d-4869-8b01-fdb66aab09e7'
]

FAKE_RANDOM = [
    '\xb7\x91e|\x7fd\x1e\xdal\x8b\x99\xe2Z\xf2\xe9Y',
    '\x11\x7ff(\x01\n\xf7\x13lHq\xcb\xfa\x81\x03\xf3'
        ]

AUTH_REDIRECT_URL = 'https://www.nrl.com/account/login?ReturnUrl=%2Faccount%2Fauthorize%3Fresponse_type%3Dcode%26scope%3Dopenid%2520email%2520profile%2520offline_access%26client_id%3Dnrlapp-ios%26redirect_uri%3Dhttps%3A%2F%2Fredirect.nrl-live.app.openid.yinzcam.com'
AUTH_REDIRECT_CODE_URL = 'https://redirect.nrl-live.app.openid.yinzcam.com?code=abcdefg'
NRL_TOKEN_JSON = {
    "access_token": "abcdefg",
    "expires_in": 3600,
    "id_token": "hijklmn",
    "refresh_token": "opqrstu",
    "scope": "openid email profile offline_access",
    "token_type": "Bearer"
}

YINZCAM_AUTH_RESP_JSON = {
    "AccountCreated": "false",
    "ExpireTime": "1595736000000",
    "IssueTime": "1564200000000",
    "Ticket": "ticket123",
    "ValidSpan": "31536000000",
    "YinzId": "6a8e4220-87fb-4737-9221-b736c36a6c49"
}

YINZCAM_AUTH_RESP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<TicketResponse>
  <Ticket>ticket123</Ticket>
  <IssueTime>1564280000000</IssueTime>
  <ExpireTime>1595816000000</ExpireTime>
  <ValidSpan>31536000000</ValidSpan>
  <YinzId>6a8e4220-87fb-4737-9221-b736c36a6c49</YinzId>
  <AccountCreated>true</AccountCreated>
</TicketResponse>"""


STATUS_RESP_JSON = {
    "Expiration": "2020-01-31T12:59:59.000Z",
    "NRLLive": {
        "IsPost2018Purchase": "true"
    },
    "Product": "69b1f3e1-5196-4a57-9a46-472d20b78bc8",
    "Reason": "An active subscription was found on your account.",
    "Service": "TELSTRA_ONE_PLACE",
    "Strings": {
        "Name": "$0.00 Season Pass",
        "Type": "NRL Live Pass"
    },
    "UnsubscribeUrl": "http://hub.telstra.com.au/sp2017-nrl-app?type=cancellation",
    "Valid": "true"
}


YINZCAM_AUTH2_RESP = {
    "AppId": "NRL_LIVE",
    "Destination": "NRL_LIVE",
    "GenerationTime": "2019-07-28T02:08:29Z",
    "OfferId": "69b1f3e1-5196-4a57-9a46-472d20b78bc8",
    "TenantId": "sp2017-nrl-app",
    "TpUid": "6a8e4220-87fb-4737-9221-b736c36a6c49|foobar",
    "Type": "SportPassConfirmation",
    "Url": "http://hub.telstra.com.au/sp2017-nrl-app?offerId=69b1f3e1-5196-4a57-9a46-472d20b78bc8&type=SportPassConfirmation",
    "YinzId": "6a8e4220-87fb-4737-9221-b736c36a6c49"
}

SPC_RESP_HTML = u'''<!DOCTYPE html ng-app="app" >
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=0.7, user-scalable=yes">
<meta name="application-name" content="Telstra Sport - NRL"/>
<meta name="msapplication-tooltip" content="Start Telstra Sport - NRL"/>
<meta name="description"/>
<meta property="og:title" content="Telstra Sport - NRL"/>
<meta property="og:description"/>
<meta property="og:image" content=""/>
<meta property="og:url"/>
<title>Telstra Sport - NRL</title>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<script src="/etc/designs/mpa/js/oidc-client.min.js;pv759685a8c67bf9a1"></script><script>
	window.__env = window.__env || {};
	window.__env.apiUrl = "https://tapi.telstra.com";
	window.__env.channel = "All_MyOffersPortal_Offerpage_4368";
	window.__env.epgEndpoint = "https://msisdn.hub.telstra.com.au";
	window.__env.ssoUrl = "https://tapi.telstra.com/v1";
	window.__env.ssoClientId = "wd8F30d550YH9ntjH44azdXYNDpSWUvf";
	</script>
</head>
</html>
'''

SSO_ID = 'wd8F30d550YH9ntjH44azdXYNDpSWUvf'

SSO_AUTH_REDIRECT_URL = 'https://signon.telstra.com/login?goto=https%3A%2F%2Ftapi.telstra.com%2Fv1%2Fsso%2Fidpcallback%3Fcbs%3Dfoobar123abc%26app_name%3DOne%20Place%20Portal'

SIGNON_REDIRECT_URL = 'https://signon.telstra.com/login?raaURLAction=cdcTransfer&raaGotoChain=signon.telstra.com%2Flogin%7Csignon.bigpond.com%2Flogin&cookieAction=write%7Cwrite&cookieName=BPSESSION%7CBPSESSION&cdcValBPSESSION=AQICapYHjH4f&goto=https%3A%2F%2Ftapi.telstra.com%2Fv1%2Fsso%2Fidpcallback%3Fcbs%3Dfoobar123abc%26app_name%3DOne+Place+Portal'

SSO_URL = 'https://tapi.telstra.com/v1/sso/idpcallback?cbs=foobar123abc&app_name=One Place Portal'

SSO_REDIRECT_URL = 'https://hub.telstra.com.au/offers/content/cached/callback.html#id_token=idtoken123&access_token=accesstoken123&token_type=Bearer&expires_in=869&state=b791657c7f641eda6c8b99e25af2e959'

OFFERS_RESP_JSON = {
    "correlationId": "",
    "data": {
        "offers": [
            {
                "bonusEndDateTime": "2020-01-31T23:59:59.000+1100",
                "bonusPeriod": 0,
                "carrierBillableOffer": False,
                "channelTags": [
                    "All_v1Apps_All_3248",
                    "TTV_OneApp_HomeScreen_7677",
                    "All_MyOffersPortal_Offerpage_4368"
                ],
                "contractTerm": 0,
                "externalId": "NA",
                "id": "69b1f3e1-5196-4a57-9a46-472d20b78bc8",
                "name": "NRL Live Pass",
                "oneOffCharge": 0,
                "productOfferingAttributes": [
                    {
                        "id": "bc8b893a-132d-4fe3-9415-c2073d884d98",
                        "name": "OfferType",
                        "value": "base"
                    },
                    {
                        "id": "1612b3d3-b4a2-4c70-ac73-444228e5d279",
                        "name": "ServiceType",
                        "value": "MSISDN"
                    },
                    {
                        "id": "bd3f5698-8b45-46c8-8dd5-ea96beba4a6c",
                        "name": "ServiceId",
                        "value": "61400000000"
                    }
                ],
                "productOffers": [
                    {
                        "contractTerm": 1,
                        "externalId": "SPORTS_PASS_$0_NRL",
                        "id": "a0d57c43-928e-4d35-bb3b-57b91fd4b79f",
                        "name": "NRL Live Pass Streaming",
                        "oneOffCharge": 0,
                        "product": {
                            "category": "Sport",
                            "description": "NRL Streaming",
                            "externalId": "NRL",
                            "id": "2c0a83d2-f9c8-4d61-8a0e-1fa2d1964db5",
                            "partner": {
                                "description": "National Rugby League",
                                "id": "nrl",
                                "name": "NRL",
                                "website": "https://www.nrl.com.au/"
                            },
                            "productName": "nrl_streaming",
                            "productUrl": "https://www.nrl.com.au/"
                        },
                        "recurringCharge": 0,
                        "requiredPaiPattern": ".*",
                        "url":
                            "https://signon-live-nrl.yinzcam.com/telstra"
                            "/oneplace/callback?browser=external"
                    }
                ],
                "publishEndDate": "2020-01-31T23:59:59.999+1100",
                "publishStartDate": "2017-01-31T00:00:00.000+1100",
                "recurringCharge": 0,
                "reuptakeAllowed": True,
                "serviceTransferAllowed": False,
                "totalPrice": 0
            }
        ]
    }
}

ORDER_RESP_JSON = {
    "correlationId": "ab8dcfe2-3159-426d-922c-934501085bce",
    "data": {
        "cac": "2091234567",
        "customerType": "CONSUMER",
        "endDateTime": "2020-01-31T23:59:59.000+1100",
        "id": "948d2cb1-ba9b-4ce1-8964-8044ff2803cc",
        "offer": {
            "bonusEndDateTime": "2020-01-31T23:59:59.000+1100",
            "bonusPeriod": 0,
            "carrierBillableOffer": False,
            "channelTags": [
                "All_v1Apps_All_3248",
                "TTV_OneApp_HomeScreen_7677",
                "All_MyOffersPortal_Offerpage_4368"
            ],
            "contractTerm": 0,
            "externalId": "NA",
            "id": "69b1f3e1-5196-4a57-9a46-472d20b78bc8",
            "name": "NRL Live Pass",
            "oneOffCharge": 0,
            "productOfferingAttributes": [
                {
                    "id": "bc8b893a-132d-4fe3-9415-c2073d884d98",
                    "name": "OfferType",
                    "value": "base"
                }
            ],
            "productOffers": [
                {
                    "contractTerm": 1,
                    "externalId": "SPORTS_PASS_$0_NRL",
                    "id": "a0d57c43-928e-4d35-bb3b-57b91fd4b79f",
                    "name": "NRL Live Pass Streaming",
                    "oneOffCharge": 0,
                    "product": {
                        "category": "Sport",
                        "description": "NRL Streaming",
                        "externalId": "NRL",
                        "id": "2c0a83d2-f9c8-4d61-8a0e-1fa2d1964db5",
                        "partner": {
                            "description": "National Rugby League",
                            "id": "nrl",
                            "name": "NRL",
                            "website": "https://www.nrl.com.au/"
                        },
                        "productName": "nrl_streaming",
                        "productUrl": "https://www.nrl.com.au/"
                    },
                    "recurringCharge": 0,
                    "requiredPaiPattern": ".*",
                    "url": "https://signon-live-nrl.yinzcam.com/telstra/oneplace/callback?browser=external"
                }
            ],
            "publishEndDate": "2020-01-31T23:59:59.999+1100",
            "publishStartDate": "2017-01-31T00:00:00.000+1100",
            "recurringCharge": 0,
            "reuptakeAllowed": True,
            "serviceTransferAllowed": False,
            "totalPrice": 0
        },
        "orderItems": [
            {
                "correlationId": "ab8dcfe2-3159-426d-922c-934501085bce",
                "endDateTime": "2020-01-31T23:59:59.000+1100",
                "id": "f382d398-c879-4d30-bd39-3934ab760bc8",
                "pai": "6a8e4220-87fb-4737-9221-b736c36a6c49|foobar",
                "productOffer": {
                    "contractTerm": 1,
                    "externalId": "SPORTS_PASS_$0_NRL",
                    "id": "a0d57c43-928e-4d35-bb3b-57b91fd4b79f",
                    "name": "NRL Live Pass Streaming",
                    "oneOffCharge": 0,
                    "product": {
                        "category": "Sport",
                        "description": "NRL Streaming",
                        "externalId": "NRL",
                        "id": "2c0a83d2-f9c8-4d61-8a0e-1fa2d1964db5",
                        "partner": {
                            "description": "National Rugby League",
                            "id": "nrl",
                            "name": "NRL",
                            "website": "https://www.nrl.com.au/"
                        },
                        "productName": "nrl_streaming",
                        "productUrl": "https://www.nrl.com.au/"
                    },
                    "recurringCharge": 0,
                    "requiredPaiPattern": ".*",
                    "url": "https://signon-live-nrl.yinzcam.com/telstra/oneplace/callback?browser=external"
                },
                "startDateTime": "2019-07-28T10:00:00.000+1000",
                "status": "COMPLETE"
            }
        ],
        "serviceId": "61435822059",
        "serviceType": "MSISDN",
        "startDateTime": "2019-07-28T10:00:00.000+1000",
        "status": "COMPLETE"
    },
    "time": "2019-07-28T10:00:00.000+1000"
}

FAKE_MOBILE_COOKIE = b'GUID_S=12345678901; path=/; secure'