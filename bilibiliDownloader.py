import json
import os
import re
import requests
import ffmpeg
from tqdm import tqdm

def get_bilibili_url():
    while True:
        # 从终端获取 Bilibili 视频 URL
        url = input("请输入Bilibili视频URL: ").strip()

        # 使用正则表达式检查 URL 是否为有效的 Bilibili 视频链接
        if re.match(r'https?://(www\.)?bilibili\.com/video/BV[0-9A-Za-z]+', url):
            return url
        else:
            print("无效的 Bilibili 视频 URL，请重新输入。")

def get_sessdata():
    # 检查 SESSDATA.txt 是否存在
    if os.path.exists("SESSDATA.txt"):
        # 如果文件存在，读取文件中的 SESSDATA
        with open("SESSDATA.txt", "r") as file:
            sessdata = file.read().strip()
            # 去掉空格回车

        if len(sessdata)!= 222:
            print("SESSDATA.txt 中的 SESSDATA 格式不正确，请检查")
            return ""
        else:# 读取文件中的 SESSDATA
            print("已从 SESSDATA.txt 获取 SESSDATA")
    else:
        # 如果文件不存在，提示用户输入 SESSDATA
        sessdata = input("请输入SESSDATA（仅用于下载高清视频的cookie参数，如果没有，直接回车跳过）: ").strip()
        # 如果用户输入了 SESSDATA，则保存到文件
        if sessdata:
            with open("SESSDATA.txt", "w") as file:
                file.write(sessdata)
            print("SESSDATA 已保存到 SESSDATA.txt")
        else:
            print("未输入 SESSDATA，跳过该步骤 视频清晰度为未登录状态")

    return sessdata
class BilibiliDownloader:
    def __init__(self, url, cookies=None, headers=None):
        """
        初始化 Bilibili 下载器

        :param url: Bilibili 视频的网址 (如 "https://www.bilibili.com/video/BV1QhieYjEyE/?spm_id_from=333.1007.tianma.4-3-13.click&vd_source=92741bd354e6564f186e2d5a4a00e64b")
        :param cookies: 请求时需要使用的 cookies（默认为 None）
        :param headers: 请求时需要使用的 headers（默认为 None）
        """
        self.url = url
        self.cookies = cookies or {}
        self.headers = headers or {}
        self.video_title = ""
        self.video_url = ""
        self.audio_url = ""
        self.video_path = "temp/video.mp4"
        self.audio_path = "temp/audio.mp3"
        self.output_path = ""


    def fetch_video_info(self):
        """从 Bilibili 获取视频信息"""
        try:
            response = requests.get(self.url, cookies=self.cookies, headers=self.headers)
            if response.status_code == 200:
                # 提取视频标题
                self.video_title = re.findall('<h1 data-title="(.*?)" title="', response.text)[0]

                # 获取视频和音频的下载链接
                video_info = json.loads(re.findall('__playinfo__=(.*?)</script>', response.text)[0])
                self.video_url = video_info['data']['dash']['video'][0]['baseUrl']
                self.audio_url = video_info['data']['dash']['audio'][0]['baseUrl']
                print(f"视频标题：{self.video_title}")
                print(f"视频URL：get ✅ 分辨率 : {video_info['data']['dash']['video'][0]['width']} * {video_info['data']['dash']['video'][0]['height']}  ")
                print(f"音频URL：get ✅ 时长 : {video_info['data']['dash']['duration']}s")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"获取视频信息时发生错误: {e}")

    def download_file(self, url, filename):
        """下载文件并保存到本地"""
        try:
            if not os.path.exists("temp"):
                os.makedirs("temp")

            # 发起请求获取视频文件
            response = requests.get(url, cookies=self.cookies, headers=self.headers, stream=True)

            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                with open(filename, 'wb') as f, tqdm(
                        desc=filename,
                        total=total_size,
                        unit='B',
                        unit_scale=True
                ) as bar:
                    for data in response.iter_content(chunk_size=1024):
                        bar.update(len(data))  # 更新进度条
                        f.write(data)  # 写入文件内容
                print(f"文件已保存为 {filename}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"下载文件时发生错误: {e}")

    def combine_video_and_audio(self, video_path, audio_path, output_path):
        print('合并视频和音频中...  取决于电脑配置')
        """使用 ffmpeg-python 合并视频和音频"""
        try:
            # 创建输出文件夹
            if not os.path.exists("download"):
                os.makedirs("download")

            # 使用 ffmpeg-python 进行视频和音频合并
            video_input = ffmpeg.input(video_path)
            audio_input = ffmpeg.input(audio_path)

            ffmpeg.output(video_input, audio_input, output_path, vcodec='libx264', acodec='aac',
                          strict='experimental', audio_bitrate='192k', loglevel='error', threads=0, preset='fast') \
                .run(overwrite_output=True)

            print(f"合并完成，输出文件: {output_path}")

        except ffmpeg.Error as e:
            print(f"FFmpeg 错误: {e}")
            print(f"错误输出: {e.stderr.decode()}")

    def download_and_merge(self):
        """下载视频和音频并合并"""
        self.fetch_video_info()

        if not self.video_url or not self.audio_url:
            print("视频或音频URL缺失，无法下载或合并")
            return

        # 下载视频和音频
        video_filename = f"temp/{self.video_title}.mp4"
        audio_filename = f"temp/{self.video_title}.mp3"

        print(f"开始下载视频: {video_filename}")
        self.download_file(self.video_url, video_filename)

        print(f"开始下载音频: {audio_filename}")
        self.download_file(self.audio_url, audio_filename)

        # 合并视频和音频
        self.output_path = f"download/{self.video_title}.mp4"
        self.combine_video_and_audio(video_filename, audio_filename, self.output_path)

        # 清空temp
        if os.path.exists("temp"):
            for file in os.listdir("temp"):
                file_path = os.path.join("temp", file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir("temp")


# 示例：使用 BilibiliDownloader 下载和合并视频与音频
if __name__ == "__main__":
    while True:
        # 示例：获取 Bilibili 视频 URL
        url = get_bilibili_url()
        print(f"获取的 Bilibili 视频 URL: {url}")

        # 从终端获取 SESSDATA
        senss_data = get_sessdata()

        # 如果没有输入 SESSDATA，设置为空字符串
        cookies = {
            'SESSDATA': senss_data if senss_data else ''
        }

        # 设置反扒三杰
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        # 初始化下载器
        downloader = BilibiliDownloader(url, headers=headers, cookies=cookies)

        # 下载
        downloader.download_and_merge()
