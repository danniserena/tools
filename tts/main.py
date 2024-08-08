# 要求用户分别输入以下信息，回车表示不选择
# 1. Gender Male Female
# 2. Locale zh-CN en-US 等
# 3. Status 国家编号，给出编号如 GA
# 使用 voice_manager.py 获取声音列表
# 让用户选择声音
# 让用户输入声音的目录以及输出的目录
# 调用submark.py 生成
import json
import os
import asyncio
import subprocess
from tts.submark import tts
from tts.voices_manager import search_voice


# 显示一个欢迎页码，要求用户输入相关的信息
# 首先告知用于当前使用edge-tts库，然后说tts库目前支持318种声音
if __name__ == "__main__":
    print("the project uses the edge-tts open-source library, which supports 318 voices")
    print("What kind of voice do you like?")
    # 性别
    gender = input("1. Male 2. Female: ")
    # 区域：
    locale = input("af-ZA	sq-AL	am-ET	ar-DZ	ar-BH	ar-EG	ar-IQ	ar-JO	ar-KW	ar-LB\n"
                   "ar-LY	ar-MA	ar-OM	ar-QA	ar-SA	ar-SY	ar-TN	ar-AE	ar-YE	az-AZ\n"
                   "bn-BD	bn-IN	bs-BA	bg-BG	my-MM	ca-ES	zh-HK	zh-CN	zh-CN-liaoning\n"
                   "zh-TW	zh-CN-shaanxi	hr-HR	cs-CZ	da-DK	nl-BE	nl-NL	en-AU\n"
                   "en-CA	en-HK	en-IN	en-IE	en-KE	en-NZ	en-NG	en-PH	en-SG\n"
                   "en-ZA	en-TZ	en-GB	en-US	et-EE	fil-P	fi-FI	fr-BE	fr-CA	fr-FR\n"
                   "fr-CH	gl-ES	ka-GE	de-AT	de-DE	de-CH	el-GR	gu-IN	he-IL	hi-IN\n"
                   "hu-HU	is-IS	id-ID	ga-IE	it-IT	ja-JP	jv-ID	kn-IN	kk-KZ    km-KH\n"
                   "ko-KR	lo-LA	lv-LV	lt-LT	mk-MK	ms-MY	ml-IN	mt-MT	mr-IN\n"
                   "mn-MN	ne-NP	nb-NO	ps-AF	fa-IR	pl-PL	pt-BR	pt-PT	ro-RO\n"
                   "ru-RU	sr-RS	si-LK	sk-SK	sl-SI	so-SO	es-AR	es-BO	es-CL	es-ES\n"
                   "es-CO	es-CR	es-CU	es-DO	es-EC	es-SV	es-GQ	es-GT	es-HN\n"
                   "es-MX	es-NI	es-PA	es-PY	es-PE	es-PR	es-US	es-UY	es-VE\n"
                   "su-ID	sw-KE	sw-TZ	sv-SE	ta-IN	ta-MY	ta-SG	ta-LK	te-IN\n"
                   "th-TH	tr-TR	uk-UA	ur-IN	ur-PK	uz-UZ	vi-VN	cy-GB	zu-ZA\n"
                   "Choose a locale: ")
    # 显示候选声音
    voices = asyncio.run(search_voice(gender=gender, locale=locale))
    for i in range(0, len(voices), 4):
        print(f'{voices[i]["Name"]}\t{voices[i + 1]["Name"]}\t{voices[i + 2]["Name"]}\t{voices[i + 3]["Name"]}')
    voice = input("Choose a voice: ")
    # 输入文件目录
    input_dir = input("Input the directory of input files: ")
    # 输出文件目录
    output_dir = input("Input the directory of output files: ")
    asyncio.run(tts(voice=voice, input_dir=input_dir, output_dir=output_dir))

