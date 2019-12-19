
# Martinescu Sorin-Alexandru

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import random
import numpy as np
from scipy.io import wavfile

sk = None
pk = None
kc = None
iv = None

mare_aux1 = None
mare_aux2 = None

def generate_pk_sk_RSA():
    global sk, pk
    sk = RSA.generate(1024)
    pk  = sk.publickey()
    return sk, pk

def generate_k_iv_aes():
    global kc, iv
    kc = get_random_bytes(16)
    iv = get_random_bytes(16)
    return kc, iv

def enc_RSA_and_enb_b64(PK, to_enc):
    encoded = PK.encrypt(to_enc, 16)[0]
    return str(base64.b64encode(encoded), 'utf8')

def get_k_IV():
    global kc, iv
    return kc, iv

def dec_RSA_and_enb_b64(SK, to_dec):
    formated = base64.b64decode(to_dec)
    decrypted = SK.decrypt(formated)
    return decrypted

def comlete_with_rand(size_rand):
    to_concatenate = ''
    while True:
        if size_rand ==0:
            break
        size_rand -= 1
        to_concatenate = to_concatenate + chr(random.randint(0, 128))
    return to_concatenate

def export_formated_pk():
    global pk
    exported_pk = pk.exportKey('PEM').decode('utf8')
    exported_pk = exported_pk[27:(len(exported_pk) - 25)]
    return exported_pk

def from_str_to_bit(from_val):
    to_ret = []
    for i in from_val:
        to_ret.append("{0:07b}".format(ord((i))))

    return to_ret

def from_array_to_values(vals):
    to_ret = ''
    for i in vals:
        for j in i:
            to_ret = to_ret + j
    return to_ret


def write_to_carrier(left, right, bin_enc_pk, save_name, rate):

    len_enc = len(bin_enc_pk) # len of array str to encode
    add = int((len(left) / (len_enc)) - 1) 
    add = int(((len(left) - 4 - 4 * add) / (len_enc)) - 1) 
    print('Dist. btw. 2 encoded bites = ' + str(add))

    left[0] = right[0] = len_enc / 1000.0
    left[1] = right[1] = len_enc % 1000.0

    while len(bin_enc_pk) % 6 != 0:
        bin_enc_pk = bin_enc_pk + '0'

    print('Dist. btw. 2 encoded (after % 6 == 0 extended) bites = ' + str( int((len(left) / (len(bin_enc_pk) )) - 1)))

    if add >= 4:
        print("OK")
    
        index = 0
        contor = 4 + 4 * add
        while index < len_enc:
            add_on_left = int(bin_enc_pk[index]) * 4 + int(bin_enc_pk[index + 1]) * 2 + int(bin_enc_pk[index + 2])
            add_on_right = int(bin_enc_pk[index + 3]) * 4 + int(bin_enc_pk[index + 4]) * 2 + int(bin_enc_pk[index + 5])

            left[contor] = np.sign(left[contor])*((int(np.abs(left[contor])/10)*10) + int(np.abs(add_on_left)))
            right[contor] = np.sign(right[contor])*((int(np.abs(right[contor])/10)*10) + int(np.abs(add_on_right)))

            contor += add
            index += 6
        audiox = np.column_stack((left, right)).astype(np.int16)

        wavfile.write(save_name ,rate, audiox)
    else:
        print('Ur carrier should be min 6x longer the ur msg for this king of stegano')

def extract_pk_from_carrier(left, right, len_enc):
    frame =  ''
    
    add = int((len(left) / (len_enc)) - 1) 
    add = int(((len(left) - 4 - 4 * add) / (len_enc)) - 1) 

    print('Dist. btw. 2 encoded bites = ' + str(add))
    
    index = 0
    contor = 4 + 4 * add

    while index < len_enc:
        add_on_left = "{0:03b}".format(int(np.abs(left[contor])%10))
        add_on_right = "{0:03b}".format(int(np.abs(right[contor])%10))
        frame = frame + add_on_left + add_on_right

        contor += add
        index  += 6
    return frame

def from_bit_to_str(from_val):
    to_ret = ''
    contor = 8
    aux = ''
    for i in from_val:
        to_conv = b''
        for v in i:
            if v == '1':
                to_conv += b'1'
            else:
                to_conv += b'0'
        to_ret = to_ret + (chr(int(i,2)))
    return to_ret
                


def from_bit_to_byte(from_val):
    to_ret = []
    for i in range(0, len(from_val), 7):
        to_ret.append(from_val[i:i+7])
                  
    return to_ret    

def import_formated_pk(pk_formated):
    global pk
    exported_pk = ('-----BEGIN PUBLIC KEY-----\n' + pk_formated + '\n-----END PUBLIC KEY-----').encode('utf8')
    return exported_pk, pk

def fromNto1Ch(inpt):
    rate, audio = wavfile.read(inpt)
    try:
        nrOfChannels = len(audio[0])   
        monoChFrame = (np.array([0]*len(audio[...,0]))).astype(np.float)
        for i in range(nrOfChannels):
            monoChFrame += 1/nrOfChannels*(audio[...,i]).astype(np.float)
        wavfile.write('aux'+inpt,rate,monoChFrame.astype(np.int16))
        print('Step - ok')
    except:
        wavfile.write('aux'+inpt,rate,audio.astype(np.int16))
        print('Step - ok but exception')



