from aes_helpers_enc_dec import *

import math, wave, struct
from scipy.io import wavfile

carrier_name = 'dope.wav'
encoded_carrier = 'shit.wav'

def send_pk():

    global carrier_name, encoded_carrier

    # get the audio carrier

    print('Read the Carrier')
    rate, audio = wavfile.read(carrier_name)
    left = audio[...,0].copy()
    right = audio[...,1].copy()
    print('Read done!')

    print('Generate the PK & SK via RSA')
    generate_pk_sk_RSA() # generate de SK & PK
    print('Done!')

    print('Format PK')
    formated_pk = export_formated_pk() # fromat PK 
    print('Done!')

    print('Convert fromated PK to bin')
    formate_pk_bin = from_str_to_bit(formated_pk)
    formate_pk_bin_str = from_array_to_values(formate_pk_bin)
    print('Done!')
    
    print('Encode in carrier')
    write_to_carrier(left, right, formate_pk_bin_str, encoded_carrier, rate)
    print('Done!')


def recive_pk():
    
    global encoded_carrier

    # read the encoded carrier

    print('Read the Carrier')
    rate, audio = wavfile.read(encoded_carrier)
    left = audio[...,0].copy()
    right = audio[...,1].copy()
    print('Done!')

    print('Extract the length of encoded pk')
    len_enc1 = right[0] 
    len_enc2 = right[1] 
    len_enc = len_enc1*1000 + len_enc2
    print('Done!')

    print('Extract PK')
    pk_recived =  extract_pk_from_carrier(left, right, len_enc)
    print('Done')

    print('Convert PK to str')
    pk_recived = pk_recived[:len_enc]
    pk_fromated = from_bit_to_str(from_bit_to_byte(pk_recived))
    pk_ready_to_import, real_pk = import_formated_pk(pk_fromated)
    print('Done')

    print('It is the recived pk key == with real pk key (the sended one?) ? ', real_pk.exportKey('PEM') == pk_ready_to_import)
    

if __name__ == '__main__':
   
    print('First step in comunication! - send the pk')
    send_pk()
    print('  ========= ')
    print('2nd step in comunication! - recive the pk')
    recive_pk()
