# Pussybot
Pussybot, a Discord bot developed by `gravy#0001` for [LDF](https://discord.gg/rwqTbbxzAN). Based on Previous code also written by `gravy#0001`.



## Setup
This will guide you through the steps of setting up pussybot to use in your own server. **Note that pussybot is designed for 1 server only and will not work on multiple servers, most of the commands are global but the events are not.**

First, connecting to our databases.
Pussybot already handles connecting to databases, but you will need to give us some information *about* it.

**JSON** (config: *make sure to put in a .json file*)
```json
{
	"host": "1.1.1.1",
	"user": "root",
	"password": "password",
	"database": "mydb",
	"raise_on_warnings": true
}
```

**Python** config:
```py
config  = {
	"host": "1.1.1.1",
	"user": "root",
	"password": "password",
	"database": "mydb",
	"raise_on_warnings": True,
}
```

Next, adding the bot token.

At the bottom of `master/pussybot.py` you should see this:

```py
with open("tkn.json") as f:
	token = json.load(f)["token"]
	bot.run(f"{token}")
```

You can go ahead and remove the first two lines and just paste your token in there, *or* you could make a json file that should look like this:

```json
{
	"token": "aaaaaaaaaaa"
}
```
named `tkn.json`

<details>
<summary>Don't have a token? Click me!</summary>
	Everything is here: https://discord.com/developers/applications
	**note: you will need to be logged in to your Discord account on your browser**

	![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/start.png)![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/create.png)
	![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/botnav.png)![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/addbot.png)![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/doit.png)![profile](https://raw.githubusercontent.com/adenviney/pussybot/master/imgs/token.png) This string of characters is your token. **Do not share this with anybody, they can (and will) take control of your bot.** This repository is not responsible if someone shares this.

</details>



And that's about it, pussybot should be good to go, just make sure you have [Python](https://python.org) installed and run it using `python pussybot.py` in the CLI (command prompt)
