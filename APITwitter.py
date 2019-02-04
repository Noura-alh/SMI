from TwitterAPI import TwitterAPI

SEARCH_TERM = '"حجاج العجمي"'
PRODUCT = 'fullarchive'
LABEL = 'TestSMI'
SANDBOX_CONSUMER_KEY = 'JR6dkIC3Cm0E9iQiFQQnRQDXl'
SANDBOX_CONSUMER_SECRET = 'zbhilbf0TpELOLvmmx83LgcYYG3p9hWqvOnJGGuY75XyeI0DIm'
SANDBOX_TOKEN_KEY = '557269145-mDE9g2ern37MjnzUQO3e8PeRpiteF3jd8RSgJuGd'
SANDBOX_TOKEN_SECRECT = 'I1d8sI0pVC4TdDDdohCy1WgZ2GvZOgkJx7C5FBenIvrDL'


api = TwitterAPI(SANDBOX_CONSUMER_KEY,
                 SANDBOX_CONSUMER_SECRET,
                 SANDBOX_TOKEN_KEY,
                 SANDBOX_TOKEN_SECRECT)

r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                {'query':SEARCH_TERM})
f = open("Twitterresult.txt", "w+")
for item in r:
    f.write(item['text'] + '\n')
    print(item['text'] if 'text' in item else item)

f.close()