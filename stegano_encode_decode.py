import argparse
import math, wave, struct
from scipy.io import wavfile
import numpy as np

from aes_helpers_enc_dec import *

inpt1 = 'dope.wav'
inpt2 = 'fsMsg.wav'
outpt = 'dope_fs.wav'


def encode_audio():
  
    global inpt1, inpt2, outpt

    print('Convert the second sound from 2 to 1 ch')
    fromNto1Ch(inpt2)
    print('Done!')

    print('Read the carrier and the secret')
    rate1, audio1 = wavfile.read(inpt1)
    rate2, audio2 = wavfile.read('aux'+inpt2)
    print('Done!')

    print('Encode the secret in carrier')
    encode_audio_on_audio_carrier(audio1, audio2, outpt, rate1)
    print('Done!')

def decode_audio():

    global outpt

    print('Read the carrier injected with secret')
    rate1, audio = wavfile.read(outpt)
    print('Done!')

    print('Extract the secret')
    decode_audio_from_audio_carrier(audio, outpt, rate1)
    print('Done!')


    

if __name__ == '__main__':

    print('Encode - audio')
    encode_audio()
    print('Done')

    print('Extract audio')
    decode_audio()
    print('Done')

