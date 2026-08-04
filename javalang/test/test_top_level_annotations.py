"""Regression tests for annotations on top-level declarations."""

import unittest

import javalang


def annotation_names(declaration):
    return [annotation.name for annotation in declaration.annotations]


class TopLevelAnnotationsTest(unittest.TestCase):
    def test_top_level_class_annotation_is_preserved(self):
        tree = javalang.parse.parse("@Entity class Customer {}")

        self.assertEqual(annotation_names(tree.types[0]), ["Entity"])

    def test_multiple_top_level_annotations_are_preserved(self):
        tree = javalang.parse.parse(
            "@Entity @Deprecated public class Customer {}"
        )

        self.assertEqual(
            annotation_names(tree.types[0]), ["Entity", "Deprecated"]
        )

    def test_qualified_top_level_annotation_is_preserved(self):
        tree = javalang.parse.parse(
            "@jakarta.persistence.Entity public class Customer {}"
        )

        self.assertEqual(
            annotation_names(tree.types[0]), ["jakarta.persistence.Entity"]
        )

    def test_top_level_record_annotation_is_preserved(self):
        tree = javalang.parse.parse("@Entity record Customer(int id) {}")

        self.assertEqual(annotation_names(tree.types[0]), ["Entity"])

    def test_top_level_interface_annotation_is_preserved(self):
        tree = javalang.parse.parse("@Entity interface Customer {}")

        self.assertEqual(annotation_names(tree.types[0]), ["Entity"])

    def test_top_level_enum_annotation_is_preserved(self):
        tree = javalang.parse.parse("@Entity enum Customer {}")

        self.assertEqual(annotation_names(tree.types[0]), ["Entity"])

    def test_annotated_module_still_parses(self):
        tree = javalang.parse.parse(
            "@Deprecated module example.application {}"
        )

        self.assertEqual(annotation_names(tree.module), ["Deprecated"])

    def test_annotated_open_module_still_parses(self):
        tree = javalang.parse.parse(
            "@Deprecated open module example.application {}"
        )

        self.assertTrue(tree.module.open)
        self.assertEqual(annotation_names(tree.module), ["Deprecated"])

    def test_package_and_member_annotations_are_preserved(self):
        tree = javalang.parse.parse(
            "@PackageAnnotation package example; "
            "@Entity class Customer { @Id int id; }"
        )

        self.assertEqual(annotation_names(tree.package), ["PackageAnnotation"])
        self.assertEqual(annotation_names(tree.types[0]), ["Entity"])
        self.assertEqual(annotation_names(tree.types[0].fields[0]), ["Id"])
