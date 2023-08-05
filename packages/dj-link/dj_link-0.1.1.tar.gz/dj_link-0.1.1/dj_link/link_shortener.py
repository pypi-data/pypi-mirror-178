import pyshorteners


class Link_Shortener:
    def __init__(self):
        self.x = pyshorteners.Shortener(api_key='8c4178f31b7aaedc3cfc0bdf9390f686afa3e664')

    def Run(self):
        UI = input("""
1. http
2. https

Enter the number: """)

        url_input = input("Enter the url: ")
        if UI == "1":
            y = "http://"
            link = self.x.bitly.short(y+url_input)
            print(link)
        elif UI == "2":
            y = "https://"
            link = self.x.bitly.short(y + url_input)
            print(link)
