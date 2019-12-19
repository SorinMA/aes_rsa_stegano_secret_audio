from aes_helpers_enc_dec import *

import math, wave, struct
from scipy.io import wavfile

carrier_name = 'dope.wav'
encoded_carrier = 'shit.wav'

def send_kc(PK):

    global carrier_name, encoded_carrier

    # get the audio carrier

    print('Read the Carrier')
    rate, audio = wavfile.read(carrier_name)
    left = audio[...,0].copy()
    right = audio[...,1].copy()
    print('Read done!')

    print('Generate the K and IV for AES')
    k, IV = generate_k_iv_aes() # generate de SK & PK
    print('Done!')
    

    print('Encrypt K & IV with PK') # after use dec_RSA_and_enb_b64 to dec
    k_enc = enc_RSA_and_enb_b64(PK, k) 
    IV_enc = enc_RSA_and_enb_b64(PK, IV)
    print('Done!')

    print('Convert fromated K & IV to bin')
    k_enc_bin = from_str_to_bit(k_enc)
    k_enc_bin_str = from_array_to_values(k_enc_bin) # use this

    IV_enc_bin = from_str_to_bit(IV_enc)
    IV_enc_bin_str = from_array_to_values(IV_enc_bin) # use this
    print('Done!')

    print('Encode in carrier K|IV')
    write_to_carrier(left, right, k_enc_bin_str + IV_enc_bin_str, encoded_carrier, rate)
    print('Done!')
 


def recive_kc(SK):
    
    global encoded_carrier

    # read the encoded carrier

    print('Read the Carrier')
    rate, audio = wavfile.read(encoded_carrier)
    left = audio[...,0].copy()
    right = audio[...,1].copy()
    print('Done!')

    print('Extract the length of encoded K|IV')
    len_enc1 = right[0] 
    len_enc2 = right[1] 
    len_enc = len_enc1*1000 + len_enc2
    print('Done!')

    print('Extract K|IV')
    kiv_recived =  extract_pk_from_carrier(left, right, len_enc)
    print('Done')

    print('Convert K|IV to str')
    K_recived = kiv_recived[:(len_enc // 2)]
    IV_recived = kiv_recived[(len_enc // 2):len_enc]

    K_fromated = from_bit_to_str(from_bit_to_byte(K_recived))
    IV_fromated  = from_bit_to_str(from_bit_to_byte(IV_recived))
    
    K_recived_dec = dec_RSA_and_enb_b64(SK, K_fromated)
    IV_recived_dec = dec_RSA_and_enb_b64(SK, IV_fromated)
    print('Done')

    KC_real, IV_real = get_k_IV()
    print('It is the recived K|IV  == with real K|IV (the sended one?) ? ', ' K_sent == K_recived: ', K_recived_dec == KC_real , '| IV_sent == IV_recived: ', IV_recived_dec == IV_real)
    

if __name__ == '__main__':
   
    print('Before sending AES key, we need the RSA pk')
    SK, PK = generate_pk_sk_RSA()

    print('First step in comunication! - send the K|IV')
    send_kc(PK)
    print('  ========= ')
    print('2nd step in comunication! - recive the K|IV')
    recive_kc(SK)
