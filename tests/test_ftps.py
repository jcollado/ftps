#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test FTPS client."""

import pytest

from mock import patch
from six import (
    BytesIO,
)
from six.moves import range

from ftps import FTPS


@pytest.fixture(name='pycurl')
def fixture_pycurl():
    """Patch pycurl library."""
    patcher = patch('ftps.ftps.pycurl')
    pycurl = patcher.start()
    yield pycurl
    patcher.stop()


@pytest.fixture(name='logger')
def fixture_logger():
    """Patch logging library."""
    patcher = patch('ftps.ftps.LOGGER')
    logger = patcher.start()
    yield logger
    patcher.stop()


def test_valid_url_scheme():
    """Client instance created if URL starts with ftps://."""
    FTPS('ftps://<user>:<password>@host')


def test_invalid_url_scheme():
    """AssertionError raised if URL doesn't start with ftps://."""
    with pytest.raises(AssertionError):
        FTPS('<url>')


class TestList(object):

    """Test directory listing."""

    def helper(self, pycurl, directory=None):
        """List remote directory content."""
        client = pycurl.Curl()

        def setopt(option, value):
            """Mock function to set output buffer."""
            if option == pycurl.WRITEDATA:
                client.output_buffer = value

        client.setopt.side_effect = setopt

        def perform():
            """Mock function to write directory listing to output buffer."""
            client.output_buffer.write(
                b'drwxr-xr-x 1 ftp ftp              0 Jan 00 00:00 d1\n'
                b'drwxr-xr-x 1 ftp ftp              0 Jan 00 00:00 d2\n'
                b'drwxr-xr-x 1 ftp ftp              0 Jan 00 00:00 d3\n'
                b'-rw-r--r-- 1 ftp ftp              0 Jan 00 00:00 f1.txt\n'
                b'-rw-r--r-- 1 ftp ftp              0 Jan 00 00:00 f2.txt\n'
                b'-rw-r--r-- 1 ftp ftp              0 Jan 00 00:00 f3.txt\n'
            )

        client.perform.side_effect = perform

        ftps = FTPS('ftps://<user>:<password>@host')
        files = ftps.list(directory)
        expected_files = ['d1', 'd2', 'd3', 'f1.txt', 'f2.txt', 'f3.txt']
        assert files == expected_files

    def test_list_no_argument(self, pycurl):
        """List default remote directory content."""
        self.helper(pycurl)

    def test_list_no_slash(self, pycurl):
        """List remote directory content."""
        self.helper(pycurl, '')


def test_download(pycurl):
    """Download remote file."""
    client = pycurl.Curl()

    def setopt(option, value):
        """Mock function to set output buffer."""
        if option == pycurl.WRITEDATA:
            client.output_buffer = value

    client.setopt.side_effect = setopt

    def perform():
        """Mock function to write downloaded file to output buffer."""
        client.output_buffer.write(b'<output>')

    client.perform.side_effect = perform

    ftps = FTPS('ftps://<user>:<password>@host')

    output_buffer = BytesIO()
    with patch('ftps.ftps.open') as open_:
        open_().__enter__.return_value = output_buffer
        ftps.download('f1.txt', 'f1.txt')

    assert output_buffer.getvalue() == b'<output>'


def test_upload(pycurl):
    """Upload local file."""
    client = pycurl.Curl()

    def setopt(option, value):
        """Mock function to set input buffer."""
        if option == pycurl.READDATA:
            client.input_buffer = value

    client.setopt.side_effect = setopt

    def perform():
        """Mock function to read local file from input buffer."""
        client.input_buffer.read()

    client.perform.side_effect = perform

    ftps = FTPS('ftps://<user>:<password>@host')

    input_buffer = BytesIO(b'<input>')
    with patch('ftps.ftps.open') as open_, patch('ftps.ftps.os'):
        open_().__enter__.return_value = input_buffer
        ftps.upload('f1.txt', 'f1.txt')

    assert input_buffer.read() == b''


def test_perform_retries(pycurl, logger):
    """Retry on failure as many attempts as requested."""
    client = pycurl.Curl()
    # Use base exception class, since pycurl has been mocked
    pycurl.error = Exception
    client.perform.side_effect = pycurl.error(28, 'Connection time-out')

    ftps = FTPS('ftps://<user>:<password>@host')
    ftps.perform()

    for retries in range(ftps.max_retries):
        logger.debug.assert_any_call('Retrying (%d)...', retries)
    logger.error.assert_called_once_with('Failed to perform operation')
