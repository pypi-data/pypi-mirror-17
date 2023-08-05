#!/usr/bin/env python
#
# test_api.py - Unit test cases for COT.helpers.api module.
#
# April 2014, Glenn F. Matthews
# Copyright (c) 2014-2016 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Unit test cases for COT.helpers.api module."""

import os
import logging

from distutils.version import StrictVersion
import mock

from COT.tests.ut import COT_UT
from COT.helpers import (
    get_checksum, create_disk_image, convert_disk_image, get_disk_format,
    get_disk_capacity, create_install_dir, install_file,
)
from COT.helpers import HelperError, HelperNotFoundError

logger = logging.getLogger(__name__)


class TestGetChecksum(COT_UT):
    """Test cases for get_checksum() function."""

    def test_get_checksum_md5(self):
        """Test case for get_checksum() with md5 sum."""
        checksum = get_checksum(self.input_ovf, 'md5')
        self.assertEqual(checksum, "4e7a3ba0b70f6784a3a91b18336296c7")

        checksum = get_checksum(self.minimal_ovf, 'md5')
        self.assertEqual(checksum, "288e1e3fcb05265cd9b8c7578e173fef")

    def test_get_checksum_sha1(self):
        """Test case for get_checksum() with sha1 sum."""
        checksum = get_checksum(self.input_ovf, 'sha1')
        self.assertEqual(checksum, "c3bd2579c2edc76ea35b5bde7d4f4e41eab08963")

        checksum = get_checksum(self.minimal_ovf, 'sha1')
        self.assertEqual(checksum,
                         "5d0635163f6a580442f01466245e122f8412e8d6")

    def test_get_checksum_unsupported(self):
        """Test invalid options to get_checksum()."""
        self.assertRaises(NotImplementedError,
                          get_checksum,
                          self.input_ovf,
                          'sha256')
        self.assertRaises(NotImplementedError,
                          get_checksum,
                          self.input_ovf,
                          'crc')


class TestGetDiskFormat(COT_UT):
    """Test cases for get_disk_format() function."""

    def test_get_disk_format(self):
        """Get format and subformat of various disk images."""
        # First, tests that just use qemu-img
        try:
            temp_disk = os.path.join(self.temp_dir, 'foo.img')
            create_disk_image(temp_disk, capacity="16M")
            (f, sf) = get_disk_format(temp_disk)
            self.assertEqual(f, 'raw')
            self.assertEqual(sf, None)

            temp_disk = os.path.join(self.temp_dir, 'foo.qcow2')
            create_disk_image(temp_disk, capacity="1G")
            (f, sf) = get_disk_format(temp_disk)
            self.assertEqual(f, 'qcow2')
            self.assertEqual(sf, None)
        except HelperNotFoundError as e:
            self.fail(e.strerror)

        # Now a test that uses both qemu-img and file inspection
        try:
            (f, sf) = get_disk_format(self.blank_vmdk)
            self.assertEqual(f, 'vmdk')
            self.assertEqual(sf, 'streamOptimized')
        except HelperNotFoundError as e:
            self.fail(e.strerror)

    def test_get_disk_format_no_file(self):
        """Negative test - get_disk_format() for nonexistent file."""
        self.assertRaises(HelperError, get_disk_format, "")
        self.assertRaises(HelperError, get_disk_format, "/foo/bar/baz")

    @mock.patch('COT.helpers.api.QEMUIMG.get_disk_format',
                return_value='vmdk')
    def test_bad_vmdk_header(self, _):
        """Test corner case in VMDK subtype identification."""
        with self.assertRaises(RuntimeError) as cm:
            get_disk_format(self.input_ovf)
        self.assertRegex(cm.exception.args[0],
                         "Could not find VMDK 'createType' in the file header")


