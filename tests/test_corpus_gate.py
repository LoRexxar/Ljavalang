"""Frozen-corpus parse gate for ljavalang — Java twin of lphply's gate.

Why this exists
---------------
Same structural defect the PHP side had (see lphply tests/
test_corpus_gate.py): grammar gaps surface as one-file-hard-failures
in real CVE campaigns, discovered late. This gate freezes a
multi-project Java corpus and asserts 100% parse, so the next
`to`/`with`-style contextual-keyword gap explodes in CI, not in a
campaign.

Corpus (seed=42 + 1337, frozen 2026-11-06, see MANIFEST.txt):
  activemq-core 90 | ureport 90 | activemq 60 | geotools 19 | msf 50
"""
import os
import unittest

import javalang

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, 'corpus', 'java')
MIN_FILES = 250  # corpus must not shrink below this


def _java_files():
    if not os.path.isdir(CORPUS):
        return []
    return sorted(f for f in os.listdir(CORPUS) if f.endswith('.java'))


class TestCorpusParseGate(unittest.TestCase):
    def test_corpus_exists_and_not_shrunk(self):
        files = _java_files()
        self.assertGreaterEqual(
            len(files), MIN_FILES,
            f'corpus shrank to {len(files)} files (<{MIN_FILES}); '
            'shrinking the corpus is not a fix — re-add files or lower '
            'the bar explicitly with justification')

    def test_corpus_100_percent_parse(self):
        files = _java_files()
        self.assertTrue(files, 'corpus directory is empty')
        failures = []
        for name in files:
            path = os.path.join(CORPUS, name)
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as fh:
                    src = fh.read()
                javalang.parse.parse(src)
            except Exception as e:
                failures.append(f'{name}: {type(e).__name__}: {e}')
        self.assertEqual(
            failures, [],
            f'{len(failures)}/{len(files)} corpus files failed to parse '
            f'(first 3):\n' + '\n'.join(failures[:3]))


if __name__ == '__main__':
    unittest.main()
