import unittest
from kdap import analysis
import os
import shutil
import json


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'testOutput/'
        self.ropar_filename = 'Indian_Institute_of_Technology_Ropar.knolml'
        self.zinc_filename = 'Zinc.knolml'
        self.k = analysis.knol()
        with open('test_data.txt', 'r') as infile:
            self.frames_data = json.loads(infile.read())

    def get_wiki_article(self):
        article_name = 'IIT Ropar'
        self.k.get_wiki_article(article_name=article_name, output_dir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))

    def test_download_dataset_article_list(self):
        self.k.download_dataset(sitename='wikipedia', article_list=['IIT Ropar', 'Zinc'], destdir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))
        self.assertTrue(os.path.exists(self.test_dir + self.zinc_filename))
        self.frame_test()

    # tests are run in alphabetical order, so download_dataset will always run
    # before, ensuring this has the necessary knolml file
    def frame_test(self):
        test_data = {
            'id': [],
            'title': [],
            'bytes': [],
            'editor': [],
            'time': [],
            'text': [],
            'stats': []
        }
        for inst in self.k.frame(file_name=self.test_dir+self.ropar_filename):
            test_data['id'].append(inst.instanceId)
            test_data['title'].append(inst.get_title())
            test_data['bytes'].append(inst.get_bytes())
            test_data['editor'].append(inst.get_editor())
            test_data['time'].append(inst.get_timestamp())
            test_data['text'].append(inst.get_text())
            test_data['stats'].append(inst.get_text_stats())

        for key in self.frames_data.keys():
            self.assertTrue(all(x in self.frames_data[key] for x in test_data[key]))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists('outputD/'):
            shutil.rmtree('outputD/')
