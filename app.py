import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

kivy.require("2.3.0")

# Store account data in a simple dictionary for now
accounts = {}

# Define Home Screen with navigation buttons
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title_label = Label(
            text="Welcome to PennyWise",
            font_size='24sp',
            size_hint=(1, 0.2),
            color=(0, 0, 1, 1)
        )

        show_accounts_button = Button(
            text="Show Accounts",
            size_hint=(1, 0.2),
            font_size='20sp',
            on_press=self.show_accounts
        )

        add_account_button = Button(
            text="Add Account",
            size_hint=(1, 0.2),
            font_size='20sp',
            on_press=self.add_account
        )

        layout.add_widget(title_label)
        layout.add_widget(show_accounts_button)
        layout.add_widget(add_account_button)

        self.add_widget(layout)

    def show_accounts(self, instance):
        self.manager.current = 'show_accounts'

    def add_account(self, instance):
        self.manager.current = 'add_account'

# Define Add Account Screen
class AddAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.account_name_input = TextInput(
            hint_text="Enter Account Name",
            font_size='18sp',
            size_hint=(1, 0.2)
        )
        self.account_amount_input = TextInput(
            hint_text="Enter Initial Amount",
            font_size='18sp',
            size_hint=(1, 0.2),
            input_filter='float'  # Ensures only numeric input
        )

        add_button = Button(
            text="Add Account",
            size_hint=(1, 0.2),
            font_size='20sp',
            on_press=self.add_account
        )

        layout.add_widget(Label(text="Add a New Account", font_size='24sp', size_hint=(1, 0.2)))
        layout.add_widget(self.account_name_input)
        layout.add_widget(self.account_amount_input)
        layout.add_widget(add_button)

        self.add_widget(layout)

    def add_account(self, instance):
        name = self.account_name_input.text
        amount = self.account_amount_input.text
        if name and amount:
            accounts[name] = float(amount)  # Store account name and amount
            self.manager.current = 'home'  # Go back to home screen
            self.account_name_input.text = ""
            self.account_amount_input.text = ""  # Reset inputs

# Define Show Accounts Screen
class ShowAccountsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.update_accounts_list()
        self.add_widget(self.layout)

    def update_accounts_list(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Accounts Overview", font_size='24sp', size_hint=(1, 0.2)))

        for account, amount in accounts.items():
            account_layout = BoxLayout(orientation='horizontal', spacing=10)

            name_input = TextInput(text=account, font_size='18sp', multiline=False)
            amount_input = TextInput(text=str(amount), font_size='18sp', multiline=False, input_filter='float')

            update_button = Button(
                text="Update",
                size_hint=(0.3, 1),
                font_size='16sp',
                on_press=lambda instance, name=name_input, amount=amount_input: self.update_account(name, amount)
            )

            account_layout.add_widget(name_input)
            account_layout.add_widget(amount_input)
            account_layout.add_widget(update_button)
            self.layout.add_widget(account_layout)

    def update_account(self, name_input, amount_input):
        # Update the account details
        name = name_input.text
        amount = amount_input.text
        if name and amount:
            accounts[name] = float(amount)  # Update the account data
            self.update_accounts_list()  # Refresh the list to reflect changes

# Set up the ScreenManager and add all screens
class PennyWiseApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(ShowAccountsScreen(name='show_accounts'))
        return sm

# Run the app
if __name__ == "__main__":
    PennyWiseApp().run()
