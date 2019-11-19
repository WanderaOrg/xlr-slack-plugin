# XL Release Slack Plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-slack-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-slack-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/80e1ff4ab8a1482c8b2ab93e6d469d07)](https://www.codacy.com/app/gsajwan/xlr-slack-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-slack-plugin&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-slack-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-slack-plugin)
<img src="https://cdn1.tnwcdn.com/wp-content/blogs.dir/1/files/2014/10/Slack.png" width="400" height="200"/>


## Preface
This document describes the functionality provide by the `xlr-slack-plugin`

## Overview
This plugin provides a notification task to send Slack messages to channels or direct messages.
It's based on Incoming Webhooks integration, which provides a URL within an authorization token ready to POST messages.
See [Slack Incoming Webhooks](https://api.slack.com/incoming-webhooks) documentation for background information on post messages from external sources into Slack.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

## Configuration
This configuration allows you to connect to multiple servers or connect to just one.
Before to use Slack notification task, it's needed to setup a Slack server definition within the following information:

- **Title:** Name of the Slack server definition.
- **Slack URL:** Tokenized URL provided by the Incoming WebHook integration.
- **User name:** Name to use in the notifications.
- **User icon:** Icon to use in the notifications, it should be a icon emoji, e.g. `:ghost:`.
- **Proxy URL:** Proxy URL to use in format <http://username:password@proxyurl:proxyport>, leave it in blank if isn't required.

![slack_sharedconfiguration](images/slack_sharedconfiguration.png)

## Available Tasks
The available tasks for interfacing with Slack. These tasks utilize the Slack REST API and the provided Slack Authentication Configuration.

## Notification task
The Slack notification task needs the next information:

- **Server:** The Slack server definition to use.
- **Channel:** The target for the notification, use `#` or `@` to refer to a channel or direct message.
- **Message:** The notification message text, it could be [formatted](https://api.slack.com/docs/formatting).

![notification](images/notification.png)

## CreateChannel task
This task creates a new channel in slack

![CreateChannel](images/CreateChannel.png)

## AddUsersToChannel
This task adds a list of users based on their email addresses

![AddUsersToChannel](images/AddUsersToChannel.png)

## postMessage
This task posts a message to a slack channel based on the channel's ID

![postMessage](images/postMessage.png)

## Adding Slack App
This plugin needs a **Slack** to communicate.  You can create a custom app to to by doing the following:

1. Got to [https://api.slack.com/apps](https://api.slack.com/apps) to start building your app

  ![YourApps](images/yourapps.png)

2. **Create a Slack App** - provide *App Name* and *Workspace*

  ![createaslackapp](images/createaslackapp.png)

3. **Add features and functionality** - *Incoming Webhooks* & *Permissions*

  a. **Incoming Webhooks**

  ![incomingwebhooks](images/incomingwebhooks.png)

  Keep track of the `Webhook URL`.  This will be the URL for sending notifications.

  b. **Permissions**

  ![permissions](images/permissions1.png)
  ![permissions](images/permissions2.png)
  ![permissions](images/permissions3.png)

  Add **Slack Permissions** as follows:
  - Access information about user's public channels `channels:read`
  - Modify your private channels `channels:write`
  - Post to specific channels in Slack `incomming-webhook`
  - Add a bot user with the username *@<botname>* `chat:write:bot`
  - Access your workspace's profile information `users:read`
  - View email addresses of people on this workspace `users:read.email`

  Keep track of the `OAuth Token` and **Reinstall App**

  Use the `Webhook URL` and the `OAuth Token` to configure the connection in *XL Release*


---
## References:
* [Slack Rest API](https://api.slack.com/web)
* [Slack Rest API->Create Channel](https://api.slack.com/methods/channels.create)
* [Slack Rest API->Create Conversation](https://api.slack.com/methods/conversations.create)
* [Slack Rest API->Channels Invite](https://api.slack.com/methods/channels.invite)
* [Slack Rest API->Users Info](https://api.slack.com/methods/users.info)
* [Slack Rest API->Chat Post Message](https://api.slack.com/methods/chat.postMessage)
* [Slack Rest API->lookup By Email](https://api.slack.com/methods/users.lookupByEmail)
