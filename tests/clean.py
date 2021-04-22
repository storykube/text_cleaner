#!/usr/bin/python3
from text_cleaner import Clean

text = "“ON YOUTUBE FRIDAY morning, [3] several hundred viewers watched $ 5.100,40 a live” ?animated video of a female " \
    "Minecraft avatar with bare breasts opening a present full of the poop emoji. In the video’s thumbnail, " \
    "two inflated breasts held up a poop Minecraft brick." \
    "It’s one of several disturbing and grotesque animated Minecraft videos identified by WIRED featured YouTubes " \
    "Minecraft Topic page, a content-sorting feature introduced in 2019. Similar Minecraft-style thumbnails found " \
    "there include an avatar with heart eyes and a bloody knife smiling at a chained-up woman in a bikini, " \
    "a mother and father holding sticks up to a crying toddler, and a woman pregnant with feces about to sit on a " \
    "man. The live videos loop for hours on end, some racking up tens of thousands of total views. Some of these " \
    "channels receive tens of thousands of views a day." \
    "In 2017, in an incident later referred to as Elsagate, journalists discovered hundreds of graphically sexual or " \
    "violent YouTube videos masquerading as “child-friendly” on the platform’s age-appropriate YouTube Kids " \
    "app. These videos, which depicted child abuse, murder, and other R-rated content, often popular children’s " \
    "TV characters like Peppa Pig or Frozen’s Elsa, or hid under innocuous titles, which apparently them fly under " \
    "the radar of YouTube’s algorithms. They were also created by independent animators. In response, YouTube  " \
    "over 150,000 videos and removed ads on 2 million. " \
    "YouTube’s Elsagate purge challenged some of the obvious ways unscrupulous content creators targeted kids, " \
    "one of YouTube’s biggest audiences. But since 2017, YouTube has added several new discoverability: topics, " \
    "hashtag pages, and video game directories. And while it’s not quite as easy to find compromisin of Peppa Pig " \
    "on YouTube right now, a WIRED investigation has unearthed of opportunistic channels targeting Minecraft and " \
    "Among Us fans. " \
    "While the videos in question did not seem to be present on the YouTube Kids app, over half most-viewed videos " \
    "on YouTube proper are marketed to children. Nursery rhymes and educational videos entertain and soothe children " \
    "whose parents need a break. And parents play them over and over again, often racking up millions of. A lot of " \
    "child-targeted videos are manufactured by official channels that own the IP to kids’ favorite characters; " \
    "others are low-budget animations by third parties cashing in on kids’ insatiable” for streaming distractions. "

r = Clean.that(text)

print(r)