# Tootbot

[![Repo](https://img.shields.io/badge/repo-Codeberg.org-blue)](https://codeberg.org/MarvinsMastodonTools/tootbot)
[![Downloads](https://pepy.tech/badge/tootbot)](https://pepy.tech/project/tootbot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked against](https://img.shields.io/badge/Checked-Safety--DB-blue)](https://pyup.io/safety/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tootbot)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tootbot)
[![CI / Woodpecker](https://ci.codeberg.org/api/badges/MarvinsMastodonTools/tootbot/status.svg)](https://ci.codeberg.org/MarvinsMastodonTools/tootbot)

This is a Python bot that looks up posts from specified subreddits and automatically posts them on [Mastodon][1].
It is based on [reddit-twitter-bot][2].

---

### !!! Tootbot no longer supports posting to Twitter. !!!

If you need twitter functionality look into [reddit-twitter-bot][2] as a possible alternative.

### !!! Tootbot no longer supports deleting old toots. !!!

If you'd like to delete older toots from your Mastodon account look into [MastodonAmnesia][3] as a tool that might
work for you.


---

**Features:**

* Tootbot posts to [Mastodon][1]
* Media from direct links, Gfycat, Imgur, Reddit, and Giphy is automatically attached in the social media post.
  Tootbot attaches up to the first 4 pictures for imgur albums and reddit gallery posts.
* Links that do not contain media can be skipped, ideal for meme accounts like [@babyelephantgifs][4]
* NSFW content, spoilers, and self-posts can be filtered
* Tootbot can monitor multiple subreddits at once
* Tootbot is fully open-source, so you don't have to give an external service full access to your social media accounts
* Tootbot also checks the sha256 checksum of media files to stop posting of the same media file from different subreddits.
* Tootbot can ping a [Healthchecks][5] instance for monitoring continuous operation of Tootbot
* Optionally throttle down frequency of tooting when mastodon errors are detected.

## Disclaimer

The developers of Tootbot hold no liability for what you do with this script or what happens to you by using this
script. Abusing this script *can* get you banned from Mastodon, so make sure to read up on proper usage of the API
for each site.

## Setup and usage

For instructions on setting up and using Tootbot, please visit [the wiki][6]

## Supporting Tootbot

There are a number of ways you can support Tootbot:

- Create an issue with problems or ideas you have with/for Tootboot
- You can [buy me a coffee][7].
- You can send me small change in Monero to the address below:

Monero donation address:
`87C65WhSDMhg4GfCBoiy861XTB6DL2MwHT3SWudhjR3LMeGEJG8zeZZ9y4Exrtx5ihavXyfSEschtH4JqHFQS2k1Hmn2Lkt`

[1]: https://joinmastodon.org/
[2]: https://github.com/rhiever/reddit-twitter-bot
[3]: https://pypi.org/project/mastodonamnesia/
[4]: https://botsin.space/@babyelephantgifs
[5]: https://healthchecks.io/
[6]: https://codeberg.org/MarvinsMastodonTools/tootbot/wiki
[7]: https://www.buymeacoffee.com/marvin8
