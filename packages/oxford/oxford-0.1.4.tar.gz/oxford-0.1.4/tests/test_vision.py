import copy
import os
import sys
import unittest

rootDirectory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if rootDirectory not in sys.path:
    sys.path.insert(0, rootDirectory)

from oxford.vision import Vision

class TestFace(unittest.TestCase):
    '''Tests the Project Oxford Vision API'''

    @classmethod
    def setUpClass(cls):
        # set up self.client for tests
        cls.client = Vision(os.environ['OXFORD_VISION_API_KEY'])
        cls.localFilePrefix = os.path.join(rootDirectory, 'tests', 'images')
        cls.analyzeOptions = {
            'ImageType': True,
            'Color': True,
            'Faces': True,
            'Adult': True,
            'Categories': True,
            'Tags': True,
            'Description': True,
            'Celebrities': True,
        }

        cls.thumbnailOptions = {
            'width': 100,
            'height': 100,
            'smartCropping': True
        }

        cls.ocrOptions = {
            'language': 'en',
            'detectOrientation': True
        }

    #
    # test the analyze API
    #
    def _verify_analyze_result(self, result):
        self.assertIsNotNone(result['imageType'])
        self.assertIsNotNone(result['color'])
        self.assertIsNotNone(result['faces'])
        self.assertIsNotNone(result['adult'])
        self.assertIsNotNone(result['categories'])

    def test_vision_analyze_file(self):
        options = copy.copy(self.analyzeOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_url(self):
        options = copy.copy(self.analyzeOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        result = self.client.analyze(options)
        self._verify_analyze_result(result)

    def test_vision_analyze_stream(self):
        options = copy.copy(self.analyzeOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.analyze(options)
        
        self._verify_analyze_result(result)

    #
    # test the thumbnail API
    #
    def _verify_thumbnail_result(self, result, fileName):
        outputPath = os.path.join(self.localFilePrefix, fileName)
        with open(outputPath, 'wb+') as file: file.write(result)
        self.assertTrue(True, 'file write succeeded for: {0}'.format(fileName))

    def test_vision_thumbnail_file(self):
        options = copy.copy(self.thumbnailOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.thumbnail(options)
        self._verify_thumbnail_result(result, 'thumbnail_from_file.jpg')

    def test_vision_thumbnail_url(self):
        options = copy.copy(self.thumbnailOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        result = self.client.thumbnail(options)
        self._verify_thumbnail_result(result, 'thumbnail_from_url.jpg')

    def test_vision_thumbnail_stream(self):
        options = copy.copy(self.thumbnailOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.thumbnail(options)
        self._verify_thumbnail_result(result, 'thumbnail_from_stream.jpg')

    #
    # test the OCR API
    #
    def _verify_ocr_result(self, result):
        self.assertIsNotNone(result['language'])
        self.assertIsNotNone(result['orientation'])

    def test_vision_ocr_file(self):
        options = copy.copy(self.ocrOptions)
        options['path'] = os.path.join(self.localFilePrefix, 'vision.jpg')
        result = self.client.ocr(options)
        self._verify_ocr_result(result)

    def test_vision_ocr_url(self):
        options = copy.copy(self.ocrOptions)
        options['url'] = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
        result = self.client.ocr(options)
        self._verify_ocr_result(result)

    def test_vision_ocr_stream(self):
        options = copy.copy(self.ocrOptions)
        with open(os.path.join(self.localFilePrefix, 'face1.jpg'), 'rb') as file:
            options['stream'] = file.read()
            result = self.client.ocr(options)
        
        self._verify_ocr_result(result)