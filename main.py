import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

kivy.require("2.0.0")

# Mobile Window Simulation Size (Standard Phone Display Ratio)
Window.size = (380, 720)

# =========================================================
# COLOR PALETTE
# =========================================================
COLOR_BG = get_color_from_hex("#F5F8FC")
COLOR_NAVY = get_color_from_hex("#102A63")
COLOR_BLUE = get_color_from_hex("#2878E8")
COLOR_DARK_BLUE = get_color_from_hex("#1C5BB8")
COLOR_LIGHT_BLUE = get_color_from_hex("#E8F2FF")
COLOR_WHITE = get_color_from_hex("#FFFFFF")
COLOR_GREY = get_color_from_hex("#65758B")
COLOR_YELLOW = get_color_from_hex("#FFF1D8")
COLOR_MISTAKE_RED = get_color_from_hex("#FEE2E2")
COLOR_FAIL_RED = get_color_from_hex("#DC2626")
COLOR_CORRECT_GREEN = get_color_from_hex("#DCFCE7")
COLOR_SUCCESS_GREEN = get_color_from_hex("#15803D")
COLOR_PURPLE = get_color_from_hex("#8B5CF6")
COLOR_GOLD = get_color_from_hex("#D97706")


# =========================================================
# GLOBAL TRANSLATION & TOPICS DATA
# =========================================================
current_lang = 0  # 0: English, 1: Odia, 2: Hindi

NOUN_TRANSLATIONS = {
    0: {
        "btn_text": "🌐 Translate to Odia",
        "title": "Noun — Easy Definition",
        "desc": "A noun is a naming word. It names a person, place, animal, thing, or idea.",
        "trick_title": "💡 Easy trick:",
        "trick": "If a word is used to name someone or something, it can be a noun.",
    },
    1: {
        "btn_text": "🌐 Translate to Hindi",
        "title": "Noun — ସହଜ ପରିଭାଷା",
        "desc": "Noun (ବିଶେଷ୍ୟ) ହେଉଛି ଏକ ନାମବାଚକ ଶବ୍ଦ। ଏହା କୌଣସି ବ୍ୟକ୍ତି, ସ୍ଥାନ, ପଶୁ, ବସ୍ତୁ କିମ୍ବା ଧାରଣାର ନାମକୁ ବୁଝାଏ।",
        "trick_title": "💡 ସହଜ ଉପାୟ:",
        "trick": "ଯଦି କୌଣସି ଶବ୍ଦ କାହାରି କିମ୍ବା କୌଣସି ଜିନିଷର ନାମକୁ ବୁଝାଏ, ତେବେ ସେହି ଶବ୍ଦଟି Noun (ବିଶେଷ୍ୟ) ହୋଇପାରେ।",
    },
    2: {
        "btn_text": "🌐 Translate to English",
        "title": "Noun — आसान परिभाषा",
        "desc": "Noun (संज्ञा) एक नाम बताने वाला शब्द है। यह किसी व्यक्ति, स्थान, पशु, वस्तु या विचार के नाम को दर्शाता है।",
        "trick_title": "💡 आसान तरीका:",
        "trick": "यदि कोई शब्द किसी व्यक्ति या वस्तु के नाम को दर्शाने के लिए प्रयोग किया जाता है, तो वह Noun (संज्ञा) हो सकता है।",
    },
}

NOUN_EXAMPLES = [
    ("Rohan is my friend.", "Rohan = noun (person)"),
    ("I live in Delhi.", "Delhi = noun (place)"),
    ("The dog is barking.", "dog = noun (animal)"),
    ("She has a book.", "book = noun (thing)"),
]

COMMON_MISTAKES_DATABASE = {
    "noun": [
        ("She gave me many advices.", "She gave me much advice.", "'Advice' is an uncountable noun. We never add 's' to advice."),
        ("He bought five furnitures.", "He bought five pieces of furniture.", "'Furniture' is uncountable. Use 'pieces of furniture'."),
        ("One of my friend is coming.", "One of my friends is coming.", "'One of...' must be followed by a plural noun.")
    ]
}

