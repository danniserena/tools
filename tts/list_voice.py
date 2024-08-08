import edge_tts
import asyncio
import json


async def get_voices():
    """
    获取可用 edge-tts 支持的声音
    """
    return await edge_tts.list_voices()


if __name__ == '__main__':
    voices = asyncio.run(get_voices())
    print(f'supported voices: {len(voices)}')
    formatted_json = json.dumps(voices, indent=4)
    print(formatted_json)
