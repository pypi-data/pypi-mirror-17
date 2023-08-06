"""
Functions to analyze source code and count lines in it.
"""
# Copyright (c) 2016, Thomas Aglassinger.
# All rights reserved. Distributed under the BSD License.
import codecs
import collections
import enum
import glob
import itertools
import logging
import os
import re

import pygount.common


# Attempt to import chardet.
try:
    import chardet.universaldetector
    _detector = chardet.universaldetector.UniversalDetector()
    has_chardet = True
except ImportError:
    _detector = None
    has_chardet = False

from pygments import lexers, token, util


#: Default glob patterns for folders not to analyze.
DEFAULT_FOLDER_PATTERNS_TO_SKIP_TEXT = ', '.join([
    '.*',
    '_svn',  # Subversion hack for Windows
    '__pycache__',  # Python byte code
])

SourceState = enum.Enum('SourceState', ' '.join([
    'analyzed',  # successfully analyzed
    # TODO: 'duplicate',  # source code is an identical copy of another
    'error',  # source could not be parsed
    'generated',  # source code has been genered
    # TODO: 'huge',  # source code exceeds size limit
    'unknown',  # pygments does not offer any lexer to analyze the source
]))

#: Default patterns for regular expressions to detect generated code.
#: The '(?i)' indicates that the patterns are case insensitive.
DEFAULT_GENERATED_PATTERNS_TEXT = pygount.common.REGEX_PATTERN_PREFIX + ', '.join([
    r'(?i).*automatically generated',
    r'(?i).*do not edit',
    r'(?i).*generated with the .+ utility',
    r'(?i).*this is a generated file',
    r'(?i).*generated automatically',
])

#: Default glob patterns for file names not to analyze.
DEFAULT_NAME_PATTERNS_TO_SKIP_TEXT = ', '.join([
    '.*',
    '*~',
])

_log = logging.getLogger('pygount')

_MARK_TO_NAME_MAP = (
    ('c', 'code'),
    ('d', 'documentation'),
    ('e', 'empty'),
    ('s', 'string'),
)
_BOM_TO_ENCODING_MAP = collections.OrderedDict((
    # NOTE: We need an ordered dict due the overlap between utf-32-le and utf-16-be.
    (codecs.BOM_UTF8, 'utf-8-sig'),
    (codecs.BOM_UTF32_LE, 'utf-32-le'),
    (codecs.BOM_UTF16_BE, 'utf-16-be'),
    (codecs.BOM_UTF16_LE, 'utf-16-le'),
    (codecs.BOM_UTF32_BE, 'utf-32-be'),
))
_XML_PROLOG_REGEX = re.compile(r'<\?xml\s+.*encoding="(?P<encoding>[-_.a-zA-Z0-9]+)".*\?>')
_CODING_MAGIC_REGEX = re.compile(r'.+coding[:=][ \t]*(?P<encoding>[-_.a-zA-Z0-9]+)\b', re.DOTALL)

#: Results of a source analysis derived by :py:func:`source_analysis`.
SourceAnalysis = collections.namedtuple(
    'SourceAnalysis', ['path', 'language', 'group', 'code', 'documentation', 'empty', 'string', 'state', 'state_info'])


