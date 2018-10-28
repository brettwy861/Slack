from slackclient import SlackClient
import time
sc = SlackClient("YOUR_KEY")

# get a public channels' list, shared channel not supported
def getPublicchannellist(exclude_archived=1):
    channelList = sc.api_call("channels.list",exclude_archived=exclude_archived)['channels']
    channelsDict = {}
    for item in channelList:
        channelsDict[item['name']]=item
#        print('Channel name: '+item['name']+' Channel ID: '+str(item['id']))
    return channelsDict 

# get a public channels' list, shared channel supported
def getPublicchannellist_v2(exclude_archived=1):
    channelList = sc.api_call("conversations.list",exclude_archived=exclude_archived,types='public_channel')['channels']
    channelsDict = {}
    for item in channelList:
        channelsDict[item['name']]=item
#        print('Channel name: '+item['name']+' Channel ID: '+str(item['id']))
    return channelsDict 

# get a private channels' list,  shared channel not supported
def getPrivatechannellist(exclude_archived=1):
    channelList = sc.api_call("groups.list",exclude_archived=exclude_archived)['groups']
    channelsDict = {}
    for item in channelList:
        channelsDict[item['name']]=item
#        print('Channel name: '+item['name']+' Channel ID: '+str(item['id']))
    return channelsDict 

# get a private channels' list, shared channel supported
def getPrivatechannellist_v2(exclude_archived=1):
    channelList = sc.api_call("conversations.list",exclude_archived=exclude_archived, types='private_channel')['channels']
    channelsDict = {}
    for item in channelList:
        channelsDict[item['name']]=item
#        print('Channel name: '+item['name']+' Channel ID: '+str(item['id']))
    return channelsDict 

# get channel detailed information, shared channel not supported
def getChannelinfo(channelName):
    allPublicchannels = getPublicchannellist()
    allPrivatechannels = getPrivatechannellist()
    if channelName.strip('#') in allPublicchannels.keys():
        channelInfo = sc.api_call("channels.info", channel=allPublicchannels[channelName.strip('#')]['id'])['channel']
    elif channelName.strip('#') in allPrivatechannels.keys():
        channelInfo = sc.api_call("groups.info", channel=allPrivatechannels[channelName.strip('#')]['id'])['group']
    else:
        channelInfo = False
        print('Channel does not exist')
    return channelInfo

# get channel info with conversations.list API,  shared channel supported
def getChannelinfo_v2(channelName):
    allPublicchannels = getPublicchannellist_v2()
    allPrivatechannels = getPrivatechannellist_v2()
    if channelName.strip('#') in allPublicchannels.keys():
        channelInfo = sc.api_call("conversations.info", channel=allPublicchannels[channelName.strip('#')]['id'])['channel']
    elif channelName.strip('#') in allPrivatechannels.keys():
        channelInfo = sc.api_call("conversations.info", channel=allPrivatechannels[channelName.strip('#')]['id'])['channel']
    else:
        channelInfo = False
        print('Channel does not exist')
    return channelInfo
     
# get all user info in the team
def getAlluserinfo():
    userlist = sc.api_call("users.list")
#    for item in userlist:
#        print(item['name']+':'+item['profile']['real_name']+':'+item['id'])
    return userlist.get('members')

# get all user info in the team
def getUserinfo(userId):
    userlist = sc.api_call("users.info", user=userId)
#    for item in userlist:
#        print(item['name']+':'+item['profile']['real_name']+':'+item['id'])
    return userlist['user']

#get team info
def getTeaminfo():
    return sc.api_call("team.info")['team']

# get member names of a channel, not support shared channel
def getChannelmember(channelName):
    channelInfo = getChannelinfo(channelName)
    userInfo = getAlluserinfo()
    userDict = {}
    for member in userInfo:
        userDict[member['id']]= member['name']
    memberId = channelInfo['members']
    memberName = [userDict[i] for i in memberId]
    #print(memberName)
    return [memberName, memberId]

# get member names of a channel, not support shared channel
def getChannelmember_v2(channelName):
    channelInfo = getChannelinfo_v2(channelName)
    userInfo = getAlluserinfo()
    userDict = {}
    memberName = []
    for member in userInfo:
        userDict[member['id']]= member['name']
    memberId = sc.api_call("conversations.members", channel=channelInfo['id'])
    for ID in memberId['members']:
        if ID in userDict.keys():
            memberName.append(userDict[ID])
        else:
            memberName.append('UNKNOWN')
    #print(memberName)
    return [memberName, memberId.get('members')]

