from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import spacy
import nltk
spacy.load('en_core_web_sm')

# Ensure NLTK data is downloaded
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Create ChatBot Instance
chatbot = ChatBot(
    'ChatBot for College Enquiry',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "Hi there, Welcome to TPCE! If you need any assistance, I'm always here. Go ahead and write the number of any query. ✨<br><br>  Which of the following user groups do you belong to? <br><br>1. Student's Section Enquiry.<br>2. Faculty Section Enquiry.<br>3. Parent's Section Enquiry.<br>4. Visitor's Section Enquiry.<br><br>",
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///new_database.sqlite3?check_same_thread=False'
)

# # Training with Personal Q&A
trainer = ListTrainer(chatbot)
conversation = [
"Hello",
    "Hi Human",
    "How are you doing ?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "what is your name ?" ,
    "I'm TPCE Bot",
    "who made you ?",
    "I created by Poojitha,Praniatha,Chandu,Mithesh",
    "<b style='colour:red'>Hi there, Welcome to TPCE! 👋 If you need any assistance, I'm always here.<br>Which of the following user groups do you belong to?</b>",
]   