class SourceScanner():
    def __init__(self, source_patterns, suffixes='*'):
        self._source_patterns = source_patterns
        self._suffixes = pygount.common.regexes_from(suffixes)
        self._folder_regexps_to_skip = pygount.common.regexes_from(DEFAULT_FOLDER_PATTERNS_TO_SKIP_TEXT)
        self._name_regexps_to_skip = pygount.common.regexes_from(DEFAULT_NAME_PATTERNS_TO_SKIP_TEXT)

    @property
    def source_patterns(self):
        return self._source_patterns

    @property
    def suffixes(self):
        return self._suffixes

    @property
    def folder_regexps_to_skip(self):
        return self._folder_regexps_to_skip

    @folder_regexps_to_skip.setter
    def set_folder_pattern_to_skip(self, regexps_or_pattern_text):
        self._folder_regexps_to_skip.append = pygount.common.regexes_from(
            regexps_or_pattern_text,
            self.folder_regexps_to_skip)

    @property
    def name_regexps_to_skip(self):
        return self._name_regexps_to_skip

    @name_regexps_to_skip.setter
    def set_name_regexps_to_skip(self, regexps_or_pattern_text):
        self._name_regexp_to_skip = pygount.common.regexes_from(
            regexps_or_pattern_text,
            self.name_regexps_to_skip)

    def _is_path_to_skip(self, name, is_folder):
        assert os.sep not in name, 'name=%r' % name
        regexps_to_skip = self._folder_regexps_to_skip if is_folder else self._name_regexps_to_skip
        return any(
            path_name_to_skip_regex.match(name) is not None
            for path_name_to_skip_regex in regexps_to_skip
        )

    def _paths_and_group_to_analyze_in(self, folder, group):
        assert folder is not None
        assert group is not None

        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if not os.path.islink(path):
                is_folder = os.path.isdir(path)
                if self._is_path_to_skip(os.path.basename(path), is_folder):
                    _log.debug('skip due matching skip pattern: %s', path)
                elif is_folder:
                    yield from self._paths_and_group_to_analyze_in(path, group)
                else:
                    yield path, group

    def _paths_and_group_to_analyze(self, path_to_analyse_pattern, group=None):
        for path_to_analyse in glob.glob(path_to_analyse_pattern):
            if os.path.islink(path_to_analyse):
                _log.debug('skip link: %s', path_to_analyse)
            else:
                is_folder = os.path.isdir(path_to_analyse)
                if self._is_path_to_skip(os.path.basename(path_to_analyse), is_folder):
                    _log.debug('skip due matching skip pattern: %s', path_to_analyse)
                else:
                    actual_group = group
                    if is_folder:
                        if actual_group is None:
                            actual_group = os.path.basename(path_to_analyse)
                            if actual_group == '':
                                # Compensate for trailing path separator.
                                actual_group = os.path.basename(os.path.dirname(path_to_analyse))
                        yield from self._paths_and_group_to_analyze_in(path_to_analyse_pattern, actual_group)
                    else:
                        if actual_group is None:
                            actual_group = os.path.dirname(path_to_analyse)
                            if actual_group == '':
                                actual_group = os.path.basename(os.path.dirname(os.path.abspath(path_to_analyse)))
                        yield path_to_analyse, actual_group

    def _source_paths_and_groups_to_analyze(self, patterns_to_analyze):
        assert patterns_to_analyze is not None
        result = []
        for pattern in patterns_to_analyze:
            try:
                result.extend(self._paths_and_group_to_analyze(pattern))
            except OSError as error:
                raise OSError('cannot scan "{0}" for source files: {1}'.format(pattern, error))
        result = sorted(set(result))
        return result

    def source_paths(self):
        source_paths_and_groups_to_analyze = self._source_paths_and_groups_to_analyze(self.source_patterns)

        for source_path, group in source_paths_and_groups_to_analyze:
            suffix = os.path.splitext(source_path)[1].lstrip('.')
            is_suffix_to_analyze = any(
                suffix_regexp.match(suffix)
                for suffix_regexp in self.suffixes
            )
            if is_suffix_to_analyze:
                yield source_path, group
            else:
                _log.info('skip due suffix: %s', source_path)


_LANGUAGE_TO_WHITE_WORDS_MAP = {
    'batchfile': ['@'],
    'python': ['pass'],
    'sql': ['begin', 'end']
}
for language in _LANGUAGE_TO_WHITE_WORDS_MAP.keys():
    assert language.islower()


def matching_number_line_and_regex(source_lines, generated_regexes, max_line_count=15):
    """
    The first line and its number (starting with 0) in the source code that
    indicated that the source code is generated.
    :param source_lines: lines of text to scan
    :param generated_regexes: regular expressions a line must match to indicate
        the source code is generated.
    :param max_line_count: maximum number of lines to scan
    :return: a tuple of the form ``(number, line, regex)`` or ``None`` if the
        source lines do not match any ``generated_regexes``.
    """
    initial_numbers_and_lines = enumerate(itertools.islice(source_lines, max_line_count))
    matching_number_line_and_regexps = (
        (number, line, matching_regex)
        for number, line in initial_numbers_and_lines
        for matching_regex in generated_regexes
        if matching_regex.match(line)
    )
    possible_first_matching_number_line_and_regexp = list(
        itertools.islice(matching_number_line_and_regexps, 1))
    result = (possible_first_matching_number_line_and_regexp + [None])[0]
    return result