# get channel history for the recent 100 messages
def getChannelhistory(channelName, count=100, latest='now', oldest=0):
    channel = getChannelinfo(channelName)
    if 'is_group' in channel.keys() and channel['is_group']:
        data=sc.api_call("groups.history",channel=channel['id'])
    else:
        data=sc.api_call("channels.history",channel=channel['id'])
    return data

# get channel history for the recent 100 messages, support shared channel
def getChannelhistory_v2(channelName, oldestTime=0, latestTime=time.time()):
    channel = getChannelinfo_v2(channelName)
    data=sc.api_call("conversations.history",channel=channel['id'],oldest=oldestTime,latest=latestTime)
    return data

# get channel history for the recent 100 messages, support shared channel
def getChannelcompletehistory_v2(channelName, count=100, latest=time.time(), oldest=0):
    channel = getChannelinfo_v2(channelName)
    result = sc.api_call("conversations.history",channel=channel['id'])
    data = result['messages']
    if result['has_more'] == True:
        next_cursor = result['response_metadata'].get('next_cursor')
        while next_cursor != '':
            tmp=sc.api_call("conversations.history",channel=channel['id'],cursor=next_cursor)
            data=data+tmp['messages']
            meta = tmp.get('response_metadata')
            if meta is None:
                break
            else:
                next_cursor = meta.get('next_cursor')                
    return data

#get certain thread in certain channel, must have the ts number
def getReplies(channelName, ts):
    channel = getChannelinfo(channelName)
    if 'is_group' in channel.keys() and channel['is_group']:
        data=sc.api_call("groups.replies",channel=channel['id'],thread_ts = ts)
    else:
        data=sc.api_call("channels.replies",channel=channel['id'],thread_ts = ts)
    return data  

#get certain thread in certain channel, must have the ts number, shared channel supported
def getReplies_v2(channelName, ts):
    channel = getChannelinfo_v2(channelName)
    data=sc.api_call("conversations.replies",channel=channel['id'],thread_ts = ts)
    return data  

# get all emoji in a channel as a key value pairs, key is the ':xxx:' value is url to the img
def getEmoji():
    return sc.api_call('emoji.list')['emoji']

# send a message to a channel
def sendMessage(dest, content):
    sc.api_call(
      "chat.postMessage",
      channel='#'+dest.strip('#'),
      text=content
    )

# send all team emoji to a channel
def sendAllemoji(dest):
    allEmoji = getEmoji()
    message = ''
    for item in allEmoji:
        message = message+':'+item+': '
    sendMessage(dest, message) 

# send Ephemeral message to a user in a channel
def sendEphemeralmessage(dest, userName, content):
    channelMember = getChannelmember(dest)
    if userName in channelMember[0]:
        idx=channelMember[0].index(userName)
        memberId = channelMember[1][idx]
        sc.api_call(
          "chat.postEphemeral",
          channel= getChannelinfo(dest)['id'],
          text=content,
          user = memberId
        )

#search file by channelname, filetype, username, timerange 
#type={all, spaces, snippets, images, gdocs, zips, pdfs}
def fileList(channelName, types=all, count=100, page=1, ts_from='0', ts_to='now', user='default'):
    channel = getChannelinfo(channelName)
    if user == 'default':
        data=sc.api_call(
            "files.list",
            channel=channel['id'],
            count=count,
            page=page,
            types=types,
            ts_from=ts_from,
            ts_to=ts_to)
    else:
        channelMember = getChannelmember(channelName)
        if user in channelMember[0]:
            idx=channelMember[0].index(user)
            memberId = channelMember[1][idx]
        data=sc.api_call(
            "files.list",
            channel=channel['id'],
            count=count,
            page=page,
            types=types,
            ts_from=ts_from,
            ts_to=ts_to,
            user=memberId)       
    return data

#search file across all channels by the name
def fileSearch(query, count=20, page=1, sort='score', sort_dir='desc'):
    data=sc.api_call(
        "search.files",
        query=query,
        count=count,
        page=page,
        sort=sort,
        sort_dir=sort_dir)
    for item in data['files']['matches']:
        print(item['name'])
    return data['files']['matches']

#search message across all channels by the name
def messageSearch(query, count=20, page=1, sort='score', sort_dir='desc'):
    data=sc.api_call(
        "search.messages",
        query=query,
        count=count,
        page=page,
        sort=sort,
        sort_dir=sort_dir)
    return data['messages']['matches']

#search message across all channels by the name
def allSearch(query, count=20, page=1, sort='score', sort_dir='desc'):
    data=sc.api_call(
        "search.all",
        query=query,
        count=count,
        page=page,
        sort=sort,
        sort_dir=sort_dir)
    return data


