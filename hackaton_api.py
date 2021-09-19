import requests

def synthesis_text(text):
    res = requests.get('https://translate.tatar/byhackathon_synthesize', params={
        'text' : text
    })
    return res.content