def convert_audio_array_in_str_fromated_for_aes_16b(audio):
   
    to_ret = ''.join((str(e) + '|') for e in audio)

    while len(to_ret) % 16 != 0:
        to_ret = to_ret + '|'
    
    return to_ret


def enc_with_aes(K, IV, frame):
    aes_obj = AES.new(kc, AES.MODE_CBC, iv)
    enc = aes_obj.encrypt(frame)
    return enc

def dec_with_aes(K, IV, frame):
    aes_obj = AES.new(kc, AES.MODE_CBC, iv)
    dec = aes_obj.decrypt(frame)
    return dec

def create_enc_frame(audio_enc):
    aux = np.ndarray(shape=(len(audio_enc),), dtype=int)

    index = 0

    for index in range(len(audio_enc)):
        aux[index] = ord(audio_enc[index])
    return aux

def enc_aes_audio(inpt, K, IV):
    rate, audio = wavfile.read(inpt)

    audio_string = convert_audio_array_in_str_fromated_for_aes_16b(audio)
    audio_string_enc = enc_with_aes(K, IV, audio_string)
    audio_string_enc_b64 = str(base64.b64encode(audio_string_enc), 'utf8')
    audio_string_enc_b64 = chr(random.randint(160, 256)) * 3000 + audio_string_enc_b64 + chr(random.randint(160, 256)) * 3000 # padding 
    audio_frame_enc = create_enc_frame(audio_string_enc_b64)
    wavfile.write('enc'+inpt,rate,audio_frame_enc.astype(np.int16))

def reverse_enc_frame(audio_enc):
    aux = ''
    for i in audio_enc:
        if i < 160:
            aux = aux + chr(i)

    return aux

def create_dec_frame(audio_dec):
    audio_dec = audio_dec.split('|')
    pos_of_nothing = audio_dec.index('')
    audio_dec_splited = audio_dec[:pos_of_nothing]
    aux = np.ndarray(shape=(len(audio_dec_splited),), dtype=int)

    index = 0

    for index in range(len(audio_dec_splited)):
        aux[index] = int(audio_dec_splited[index])
    return aux

def dec_aes_audio(inpt, K, IV):
    rate, audio = wavfile.read(inpt)

    audio_string_enc_b64 = reverse_enc_frame(audio)
    audio_string_enc = base64.b64decode(audio_string_enc_b64)   
    audio_string_dec = dec_with_aes(K, IV, audio_string_enc)
    audio_array_from_string = create_dec_frame(str(audio_string_dec, 'utf8'))
    wavfile.write('dec'+inpt,rate,audio_array_from_string.astype(np.int16))

def encode_audio_on_audio_carrier(audio1, audio2, outpt, rate1):

    left = audio1[...,0].copy()
    right = audio1[...,1].copy()
    left[0] = right[0] = len(audio2) / 1000.0
    left[1] = right[1] = len(audio2) % 1000.0

    contor = 4
    add = int((len(left) / len(audio2) - 1))
    if add >= 6:
        print("OK")
    
        index = 0
        while index < len(audio2):
            aux = int(np.abs(audio2[index]))
            left[contor + 5] = np.sign(left[contor+5])*((int(np.abs(left[contor+5])/10)*10)  + 1+ np.sign(audio2[index])) 
            right[contor + 4] = np.sign(right[contor+4])*((int(np.abs(right[contor+4])/10)*10) + int(np.abs(aux) % 10))
            aux = int(aux/10)
            left[contor + 3] =  np.sign(left[contor+3])*((int(np.abs(left[contor+3])/10)*10) + int(np.abs(aux) % 10))
            aux = int(aux/10)
            right[contor + 2] =  np.sign(right[contor+2])*((int(np.abs(right[contor+2])/10)*10) + int(np.abs(aux) % 10))
            aux = int(aux/10)
            left[contor + 1] =  np.sign(left[contor+1])*((int(np.abs(left[contor+1])/10)*10) + int(np.abs(aux) % 10))
            aux = int(aux/10)
            right[contor] =  np.sign(right[contor])*((int(np.abs(right[contor])/10)*10) + int(np.abs(aux) % 10))
            contor += add
            index +=1
        audiox = np.column_stack((left, right)).astype(np.int16)

        wavfile.write(outpt,rate1,audiox)
    else:
        print('Ur carrier should be min 6x longer the ur msg for this king of stegano')

def decode_audio_from_audio_carrier(audio1, outpt, rate1):
    left = audio1[...,0].copy()
    right = audio1[...,1].copy()
    a1 = right[0] 
    a2 = right[1] 
    a = a1*1000+a2

    frame =  np.array([])
    add = int((len(left) / a - 1))
    contor = 4
    index = 0
    narray = []
    while index < a:
        aux = 0
        aux += int(np.abs(right[contor])%10)  
        aux = aux * 10 + int(np.abs(left[contor+1])%10)  
        aux = aux * 10 + int(np.abs(right[contor+2])%10)
        aux = aux * 10 + int(np.abs(left[contor+3])%10)  
        aux = aux * 10 + int(np.abs(right[contor+4])%10)
        signA = int(np.abs(left[contor + 5])%10)
        aux = aux * (signA - 1)
        narray.append(aux)
        contor += add
        index = index + 1
    frame = np.append(frame, narray)

    wavfile.write('dec'+outpt,rate1,(frame.T).astype(np.int16))

