#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests module for the roc.film plugin.
"""

import os.path as osp
import zipfile
from pathlib import Path

from poppy.core.test import TaskTestCase


import filecmp
import os
import tempfile
from pprint import pformat

import pytest
import shutil
import unittest.mock as mock
from poppy.core.generic.requests import download_file
from poppy.core.logger import logger
from poppy.core.test import CommandTestCase


class FilmTest:

    base_url = 'https://rpw.lesia.obspm.fr/roc/data/private/devtest/roc/test_data/rodp/film'
    base_path = '/volumes/plasma/rpw/roc/data/https/private/devtest/roc/test_data/rodp/film'

    # test credentials
    host = 'roc2-dev.obspm.fr'
    username = 'roctest'
    password = None

    def __init__(self):
        logger.debug('FilmTest setup_class()')
        logger.debug(f'base_url = {self.base_url}')
        logger.debug(f'base_path = {self.base_path}')
        try:
            self.password = os.environ['ROC_TEST_PASSWORD']
        except KeyError:
            raise KeyError('You have to define the test user password using'
                           'the "ROC_TEST_PASSWORD" environment variable')

    @staticmethod
    def get_test_data_path():
        """
        Read the config file and returns ROC_FILM_TEST_DATA_PATH
        which is the path where to store the test dataset locally
        """
        conf = FilmTest.load_configuration()

        try:
            data_test_path = conf['environment']['ROC_FILM_TEST_DATA_PATH']
        except Exception:
            logger.info('Env. variable ROC_FILM_TEST_DATA_PATH not set')
            logger.info('Using /tmp/FILM_TEST_DATA/')
            data_test_path = '/tmp/FILM_TEST_DATA/'

        return data_test_path

    def get_test_data(self,
                      base_path=None,
                      manifest_file_url=None,
                      archive_file_url=None,
                      rsync=False):
        """
        Get the test dataset indicated by the environment variable
        ROC_FILM_TEST_DATA_PATH

        :param subdir: optional subdirectory

        Try to make a rsync with the roctest account
        A public key has to be setup on the server to allow connexion
        If the command is not available (Windows),
        use the download_file() method
        """
        data_test_path = FilmTest.get_test_data_path()
        os.makedirs(data_test_path, exist_ok=True)

        if not base_path:
            base_path = self.base_path

        if rsync:
            logger.info('Starting rsync')
            ssh_option = '\"ssh -o \'StrictHostKeyChecking no\'\"'
            rsync_cmd = 'rsync -e {} -irtzuv {}@{}:{}/ {}/'.format(
                ssh_option,
                self.username,
                self.host,
                base_path,
                data_test_path
            )
            logger.info('Executing ' + rsync_cmd)
            output = os.popen(rsync_cmd)
            rsync_output = output.read()
            if output.close() is not None:
                raise ValueError('Rsync failed : {}'.format(rsync_output))
        else:
            logger.info('Call download_test_data()')
            self.download_test_data(data_test_path,
                                    manifest_file_url=manifest_file_url,
                                    archive_file_url=archive_file_url,)

        return data_test_path

    def download_test_data(self, data_test_path,
                           base_url=None,
                           manifest_file_url=None,
                           archive_file_url=None):
        """
        Download the manifest.txt file located at self.base_url
        And for each file, download it only if the file does not exist
        in data_test_path
        """
        logger.debug('download_test_data()')

        if not base_url:
            base_url = self.base_url

        # get authentication login and password
        auth = (self.username, self.password)

        if manifest_file_url:
            manifest_filepath = osp.join(data_test_path, 'manifest.txt')
            file_list = list(self.load_manifest_file(
                manifest_filepath, manifest_file_url, auth=auth))

            for relative_filepath in file_list:
                # skip empty strings
                if not relative_filepath:
                    continue

                # get the complete filepath
                filepath = osp.join(data_test_path, relative_filepath)
                os.makedirs(osp.dirname(filepath), exist_ok=True)

                # download it only if it does not exist
                if not osp.isfile(filepath):
                    logger.info('Downloading {}'.format(filepath))
                    download_file(filepath,
                                  f'{base_url}/{relative_filepath}',
                                  auth=auth)
        elif archive_file_url:
            archive_filepath = osp.join(data_test_path, os.path.basename(archive_file_url))
            is_zip = zipfile.is_zipfile(archive_filepath)

            if not osp.isfile(archive_filepath):
                logger.info('Downloading {}'.format(archive_filepath))
                # Download archive file
                download_file(archive_filepath,
                              archive_file_url,
                              auth=auth)
            elif not is_zip:
                # if file exists, but not seems to be a ZIP file,
                # Then try to resume downloading
                path = Path(archive_filepath)
                resume_byte_pos = path.stat().st_size
                resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
                download_file(archive_filepath,
                              archive_file_url,
                              headers=resume_header,
                              auth=auth)

            # unpack archive file
            shutil.unpack_archive(archive_filepath,
                                      data_test_path,
                                      'zip')

        else:
            raise ValueError(f'Missing input argument, one of the following parameter must be defined: (archive_file_url, manifest_file_url)')

    @staticmethod
    def get_test_io(test_data_path):
        """

        :param test_data_path:
        :return:
        """
        # Initialize returned values
        inputs = []
        expected_outputs = []
        ancillaries = []

        if os.path.isdir(test_data_path):

            # Walk through the test_data_path to get inputs, expected_outputs and ancillaries data files
            for root, dirs, files in os.walk(test_data_path):
                root_name = os.path.basename(root)
                if root_name == 'inputs':
                    inputs.extend([os.path.join(root, file)
                                   for file in files])
                elif root_name == 'expected_outputs':
                    expected_outputs.extend([os.path.join(root, file)
                                             for file in files])
                elif root_name == 'ancillaries':
                    ancillaries.extend([os.path.join(root, file)
                                        for file in files])
        else:
            raise IsADirectoryError(f'{test_data_path} does not exist!')

        return inputs, expected_outputs, ancillaries

    @staticmethod
    def load_manifest_file(
            manifest_filepath, manifest_file_url,
            auth=None):
        """
        Read the manifest.txt file located at manifest_file_url
        and returns the list composed by the file list

        :param manifest_filepath:
        :param manifest_file_url:
        :param auth:
        :return:
        """

        download_file(manifest_filepath, manifest_file_url, auth=auth)

        with open(manifest_filepath) as manifest_file:
            for line in manifest_file:
                yield line.strip('\n\r')

        os.remove(manifest_filepath)

    @staticmethod
    def get_diff_files(dirs_cmp, path=''):
        for name in dirs_cmp.diff_files:
            yield os.path.join(path, name)
        for parent, sub_dirs_cmp in dirs_cmp.subdirs.items():
            for filepath in FilmTest.get_diff_files(sub_dirs_cmp, path=os.path.join(path, parent)):
                yield filepath

    @staticmethod
    def load_configuration():
        from poppy.core.configuration import Configuration

        configuration = Configuration(os.getenv('PIPELINE_CONFIG_FILE', None))
        configuration.read()

        return configuration

    @staticmethod
    def extract_spice_kernels(zip_file_path, target_dir):
        """
        Extract SPICE kernels from ZIP file.

        :param zip_file_path:
        :param target_dir:
        :return:
        """

        kernels_symlink = os.path.join(target_dir, 'spice_kernels')
        if not os.path.islink(kernels_symlink):
            if FilmTest.unzip(zip_file_path, target_dir=target_dir):
                kernels_dir = os.path.join(target_dir, 'kernels')
                # Create a "spice_kernels" symlink used by the pipeline

                os.symlink(kernels_dir, kernels_symlink)
            else:
                raise zipfile.error(f'SPICE kernels in {zip_file_path} cannot be extracted!')

    @staticmethod
    def unzip(zip_file_path,
              target_dir=None):
        """
        Unzip an input ZIP file.

        :param zip_file_path: Path to the input zip file
        :param target_dir: If provided, move unzipped items into target_dir
        :return: True if unpack is OK
        """
        is_unpacked = False
        # check zip file existence
        if not os.path.isfile(zip_file_path):
            raise FileNotFoundError(f'input ZIP file not found ({zip_file_path})!')

        # Get zip directory
        if not target_dir:
            target_dir = os.path.dirname(zip_file_path)

        # Unzip ZIP file
        try:
            # unpack archive file
            shutil.unpack_archive(zip_file_path,
                                      target_dir,
                                      'zip')

        except:
            logger.exception(f'Extracting {zip_file_path} has failed!')
        else:
            is_unpacked = True

        return is_unpacked
