from mycroft import MycroftSkill, intent_file_handler
import datetime
import re

__author__ = 'jrwarwick'

# TODO:
# - speed modifier comprehension
#   if "quickly" then every half second
#   if "slowly" then every 2 seconds
#   else every second.
# - prompt for number to count down from, if utterance is simply "begin count down".
# - Option to include or exclude zero, and/or end with "go!"
# - if you say "count us down again" the again means use previous value of count_number
# - if utterance contains "second", make sure to use "normal" 1 second interval

class CountDown(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('down.count.intent')
    def handle_down_count(self, message):
        self.settings["count_number"] = 11 #reasonable default??
        self.settings["count_speed"] = 2
        #this cheesey pseudo random probably should be replaced
        #perhaps with a settingsmeta for "verbosity"
        if int(datetime.datetime.now().strftime('%S')[1]) < 3:
            self.speak_dialog('down.count')
        # Start a callback that repeats every .5, 1, or 2 seconds (slow, normal, quick)
        now = datetime.datetime.now()
        self.log.debug(now)
        self.settings["count_number"] = message.data.get('count_number')
        self.schedule_repeating_event(self.decrement, now, self.settings["count_speed"], "COUNTDOWN" )

    def decrement(self,speed):
        numeral = self.settings["count_number"] 
        re_numerals_only = re.compile(r'^\d+$')
        if not re_numerals_only.search(numeral):
            #TODO: make an attempt at using some parsing/comprehension/helper/utility functions 
            #to extract the intended quantity here if it was spelled out, like "twenty" or "eight"
            self.speak('Sorry, I cannot continue the count. I got confused.')
            self.log.info("TERMINATING the countdown, had a bad numeral to deal with.")
            self.cancel_all_repeating_events()
        else:
            self.log.debug(numeral)
            self.speak(str(numeral))
            self.settings["count_number"] = str(int(self.settings["count_number"]) - 1)
            if int(numeral) <= 0:
                self.log.info("TERMINATING the countdown, normally.")
                self.cancel_all_repeating_events()

def create_skill():
    return CountDown()

