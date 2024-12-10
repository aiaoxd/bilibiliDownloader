# Bilibili Downloader
这是一个用于下载Bilibili 视频Python 脚本。 2024-12-10

## 功能
- 从 Bilibili 获取视频和音频并下载链接
- 使用 `ffmpeg` 合并视频和音频
- 生成合并后的 MP4 文件

## 安装依赖

在项目根目录下运行以下命令安装所有必需的 Python 包：

```bash
pip install -r requirements.txt
bash

## 运行
```bash
python bilibiliDownloader.py
```bash
## 如何获取SESSDATA
  1.打开https://www.bilibili.com/
  2.登录
  3.右键检查或F12
  4.network/网络  >>  选择一个请求  >>  Headers  >>  cookie >>   找到"SESSDATA=" >> 后面222位的值就是你的令牌

一般为IEC结尾 例如:
```bash
b106234%2C1748070390%2C4cfd5%2Ab1CjAVsNIDKYDjQfJnua6M5Dd-ddkmRWoJwFgUuM53N3UQ6JegiIK0c-9o0fJQAzBMI3gSVlNGWkJJZjd1a2FtUDVjWnlVVS1NdjhpcmRval96aUdmUi01ZGNvdF8zVUVNMVFuRGJ3a....XNWOFdRaG1oZFdpcnJ2oNS1UbVBoSFZyRVJjSHVnNWRnIIEC(这是假的)
```bash



