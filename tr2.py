import discord
import os
import requests
import json

# Deepl API 키
DEEPL_API_KEY = '6eb802fa-ae94-4f9e-8c72-72d2948fed71'
# Deepl API 엔드포인트
DEEPL_API_ENDPOINT = 'https://api.deepl.com/v2/translate'

# 디스코드 클라이언트 생성
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}로 로그인합니다.')

@client.event
async def on_message(message):
    # 봇이 보낸 메시지 또는 봇의 반응은 무시
    if message.author == client.user or message.author.bot:
        return

    # 메시지가 텍스트이고 "https://tenor.com"이 포함되지 않은 경우에만 번역 수행
    if message.content and not has_tenor_link(message):
        # 번역할 문장
        original_message = message.content

        # 번역 결과를 담을 문자열 초기화
        translated_text = ""

        # 한국어 -> 스페인어 번역
        translated_message = translate_message(original_message, 'ko', 'es')
        translated_text += f"Español : {translated_message}\n"

        # 스페인어 -> 한국어 번역
        translated_message = translate_message(original_message, 'es', 'ko')
        translated_text += f"Korean : {translated_message}\n"

        # 한국어 -> 영어 번역
        translated_message = translate_message(original_message, 'ko', 'en')
        translated_text += f"English : {translated_message}\n"

        # 디스코드로 번역 결과 전송
        await message.channel.send(translated_text)

def translate_message(text, source_lang, target_lang):
    # Deepl API에 보낼 요청 데이터
    data = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }

    # Deepl API에 POST 요청 보내기
    response = requests.post(DEEPL_API_ENDPOINT, data=data)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형식으로 응답된 데이터 파싱
        translation_result = json.loads(response.text)
        # 번역된 텍스트 반환
        return translation_result['translations'][0]['text']
    else:
        print("구글이 당신의 언어를 이해하지 못했어요!:", response.status_code)
        return None

def has_tenor_link(message):
    # 메시지 내용에 "https://tenor.com"이 포함되어 있는지 확인
    return "https://tenor.com" in message.content

# 디스코드 봇 실행
access_token = os.environ['BOT_TOKEN']
client.run(access_token)
