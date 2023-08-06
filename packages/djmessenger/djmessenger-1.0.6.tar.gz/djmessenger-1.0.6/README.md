# djmessenger

[![PyPI version](https://badge.fury.io/py/djmessenger.svg)](https://badge.fury.io/py/djmessenger)
[![python version](https://img.shields.io/badge/python-3.4-brightgreen.svg)]()

djmessenger provides a simple way to build a Facebook Messenger BOT

## Contributors Needed

To make `djmessenger` more robust and solid, I really need some contributors
to help with the following items

- Testings

    Right now there are almost 0 automatic testings, I mostly did the 
    testing manually (I know...), but I am still trying to figure out a 
    way to do this automatically, really need someone to brainstorm on 
    this
    
- More builtin handlers

    There are a lot more different event types that Facebook can send 
     over including **Authentication**, **Account Linking**, 
     **Message Delivered**, **Message Read** and **Message Echo**. Need 
     to think about what `djmessenger` can do to provide builtin 
     handlers to handle these.

- More builtin senders

    There are a lot more different sending types that Facebook supports,
     including **Generic Template**, **Receipt Template**, and airline 
     info templates. Although they are kinda rarely used, it would be 
     nice to have them supported as well. 
     
    Especially for **Generic Template**, might need some mechanism so 
    that dev can easily construct a generic template
    
- Docs

    I mostly write docs as I wrote code and they are all in Markdown, 
    I tried to use `Sphinx` but actually **rST** is really not my thing.
    So if someone can help on creating detailed docs in any way, that 
    would be perfect.

## Overview

![Overview](https://www.lucidchart.com/publicSegments/view/75d4b7e2-b509-4a06-a7b9-7273b1cc4cf5/image.png)

**djmessenger** is essentially a REST API. djmessenger simply exposes a REST API
endpoint for Facebook Messenger webhook so that Facebook will send a 
request to **djmessenger** endpoint when subscribed events happen. 

Here is how **djmessenger** works (roughly, though)

1. Upon receiving message relayed by Facebook (Facebook call this a 
   **callback**), `receiving` module kicks in and determines what's 
   the `ReceivingType` (defined by **djmessenger**) of the message
2. Because each **callback** could contain multiple messages, we loop 
   them one by one
   
> this could happen if your BOT was somehow not responding for a while, 
  and when the BOT just comes online, it will get all the messages that 
  were failed to deliver previously at once
   
3. From [routing policy](https://github.com/ifanchu/djmessenger/wiki/Routing-Policy), 
   we got the handlers for this type of **callback**
4. Ask the handlers to handle the message, one by one
5. Each handler could define multiple senders, so once a handler 
   successfully handled the message, invoke the corresponding senders
   
> only if the handler actually handles the message would senders be 
  invoked. If the message does not pass handlers `should_handle()` 
  method, its senders won't be invoked

## Features

- For each message sent, record sender's PSID (page-scoped ID) so that
  we can send something back to the sender
- Save user basic info
- If the user sends a location, save it into database
- If the suer sends a simple text, filter it with regex and send back 
  something
- Send Quick Replies and handle its postback
- Send Buttons and handle its postback
- Easy to [setup](https://github.com/ifanchu/djmessenger/wiki/Minimal-BOT-Setup)
- Flexible to extend
- Flexible [routing policy](https://github.com/ifanchu/djmessenger/wiki/Routing-Policy)
- [i18n support](https://github.com/ifanchu/djmessenger/wiki/i18n-Support)

### Current Receiving Types

```
ReceivingType.SIMPLE_TEXT = ReceivingType('SIMPLE_TEXT')
ReceivingType.QUICK_REPLY = ReceivingType('QUICK_REPLY')
ReceivingType.IMAGE = ReceivingType('IMAGE')
ReceivingType.AUDIO = ReceivingType('AUDIO')
ReceivingType.VIDEO = ReceivingType('VIDEO')
ReceivingType.FILE = ReceivingType('FILE')
ReceivingType.LOCATION = ReceivingType('LOCATION')
ReceivingType.STICKER = ReceivingType('STICKER')
ReceivingType.POSTBACK = ReceivingType('POSTBACK')
ReceivingType.AUTHENTICATION = ReceivingType('AUTHENTICATION')
ReceivingType.ACCOUNT_LINKING = ReceivingType('ACCOUNT_LINKING')
ReceivingType.DELIVERED = ReceivingType('DELIVERED')
ReceivingType.READ = ReceivingType('READ')
ReceivingType.ECHO = ReceivingType('ECHO')
# this is not a real type, this is for routing.py to indicate the settings is
# not for a specific type but for all type
ReceivingType.DEFAULT = ReceivingType('DEFAULT')
# the follows are special types to handle thread settings, all of these will
# be handled by PostbackReceivedChecker
ReceivingType.PERSISTENT_MENU_ONE = ReceivingType('PERSISTENT_MENU_ONE')
ReceivingType.PERSISTENT_MENU_TWO = ReceivingType('PERSISTENT_MENU_TWO')
ReceivingType.PERSISTENT_MENU_THREE = ReceivingType('PERSISTENT_MENU_THREE')
ReceivingType.PERSISTENT_MENU_FOUR = ReceivingType('PERSISTENT_MENU_FOUR')
ReceivingType.PERSISTENT_MENU_FIVE = ReceivingType('PERSISTENT_MENU_FIVE')
ReceivingType.GET_STARTED_BUTTON = ReceivingType('GET_STARTED_BUTTON')
```

### Current Handlers

See [Handling module](https://github.com/ifanchu/djmessenger/wiki/Handling-module) for more details

- **UserProfileHandler**

    This handler saves user PSID (page-scoped ID, which is required in 
    order to send something back) and/or some user basic info such as
    first name, last name, locale, and etc
    
- **ThumbUpHandler**

    This handler increment the user's thumbup count in the database if
    `UserProfileHandler` was enabled in [Routing Policy](https://github.com/ifanchu/djmessenger/wiki/Routing-Policy)
    
- **SimpleTextBaseHandler**

    Provides regex matching for the incoming message text. 
    
- **BaseQuickReplyPayloadHandler**

    Handles the quick reply, dev need to subclass this handler to provide
    cusomized handling logic, or just use `DummyHandler` to do nothing
    
- **DummyHandler**

    Do nothing, simply route to senders
    
- **MultimediaBaseHandler**

    Handles all multimedia `ReceivingType` including `AUDIO`, `VIDEO`, 
    `FILE` and `IMAGE`. Dev needs to subclass this base handler to 
    provide customized `handle()` logic
    
### Current Senders

See [Sending module](https://github.com/ifanchu/djmessenger/wiki/Sending-module) for more details

- **SimpleMessageSender**

    Sends back a text message
    
- **SenderActionSender**

    Sends back a sender action
    
- **MultimediaSender**

    Sends back a multimedia which needs an URL and sending type
    
- **BaseQuickReplySender**

    Sends back at most 10 quick replies, dev needs to subclass this sender
    to provide custom payload for the quick replies
    
- **BaseButtonSender**

    Sends back at most 3 buttons, dev needs to subclass this sender to 
    provide custom payload for postback buttons
    
## Thread Settings

Thread settings are defined in `settings.py` and use management command
to invoke

- Persistent Menu
- Greetings
- Get Started Button

## Next Features
    
- More handlers
    - `AuthenticationBaseHandler` to handle Authentication
    - `AccountLinkingBaseHandler` to handle account linking
    - `DeliveryBaseHandler` to handle message delivered callback
    - `ReadBaseHandler` to handle message has been read callback
    - `EchoBaseHandler` to handle message echo callback
    
- More senders
    - `GenericTemplateSender`
 
- testing

    > right now, no much tests are there...
    
- Automatic thread setting

    Maybe to find a place to automatically invoke management commands 
    every time the server starts
    
If anyone wants to contribute to any of the above items, please let me know

## Install

```
pip install djmessenger
```

## Prerequisites

1. You must have a Facebook page, this is different from having a personal account, but you can always create a page as you like for free
2. Obtain your page access token
    - Login to [Facebook Developers](https://developers.facebook.com)
    - From top right **My Apps**, click on **Add a New App**
    - Enter this new app
    - From left side, **+ Add Product**
    - Click **Get Started** on **Messenger** and **Webhooks**
    - Go to **Messenger**, in **Token Generation**, choose a page and copy the token for later use
    - Click **Webhooks** and leave this page open for later

## Minimal BOT Setup

Check [here](https://github.com/ifanchu/djmessenger/wiki/Minimal-BOT-Setup)

## Detailed customized BOT

check [here](https://github.com/ifanchu/djmessenger/wiki/Customized-BOT-Showcase)

## Example App

Check out [testapp](https://github.com/ifanchu/djmessenger/tree/master/testapp)
