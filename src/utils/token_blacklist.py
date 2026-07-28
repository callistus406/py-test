
blacklist:set = set()
class BlacklistToken:
    def add_token(token:str):
        blacklist.add(token)
        print("Token added", token)

    def is_blacklisted(token:str):
        print(token ,blacklist )
        return token in blacklist
