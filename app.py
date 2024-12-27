from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import os
import re
from gtts import gTTS
import pygame
from io import BytesIO

os.environ["OPENAI_API_KEY"] = ""

def play_text_jp(text: str):
    """GTTSを使用してテキストを音声に変換して再生"""
    # テキストを音声に変換
    tts = gTTS(text=text, lang='ja')
    
    # 音声データをメモリ上のバッファに保存
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Pygameで音声を再生
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    
    # 再生が終わるまで待機
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def find_text_to_read(history_list):
    # 'done' と 'text' の値を抽出
    result_pattern = r"'done': \{'text': '([^']+)'"
    match = re.search(result_pattern, str(history_list))
    
    if match:
        return match.group(1)
        
    # バックアップパターン: 'Result: ' の後のテキストを探す
    result_pattern2 = r'Result: ([^\n]+)'
    match = re.search(result_pattern2, str(history_list))
    if match:
        return match.group(1).strip()
    
    return None

async def main():
    agent = Agent(
        task="音声読み上げ用に、AIの時事ネタを調べて日本語150字程度にまとめて",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    
    # 読み上げるテキストを探す
    text_to_read = find_text_to_read(result)
    
    if text_to_read:
        print(f"読み上げるテキスト: {text_to_read}")
        play_text_jp(text_to_read)
    else:
        print("読み上げるテキストが見つかりませんでした")

if __name__ == "__main__":
    asyncio.run(main())