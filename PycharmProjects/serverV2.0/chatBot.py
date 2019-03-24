from __future__ import unicode_literals
import requests
import pickle
from model import *

print("Write Your Name:")


with open('./data/seq2seq.pk', 'rb') as f:
    data = pickle.load(f)
input_lang = data['input_lang']
output_lang = data['output_lang']
encoder = data['encoder']
attn_decoder = data['attn_decoder']
hidden_size = encoder.hidden_size


# print(get_answer("привет", input_lang, output_lang, encoder, attn_decoder))



name = input()
add = requests.post("http://127.0.0.1:5000/find_user", data=name)

print("Okey, your id is %s and now you can chat with bot" % add.text)

print("write me smth, %s, and i will answer" % name)
# print("me: ")
new_request = input("me: ")
# new_request.encode('latin-1')
while(new_request != "exit"):
    print("bot: %s" % get_answer(new_request, input_lang, output_lang, encoder, attn_decoder))
    # r = requests.post("http://127.0.0.1:5000/get_ans/0", data=new_request.encode('utf-8'))
    # print(r.text)
    new_request = input("me: ")
