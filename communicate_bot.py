from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def train_english_bot(bot):
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english")

def main():
    english_bot = ChatBot("EnglishBot")

    train_english_bot(english_bot)

    print("English Learning Assistant: Hello! Let's learn English together. (Type 'exit' to end the conversation)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("English Learning Assistant: Goodbye! Keep practicing English.")
            break

        response = english_bot.get_response(user_input)
        print(f"English Learning Assistant: {response}")

if __name__ == "__main__":
    main()