class TestConvertDiskImage(COT_UT):
    """Test cases for convert_disk_image()."""

    def test_convert_no_work_needed(self):
        """Convert a disk to its own format."""
        try:
            new_disk_path = convert_disk_image(self.blank_vmdk, self.temp_dir,
                                               'vmdk', 'streamOptimized')
            # No change -> don't create a new disk but just return existing.
            self.assertEqual(new_disk_path, self.blank_vmdk)
        except HelperNotFoundError as e:
            self.fail(e.strerror)

    def raw_to_vmdk_stream_optimized_test(self):
        """Test conversion of raw to vmdk streamOptimized."""
        temp_disk = os.path.join(self.temp_dir, "foo.img")
        try:
            create_disk_image(temp_disk, capacity="16M")
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        try:
            new_disk_path = convert_disk_image(temp_disk, self.temp_dir,
                                               'vmdk', 'streamOptimized')
        except HelperNotFoundError as e:
            self.fail(e.strerror)

        (f, sf) = get_disk_format(new_disk_path)
        self.assertEqual(f, 'vmdk')
        self.assertEqual(sf, 'streamOptimized')

    def vmdk_to_vmdk_stream_optimized_test(self):
        """Test conversion of unoptimized vmdk to streamOptimized."""
        temp_disk = os.path.join(self.temp_dir, "foo.vmdk")
        create_disk_image(temp_disk, capacity="16M")
        new_disk_path = convert_disk_image(temp_disk, self.temp_dir,
                                           'vmdk', 'streamOptimized')
        (f, sf) = get_disk_format(new_disk_path)
        self.assertEqual(f, 'vmdk')
        self.assertEqual(sf, 'streamOptimized')

    def qcow2_to_vmdk_stream_optimized_test(self):
        """Test conversion of qcow2 to vmdk streamOptimized."""
        try:
            temp_disk = os.path.join(self.temp_dir, "foo.qcow2")
            create_disk_image(temp_disk, capacity="16M")
            new_disk_path = convert_disk_image(temp_disk, self.temp_dir,
                                               'vmdk', 'streamOptimized')
            self.assertEqual(new_disk_path,
                             os.path.join(self.temp_dir, "foo.vmdk"))
            (f, sf) = get_disk_format(new_disk_path)
            self.assertEqual(f, 'vmdk')
            self.assertEqual(sf, 'streamOptimized')
        except HelperNotFoundError as e:
            self.fail(e.strerror)

    @mock.patch('COT.helpers.qemu_img.QEMUImg.version',
                new_callable=mock.PropertyMock,
                return_value=StrictVersion("1.0.0"))
    def test_disk_conversion_old_qemu(self, _):
        """Test disk conversion flows with older qemu-img version."""
        self.raw_to_vmdk_stream_optimized_test()
        self.vmdk_to_vmdk_stream_optimized_test()
        self.qcow2_to_vmdk_stream_optimized_test()

    @mock.patch('COT.helpers.qemu_img.QEMUImg.version',
                new_callable=mock.PropertyMock,
                return_value=StrictVersion("2.1.0"))
    def test_disk_conversion_new_qemu(self, _):
        """Test disk conversion flows with newer qemu-img version."""
        self.raw_to_vmdk_stream_optimized_test()
        self.vmdk_to_vmdk_stream_optimized_test()
        self.qcow2_to_vmdk_stream_optimized_test()

    def test_convert_to_raw(self):
        """No support for converting VMDK to RAW at present."""
        self.assertRaises(NotImplementedError,
                          convert_disk_image,
                          self.blank_vmdk, self.temp_dir, 'raw', None)


class TestCreateDiskImage(COT_UT):
    """Test cases for create_disk_image()."""

    def test_create_invalid(self):
        """Invalid arguments."""
        # Must specify contents or capacity
        self.assertRaises(RuntimeError,
                          create_disk_image,
                          os.path.join(self.temp_dir, "out.iso"))
        # If extension not given, cannot guess file format
        self.assertRaises(RuntimeError,
                          create_disk_image,
                          os.path.join(self.temp_dir, "out"),
                          capacity="1M")
        # Trying to create a VHD format image, not currently possible
        self.assertRaises(HelperError,
                          create_disk_image,
                          os.path.join(self.temp_dir, "out.vhd"),
                          capacity="1M")
        self.assertRaises(HelperError,
                          create_disk_image,
                          os.path.join(self.temp_dir, "out.vmdk"),
                          file_format="vhd",
                          capacity="1M")
        # Don't know how to populate a qcow2 image with a file
        self.assertRaises(NotImplementedError,
                          create_disk_image,
                          os.path.join(self.temp_dir, "out.vmdk"),
                          file_format="qcow2",
                          contents=[self.input_ovf])

    def test_create_iso_with_contents(self):
        """Creation of ISO image containing files."""
        disk_path = os.path.join(self.temp_dir, "out.iso")
        try:
            create_disk_image(disk_path, contents=[self.input_ovf])
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        # TODO check ISO contents

    # Creation of empty disks is tested implicitly in other test classes
    # above - no need to repeat that here

    def test_create_raw_with_contents(self):
        """Creation of raw disk image containing files."""
        disk_path = os.path.join(self.temp_dir, "out.img")
        try:
            create_disk_image(disk_path, contents=[self.input_ovf])
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        (f, sf) = get_disk_format(disk_path)
        self.assertEqual(f, 'raw')
        self.assertEqual(sf, None)
        try:
            capacity = get_disk_capacity(disk_path)
            self.assertEqual(capacity, "8388608")
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        # TODO check raw file contents

        # Again, but now force the disk size
        try:
            create_disk_image(disk_path, contents=[self.input_ovf],
                              capacity="64M")
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        (f, sf) = get_disk_format(disk_path)
        self.assertEqual(f, 'raw')
        self.assertEqual(sf, None)
        try:
            capacity = get_disk_capacity(disk_path)
            self.assertEqual(capacity, "67108864")
        except HelperNotFoundError as e:
            self.fail(e.strerror)
        # TODO check raw file contents