def white_characters(language_id):
    """
    Characters that count as white space if they are the only characters in a
    line.
    """
    assert language_id is not None
    assert language_id.islower()
    return '(),:;[]{}'


def white_code_words(language_id):
    """
    Words that do not count as code if it is the only word in a line.
    """
    assert language_id is not None
    assert language_id.islower()
    return _LANGUAGE_TO_WHITE_WORDS_MAP.get(language_id, set())


def _delined_tokens(tokens):
    for token_type, token_text in tokens:
        newline_index = token_text.find('\n')
        while newline_index != -1:
            yield token_type, token_text[:newline_index + 1]
            token_text = token_text[newline_index + 1:]
            newline_index = token_text.find('\n')
        if token_text != '':
            yield token_type, token_text


def _pythonized_comments(tokens):
    """
    Similar to tokens but converts strings after a colon (:) to comments.
    """
    is_after_colon = True
    for token_type, token_text in tokens:
        if is_after_colon and (token_type in token.String):
            token_type = token.Comment
        elif token_text == ':':
            is_after_colon = True
        elif token_type not in token.Comment:
            is_whitespace = len(token_text.rstrip(' \f\n\r\t')) == 0
            if not is_whitespace:
                is_after_colon = False
        yield token_type, token_text


def _line_parts(lexer, text):
    line_marks = set()
    tokens = _delined_tokens(lexer.get_tokens(text))
    if lexer.name == 'Python':
        tokens = _pythonized_comments(tokens)
    language_id = lexer.name.lower()
    white_text = ' \f\n\r\t' + white_characters(language_id)
    white_words = white_code_words(language_id)
    for token_type, token_text in tokens:
        if token_type in token.Comment:
            line_marks.add('d')  # 'documentation'
        elif token_type in token.String:
            line_marks.add('s')  # 'string'
        else:
            is_white_text = (token_text.strip() in white_words) or (token_text.rstrip(white_text) == '')
            if not is_white_text:
                line_marks.add('c')  # 'code'
        if token_text.endswith('\n'):
            yield line_marks
            line_marks = set()
    if len(line_marks) >= 1:
        yield line_marks


def encoding_for(source_path, encoding='automatic', fallback_encoding='cp1252'):
    """
    The encoding used by the text file stored in ``source_path``.

    The algorithm used is:

    * If ``encoding`` is ``'automatic``, attempt the following:
      1. Check BOM for UTF-8, UTF-16 and UTF-32.
      2. Look for XML prolog or magic heading like ``# -*- coding: cp1252 -*-``
      3. Read the file using UTF-8.
      4. If all this fails, use assume the ``fallback_encoding``.
    * If ``encoding`` is ``'chardet`` use :mod:`chardet` to obtain the encoding.
    * For any other ``encoding`` simply use the specified value.
    """
    assert encoding is not None
    assert fallback_encoding is not None

    if encoding == 'automatic':
        with open(source_path, 'rb') as source_file:
            heading = source_file.read(128)
        result = None
        if len(heading) == 0:
            # File is empty, assume a dummy encoding.
            result = 'utf-8'
        if result is None:
            # Check for known BOMs.
            for bom, encoding in _BOM_TO_ENCODING_MAP.items():
                if heading[:len(bom)] == bom:
                    result = encoding
                    break
        if result is None:
            # Look for common headings that indicate the encoding.
            ascii_heading = heading.decode('ascii', errors='replace')
            ascii_heading = ascii_heading.replace('\r\n', '\n')
            ascii_heading = ascii_heading.replace('\r', '\n')
            ascii_heading = '\n'.join(ascii_heading.split('\n')[:2]) + '\n'
            coding_magic_match = _CODING_MAGIC_REGEX.match(ascii_heading)
            if coding_magic_match is not None:
                result = coding_magic_match.group('encoding')
            else:
                first_line = ascii_heading.split('\n')[0]
                xml_prolog_match = _XML_PROLOG_REGEX.match(first_line)
                if xml_prolog_match is not None:
                    result = xml_prolog_match.group('encoding')
        if result is None:
            try:
                # Attempt to read the first 16 KiB of the file as UTF-8.
                with open(source_path, 'r', encoding='utf-8') as source_file:
                    source_file.read(16384)
                result = 'utf-8'
            except UnicodeDecodeError:
                # It is not UTF-8, just assume the fallback encoding.
                result = fallback_encoding
    elif encoding == 'chardet':
        assert _detector is not None, \
            'without chardet installed, encoding="chardet" must be rejected before calling encoding_for()'
        _detector.reset()
        with open(source_path, 'rb') as source_file:
            for line in source_file.readlines():
                _detector.feed(line)
                if _detector.done:
                    break
        result = _detector.result['encoding']
    else:
        # Simply use the specified encoding.
        result = encoding
    assert result is not None
    return result


