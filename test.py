import requests

url = 'https://support.readaloud.app/read-aloud/list-voices/premium'
r = requests.get(url).json()

# for item in r:
#     if item['voiceName'].startswith('Amazon'):
#         # raw = item['voiceName'].split(' (')
#         # lang = raw[0].replace('Amazon ', '')
#         # name = raw[1].replace(')','')

#         print(item['voiceName'].replace('Amazon ', ''))

# a = " ".join([item for item in r])


# for item in r:
#     if item['voiceName'].startswith('Amazon'):
#         print(item['voiceName'].replace('Amazon ', ''))
#         a = "\n".join(f"{item['voiceName'].replace('Amazon ', '')}")


# print(a)

langs_dict = {}
for item in r:
    if item['voiceName'].startswith('Amazon'):
        langs_dict.update({item['voiceName'].replace('Amazon ', ''):item['lang']})

# a = '\n'.join(langs_dict.keys())

a = '\n'.join([f'{text[0]} :flag_{text[1].split("-")[0]}:' for text in langs_dict.items()])
print(a)
