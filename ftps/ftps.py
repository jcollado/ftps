# -*- coding: utf-8 -*-

"""Python interface to FTPS using pycurl."""

import logging
import os

from six import BytesIO

import pycurl


LOGGER = logging.getLogger('ftps')


class FTPS(object):
    """FTPS client based on pycurl.

    :param url: Server URL including authorization
    :type url: str
    :param connect_timeout: Connection timeout in seconds
    :type connect_timeout: int
    :param max_retries: Maximum number of retry attempts
    :type max_retries: int

    """

    def __init__(self, url, connect_timeout=5, max_retries=5):
        """Create pycurl client."""
        assert url.startswith('ftps://'), 'Expected URL scheme is ftps'

        self.base_url = url
        self.connect_timeout = connect_timeout
        self.max_retries = max_retries

        self.client = pycurl.Curl()
        self.reset()

    def reset(self):
        """Reset client.

        This is useful after each operation to make sure the client options are
        set to its default state.

        """
        self.client.reset()
        self.client.setopt(pycurl.SSL_VERIFYPEER, False)
        self.client.setopt(pycurl.SSL_VERIFYHOST, False)
        self.client.setopt(pycurl.CONNECTTIMEOUT, self.connect_timeout)

    def perform(self):
        """Perform operation with retries."""
        retries = 0
        while retries < self.max_retries:
            try:
                self.client.perform()
                LOGGER.debug('Operation performed successfully')
                return
            except pycurl.error as exc:
                LOGGER.warning(exc)
                LOGGER.debug('Retrying (%d)...', retries)
                retries += 1
        LOGGER.error('Failed to perform operation')

    def list(self, remote_dir=None):
        """List files in remote directory.

        :param remote_dir: Path to remote directory to get the file list.
        :type remote_dir: str

        """
        if remote_dir is None:
            # List root directory by default
            remote_dir = ''
        elif not remote_dir.endswith('/'):
            # Make sure that directory ends with a forward slash character
            remote_dir += '/'

        url = '/'.join((self.base_url, remote_dir))
        self.client.setopt(pycurl.URL, url)

        output_buffer = BytesIO()
        self.client.setopt(pycurl.WRITEDATA, output_buffer)

        LOGGER.debug('Listing directory: %s', url)
        self.perform()
        self.reset()

        output = output_buffer.getvalue().decode('utf-8')
        files = [
            line.split()[-1]
            for line in output.split('\n')
            if line
        ]

        return files

    def download(self, remote_filename, local_filename):
        """Download remote file and save it locally.

        :param remote_filename: Path to remote file in server to download.
        :type remote_filename: str
        :param local_filename: Path to local file to create to.
        :type local_filename: str

        """
        url = '/'.join((self.base_url, remote_filename))
        self.client.setopt(pycurl.URL, url)

        with open(local_filename, 'wb') as output_file:
            self.client.setopt(pycurl.WRITEDATA, output_file)
            LOGGER.debug('Downloading file: %s -> %s', url, local_filename)
            self.perform()
        self.reset()

    def upload(self, local_filename, remote_filename):
        """Upload local_filename to server.

        :param local_filename: Path to local file to upload.
        :type local_filename: str
        :param remote_filename: Path to remote file to create.
        :type remote_filename: str

        """
        url = '/'.join((self.base_url, remote_filename))
        self.client.setopt(pycurl.URL, url)

        with open(local_filename, 'rb') as input_file:
            self.client.setopt(pycurl.UPLOAD, True)
            self.client.setopt(pycurl.READDATA, input_file)
            self.client.setopt(
                pycurl.INFILESIZE_LARGE,
                os.path.getsize(local_filename),
            )
            LOGGER.debug('Uploading file: %s -> %s', local_filename, url)
            self.perform()
        self.reset()