def source_analysis(
        source_path, group, encoding='automatic', fallback_encoding='cp1252',
        generated_regexes=pygount.common.regexes_from(DEFAULT_GENERATED_PATTERNS_TEXT)):
    """
    Analysis for line counts in source code stored in ``source_path``.

    :param source_path:
    :param group: name of a logical group the sourc code belongs to, e.g. a
      package.
    :param encoding: encoding according to :func:`encoding_for`
    :param fallback_encoding: fallback encoding according to
      :func:`encoding_for`
    :return: a :class:`SourceAnalysis`; if no matching lexer could be found,
      `language`` is ``None``.
    """
    assert encoding is not None
    assert fallback_encoding is not None
    assert generated_regexes is not None

    result = None
    try:
        lexer = lexers.get_lexer_for_filename(source_path)
        if lexer.name.lower() == 'xml+evoque':
            lexer = lexers.get_lexer_by_name('XML')
    except util.ClassNotFound:
        lexer = None
    if lexer is not None:
        if encoding == 'automatic':
            encoding = encoding_for(source_path, encoding, fallback_encoding)
        _log.info('%s: analyze as %s using encoding %s', source_path, lexer.name, encoding)
        try:
            with open(source_path, 'r', encoding=encoding) as source_file:
                text = source_file.read()
        except (LookupError, OSError, UnicodeDecodeError) as error:
            _log.warning('cannot read %s: %s', source_path, error)
            result = SourceAnalysis(
                path=source_path,
                language='__error__',
                group=group,
                code=0,
                documentation=0,
                empty=0,
                string=0,
                state=SourceState.error.name,
                state_info=error,
            )
        if (result is None) and (len(generated_regexes) != 0):
            number_line_and_regex = matching_number_line_and_regex(
                pygount.common.lines(text), generated_regexes
            )
            if number_line_and_regex is not None:
                number, line, regex = number_line_and_regex
                result = SourceAnalysis(
                    path=source_path,
                    language='__generated__',
                    group=group,
                    code=0,
                    documentation=0,
                    empty=0,
                    string=0,
                    state=SourceState.generated.name,
                    state_info='line {0} matches {0}'.format(number, regex),
                )
        if result is None:
            mark_to_count_map = {'c': 0, 'd': 0, 'e': 0, 's': 0}
            for line_parts in _line_parts(lexer, text):
                mark_to_increment = 'e'
                for mark_to_check in ('d', 's', 'c'):
                    if mark_to_check in line_parts:
                        mark_to_increment = mark_to_check
                mark_to_count_map[mark_to_increment] += 1
            result = SourceAnalysis(
                path=source_path,
                language=lexer.name,
                group=group,
                code=mark_to_count_map['c'],
                documentation=mark_to_count_map['d'],
                empty=mark_to_count_map['e'],
                string=mark_to_count_map['s'],
                state=SourceState.analyzed.name,
                state_info=None,
            )
    else:
        _log.info('%s: skip', source_path)
        result = SourceAnalysis(source_path, '__unknown__', group, 0, 0, 0, 0, SourceState.unknown.name, None)

    assert result is not None
    return result
