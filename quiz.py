import requests
from bs4 import BeautifulSoup
import re
import random

client_id = "upqAVTTh3Uf8zMEBIkYV"
client_secret = "PvZwDWDIfJ"
papago_api_url = "https://openapi.naver.com/v1/papago/n2mt"

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
    """영어 단어를 번역하는 연습 문제 생성 함수."""
    questions = []
    
    for _ in range(num_questions):
        random_word = random.choice(english_words)
        
        translation = get_papago_translation(random_word)
        
        if translation:
            question = f"'{random_word}'를 한국어로 번역하면 무엇인가요? "
            answer = translation
            questions.append((question, answer))
    
    return questions

def get_papago_translation(word):
    """파파고 API를 사용하여 영어 단어를 번역하는 함수."""
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    params = {"source": "en", "target": "ko", "text": word}

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

webpage_url = "https://www.voanews.com/a/discipline-handed-down-for-us-intelligence-discord-leaks/7393362.html"
english_words = get_english_words(webpage_url)

translation_questions = create_translation_questions(english_words)

if english_words:
    print("번역 퀴즈를 시작합니다. 종료하려면 'exit'을 입력하세요.")

    while True:
        random_word = random.choice(english_words)
        translation = get_papago_translation(random_word)

        if translation:
            question = f"'{random_word}'를 한국어로 번역하면 무엇인가요? "
            answer = translation
            user_answer = input(question)

            if user_answer.lower() == answer.lower():
                print("정답입니다!\n")
            elif user_answer.lower() == 'exit':
                print("퀴즈를 종료합니다. 수고하셨습니다.")
                break
            else:
                print(f"죄송합니다, 정답은 {answer}입니다.\n")
else:
    print("Failed to retrieve English words from the webpage.")