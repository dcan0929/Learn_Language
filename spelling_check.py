import enchant

def spell_check(text):
    english_dict = enchant.Dict("en_US")

    words = text.split()

    misspelled_words = [word for word in words if not english_dict.check(word)]
    suggestions = {word: english_dict.suggest(word) for word in misspelled_words}

    return suggestions

while True:
    user_input = input("Enter a sentence (or 'exit' to quit): ")

    if user_input.lower() == 'exit':
        print("Exiting the spelling check program.")
        break

    misspelled_word_suggestions = spell_check(user_input)
    if not misspelled_word_suggestions:
        print("No misspelled words.")
    else:
        print("Misspelled words and suggestions:")
        for word, suggestions in misspelled_word_suggestions.items():
            print(f"{word}: {', '.join(suggestions)}")
