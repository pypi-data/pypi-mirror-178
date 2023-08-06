import requests
import json
import string
import TvShaBot.tv_program as tv_program


class Bot:
    special_commands = ["$show", "$add", "$delete"]

    def __init__(self, token):
        api_url = "https://api.telegram.org/bot"
        self.url = api_url + token + "/"
        self.favourites = dict()
        self.current_shows = dict()

    def send_message(self, client_id, text):
        mes_url = self.url + f"sendMessage?chat_id={client_id}&text={text}"
        requests.get(mes_url)

    def get_update(self, prev):
        get_url = self.url + "getUpdates"
        offset_param = {"offset": -1}
        while True:
            response = requests.get(get_url, params=offset_param).text
            data = json.loads(response)
            if data != prev:
                return data

    def start(self):
        prev = self.get_update(None)
        while True:
            data = self.get_update(prev)
            client_id = data["result"][0]["message"]["chat"]["id"]
            verify = self.verify_data(data)
            print(data)
            if verify == "is_tv_show":
                show_name = data["result"][0]["message"]["text"]
                try:
                    show_info = tv_program.get_show_info(show_name)
                    answer = "\n".join(show_info)
                    self.current_shows[client_id] = show_name
                    self.send_message(client_id, answer)
                except ValueError:
                    self.send_message(client_id, "Never heard about it")
            elif verify == "is_command":
                command = data["result"][0]["message"]["text"]
                self.try_execute_command(client_id, command)
            else:
                self.send_message(client_id, "Don't be silly")
            prev = data

    def verify_data(self, data):
        if not data["ok"]:
            print("Error: data is not ok")
            return None
        message = data["result"][0]["message"]
        if "text" not in message:
            print("Error: text not in message")
            return None
        text = message["text"]
        enabled_letters = set(string.ascii_letters + "$1234567890 ")
        not_enabled_letters = set(text) - enabled_letters
        if not_enabled_letters:
            print("Error: not enabled letters")
            return None
        print("VERIFYING IS OKAY")
        first_word = text.split()[0]
        if first_word in Bot.special_commands:
            return "is_command"
        else:
            return "is_tv_show"

    def try_execute_command(self, client_id, command):
        parts = command.split()
        if parts[0] == "$add" and len(parts) == 1:
            if client_id in self.current_shows:
                show = self.current_shows[client_id]
                self.add_show(client_id, show)
            else:
                self.send_message(client_id, "Don't have any to add")
        elif parts[0] == "$delete" and len(parts) > 1:
            show = " ".join(parts[1:len(parts)])
            self.delete_show(client_id, show)
        elif parts[0] == "$show" and len(parts) == 1:
            self.show_shows(client_id)
        else:
            self.send_message(client_id, "Rather strange question")

    def add_show(self, client_id, show):

        if client_id in self.favourites:
            self.favourites[client_id] = self.favourites[client_id] | {show}
        else:
            self.favourites[client_id] = {show}

        self.send_message(client_id, f"Show {show} was added to favourites")

    def delete_show(self, client_id, show):

        if client_id in self.favourites:
            self.favourites[client_id] = self.favourites[client_id] - {show}

        self.send_message(client_id, f"Show {show} no more in favourites")

    def show_shows(self, client_id):
        shows = self.favourites[client_id]
        answer = "\n".join(shows)
        if answer != "":
            self.send_message(client_id, answer)
        else:
            self.send_message(client_id, "Favourites list is empty")
