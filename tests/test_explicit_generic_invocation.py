"""Fix 63: explicit generic type-witness invocations keep their member.

`request.<String>getParameter("realm")` used to be clobbered by
parse_primary's post-processing: the suffix already carried
member='getParameter', but the unconditional
`identifier_suffix.member = qualified_identifier.pop()` renamed the
call to member='request'/qualifier='' — every downstream name match
(source registries, sink rules, CG) went dark.  117 occurrences in the
OpenAM 16.1.0 oauth2 corpus alone.

Found in the CVE-2026-44203 campaign (Kunlun-M Fix 138).
"""
import unittest

import javalang


def _invocations(src):
    tree = javalang.parse.parse(src)
    out = []
    for _, node in tree:
        if isinstance(node, javalang.tree.MethodInvocation):
            out.append(node)
    return out


class TestExplicitGenericInvocation(unittest.TestCase):
    def test_receiver_witness_call_keeps_member(self):
        invs = _invocations(
            'class T { void m(Object request) {'
            ' String r = request.<String>getParameter("realm"); } }')
        self.assertEqual(len(invs), 1)
        self.assertEqual(invs[0].member, 'getParameter')
        self.assertEqual(invs[0].qualifier, 'request')
        self.assertEqual(len(invs[0].arguments), 1)
        self.assertIsNotNone(invs[0].type_arguments)

    def test_plain_qualified_call_unchanged(self):
        invs = _invocations(
            'class T { void m() { String r = foo.bar(x); } }')
        self.assertEqual(invs[0].member, 'bar')
        self.assertEqual(invs[0].qualifier, 'foo')
        self.assertIsNone(invs[0].type_arguments)

    def test_bare_witness_call(self):
        invs = _invocations(
            'class T { void m() { Object l = Collections.<String>emptyList(); } }')
        self.assertEqual(invs[0].member, 'emptyList')
        self.assertEqual(invs[0].qualifier, 'Collections')

    def test_plain_bare_call(self):
        invs = _invocations('class T { void m() { sink(x); } }')
        self.assertEqual(invs[0].member, 'sink')
        self.assertEqual(invs[0].qualifier, '')

    def test_chained_selector_witness(self):
        # selector path (`expr` already a primary, then `.<T>m()`);
        # tree walk yields the outer invocation first (parent-first)
        invs = _invocations(
            'class T { void m() { Object o = foo().<String>bar(1); } }')
        by_member = {i.member: i for i in invs}
        self.assertIn('bar', by_member)
        self.assertIsNotNone(by_member['bar'].qualifier)  # nested on foo()


if __name__ == '__main__':
    unittest.main()
