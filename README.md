# Slack
useful function based on Slack API

- get a public channels' list 
getPublicchannellist_v2(exclude_archived=1)

- get a private channels' list 
getPrivatechannellist_v2(exclude_archived=1) 

- get channel info with conversations.list API 
getChannelinfo_v2(channelName)
     
- get all user info in the team
getAlluserinfo()

- get a user's info in the team
getUserinfo(userId)

- get team info
getTeaminfo()

- get member names of a channel 
getChannelmember_v2(channelName)

- get channel history for the recent 100 messages 
getChannelhistory_v2(channelName, oldestTime=0, latestTime=time.time())

- get channel history for the recent 100 messages 
getChannelcompletehistory_v2(channelName, count=100, latest=time.time(), oldest=0)

- get certain thread in certain channel, must have the ts number 
getReplies_v2(channelName, ts)

- get all emoji in a channel as a key value pairs, key is the ':xxx:' value is url to the img
getEmoji()

- send a message to a channel
sendMessage(dest, content)

- send all team emoji to a channel
sendAllemoji(dest)

- send Ephemeral message to a user in a channel
sendEphemeralmessage(dest, userName, content)

- search file by channelname, filetype, username, timerange type={all, spaces, snippets, images, gdocs, zips, pdfs}
fileList(channelName, types=all, count=100, page=1, ts_from='0', ts_to='now', user='default')

- search file across all channels by the name
fileSearch(query, count=20, page=1, sort='score', sort_dir='desc')

- search message across all channels by the name
messageSearch(query, count=20, page=1, sort='score', sort_dir='desc')
 
- search message across all channels by the name
allSearch(query, count=20, page=1, sort='score', sort_dir='desc')
   
