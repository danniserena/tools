import json
import asyncio
import edge_tts as tts


async def search_voice(gender="", locale="") -> None:
    """
    Search voice by gender and locale
    """
    manager = await tts.VoicesManager.create()
    return manager.find(Gender=gender, Locale=locale)


if __name__ == "__main__":
    voices = asyncio.run(search_voice("Male", "zh-CN"))
    print(json.dumps(voices, indent=4))
