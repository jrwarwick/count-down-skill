from mycroft import MycroftSkill, intent_file_handler


class CountDown(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('down.count.intent')
    def handle_down_count(self, message):
        self.speak_dialog('down.count')


def create_skill():
    return CountDown()

