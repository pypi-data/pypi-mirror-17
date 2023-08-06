from unittest import TestCase

from mock import patch

from regulations.generator.layers.paragraph_markers import (
    MarkerHidingLayer, MarkerInfoLayer, ParagraphMarkersLayer)


class ParagraphMarkersLayerTest(TestCase):
    @patch('regulations.generator.layers.paragraph_markers.loader')
    def test_apply_layer(self, loader):
        pml = ParagraphMarkersLayer({
            '1001-12-a': [{'text': '(a)', 'locations': [0]}],
            '1001-12-q': [{'text': 'q.', 'locations': [1]}]
        })
        self.assertEqual([], list(pml.apply_layer('1002-01-01')))

        a = list(pml.apply_layer('1001-12-a'))
        self.assertEqual(1, len(a))
        self.assertEqual('(a)', a[0][0])
        self.assertEqual([0], a[0][2])
        call_args = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('(a)', call_args['paragraph'])
        self.assertEqual('a', call_args['paragraph_stripped'])

        q = list(pml.apply_layer('1001-12-q'))
        self.assertEqual(1, len(q))
        self.assertEqual('q.', q[0][0])
        self.assertEqual([1], q[0][2])
        call_args = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('q.', call_args['paragraph'])
        self.assertEqual('q', call_args['paragraph_stripped'])


class MarkerHidingLayerTest(TestCase):
    @patch('regulations.generator.layers.paragraph_markers.loader')
    def test_apply_layer(self, loader):
        pml = MarkerHidingLayer({
            '1001-12-a': [{'text': '(a)', 'locations': [0]}],
            '1001-12-q': [{'text': 'q.', 'locations': [1]}]
        })
        self.assertEqual([], list(pml.apply_layer('1002-01-01')))

        a = list(pml.apply_layer('1001-12-a'))
        self.assertEqual(1, len(a))
        self.assertEqual('(a)', a[0][0])
        self.assertEqual([0], a[0][2])
        call_args = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('(a)', call_args['paragraph'])

        q = list(pml.apply_layer('1001-12-q'))
        self.assertEqual(1, len(q))
        self.assertEqual('q.', q[0][0])
        self.assertEqual([1], q[0][2])
        call_args = loader.get_template.return_value.render.call_args[0][0]
        self.assertEqual('q.', call_args['paragraph'])


class MarkerInfoLayerTest(TestCase):
    def test_apply_layer(self):
        pml = MarkerInfoLayer({
            '1001-12-a': [{'text': '(a)', 'locations': [0]}],
            '1001-12-q': [{'text': 'q.', 'locations': [1]}]
        })
        self.assertIsNone(pml.apply_layer('1002-01-01'))
        self.assertEqual(tuple(pml.apply_layer('1001-12-a')),
                         ('paragraph_marker', 'a'))
        self.assertEqual(tuple(pml.apply_layer('1001-12-q')),
                         ('paragraph_marker', 'q'))
