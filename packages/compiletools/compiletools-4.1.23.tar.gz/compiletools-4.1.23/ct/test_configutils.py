from __future__ import print_function
from __future__ import unicode_literals

import sys
import unittest
import configargparse

import ct.unittesthelper as uth
import ct.configutils
import ct.apptools


class TestVariant(unittest.TestCase):

    def setUp(self):
        uth.delete_existing_parsers()

    def test_extract_variant(self):
        self.assertEqual(
            "abc",
            ct.configutils.extract_variant(
                "--variant=abc".split()))
        self.assertEqual(
            "abc",
            ct.configutils.extract_variant(
                "--variant abc".split()))
        self.assertEqual(
            "abc.123",
            ct.configutils.extract_variant(
                "-a -b -x --blah --variant=abc.123 -a -b -z --blah".split()))
        self.assertEqual(
            "abc.123",
            ct.configutils.extract_variant(
                "-a -b -x --blah --variant abc.123 -a -b -cz--blah".split()))

        # Note the -c overrides the --variant
        self.assertEqual(
            "blah",
            ct.configutils.extract_variant(
                "-a -b -c blah.conf --variant abc.123 -a -b -cz--blah".split()))

    def test_variant_with_hash(self):
        config_files = ct.configutils.config_files_from_variant(
            exedir=uth.cakedir())
        cap = configargparse.getArgumentParser(
            description='TestNamer',
            formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
            default_config_files=config_files,
            args_for_setting_config_path=["-c", "--config"],
            ignore_unknown_config_file_keys=True)
        argv1 = "--variant=gcc.debug".split()
        ct.apptools.add_common_arguments(
            cap=cap,
            argv=argv1,
            variant="gcc.debug")
        args1 = ct.apptools.parseargs(cap, argv1)

        # Make a second, different, but logically equivalent argv
        argv2 = "--no-shorten --variant=gcc.debug".split()
        args2 = ct.apptools.parseargs(cap, argv2)
        self.assertEqual(args1, args2)

        # And a third ...
        argv3 = []
        args3 = ct.apptools.parseargs(cap, argv3)
        self.assertEqual(args1, args3)

        vwh1 = ct.configutils.variant_with_hash(
            args1,
            argv=argv1,
            user_config_dir='/var',
            system_config_dir='/var',
            exedir=uth.cakedir())
        vwh2 = ct.configutils.variant_with_hash(
            args2,
            argv=argv2,
            user_config_dir='/var',
            system_config_dir='/var',
            exedir=uth.cakedir())
        self.assertEqual(vwh1, vwh2)

        vwh3 = ct.configutils.variant_with_hash(
            args3,
            argv=argv3,
            user_config_dir='/var',
            system_config_dir='/var',
            exedir=uth.cakedir())
        self.assertEqual(vwh1, vwh3)

    def test_extract_variant_from_ct_conf(self):
        # Should find the one in the git repo ct.conf.d/ct.conf
        # Unless there is a system one to be found
        variant = ct.configutils.extract_item_from_ct_conf(
            key='variant',
            exedir=uth.cakedir())
        self.assertEqual("debug", variant)

    def test_extract_variant_from_blank_argv(self):
        # Force to find the git repo ct.conf.d/ct.conf
        variant = ct.configutils.extract_variant(
            user_config_dir='/var',
            system_config_dir='/var',
            exedir=uth.cakedir(),
            verbose=3)
        self.assertEqual("gcc.debug", variant)

    def tearDown(self):
        uth.delete_existing_parsers()

if __name__ == '__main__':
    unittest.main()
