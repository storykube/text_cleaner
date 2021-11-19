#!/usr/bin/python3

import logging
import re
from copy import deepcopy
from .unicode import unicode_simplify_punctuation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Clean:
    MIN_SENT_LENGTH = 20

    @staticmethod
    def remove_tags(text):
        cleaner = re.compile("<.*?>")
        clean_text = re.sub(cleaner, "", text)
        return clean_text

    @staticmethod
    def check_html(text) -> str:

        text = unicode_simplify_punctuation(text)

        # useless empty paragraph or error during generation of paragraph html tag (in case of html body)
        text = text.replace("<p></p>", "")
        text = text.replace(". </p>", ".</p> ")
        text = text.replace(".</p>.", ".</p>")

        # useless dot after blockquote
        text = text.replace("</blockquote>.", "</blockquote>")
        text = text.replace("</blockquote><p>.", ".</blockquote><p>")

        # it's no-sense to keep the comma after new paragraph
        text = text.replace("</blockquote><p>,", "</blockquote><p>")
        text = text.replace("</blockquote><p> ,", "</blockquote><p>")

        # fix introduction missing dot
        text = text.replace("</li></ul></div><p>.", ".</li></ul></div><p>")

        # Remove wrong char positioned
        text = text.replace(' "</p>', '"</p>')
        # ^ theoretically, there must be a blockquote or anyway, not any space before.

        # last change to review paragraphs
        # remove empty paragraph, double dot
        text = text.replace(".</p><p>.", "")

        # remove empty paragraph, double dot and space
        text = text.replace("</p> <p>.", "</p>")

        # remove empty paragraph with space char
        text = text.replace("<p>&nbsp;</p>", "")
        # text = text.replace("<p>.</p>", "")  # remove empty paragraph, with unique dot
        text = text.replace("<p></p>", "")  # remove totally empty p
        # remove empty paragraph with space in between
        text = text.replace("<p> </p>", "")
        text = text.replace("<p> ", "<p>")

        text = text.replace("<p><p>", "<p>")  # remove duplicate
        text = text.replace("</p></p>", '</p>')
        text = text.replace("<p><p class", "<p class")

        # fix classname separated from the equal sign, due the quote whitespace replaced below.
        text = text.replace('= "', '="')
        text = text.replace('" >', '">')

        text = text.replace(
            '"""', '"')  # to avoid error for class="""something"""
        text = text.replace('""', '"')

        return text

    @staticmethod
    def that(input_text, remove_tags=True) -> str:

        text = deepcopy(input_text)

        # Improve the \n
        text = text.replace("\n", '. ')

        # Fix some punctuation errors
        text = text.replace('.. ', '. ')
        text = text.replace(':.. ', ': ')
        text = text.replace(':. ', ': ')

        # Clean text from wrong repeated quotes.
        text = text.replace('“““', '“')  # open apices (x3)
        text = text.replace('““', '“')  # open apices (x2)
        text = text.replace('”””', '”')  # close apices (x3)
        text = text.replace('””', '”')  # close apices (x2)
        text = text.replace('“”', '')  # empty

        # removing double space (replace with only one)
        text = text.replace("  ", " ")

        text = text.replace("*", "")  # useless star *

        text = text.replace("--", "")

        text = text.replace(" `` ", ' "')
        text = text.replace(" ``", ' "')
        text = text.replace("``", '"')

        text = text.replace(" '' ", '" ')
        text = text.replace("'' ", '" ')
        text = text.replace("'' ", '" ')

        text = text.replace(" ` ", " \"")
        text = text.replace(" `", " \"")
        text = text.replace('.".', '."')

        # restore doubled quotes
        text = re.sub(r'(^|\s)\"', " “", text)
        text = re.sub(r'\"\s', "” ", text)
        text = re.sub(r'\"\.', "”.", text)
        text = re.sub(r'\"\,', "”,", text)
        text = re.sub(r'\"\-', "”-", text)
        text = re.sub(r'\"\s\-', "” -", text)
        text = re.sub(r'\"$', "”", text)

        text = re.sub('’’', "”", text)
        # example: “They played around with a third party … but decided against any deal,’’ a source said.
        text = re.sub('’ ’', "”", text)

        text = text.replace('"', '“')  # latest tentative, classic replace.

        # single quote replace.
        res = re.findall('‘(.*?)’', text)
        for r in res:
            if len(r) <= 200:
                text = text.replace('‘' + r + '’', '«' + r + '»')

        # if those ’ remain in the text, then:
        # ’
        text = text.replace("\u2019", "'")

        text = text.replace('”~“', '”')
        text = text.replace('”~ “', '”')

        text = text.replace('”~', '”')
        text = text.replace('””', '”')

        text = text.replace(' ”', '” ')
        text = text.replace('“ ', ' “')
        text = text.replace('“', ' “')
        text = text.replace('”', '” ')

        text = text.replace("’", "'")

        # Issues here. Better to skip.
        # for x in range(5):
        #     res = re.findall('“(.*?)”', text)
        #     for r in res:
        #         original_sent = deepcopy(r)
        #         if len(r) <= 300:
        #             r = r.replace('”', '')
        #             text = text.replace(original_sent, r)

        text = text.replace("?.", "?")
        text = text.replace("!.", "!")

        if remove_tags:
            text = Clean.remove_tags(text)
        else:
            # protect quotes in the html attributes
            res_q = re.findall('<(.*?)>', text)
            print(res_q)
            for r in res_q:
                original_sent = deepcopy(r)
                r = r.replace('”', '"')
                r = r.replace('“', '"')
                r = r.replace(' "', '"')
                text = text.replace(original_sent, r)

        # add spaces after ?!  - only if you have a word after with first char uppercase only.
        text = re.sub(r'(?<=[?!.])(?=[A-Z]{1,20}[a-z]*[^\s])', r' ', text)

        # paragraph or notes marks
        ac = -1
        while ac < 101:  # While the value of the variable a is less than 101 do the following:
            ac += 1
            text = text.replace(f' [{str(ac)}] ', '')
            text = text.replace(' { ' + str(ac) + ' } ', '')
            text = text.replace(f' ({str(ac)} ', '')

        # duplicate chars:
        text = text.replace("----", "-")
        text = text.replace("---", "-")
        text = text.replace("--", "-")

        # dash
        text = text.replace(" - ", "-")
        text = text.replace("- ", "-")
        text = text.replace(" -", "-")
        text = text.replace("—", ",")

        text = text.replace("___", "")

        # common errors from AI
        text = text.replace(" ' t ", "'t ")  # don't
        text = text.replace(" ' s ", "'s ")  # genitive's
        text = text.replace(" ' m ", "'m ")  # I'm
        text = text.replace(" ' ll ", "'ll ")  # we'll
        text = text.replace(" ' d ", "'d ")  # I'd like to...
        text = text.replace(" ' ve ", "'ve ")  # We've
        text = text.replace(" ' re ", "'re ")  # We're
        text = text.replace("' t ", "'t ")
        text = text.replace("' s ", "'s ")
        text = text.replace("' m ", "'m ")
        text = text.replace("' ll ", "'ll ")
        text = text.replace("' d ", "'d ")
        text = text.replace("' ve ", "'ve ")
        text = text.replace("' re ", "'re ")

        text = text.replace("\"i'", "\"I'")
        text = text.replace(". i'", ". I'")

        text = text.replace(",.", ".")
        text = text.replace('."', '. "')

        text = text.replace(" ,", ",")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")
        text = text.replace(" :", ":")
        text = text.replace(" %", "%")

        text = text.replace("( ", "(")
        text = text.replace("[ ", "[")
        text = text.replace(" )", ")")
        text = text.replace(" ]", "]")
        text = text.replace(" .)", ").")
        text = text.replace("[?]", "")

        # Wrong symbols. It's better to remove them.
        text = text.replace(".).", "")
        text = text.replace(".(.", "")

        text = text.replace('()', '')
        text = text.replace('[]', '')

        # if start with wrong char
        if text.lower().startswith((",", ";", "|", "-", "!", ".", "?", ")", "/", "\\", "]")):
            text = text[1:]
            text = text.strip()

        # removing double space (replace with only one) after sentences join
        text = text.replace("  ", " ")

        # parenthesis fix
        text = text.replace("( ", "(")
        text = text.replace("[ ", "[")
        text = text.replace(" )", ")")
        text = text.replace(" ]", "]")
        text = text.replace(" .)", ").")

        # Remove emoji
        re_emoji = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
        text = re_emoji.sub(r"", text)

        # am / pm
        text = text.replace(" AM ", " a.m. ")
        text = text.replace(" PM ", " p.m. ")
        text = text.replace(" p. M.", " p.m.")
        text = text.replace(" a. M.", " a.m.")
        text = text.replace(" a.M.", " a.m.")
        text = text.replace(" p.M.", " p.m.")
        text = text.replace(" a.M", " a.m.")
        text = text.replace(" p.M", " p.m.")
        text = text.replace(" a. M", " a.m.")
        text = text.replace(" p. M", " p.m.")

        text = text.replace(" U. S.", " U.S.")
        text = text.replace(" u. S.", " U.S.")
        text = text.replace(" u. s.", " U.S.")

        # If sep is not specified or is None, a different splitting algorithm is applied: runs of consecutive
        # whitespace are regarded as a single separator, and the result will contain no empty strings at the start or
        # end if the string has leading or trailing whitespace.
        text = " ".join(text.split(sep=None))

        quotes_match = re.findall('“|”', text)
        if len(quotes_match) > 0:
            if quotes_match[0] == '”' and len(text.split('”')[0]) < 150:
                text = '“' + text
            if quotes_match[-1] == '“' and len(text.split('“')[-1]) < 150:
                text = text + '”'

        return text

    @staticmethod
    def replace_from_right(text: str, original_text: str, new_text: str) -> str:
        """ Replace first occurrence of original_text by new_text. """
        return text[::-1].replace(original_text[::-1], new_text[::-1], 1)[::-1]
