from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import random
import enchant

app = Flask(__name__)

client_id = "upqAVTTh3Uf8zMEBIkYV"
client_secret = "PvZwDWDIfJ"
papago_api_url = "https://openapi.naver.com/v1/papago/n2mt"

english_dict = enchant.Dict("en_US")

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/english')
def english():
    return render_template('english.html')

@app.route('/japanese')
def japanese():
    return render_template('japanese.html')

@app.route('/chinese')
def chinese():
    return render_template('chinese.html')

@app.route('/spanish')
def spanish():
    return render_template('spanish.html')

@app.route('/back-to-main')
def back_to_main():
    return render_template('main.html')

@app.route('/spelling')
def spelling():
    return render_template('spelling.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        webpage_url = "https://www.voanews.com/a/discipline-handed-down-for-us-intelligence-discord-leaks/7393362.html"
        english_words = get_english_words(webpage_url)

        if english_words:
            quiz_questions = create_translation_questions(english_words, num_questions=5)
            return render_template('quiz.html', quiz_questions=quiz_questions)
        else:
            print("Failed to retrieve English words from the webpage.")
            return render_template('quiz.html', error_message="Failed to retrieve English words from the webpage.")

    elif request.method == 'POST':
        user_answers = {key: request.form[key] for key in request.form.keys()}
        quiz_results = evaluate_quiz(user_answers)
        return render_template('quiz_result.html', quiz_results=quiz_results)

def evaluate_quiz(user_answers):
    webpage_url = "https://www.voanews.com/a/discipline-handed-down-for-us-intelligence-discord-leaks/7393362.html"
    english_words = get_english_words(webpage_url)

    if english_words:
        quiz_results = []
        for word in user_answers.keys():
            correct_answer = get_papago_translation(word)
            is_correct = user_answers[word].lower() == correct_answer.lower()
            quiz_results.append((word, correct_answer, user_answers[word], is_correct))
        return quiz_results
    else:
        print("Failed to retrieve English words from the webpage.")
        return []
def get_english_words(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        english_words = re.findall(r'\b\w{3,}\b', soup.get_text())
        return english_words
    except requests.exceptions.HTTPError as err:
        print(f"Error accessing the URL: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def create_translation_questions(english_words, num_questions=5):
    questions = []
    for _ in range(num_questions):
        random_word = random.choice(english_words)
        translation = get_papago_translation(random_word, source='en', target='ko')
        if translation:
            question = f"'{random_word}'을(를) 한국어로 무엇이라고 하나요? "
            answer = translation
            questions.append((question, answer))
    return questions

def get_papago_translation(word, source="en", target="ko"):
    client_id = "upqAVTTh3Uf8zMEBIkYV"
    client_secret = "PvZwDWDIfJ"
    papago_api_url = "https://openapi.naver.com/v1/papago/n2mt"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    params = {"source": source, "target": target, "text": word}

    try:
        response = requests.post(papago_api_url, headers=headers, data=params)
        response.raise_for_status()
        translation_result = response.json()["message"]["result"]["translatedText"]
        return translation_result
    except requests.exceptions.HTTPError as err:
        print(f"Error accessing Papago API: {err}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def spell_check(text):
    english_dict = enchant.Dict("en_US")

    words = text.split()

    misspelled_words = [word for word in words if not english_dict.check(word)]
    suggestions = {word: english_dict.suggest(word) for word in misspelled_words}

    return suggestions

@app.route('/run-spelling-check', methods=['POST'])
def run_spelling_check():
    data = request.get_json()
    user_input = data['input']
    misspelled_word_suggestions = spell_check(user_input)

    response_data = {
        'errors': [{'word': word, 'suggestions': suggestions} for word, suggestions in misspelled_word_suggestions.items()]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
