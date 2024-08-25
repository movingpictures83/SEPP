'''
Created on June 14, 2018

@author: Stefan.M.Janssen@gmail.com
'''
import sys
import tempfile
import shutil
import unittest
import sepp
from sepp.filemgr import get_data_path
import platform
from argparse import Namespace

from sepp.exhaustive import ExhaustiveAlgorithm
# sepp._DEBUG = True
# sepp.reset_loggers()

global config_file
global alignment_file
global info_file
global tree_file
global fragments_file

class Test(unittest.TestCase):
    x = None

    def setUp(self):
        # ensure necessary settings are made
        sepp.scheduler._jobPool = None
        #sys.argv = [sys.argv[0], "-c", get_data_path(config_file)]
        self.x = ExhaustiveAlgorithm()
        self.x.options.alignment_file = open(self.alignment_file, "r")
        self.x.options.info_file = open(self.info_file, "r")
        self.x.options.tree_file = open(self.tree_file, "r")
        self.x.options.outdir = tempfile.mkdtemp()

        suff_bit = "-64" if sys.maxsize > 2**32 else "-32"
        if platform.system() == 'Darwin':
            suff_bit = ""
        for prog in ['hmmalign', 'hmmbuild', 'hmmsearch', 'pplacer']:
            setattr(self.x.options, prog, Namespace(
                path=get_data_path("/usr/share/bin/%s%s" % (
                    prog, suff_bit))))

    def tearDown(self):
        self.x.options.alignment_file.close()
        self.x.options.info_file.close()
        self.x.options.tree_file.close()
        self.x.options.fragment_file.close()
        sepp.scheduler._jobPool = None
        #shutil.rmtree(self.x.options.outdir, ignore_errors=True)

    def test_id_collision_working(self):
        self.x.options.fragment_file = open(
            self.fragments_file, "r")
        self.x.run()
        self.assertTrue(self.x.results is not None)

    #def test_id_collision_collision(self):
    #    self.x.options.fragment_file = open(
    #        get_data_path(
    #            "q2-fragment-insertion/input_fragments_collide.fasta"), "r")
    #    with self.assertRaisesRegex(
    #            ValueError,
    #            ' whose names overlap with names in your reference'):
    #        self.x.run()
    #    self.assertTrue(self.x.results is None)

    #def test_seqnames_whitespaces(self):
    #    self.x.options.fragment_file = open(
    #        get_data_path(
    #            "q2-fragment-insertion/input_fragments_spaces.fasta"), "r")
    #    with self.assertRaisesRegex(
    #            ValueError,
    #            "contain either whitespaces: "):
    #        self.x.run()
    #    self.assertTrue(self.x.results is None)

    #def test_fake_jobs(self):
    #    self.x.options.fragment_file = open(
    #        get_data_path(
    #            "q2-fragment-insertion/input_fragments_tiny.fasta"), "r")
    #    self.x.run()
    #    self.assertTrue(self.x.results is not None)

    #def test_notpiped_jobs(self):
    #    sepp.config.options().hmmsearch.piped = "False"
    #    self.x.options.fragment_file = open(
    #        get_data_path(
    #            "q2-fragment-insertion/input_fragments_tiny.fasta"), "r")
    #    self.x.run()
    #    self.assertTrue(self.x.results is not None)


import PyIO
import PyPluMA
class SEPPPlugin:
    def input(self, inputfile):
       self.parameters = PyIO.readParameters(inputfile)
       self.t = Test()
       self.t.config_file = PyPluMA.prefix()+"/"+self.parameters["config_file"]  
       self.t.alignment_file = PyPluMA.prefix()+"/"+self.parameters["alignment_file"]  
       self.t.info_file = PyPluMA.prefix()+"/"+self.parameters["info_file"]  
       self.t.tree_file = PyPluMA.prefix()+"/"+self.parameters["tree_file"]  
       self.t.fragments_file = PyPluMA.prefix()+"/"+self.parameters["fragments_file"]  

    def run(self):
        pass

    def output(self, outputfile):
        sys.argv = ['SEPP']
        self.t.setUp()
        self.t.test_id_collision_working()
        self.t.tearDown()
        #sys.argv = ['SEPP']
        #unittest.main()
