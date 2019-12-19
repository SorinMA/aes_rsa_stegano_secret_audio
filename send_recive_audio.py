import argparse
import math, wave, struct
from scipy.io import wavfile
import numpy as np

from aes_helpers_enc_dec import *

inpt = 'fsMsg.wav'


if __name__ == '__main__':

    print('Get the AES K')
    generate_k_iv_aes()
    K, IV = get_k_IV()
    print(K, IV)
    print('Done')

    print('Enc AES audio')
    enc_aes_audio(inpt, K, IV)
    print('Done')

    print('Dec AES audio')
    dec_aes_audio('enc'+inpt, K, IV)
    print('Done')