import asyncio
import re
import edge_tts
import os

VOICE = "en-GB-SoniaNeural"
INPUT_DIR = "input"
OUTPUT_DIR = "output"


async def tts(voice, input_dir=INPUT_DIR, output_dir=OUTPUT_DIR) -> None:
    """
    将.txt生成为 .mp3 文件，并生成 .vtt 字幕文件和.lrc 歌词文件
    :param voice: 声音名称
    :param fpath: 文本文件路径
    :param input_dir: 输入文件夹路径
    :param output_dir: 输出文件夹路径
    :return: None
    """
    # 获取所有输入文件列表
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    for fpath in input_files:
        base_name = os.path.splitext(os.path.basename(fpath))[0]
        audio_file = os.path.join(output_dir, f"{base_name}.mp3")
        vtt_file = os.path.join(output_dir, f"{base_name}.vtt")
        lrc_file = os.path.join(output_dir, f"{base_name}.lrc")

        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        communicate = edge_tts.Communicate(text, voice)
        submaker = edge_tts.SubMaker()

        with open(audio_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        with open(vtt_file, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())
        vtt_to_lrc(vtt_file=vtt_file, lrc_file=lrc_file)


def vtt_to_lrc(vtt_file, lrc_file):
    """
    将 VTT 文件转换为 LRC 文件
    :param vtt_file: VTT 文件路径
    :param lrc_file: LRC 文件路径
    :return: None
    """

    def vtt_to_lrc_time(vtt_time):
        # 将 VTT 时间格式转换为 LRC 时间格式
        match = re.match(r'(\d+):(\d+):(\d+)\.(\d+)', vtt_time)
        if match:
            hours, minutes, seconds, milliseconds = match.groups()
            return f"[{minutes.zfill(2)}:{seconds.zfill(2)}.{milliseconds.zfill(2)}]"
        return ""

    with open(vtt_file, 'r', encoding='utf-8') as vtt, open(lrc_file, 'w', encoding='utf-8') as lrc:
        lines = vtt.readlines()
        for line in lines:
            # 忽略空行和 VTT 特有的元数据行
            if line.strip() and not line.startswith('WEBVTT') and not line.startswith('NOTE') and '-->' not in line:
                lrc.write(line.strip() + '\n')
            elif '-->' in line:
                start, end = line.strip().split(' --> ')
                lrc.write(vtt_to_lrc_time(start))


if __name__ == "__main__":
    asyncio.run(tts(voice=VOICE))