@mock.patch('COT.helpers.helper.Helper._check_call')
@mock.patch('os.makedirs')
@mock.patch('os.path.exists', return_value=False)
@mock.patch('os.path.isdir', return_value=False)
class TestCreateInstallDir(COT_UT):
    """Test cases for create_install_dir()."""

    def test_already_exists(self, mock_isdir, mock_exists,
                            mock_makedirs, mock_check_call):
        """Test case where the target directory already exists."""
        mock_isdir.return_value = True
        self.assertTrue(create_install_dir('/foo/bar'))
        mock_isdir.assert_called_with('/foo/bar')
        mock_exists.assert_not_called()
        mock_makedirs.assert_not_called()
        mock_check_call.assert_not_called()

    def test_not_directory(self, mock_isdir, mock_exists,
                           mock_makedirs, mock_check_call):
        """Test case where a file exists at the target path."""
        mock_exists.return_value = True
        self.assertRaises(RuntimeError, create_install_dir, '/foo/bar')
        mock_isdir.assert_called_with('/foo/bar')
        mock_exists.assert_called_with('/foo/bar')
        mock_makedirs.assert_not_called()
        mock_check_call.assert_not_called()

    def test_permission_ok(self, mock_isdir, mock_exists,
                           mock_makedirs, mock_check_call):
        """Successfully create directory with user permissions."""
        self.assertTrue(create_install_dir('/foo/bar'))
        mock_isdir.assert_called_with('/foo/bar')
        mock_exists.assert_called_with('/foo/bar')
        mock_makedirs.assert_called_with('/foo/bar', 493)  # 493 == 0o755
        mock_check_call.assert_not_called()

    def test_need_sudo(self, mock_isdir, mock_exists,
                       mock_makedirs, mock_check_call):
        """Directory creation needs sudo."""
        mock_makedirs.side_effect = OSError
        self.assertTrue(create_install_dir('/foo/bar'))
        mock_isdir.assert_called_with('/foo/bar')
        mock_exists.assert_called_with('/foo/bar')
        mock_makedirs.assert_called_with('/foo/bar', 493)  # 493 == 0o755
        mock_check_call.assert_called_with(
            ['sudo', 'mkdir', '-p', '--mode=755', '/foo/bar'])

    def test_nondefault_permissions(self, mock_isdir, mock_exists,
                                    mock_makedirs, mock_check_call):
        """Non-default permissions should be applied whether sudo or not."""
        # Non-sudo case
        self.assertTrue(create_install_dir('/foo/bar', 511))  # 511 == 0o777
        mock_isdir.assert_called_with('/foo/bar')
        mock_exists.assert_called_with('/foo/bar')
        mock_makedirs.assert_called_with('/foo/bar', 511)
        mock_check_call.assert_not_called()

        # Sudo case
        mock_makedirs.reset_mock()
        mock_makedirs.side_effect = OSError
        self.assertTrue(create_install_dir('/foo/bar', 511))  # 511 == 0o777
        mock_makedirs.assert_called_with('/foo/bar', 511)
        mock_check_call.assert_called_with(
            ['sudo', 'mkdir', '-p', '--mode=777', '/foo/bar'])


@mock.patch('COT.helpers.helper.Helper._check_call')
@mock.patch('shutil.copy')
class TestInstallFile(COT_UT):
    """Test cases for install_file()."""

    def test_permission_ok(self, mock_copy, mock_check_call):
        """File copy succeeds with user permissions."""
        self.assertTrue(install_file('/foo', '/bar'))
        mock_copy.assert_called_with('/foo', '/bar')
        mock_check_call.assert_not_called()

    def test_need_sudo(self, mock_copy, mock_check_call):
        """File copy needs sudo."""
        mock_copy.side_effect = OSError
        self.assertTrue(install_file('/foo', '/bar'))
        mock_copy.assert_called_with('/foo', '/bar')
        mock_check_call.assert_called_with(['sudo', 'cp', '/foo', '/bar'])
