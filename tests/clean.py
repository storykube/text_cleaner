#!/usr/bin/python3
from text_cleaner import Clean

text = "The agency was expected to choose two of the three teams\", so SpaceX's selection was unexpected. SpaceX " \
       "chose the third from among the four, and made it its preferred vehicle to\" fly a mission in the next two " \
       "years. The SN11 prototype rocket stands on the launchpad at the company's facility in Boca Chica, Texas." \
       "Let's try to write a website domain www.storykube.com, does it work? Also:. this is the #hashtag of this post. " \
       "For example this is a number with letter later 2.B than start another text.But now we need to fix that " \
       "bottles.He knows it. "

r = Clean.that(text)

print(r)
