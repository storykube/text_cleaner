#!/usr/bin/python3

import copy
import hashlib
import logging
import re
from copy import deepcopy

from sentence_tokenizer import SentenceTokenizer
from .unicode import unicode_simplify_punctuation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_md5_from_string(input_string: str = ''):
    if len(input_string) < 1:
        return ''
    hash_object = hashlib.md5(str(input_string).encode('utf-8'))
    key = str(hash_object.hexdigest())
    return key


class CleanStaticMem:
    cache = {}


class Clean:
    MIN_SENT_LENGTH = 20

    @staticmethod
    def valid_to_be_cleaned(text):
        if text.count('“') > 30 or text.count('”') > 30 or text.count('"') > 30:
            logger.error(
                f'The text contains a lot of weird quotes. It\'s not valid.')
            return False
        return True

    @staticmethod
    def remove_tags(text):
        cleaner = re.compile("<.*?>")
        clean_text = re.sub(cleaner, "", text)
        return clean_text

    @staticmethod
    def checkHTML(text) -> str:

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
    def that(input_text) -> str:

        text = deepcopy(input_text)

        cache_key = get_md5_from_string(input_text)
        if text in CleanStaticMem.cache.keys():
            return CleanStaticMem.cache[cache_key]

        # Clean text from wrong repeated quotes.
        text = text.replace('“““', '“')  # open apices (x3)
        text = text.replace('““', '“')  # open apices (x2)
        text = text.replace('”””', '”')  # close apices (x3)
        text = text.replace('””', '”')  # close apices (x2)

        text = Clean.remove_tags(text)
        # Add some space to between symbols
        # to separate them from chars.
        # (the double spaces must be removed
        # immediately after this).
        text = text.replace("/", " / ")

        # -------------------------------------------
        # Replace strange quotes: ‘something’
        # with "something"
        # -------------------------------------------

        text = Clean.replace_strange_quotes(text)

        # -------------------------------------------

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

        text = text.replace('." ', '". ')
        text = text.replace('" .', '".')
        text = text.replace(' ".', '".')
        text = text.replace('.".', '".')

        text = text.replace('." ', '". ')
        text = text.replace('" .', '".')
        text = text.replace(' ".', '".')
        text = text.replace(", ' \"", ', "')  # , ' " => , "

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

        text = text.replace('.” ', '”. ')
        text = text.replace(',” ', '”, ')
        text = text.replace('” .', '”.')
        text = text.replace(' ”.', '”.')

        # single quote replace.
        res = re.findall('‘(.*?)’', text)
        for r in res:
            if len(r) <= 200:
                text = text.replace('‘' + r + '’', '«' + r + '»')

        # if those ’ remain in the text, then:
        # ’
        text = text.replace("\u2019", "'")

        res = re.findall('“(.*?)”', text)
        for r in res:
            if '. “' in r:
                to_replace = deepcopy(r)
                to_replace = to_replace.replace('. “', '. ')
                text = text.replace(r, to_replace)

        # re-analyze, to get, now, only a single question mark with comma before
        res = re.findall('“(.*?)”', text)
        for r in res:
            if ', “' in r:
                to_replace = deepcopy(r)
                to_replace = to_replace.replace(', “', ' ')
                text = text.replace(r, to_replace)

        # if there is a duplicate “ “ in a short len (150chars), fix
        # ex: [...] which has been run under the “ one country, two systems “
        # becomes: [...] which has been run under the “one country, two systems”
        res = re.findall('“(.*?)“', text)
        for r in res:
            if len(r) <= 150 and '”' not in r:
                text = text.replace(r, r + '”~')

        text = text.replace('”~“', '”')
        text = text.replace('”~ “', '”')

        text = text.replace('”~', '”')
        text = text.replace('””', '”')

        text = text.replace(' ”', '” ')
        text = text.replace('“ ', ' “')
        text = text.replace('“', ' “')
        text = text.replace('”', '” ')

        text = text.replace("’", "'")

        # fix odd quotes.
        text = Clean.fix_odd_quotes(text)

        for x in range(5):
            res = re.findall('“(.*?)”', text)
            for r in res:
                original_sent = deepcopy(r)
                if len(r) <= 300:
                    r = r.replace('”', '')
                    text = text.replace(original_sent, r)

        text = text.replace("?.", "?")
        text = text.replace("!.", "!")

        # add spaces after ?!,.  - only if you have a word after.
        text = re.sub(r'(?<=[.,?!])(?=[a-zA-Z][^\s])', r' ', text)

        # domains ---------------------------------------
        text = f' {text} '
        # ^ Here, it's usefull to keep space 
        # at start and end of string.
        text = text.replace(' . com ', '.com ')
        text = text.replace('. com ', '.com ')
        text = text.replace(' .com ', '.com ')
        text = text.replace('. com,', '.com,')

        text = text.replace(' . gov ', '.gov ')
        text = text.replace('. gov ', '.gov ')
        text = text.replace(' .gov ', '.gov ')
        text = text.replace('. gov,', '.gov,')

        text = text.replace(' . it ', '.it ')
        text = text.replace('. it ', '.it ')
        text = text.replace(' .it ', '.it ')
        text = text.replace('. it,', '.it,')

        text = text.replace(' . fr ', '.fr ')
        text = text.replace('. fr ', '.fr ')
        text = text.replace(' .fr ', '.fr ')
        text = text.replace('. fr,', '.fr,')

        text = text.replace(' . uk ', '.uk ')
        text = text.replace('. uk ', '.uk ')
        text = text.replace(' .uk ', '.uk ')
        text = text.replace('. uk,', '.uk,')

        text = text.replace(' . us ', '.us ')
        text = text.replace('. us ', '.us ')
        text = text.replace(' .us ', '.us ')
        text = text.replace('. us,', '.us,')

        text = text.replace(' . pk ', '.pk ')
        text = text.replace('. pk ', '.pk ')
        text = text.replace(' .pk ', '.pk ')
        text = text.replace('. pk,', '.pk,')

        text = text.replace(' . eu ', '.eu ')
        text = text.replace('. eu ', '.eu ')
        text = text.replace(' .eu ', '.eu ')
        text = text.replace('. eu,', '.eu,')

        text = text.replace(' . ru ', '.ru ')
        text = text.replace('. ru ', '.ru ')
        text = text.replace(' .ru ', '.ru ')
        text = text.replace('. ru,', '.ru,')

        text = text.replace(' . org ', '.org ')
        text = text.replace('. org ', '.org ')
        text = text.replace(' .org ', '.org ')
        text = text.replace('. org,', '.org,')

        text = text.replace(' . net ', '.net ')
        text = text.replace('. net ', '.net ')
        text = text.replace(' .net ', '.net ')
        text = text.replace('. net,', '.net,')
        text = text.strip()
        # ------------------------------------------------

        # paragraph or notes marks
        ac = -1
        while ac < 101:  # While the value of the variable a is less than 101 do the following:
            ac += 1
            text = text.replace(f' [{str(ac)}] ', '')
            text = text.replace(' { ' + str(ac) + ' } ', '')
            text = text.replace(f' ({str(ac)} ', '')

        # duplicate chars:
        text = text.replace("????", "?")
        text = text.replace("???", "?")
        text = text.replace("??", "!")
        text = text.replace("!!!!", "!")
        text = text.replace("!!!", "!")
        text = text.replace("!!", "!")
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

        # text = text.replace(".", ". ")  # this could be separate numbers. please keep it commented.

        text = text.replace("  ", " ")  # after, dot-fix, single space, please
        text = text.replace(" . ", ". ")
        text = text.replace("  ", " ")  # after, dot-fix, single space, please
        text = text.replace(" .", ".")
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

        # capitalize first letter on every sentences.
        st = SentenceTokenizer()
        st.set(text)
        sentences = st.get()
        for sent in sentences:
            text = text.replace(sent, sent[0].upper() + sent[1:])

        # capitalize first char of news
        try:
            text = text[0].upper() + text[1:]
        except IndexError as e:
            # logger.error(e)
            pass

        # removing double space (replace with only one) after sentences join
        text = text.replace("  ", " ")

        # text = Clean.__clean_not_understandable_text(text)
        text = Clean.clean_first_parts(text)

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

        # replace the number like 33, 3333 (error with comma formatting) with 33,3333
        text = re.sub('(\d+)\,\s(\d{3,6})', r"\1,\2", text)

        # If sep is not specified or is None, a different splitting algorithm is applied: runs of consecutive
        # whitespace are regarded as a single separator, and the result will contain no empty strings at the start or
        # end if the string has leading or trailing whitespace.
        text = " ".join(text.split(sep=None))

        # If there are some ~ maybe is because the procedure
        # it was no able to clean all the stuff.
        # It's better to remove it.
        text = text.replace('~', '')

        CleanStaticMem.cache[cache_key] = text

        # I'm saving into cache also the elaborated clean text, to avoid multiple clean of the same input.
        text_cleaned_cache_key = get_md5_from_string(input_text)

        # text = unicode_simplify_punctuation(text)  # latest unicode replacement

        CleanStaticMem.cache[text_cleaned_cache_key] = text

        return text

    @staticmethod
    def fix_odd_quotes(text):
        # fix odd quotes.
        count_quotes_open = text.count('“')
        count_quotes_close = text.count('”')
        count_quotes = count_quotes_open + count_quotes_close
        if count_quotes > 0 and count_quotes % 2 != 0:  # odd results
            dict_occurs = {}
            dict_scores = {}
            quotes_occurs = re.findall(r'(“.*?”)', text)
            quotes_occurs_greedy = re.findall(r'(“.*”)', text)
            quotes_occurs.extend(quotes_occurs_greedy)
            iq = -1
            for text_quoted in quotes_occurs:
                iq += 1
                dict_scores[iq] = int(len(text_quoted))
                dict_occurs[iq] = text_quoted

            if len(dict_scores) > 0:  # if found.
                to_remove_id = max(dict_scores, key=dict_scores.get)
                to_remove_text = dict_occurs[to_remove_id]
                if count_quotes_open > count_quotes_close:
                    text = text.replace(to_remove_text, to_remove_text[1:])
                else:
                    text = text.replace(to_remove_text, to_remove_text[:-1])
        return text

    @staticmethod
    def clean_first_parts(text_string: str) -> str:

        hypothetical_introduction = text_string[:50]
        # logger.info(hypothetical_introduction)

        parenthesis_content = re.findall("\(.*?\)", hypothetical_introduction)
        for tx in parenthesis_content:
            # logger.info(tx + " deleted")
            if tx != 'SK':
                text_string = text_string.replace(" " + tx, "")

        st = SentenceTokenizer()
        st.set(text_string)
        sentences = st.get()

        for sent in sentences:

            if len(sent) >= 20:

                original_sent = deepcopy(sent)

                sent_hypothetical_intro = sent[:20]

                if ' - ' in sent_hypothetical_intro:
                    before_sep = sent_hypothetical_intro.split(' - ')[0]
                    sent = sent.replace(f"{before_sep} - ", '')

                if ' \ ' in sent_hypothetical_intro:
                    before_sep = sent_hypothetical_intro.split(' \\ ')[0]
                    sent = sent.replace(f"{before_sep} \\ ", '')

                if ' / ' in sent_hypothetical_intro:
                    before_sep = sent_hypothetical_intro.split(' / ')[0]
                    sent = sent.replace(f"{before_sep} / ", '')

                text_string = text_string.replace(original_sent, sent)

        return text_string

    @staticmethod
    def replace_from_right(text: str, original_text: str, new_text: str) -> str:
        """ Replace first occurrence of original_text by new_text. """
        return text[::-1].replace(original_text[::-1], new_text[::-1], 1)[::-1]

    @staticmethod
    def replace_strange_quotes(text: str):

        sent_tok = SentenceTokenizer()
        sent_tok.set(text)
        sentences = sent_tok.get()

        for original_sentence in sentences:

            new_sentence = deepcopy(original_sentence)

            matches = re.findall(r'\‘(.+?)\’', new_sentence)
            for strange_quote in matches:
                new_sentence = new_sentence.replace(
                    strange_quote, '~~' + strange_quote + '~~')

            new_sentence = new_sentence.replace('‘~~', ' «')
            new_sentence = new_sentence.replace('~~’', '» ')

            matches = re.findall(
                r"(^|\s)\'([a-zA-Z0-9\-\,\s]{0,150}?)\'($|\s)", new_sentence)

            for strange_quote in matches:

                for st in strange_quote:
                    if len(st.strip()) > 1:
                        new_sentence = new_sentence.replace(
                            st, '~~' + st + '~~')

            new_sentence = new_sentence.replace("'~~", ' "')
            new_sentence = new_sentence.replace("~~'", '" ')

            text = text.replace(original_sentence, new_sentence)
            text = text.replace('  ', ' ')

        return text
