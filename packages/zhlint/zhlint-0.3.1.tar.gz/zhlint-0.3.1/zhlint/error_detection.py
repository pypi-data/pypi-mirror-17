# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import re
from operator import methodcaller
from collections import defaultdict
# import itertools

from zhlint.utils import (
    TextElement,
    count_newlines,
    count_offset,
    try_invoke
)


ZH_CHARACTERS = (
    r'[\u4e00-\u9fff]'
)

ZH_SYMBOLS = (
    r'['
    r'\u3000-\u303f'
    r'\uff00-\uff0f'
    r'\uff1a-\uff20'
    r'\uff3b-\uff40'
    r'\uff5b-\uff64'
    r'\uffe0-\uffee'
    r']'
)


# 1: a.
# 2: whitespaces.
# 3: b.
def single_space_patterns(
        a, b,
        a_join_b=True, b_join_a=True,
        a_non_preceding='', b_non_preceding=''):

    def join_non_preceding(non_preceding, text):
        if non_preceding:
            return r'(?:(?<!{0}))({1})'.format(non_preceding, text)
        else:
            return r'({0})'.format(text)

    # 1. no space.
    # prefix check.
    p11 = r'{a_component}(){b_component}'
    # suffix check.
    p12 = r'{b_component}(){a_component}'

    # 2. more than one whitespaces.
    # prefix check.
    p21 = (
        r'{a_component}'
        r'((?:(?!\n)\s){{2,}})'
        r'{b_component}'
    )
    # suffix check.
    p22 = (
        r'{b_component}'
        r'((?:(?!\n)\s){{2,}})'
        r'{a_component}'
    )

    # 3. wrong single whitespace: [\t\r\f\v]
    # only allow ' ' and '\n'.
    # prefix check.
    p31 = (
        r'{a_component}'
        r'((?:(?![ \n])\s){{1}})'
        r'{b_component}'
    )
    # suffix check.
    p32 = (
        r'{b_component}'
        r'((?:(?![ \n])\s){{1}})'
        r'{a_component}'
    )

    patterns = []
    if a_join_b:
        patterns.extend([
            p11,
            p21,
            p31,
        ])
    if b_join_a:
        patterns.extend([
            p12,
            p22,
            p32,
        ])

    return list(map(
        methodcaller(
            'format',
            a_component=join_non_preceding(a_non_preceding, a),
            b_component=join_non_preceding(b_non_preceding, b),
        ),
        patterns,
    ))


# 1: a.
# 2: whitespaces.
# 3: b.
def no_space_patterns(a, b):

    # prefix check.
    p1 = (
        r'({0})'
        r'((?:(?!\n)\s)+)'
        r'({1})'
    )
    # suffix check.
    p2 = (
        r'({1})'
        r'((?:(?!\n)\s)+)'
        r'({0})'
    )

    return list(map(
        methodcaller('format', a, b),
        [p1, p2],
    ))


def detect_by_patterns(patterns, element, ignore_matches=set()):

    for pattern in patterns:
        for m in re.finditer(pattern, element.content, re.UNICODE):
            if m.group(0) in ignore_matches:
                continue
            yield m


def detect_e101(element):

    return detect_by_patterns(
        single_space_patterns(ZH_CHARACTERS, r'[a-zA-z]'),
        element,
    )


def detect_e102(element):

    return detect_by_patterns(
        single_space_patterns(ZH_CHARACTERS, r'\d'),
        element,
    )


def detect_e103(element):

    p = (
        # non-digit, non-chinese
        r'(?:(?!\d|{0}|{1}|[!-/:-@\[-`{{-~]|\s))'
        # ignore ％, ℃, x, n.
        r'[^\uff05\u2103xn\%]'
    )
    p = p.format(ZH_CHARACTERS, ZH_SYMBOLS)

    return detect_by_patterns(
        single_space_patterns(
            r'\d+',
            p,
            b_join_a=False,
            a_non_preceding='\w',
        ),
        element,
    )


# 1: whitespaces.
# 2: left parenthesis.
# 3: digits.
# 4: right parenthesis.
def detect_e104(element):

    p1 = (
        r'(?<=[^\s]{1})'
        r'(\s*)'
        r'([(\uff08])'
        r'(\d+)'
        r'([)\uff09])'
    )

    # cover
    p2 = (
        r'(?:^|\n)'
        r'(\s*)'
        r'([(\uff08])'
        r'(\d+)'
        r'([)\uff09])'
    )

    patterns = [p1, p2]
    for i, p in enumerate(patterns):
        for m in detect_by_patterns([p], element):
            yield_tag = None
            if m.group(2) != '(' or m.group(4) != ')':
                yield_tag = 0
            # preceded by non-whitespace.
            if i == 0 and m.group(1) not in (' ', '\n'):
                yield_tag = 1
            # preceded by nothing or newline.
            if i == 1 and m.group(1) != '':
                yield_tag = 2

            if yield_tag is not None:
                yield m, yield_tag


def detect_e203(element):

    return detect_by_patterns(
        no_space_patterns(
            ZH_SYMBOLS,
            r'(?:(?!{0}|\s)).'.format(ZH_SYMBOLS),
        ),
        element,
    )


