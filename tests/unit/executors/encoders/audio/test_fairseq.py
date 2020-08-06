import os
import pytest

import numpy as np

from jina.executors.encoders.audio.fairseq import Wav2VecSpeechEncoder
from tests.unit.executors import ExecutorTestCase


class FairSeqTestCase(ExecutorTestCase):
    def _get_encoder(self):
        self.target_output_dim = 512
        return Wav2VecSpeechEncoder(model_path='/tmp/wav2vec_large.pt', input_sample_rate=16000)

    @pytest.mark.skipif('JINA_TEST_PRETRAINED' not in os.environ, reason='skip the pretrained test if not set')
    def test_encoding_results(self):
        batch_size = 10
        signal_length = 1024
        test_data = np.random.randn(batch_size, signal_length).astype('f')
        encoder = self._get_encoder()
        encoded_data = encoder.encode(test_data)
        self.assertEqual(encoded_data.shape[0], batch_size)
        self.assertTrue(encoded_data.shape[1] % self.target_output_dim == 0)
