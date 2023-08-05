import json
from requests import get

class Kora():
    def __init__(self, token):
        self.url = 'https://kora-api.vercel.app'
        self.token = token
    
    def chatbot(self, message, owner, botname):
        try:
            url = f"{self.url}/chatbot/{self.token}/{botname}/{owner}/message={message}"
            try:
                res = get(url)
                Kora = json.loads(res.text)
                msg = Kora['reply']
                return msg
            except:
                result = "I'm Busy Now"
                return result
        except Exception as e:
            return e
        


