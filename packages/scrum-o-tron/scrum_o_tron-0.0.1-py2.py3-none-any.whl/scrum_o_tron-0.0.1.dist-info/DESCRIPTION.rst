Slack BOT that implements a very simple standup.
================================================

[![Build Status](https://travis-ci.org/CustardCat/scrum-o-tron.png)](https://travis-ci.org/CustardCat/scrum-o-tron)


Usage
-----

* scrumotron

Invite the scrumotron user to a channel.

Commands:

* !standup start - Starts the standup and clears out old standup data.
* !standup message - Adds message to the standup
* !standup - shows the current messages in the standup

Configuration
-------------

Environment Variables:

* SLACK_BOT_NAME=scrum-o-tron
* SLACK_BOT_TOKEN=xxx

Obtain the name and token from Slack by creating a new bot.

Installation
------------

* python setup.py install

Development
-----------

* pip install -r requirements.txt
* python setup.py test
* python setup.py develop


