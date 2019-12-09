from mycroft import MycroftSkill, intent_file_handler
import datetime

__author__ = 'jrwarwick'

# TODO:
# - speed modifier comprehension
#   if "quickly" then every half second
#   if "slowly" then every 2 seconds
#   else every second.
# - prompt for number to count down from, if utterance is simply "begin count down".
#
# - Option to include or exclude zero, and/or end with "go!"

class CountDown(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('down.count.intent')
    def handle_down_count(self, message):
        self.settings["count_number"] = 11 #reasonable default??
        self.settings["count_speed"] = 2
        #self.speak_dialog('down.count')
        # Start a callback that repeats every .5, 1, or 2 seconds
        now = datetime.datetime.now()
        self.log.debug(now)
        self.settings["count_number"] = message.data.get('count_number')
        self.schedule_repeating_event(self.decrement, now, self.settings["count_speed"], "COUNTDOWN" )

    def decrement(self,speed):
        numeral = self.settings["count_number"] 
        self.log.debug(numeral)
        self.speak(str(numeral))
        self.settings["count_number"] = str(int(self.settings["count_number"]) - 1)
        if int(numeral) <= 0:
            self.cancel_all_repeating_events()

def create_skill():
    return CountDown()