# 1: ellipsis.
def detect_e205(element):

    p = r'(\.{2,}|。{2,})'
    for m in re.finditer(p, element.content, flags=re.UNICODE):
        detected = m.group(0)
        if detected[0] != '.' or len(detected) != 6:
            yield m


# 1: duplicated marks.
def detect_e206(element):

    p1 = r'([!！]{2,})'
    p2 = r'([?？]{2,})'

    return detect_by_patterns(
        [p1, p2],
        element,
    )


# 1: ~
def detect_e207(element):

    p1 = r'(~+)'

    return detect_by_patterns(
        [p1],
        element,
    )


def contains_chinese_characters(content):
    return re.search(ZH_CHARACTERS, content, re.UNICODE)


def delimiter_in_email(content, m):
    OFFSET = 20
    i = m.start()
    lb = max(0, i - OFFSET)
    ub = i + OFFSET + 1

    segment = content[lb:ub]
    i = min(i, OFFSET)

    EMAIL = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    for email_m in re.finditer(EMAIL, segment):
        if email_m.start() <= i < email_m.end():
            return True
    return False


# simple url and filename.
def delimiter_in_simple_uri(content, m):
    i = m.start()

    if content[i] == '.':
        if i == 0 or i == len(content) - 1:
            return False
        else:
            return content[i - 1].isalnum() and content[i + 1].isalnum()

    if content[i] == ':':
        return i + 2 < len(content) and content[i:i + 3] == '://'

    return False


def delimiter_in_latex_punctuation(content, m):
    i = m.start()

    if content[i] not in ('\\', '(', ')'):
        return False

    if content[i] == '\\':
        return i + 1 < len(content) and content[i + 1] in ('(', ')')
    else:
        return 0 < i and content[i - 1] == '\\'


# 1: en punctuations.
# 2: whitespaces.
def detect_e201(element):
    if not contains_chinese_characters(element.content):
        return False

    def marks_pattern(pattern_template, texts):

        patterns = []
        for text in texts:
            pattern = r'(?:{0})'.format(re.escape(text))
            patterns.append(pattern)

        return pattern_template.format(r'|'.join(patterns))

    def parenthesis_ranges(content):

        ranges = []
        for m in re.finditer(r'\(\d+\)', content, flags=re.UNICODE):
            ranges.append(
                (m.start(), m.end() - 1),
            )
        return ranges

    def match_in_ranges(match, ranges):
        mi = m.start()
        mj = m.end() - 1
        for ri, rj in ranges:
            if ri <= mi <= rj or ri <= mj <= rj:
                return True
        return False

    PUNCTUATIONS = set('!"$\'(),.:;<>?[\\]^_{}')

    ret = []

    # gerneral forms, ignore common shared characters: '@#%&+*-=|~'
    p1 = r'({0})(\s*)'.format(
        r'|'.join(
            map(lambda punc: r'{0}+'.format(re.escape(punc)), PUNCTUATIONS),
        ),
    )

    patterns = [p1]
    ranges = parenthesis_ranges(element.content)

    for m in detect_by_patterns(
        patterns,
        element,
        ignore_matches=set(['......']),
    ):
        if match_in_ranges(m, ranges):
            continue
        if SpecialWordHelper.delimiter_in_word(element.content, m):
            continue
        if delimiter_in_email(element.content, m):
            continue
        if delimiter_in_simple_uri(element.content, m):
            continue
        if delimiter_in_latex_punctuation(element.content, m):
            continue

        if m.group(1) != '$$':
            ret.append(m)

    return ret


# 1: chineses.
def detect_e202(element):
    if contains_chinese_characters(element.content):
        return False

    return detect_by_patterns(
        ['({0})'.format(ZH_SYMBOLS)],
        element,
    )


# 1: wrong 「」.
def detect_e204(element):
    if not contains_chinese_characters(element.content):
        return False

    p = (
        r'('

        # ', " is handled by E201.
        # r"'"
        # r'|'
        # r'"'
        # r'|'

        # ‘’
        r'\u2018|\u2019'
        r'|'
        # “”
        r'\u201c|\u201d'

        r')'
    )
    return detect_by_patterns(
        [p],
        element,
    )


