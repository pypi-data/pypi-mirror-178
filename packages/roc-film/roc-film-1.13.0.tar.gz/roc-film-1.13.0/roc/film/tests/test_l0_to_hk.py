#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test l0_to_hk command of the roc.film plugin.
"""

import filecmp
import os
import tempfile
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock

from maser.tools.cdf.cdfcompare import cdf_compare

from poppy.core.logger import logger
from poppy.core.test import CommandTestCase

from roc.film.tests.test_film import FilmTest


class TestL0ToHk(CommandTestCase):

    film = FilmTest()

    cmd = 'l0_to_hk'

    def setup_method(self, method):
        super().setup_method(method)

        # Make sure test data files exists
        # if not download them
        archive_file_url = f'{self.film.base_url}/test_data.zip'
        test_data_dir = self.film.get_test_data(
            archive_file_url=archive_file_url)

        # Get list of inputs and expected output files
        self.test_data_dir = os.path.join(test_data_dir, self.cmd)
        self.inputs, self.expected_outputs, self.ancillaries = FilmTest.get_test_io(
            self.test_data_dir
        )

        # extract spice kernels
        if self.ancillaries:
            self.spice_kernel_dir_path = FilmTest.extract_spice_kernels(self.ancillaries[0],
                                                                        '/pipeline/data')

        # generated_output_dir_path = os.path.join(self.tmp_dir_path, 'generated_output')
        self.generated_output_dir_path = os.path.join(self.test_data_dir, 'outputs')
        os.makedirs(self.generated_output_dir_path, exist_ok=True)



    def teardown_method(self, method):
        """
        Method called immediately after the test method has been called and the result recorded.

        This is called even if the test method raised an exception.

        :param method: the test method
        :return:
        """

        # rollback the database
        super().teardown_method(method)

        # clear the downloaded files
        shutil.rmtree(self.test_data_dir)

    @pytest.mark.parametrize('idb_source,idb_version', [
        ('MIB', '20200131'),
        ('PALISADE', '4.3.5_MEB_PFM'),
    ])
    def test_l0_to_hk(self, idb_source, idb_version):
        from poppy.core.conf import Settings

        # Name of the command to test
        cmd = 'l0_to_hk'

        # initialize the main command
        main_command = ['pop', 'film',
                        '--idb-version', idb_version,
                        '--idb-source', idb_source,
                        cmd,
                        ' '.join(self.inputs),
                        '--output-dir', self.generated_output_dir_path,
                        '-ll', 'INFO']

        print(main_command)

        #
        # # define the required plugins
        # plugin_list = ['poppy.pop', 'roc.idb', 'roc.rpl', 'roc.rap', 'roc.dingo', 'roc.film']
        #
        # # run the command
        # # force the value of the plugin list
        # with mock.patch.object(Settings, 'configure',
        #                        autospec=True,
        #                        side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
        #     self.run_command('pop db upgrade heads -ll INFO')
        #     self.run_command(['pop', '-ll', 'INFO', 'idb', 'install', '-s', idb_source, '-v', idb_version, '--load'])
        #     self.run_command(main_command)
        #
        # # compare directory content
        # dirs_cmp = filecmp.dircmp(generated_output_dir_path,
        #                           expected_output_dir_path)
        #
        # dirs_cmp.report()
        #
        # # ensure that we have the same files in both directories
        # assert (len(dirs_cmp.left_only) == 0) and (len(dirs_cmp.right_only) == 0)
        #
        # for filename in self.get_diff_files(dirs_cmp):
        #     # compare only cdf files with differences
        #     if filename.endswith('.cdf'):
        #         # use cdf compare to compute the differences between expected output and the command output
        #         result = cdf_compare(
        #             os.path.join(generated_output_dir_path, filename),
        #             os.path.join(expected_output_dir_path, filename),
        #             list_ignore_gatt=[
        #                 'File_ID',
        #                 'Generation_date',
        #                 'Pipeline_version',
        #                 'Pipeline_name',
        #                 'Software_version',
        #                 'IDB_version'
        #             ]
        #         )
        #
        #         # compare the difference dict with the expected one
        #         if result:
        #             logger.error(f'Differences between expected output and the command output: {pformat(result)}')
        #
        #         assert result == {}
