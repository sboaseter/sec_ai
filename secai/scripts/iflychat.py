import requests
class IFlyPoster:
    def __init__(self):
        self.ifc_key = "Ff3bAAZyGtK09tos5ZfXZLEvRy_60nkFsVMhy79vvykW6831" 
        self.publish_url = "https://api.iflychat.com/api/1.1/room/11/publish"

    def postMessage(self, ifc_message):
        try:
            r = requests.post(self.publish_url, 
                data = { 
                    'api_key': self.ifc_key,
                    'uid': 42, 
                    'name': 'secai',
                    'picture_url': 'http://www.vnrllc.com/wp-content/uploads/2015/04/sec-filings.jpg',
                    'profile_url': 'javascript:void(0)',
                    'message': ifc_message,
                    'color': '#222222',
                    'roles[]': '0'
                })

            if r.ok == True:
                pass
            else:
                pass
        except:
            pass


