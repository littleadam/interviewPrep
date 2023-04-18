# questions_options_app.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# Set up the Google Sheet API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope) # change here

# Connect to the Google Sheet
gc = gspread.authorize(credentials)
sh = gc.open('Quiz Questions')
worksheet = sh.sheet1

# Get the questions and options from the Google Sheet.The QA is expected to be in QAAA... order.
questions = worksheet.col_values(1)
options = [worksheet.row_values(i)[1:] for i in range(1, worksheet.row_count + 1)]

# Create the GUI
class QuizApp(App):
    score = 0

    def build(self):
        self.box = BoxLayout(orientation='vertical')
        self.ask_question()
        return self.box

    def ask_question(self):
        self.box.clear_widgets()
        if len(questions) > self.score:
            self.box.add_widget(Label(text=questions[self.score], size_hint_y=0.2, halign='center'))
            for i, option in enumerate(options[self.score]):
                btn = Button(text=option, size_hint_y=0.1)
                btn.bind(on_press=self.check_answer)
                self.box.add_widget(btn)
        else:
            self.box.add_widget(Label(text=f'Your final score is {self.score}/{len(questions)}.', size_hint_y=0.2, halign='center'))

    def check_answer(self, instance):
        if instance.text == worksheet.cell(self.score + 1, 5).value:
            self.score += 1
        self.ask_question()

if __name__ == '__main__':
    QuizApp().run()
