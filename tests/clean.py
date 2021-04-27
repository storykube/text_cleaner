#!/usr/bin/python3
from text_cleaner import Clean

text = "““\"The agency was expected to choose two of the three teams, so SpaceX's selection was unexpected. SpaceX " \
       "chose the third from among the four, and made it its preferred vehicle to fly a mission in the next two " \
       "years. The SN11 prototype rocket stands on the launchpad at the company's facility in Boca Chica, Texas. "

r = Clean.that(text)

print(r)