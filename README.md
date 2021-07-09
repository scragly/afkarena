# AFK Arena API.

Simple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global.

> **Note:** This wrapper is unofficial and is not associated with nor endorsed by Lilith Games.

The logic of this library has been part of my Discord bot, [Dreaf](https://github.com/scragly/Dreaf), ever since AFK Arena changed to the external gift code redemption site. Due to the increased interest of community members on making use of this unofficial API, and the fact that this logic is currently being used across two seperate projects of my own, I figured it's time to make the API interactions standalone to ease maintenance and keep the feature scope focused on the essentials of its functionality.

## Install

```
pip install afkarena
```

## Requirements

- Python 3.9+
- aiohttp 3.7+

## How to use

```python
# create a Player object for the main user account.
player = Player(main_user_id)

# authenticate using the authentication code in game settings.
await player.verify(authentication_code)

# fetch data of all linked user accounts
await player.fetch_users()

# redeem one or more gift codes for all linked user accounts
results = await player.redeem_codes(gift_code_one, gift_code_two)

# view code redemption results
print(results)
```