TOPICS_INTERACTIVE_QUIZZES = {
    "noun": {
        "title": "Noun Practice Exercise",
        "instruction": "Tap all NOUNS in the sentence below:",
        "questions": [
            {"sentence": ["The", "cat", "slept", "on", "the", "mat."], "target_indices": [1, 5], "explanation": "'cat' (animal) and 'mat' (thing) are Nouns."},
            {"sentence": ["Rohan", "bought", "a", "beautiful", "book."], "target_indices": [0, 4], "explanation": "'Rohan' (person) and 'book' (thing) are Nouns."}
        ]
    }
}


# =========================================================
# REUSABLE BOTTOM NAVIGATION BAR
# =========================================================
class BottomNavBar(BoxLayout):
    def __init__(self, nav_callback, active_tab="home", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "60dp"
        self.padding = ["5dp", "5dp"]
        self.spacing = "5dp"

        items = [
            ("Home", "home"),
            ("Lessons", "lessons"),
            ("Saved", "saved"),
            ("More", "more")
        ]

        for label, tab_key in items:
            btn = Button(
                text=label,
                font_size="12sp",
                bold=(active_tab == tab_key),
                background_color=COLOR_BLUE if active_tab == tab_key else COLOR_GREY,
                color=COLOR_WHITE
            )
            btn.bind(on_release=lambda instance, k=tab_key: nav_callback(k))
            self.add_widget(btn)


# =========================================================
# HOME SCREEN
# =========================================================
class HomeScreen(Screen):
    def __init__(self, screen_manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager_ref

        main_layout = BoxLayout(orientation="vertical")

        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding="15dp", spacing="15dp")
        content.bind(minimum_height=content.setter("height"))

        # Header
        header = Label(
            text="[b]English Grammar[/b]\nLearn • Practice • Improve",
            markup=True,
            font_size="20sp",
            color=COLOR_NAVY,
            size_hint_y=None,
            height="60dp",
            halign="left"
        )
        header.bind(size=header.setter('text_size'))
        content.add_widget(header)

        # Search Bar
        search_input = TextInput(
            hint_text="Search grammar topics...",
            size_hint_y=None,
            height="45dp",
            multiline=False
        )
        content.add_widget(search_input)

        # Hero Banner
        banner = Button(
            text="[b]Welcome![/b]\nSmall Steps, Big Improvements\nTap here to Start Learning →",
            markup=True,
            font_size="15sp",
            background_color=COLOR_BLUE,
            color=COLOR_WHITE,
            size_hint_y=None,
            height="120dp"
        )
        banner.bind(on_release=lambda x: self.sm.navigate_to("topics"))
        content.add_widget(banner)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        # Bottom Navigation
        main_layout.add_widget(BottomNavBar(self.sm.bottom_nav_click, active_tab="home"))
        self.add_widget(main_layout)


# =========================================================
# TOPICS SCREEN
# =========================================================
class TopicsScreen(Screen):
    def __init__(self, screen_manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager_ref

        main_layout = BoxLayout(orientation="vertical")

        # Header
        top_bar = BoxLayout(size_hint_y=None, height="50dp", padding="5dp")
        btn_back = Button(text="←", size_hint_x=None, width="50dp", on_release=lambda x: self.sm.go_back())
        title = Label(text="Grammar Topics", font_size="18sp", bold=True, color=COLOR_NAVY)
        top_bar.add_widget(btn_back)
        top_bar.add_widget(title)
        main_layout.add_widget(top_bar)

        # Scrollable Topics List
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing="10dp", padding="10dp", size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        topics = [
            ("Noun", "Names a person, place, animal or thing.", "noun"),
            ("Pronoun", "Words used instead of nouns.", "pronoun"),
            ("Verb", "Shows an action, state or occurrence.", "verb"),
            ("Adjective", "Describes or gives details about a noun.", "adjective")
        ]

        for t_title, t_desc, t_key in topics:
            card = Button(
                text=f"[b]{t_title}[/b]\n{t_desc}",
                markup=True,
                font_size="14sp",
                size_hint_y=None,
                height="70dp",
                background_color=COLOR_LIGHT_BLUE,
                color=COLOR_NAVY
            )
            card.bind(on_release=lambda instance, k=t_key, title=t_title: self.sm.open_topic(k, title))
            grid.add_widget(card)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        # Bottom Bar
        main_layout.add_widget(BottomNavBar(self.sm.bottom_nav_click, active_tab="lessons"))
        self.add_widget(main_layout)


# =========================================================
# TOPIC DETAIL SCREEN
# =========================================================
class TopicDetailScreen(Screen):
    def __init__(self, screen_manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager_ref
        self.topic_key = "noun"
        self.topic_header = "NOUN"

    def build_content(self, topic_key, topic_header):
        self.clear_widgets()
        self.topic_key = topic_key
        self.topic_header = topic_header

        global current_lang
        data = NOUN_TRANSLATIONS.get(current_lang, NOUN_TRANSLATIONS[0])

        main_layout = BoxLayout(orientation="vertical")

        # Top Bar
        top_bar = BoxLayout(size_hint_y=None, height="50dp", padding="5dp")
        btn_back = Button(text="←", size_hint_x=None, width="50dp", on_release=lambda x: self.sm.go_back())
        title = Label(text=topic_header, font_size="18sp", bold=True, color=COLOR_NAVY)
        top_bar.add_widget(btn_back)
        top_bar.add_widget(title)
        main_layout.add_widget(top_bar)

        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding="15dp", spacing="12dp")
        content.bind(minimum_height=content.setter("height"))

        # Definition Card
        def_label = Label(
            text=f"[b]{data['title']}[/b]\n\n{data['desc']}",
            markup=True,
            font_size="14sp",
            color=COLOR_NAVY,
            size_hint_y=None,
            height="100dp"
        )
        content.add_widget(def_label)

        # Practice Button
        btn_practice = Button(
            text="📝 PRACTICE EXERCISES",
            font_size="14sp",
            bold=True,
            background_color=COLOR_PURPLE,
            color=COLOR_WHITE,
            size_hint_y=None,
            height="45dp"
        )
        btn_practice.bind(on_release=lambda x: self.open_quiz_popup())
        content.add_widget(btn_practice)

        # Common Mistakes Button
        btn_mistakes = Button(
            text="⚠️ COMMON MISTAKES",
            font_size="14sp",
            bold=True,
            background_color=COLOR_GOLD,
            color=COLOR_WHITE,
            size_hint_y=None,
            height="45dp"
        )
        btn_mistakes.bind(on_release=lambda x: self.sm.open_mistakes(self.topic_key, self.topic_header))
        content.add_widget(btn_mistakes)

        # Language Switcher
        btn_lang = Button(
            text=data["btn_text"],
            font_size="13sp",
            background_color=COLOR_LIGHT_BLUE,
            color=COLOR_BLUE,
            size_hint_y=None,
            height="40dp"
        )
        btn_lang.bind(on_release=self.toggle_lang)
        content.add_widget(btn_lang)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        main_layout.add_widget(BottomNavBar(self.sm.bottom_nav_click, active_tab="lessons"))
        self.add_widget(main_layout)

    def toggle_lang(self, instance):
        global current_lang
        current_lang = (current_lang + 1) % 3
        self.build_content(self.topic_key, self.topic_header)

    def open_quiz_popup(self):
        quiz_data = TOPICS_INTERACTIVE_QUIZZES.get(self.topic_key, TOPICS_INTERACTIVE_QUIZZES["noun"])
        
        popup_content = BoxLayout(orientation="vertical", padding="10dp", spacing="10dp")
        popup_content.add_widget(Label(text=quiz_data["title"], font_size="16sp", bold=True))
        popup_content.add_widget(Label(text=quiz_data["instruction"], font_size="12sp"))

        q_info = quiz_data["questions"][0]
        words_layout = GridLayout(cols=3, spacing="5dp", size_hint_y=None, height="120dp")

        selected = set()

        for idx, word in enumerate(q_info["sentence"]):
            btn_word = Button(text=word, font_size="13sp")
            def on_word_tap(b, i=idx):
                if i in selected:
                    selected.remove(i)
                    b.background_color = [1, 1, 1, 1]
                else:
                    selected.add(i)
                    b.background_color = COLOR_PURPLE
            btn_word.bind(on_release=on_word_tap)
            words_layout.add_widget(btn_word)

        popup_content.add_widget(words_layout)

        feedback_label = Label(text="", markup=True, font_size="13sp", size_hint_y=None, height="60dp")
        popup_content.add_widget(feedback_label)

        def submit_quiz(x):
            if selected == set(q_info["target_indices"]):
                feedback_label.text = "[color=15803D][b]✔ CORRECT ANSWER![/b][/color]\n" + q_info["explanation"]
            else:
                feedback_label.text = "[color=DC2626][b]✖ WRONG ANSWER![/b][/color]\n" + q_info["explanation"]

        btn_submit = Button(text="Submit Answer", size_hint_y=None, height="40dp", background_color=COLOR_BLUE)
        btn_submit.bind(on_release=submit_quiz)
        popup_content.add_widget(btn_submit)

        popup = Popup(title="Practice Quiz", content=popup_content, size_hint=(0.9, 0.8))
        popup.open()


# =========================================================
# COMMON MISTAKES SCREEN
# =========================================================
class CommonMistakesScreen(Screen):
    def __init__(self, screen_manager_ref, **kwargs):
        super().__init__(**kwargs)
        self.sm = screen_manager_ref

    def build_content(self, topic_key, topic_title):
        self.clear_widgets()

        main_layout = BoxLayout(orientation="vertical")

        # Header
        top_bar = BoxLayout(size_hint_y=None, height="50dp", padding="5dp")
        btn_back = Button(text="←", size_hint_x=None, width="50dp", on_release=lambda x: self.sm.go_back())
        title = Label(text=f"Mistakes — {topic_title.title()}", font_size="16sp", bold=True, color=COLOR_NAVY)
        top_bar.add_widget(btn_back)
        top_bar.add_widget(title)
        main_layout.add_widget(top_bar)

        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding="10dp", spacing="10dp")
        content.bind(minimum_height=content.setter("height"))

        mistakes = COMMON_MISTAKES_DATABASE.get(topic_key, COMMON_MISTAKES_DATABASE["noun"])

        for idx, (wrong, right, why) in enumerate(mistakes):
            box = BoxLayout(orientation="vertical", size_hint_y=None, height="120dp", padding="8dp")
            box.add_widget(Label(text=f"❌ [color=DC2626]{wrong}[/color]", markup=True, font_size="13sp"))
            box.add_widget(Label(text=f"✅ [color=15803D]{right}[/color]", markup=True, font_size="13sp"))
            box.add_widget(Label(text=f"💡 Why? {why}", font_size="11sp", color=COLOR_GREY))
            content.add_widget(box)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        main_layout.add_widget(BottomNavBar(self.sm.bottom_nav_click, active_tab="lessons"))
        self.add_widget(main_layout)


# =========================================================
# APPLICATION MANAGER
# =========================================================
class GrammarAppManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []

        self.home_screen = HomeScreen(self, name="home")
        self.topics_screen = TopicsScreen(self, name="topics")
        self.detail_screen = TopicDetailScreen(self, name="detail")
        self.mistakes_screen = CommonMistakesScreen(self, name="mistakes")

        self.add_widget(self.home_screen)
        self.add_widget(self.topics_screen)
        self.add_widget(self.detail_screen)
        self.add_widget(self.mistakes_screen)

    def navigate_to(self, screen_name):
        self.transition = SlideTransition(direction="left")
        self.history.append(self.current)
        self.current = screen_name

    def go_back(self):
        if self.history:
            self.transition = SlideTransition(direction="right")
            self.current = self.history.pop()

    def open_topic(self, topic_key, topic_title):
        self.detail_screen.build_content(topic_key, topic_title)
        self.navigate_to("detail")

    def open_mistakes(self, topic_key, topic_title):
        self.mistakes_screen.build_content(topic_key, topic_title)
        self.navigate_to("mistakes")

    def bottom_nav_click(self, tab_key):
        if tab_key == "home":
            self.navigate_to("home")
        elif tab_key == "lessons":
            self.navigate_to("topics")


class GrammarMobileApp(App):
    def build(self):
        self.title = "English Grammar App"
        return GrammarAppManager()


if __name__ == "__main__":
    GrammarMobileApp().run()
