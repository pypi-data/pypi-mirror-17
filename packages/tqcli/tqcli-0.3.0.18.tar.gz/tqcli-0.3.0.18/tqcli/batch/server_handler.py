import requests
import json
import base64
import os
import logging
import glob

from tqcli.batch.file_manager import TQFile
from tqcli.config.config import DEFAULT_CHUNK_SIZE

logger = logging.getLogger(os.path.basename(__file__))


class Client(object):
    endpoints = {
        'initiate': '/upload/initiate/',
        'part': '/upload/part/',
        'complete': '/upload/complete/'
    }

    def __init__(self, root_url, token, datasource_id, dataset_id):
        self.root_url = root_url
        self.datasource_id = datasource_id
        self.dataset_id = dataset_id
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'token token="%s"' % self.token, 'Content-Type': 'application/json'})

    def upload_file_in_parts(self, tq_file):
        filename = tq_file.filename()
        file_and_upload_id = self.initiate_multipart_upload(filename)
        upload_id = file_and_upload_id["upload_id"]
        self.dataset_id = file_and_upload_id['file']['dataset_id']
        part_tags = [self.upload_part(upload_id, bytes_to_be_read, chunk_iterator, a_chunk, filename, total_chunks)
            for chunk_iterator, bytes_to_be_read, from_byte, to_byte, remained_bytes, a_chunk, total_chunks in tq_file.chunks()]
        self.upload_complete(upload_id, part_tags, filename)

    def _format_response(self, content):
        return '\tFile Name: %s\n\tData Source ID: %s\n\tData Set ID: %s\n\tUpload ID: %s' % (
            content.get('file').get('filename'),
            content.get('file').get('datasource_id'),
            content.get('file').get('dataset_id'),
            content.get('upload_id'),
        )

    def initiate_multipart_upload(self, filename):
        url = self.root_url + Client.endpoints['initiate']
        payload = {
          'datasource_id': self.datasource_id,
          'filename': filename
        }
        response = self.session.post(url, data=json.dumps(payload))
        logger.info('Initiated upload response...\n' + self._format_response(response.json()))
        if response.status_code == 401:
            raise Exception("We could not authenticate :( your token doesn't seem to be valid!")
        return json.loads(response.content.decode('utf-8'))

    def upload_part(self, upload_id, part_size, part_number, part, filename, total_parts):
        url = self.root_url + Client.endpoints['part']
        payload = {
            'file': {
              'datasource_id': self.datasource_id,
              'dataset_id': self.dataset_id,
              'filename': filename
            },
            'upload_id': upload_id,
            'part_number': part_number,
            'part_size': part_size,
            'base64_part': base64.b64encode(part).decode('utf-8')
        }
        logger.info("Uploading part %s of %s (%s bytes)" % (part_number, total_parts, part_size))
        response = self.session.post(url, data=json.dumps(payload))
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            logger.debug(response.content)
            raise Exception('Failed to upload part - Response Status: %d' % response.status_code)

    def upload_complete(self, upload_id, part_tags, filename):
        url = self.root_url + Client.endpoints['complete']
        payload = {
            'file': {
                'datasource_id': self.datasource_id,
                'dataset_id': self.dataset_id,
                'filename': filename
            },
            'upload_id': upload_id,
            'part_tags': part_tags
        }
        response = self.session.post(url, data=json.dumps(payload))
        if response.status_code == 200:
            logger.info("Yes! Upload completed!")
        else:
            logger.debug(response.content)
            raise Exception('Status code of upload confirmation is %d' % response.status_code)

    def close(self):
        self.session.close()


class TranQuant(object):
    def __init__(self, root_url, token, datasource_id, dataset_id):
        self.client = Client(root_url, token, datasource_id, dataset_id)

    def upload(self, input_path):
        for path in glob.glob(input_path):
            tq_file = TQFile(path, chunk_size=DEFAULT_CHUNK_SIZE)
            if not tq_file.is_valid():
              raise Exception("This file does not seem to be valid!")
            self.client.upload_file_in_parts(tq_file)
        logger.info('-'*80)

    def is_valid(self):
        if not self.client.datasource_id:
            logger.debug(self.client.__dict__)
            raise Exception('You forgot to provide a Data Source ID :)')

        if not self.client.token:
            logger.debug(self.client.__dict__)
            raise Exception('You forgot to provide a valid Token ID :)')