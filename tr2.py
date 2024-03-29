import discord
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

    # 상대방의 언어를 영어, 한국어, 스페인어로만 번역
    target_langs = ['EN', 'KO', 'ES']

    # 메시지가 텍스트인 경우에만 번역 수행
    if message.content:
        # 번역할 문장
        original_message = message.content

        # 번역 및 전송
        translated_texts = []
        for lang in target_langs:
            translated_text = translate_message(original_message, lang)
            if translated_text:
                translated_texts.append(f"Translated ({lang}): {translated_text}")

        # 번역 결과와 함께 상대방의 프로필과 닉네임을 포함하여 메시지 전송
        if translated_texts:
            translated_message = "\n".join(translated_texts)
            await message.channel.send(f"{message.author.mention} 님이 보낸 메시지:\n{translated_message}")

def translate_message(text, target_lang):
    # Deepl API에 보낼 요청 데이터
    data = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
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
        print("봇이 당신의 언어를 이해하지 못했어요!:", response.status_code)
        return None

# 디스코드 봇 실행
access_token = os.environ['BOT_TOKEN']
Client.run(access_token)
