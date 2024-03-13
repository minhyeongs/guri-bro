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
    # 봇이 보낸 메시지는 무시
    if message.author == client.user:
        return

    # 이모지, 이모티콘, 이미지 또는 다른 봇에 반응하지 않도록 필터링
    if not message.content or message.author.bot or message.attachments:
        return

    # 번역할 문장
    original_message = message.content

    # Embed 메시지 생성
    embed = discord.Embed(title="구그리가 번역했어요!", color=0x007199)  # 초록색 Embed

    # 한국어 -> 스페인어 번역
    translated_message = translate_message(original_message, 'ko', 'es')
    embed.add_field(name="Español :", value=translated_message, inline=False)

    # 스페인어 -> 한국어 번역
    translated_message = translate_message(original_message, 'es', 'ko')
    embed.add_field(name="Korean :", value=translated_message, inline=False)

    # 한국어 -> 영어 번역
    translated_message = translate_message(original_message, 'ko', 'en')
    embed.add_field(name="English :", value=translated_message, inline=False)

    # Embed 메시지를 디스코드로 전송
    await message.channel.send(embed=embed)

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
        print("구그리가 당신의 언어를 이해하지 못했어요!:", response.status_code)
        return None

# 디스코드 봇 실행
access_token = os.environ['BOT_TOKEN']
client.run(access_token)