class SpecialWordHelper(object):

    WORD_PATTERN = {
        'App': r'app',
        'Android': r'android',
        'iOS': r'ios',
        'iPhone': r'iphone',
        'App Store': r'app\s?store',
        'WiFi': r'wi-*fi',
        'email': r'e-*mail',
        'P.S.': r'P\.*S\.*',
    }

    WORD_MAX_LENGTH = None
    SENTENCE_DELIMITER_TO_WORD = None

    @classmethod
    def init(cls):
        if cls.WORD_MAX_LENGTH and cls.SENTENCE_DELIMITER_TO_WORD:
            return

        delimiters = [
            '!', ';', '.', '?',
            '\uff01', '\uff1b', '\u3002', '\uff1f',
        ]

        cls.SENTENCE_DELIMITER_TO_WORD = defaultdict(list)
        for delimiter in delimiters:
            for word in cls.WORD_PATTERN:
                if delimiter not in word:
                    continue
                cls.SENTENCE_DELIMITER_TO_WORD[delimiter].append(word)

        cls.WORD_MAX_LENGTH = 0
        for word in cls.WORD_PATTERN:
            cls.WORD_MAX_LENGTH = max(cls.WORD_MAX_LENGTH, len(word))

    @classmethod
    def select_segment(cls, content, match):
        segment_begin = max(
            0,
            match.end() - SpecialWordHelper.WORD_MAX_LENGTH,
        )
        segment_end = min(
            len(content) - 1,
            match.start() + SpecialWordHelper.WORD_MAX_LENGTH,
        )
        return content[segment_begin:segment_end]

    @classmethod
    def delimiter_in_word(cls, content, match):
        delimiter = match.group(1)
        if delimiter not in cls.SENTENCE_DELIMITER_TO_WORD:
            return False

        segment = cls.select_segment(content, match)
        for word in cls.SENTENCE_DELIMITER_TO_WORD.get(delimiter, []):
            if segment.find(word) >= 0:
                return True
        return False


SpecialWordHelper.init()


# 1: wrong special word.
def detect_e301(element):

    for correct_form, pattern in SpecialWordHelper.WORD_PATTERN.items():

        # (?<!xxx) and (?!xxx) could match ^ and $.
        p = r'(?<![a-zA-Z])({0})(?![a-zA-Z])'.format(pattern)

        for m in re.finditer(
            p, element.content,
            flags=re.UNICODE | re.IGNORECASE,
        ):
            if m.group(0) != correct_form:
                yield m, correct_form


def process_errors_by_handler(error_codes, error_handler, element):

    for error_code in error_codes:
        detector = globals()['detect_{0}'.format(error_code.lower())]
        error_handler(error_code, element, detector(element))


def process_block_level_errors(error_handler, element):

    process_errors_by_handler(
        [
            'E101',
            'E102',
            'E103',
            'E104',

            'E203',
            'E205',
            'E206',
            'E207',

            'E301',
        ],
        error_handler,
        element,
    )


def split_text_element(element):

    # block_type should be split by newline first.
    SPLIT_BY_NEWLINES = [
        'list_block',
        'table',
    ]

    elements = []
    if element.block_type not in SPLIT_BY_NEWLINES:
        elements.append(element)
    else:
        content = element.content
        loc_begin = element.loc_begin

        if not content.strip('\n'):
            return []
        else:
            content = content.strip('\n')
            for line in content.split('\n'):
                elements.append(
                    TextElement(
                        'paragraph',
                        loc_begin, loc_begin,
                        line,
                    )
                )
                loc_begin += 1

    # split sentences.
    SENTENCE_DELIMITERS = (
        r'('
        r'\.{6}'
        r'|'
        r'!|;|\.|\?'
        r'|'
        r'\uff01|\uff1b|\u3002|\uff1f'
        r')'
    )

    OPEN_PARENTHESIS = set(
        '('
        '['
        "'"
        '"'
        '（'
        '「'
        '『'
    )
    CLOSE_PARENTHESIS = set(
        ')'
        ']'
        "'"
        '"'
        '）'
        '」'
        '』'
    )

    sentences = []

    for element in elements:
        content = element.content.strip('\n')

        loc_begin = element.loc_begin
        sbegin = 0

        for m in re.finditer(SENTENCE_DELIMITERS, content, flags=re.UNICODE):
            # ignore delimiter within special words.
            if SpecialWordHelper.delimiter_in_word(content, m):
                continue
            if delimiter_in_email(content, m):
                continue
            if delimiter_in_simple_uri(element.content, m):
                continue

            send = m.end()
            tailing_newlines = 0
            while send < len(content) and content[send] == '\n':
                send += 1
                tailing_newlines += 1

            sentence = content[sbegin:send]

            level = 0
            for c in sentence:
                if c in OPEN_PARENTHESIS:
                    level += 1
                elif c in CLOSE_PARENTHESIS:
                    level -= 1
            if level != 0:
                continue

            newlines = count_newlines(sentence)
            offset = count_offset(content[:sbegin])

            sentences.append(
                TextElement(
                    'paragraph',
                    loc_begin,
                    loc_begin + newlines - tailing_newlines,
                    sentence,
                    offset=offset,
                )
            )

            loc_begin += newlines
            sbegin = send

        if sbegin < len(content):
            sentences.append(
                TextElement(
                    'paragraph',
                    loc_begin, loc_begin,
                    content[sbegin:],
                    offset=count_offset(content[:sbegin]),
                )
            )
    return sentences


def process_sentence_level_errors(error_handler, element):

    process_errors_by_handler(
        [
            'E201',
            'E202',
            'E204',
        ],
        error_handler,
        element,
    )


def process_errors(error_handler, element):

    try_invoke(error_handler, 'before_block_level')
    process_block_level_errors(error_handler, element),
    try_invoke(error_handler, 'after_block_level')

    try_invoke(error_handler, 'before_sentence_level')
    for sentence in split_text_element(element):
        process_sentence_level_errors(error_handler, sentence)
    try_invoke(error_handler, 'after_sentence_level')
