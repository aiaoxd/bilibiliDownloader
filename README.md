# Bilibili Downloader
这是一个用于下载Bilibili 视频的Python 脚本。 2024-12-10

## 功能
- 从 Bilibili 获取视频和音频并下载链接
- 使用 `ffmpeg` 合并视频和音频
- 生成合并后的 MP4 文件
- SESSDATA为登录token,设置SESSDATA后可以下载账号权限内的最高画质视频,不设置则为未登录状态,视频画质为360P(貌似)

## 激活虚拟环境(可选)
在项目根目录下运行以下命令
对于 macOS 或 Linux，运行：
```bash
cd ~/Downloads/bilibiliDownloader-main
```
对于 Windows，运行：
```bash
cd %USERPROFILE%\Downloads\bilibiliDownloader-main
```
创建虚拟环境
```bash
python3 -m venv venv
```
对于 macOS 或 Linux，运行：
```bash
source venv/bin/activate
```
对于 Windows，运行：
```bash
venv\Scripts\activate
```

## 安装依赖

在项目根目录下运行以下命令安装所有必需的 Python 包：

```bash
pip install -r requirements.txt
```

## 运行
```bash
python bilibiliDownloader.py
```
按照提示 输入目标网址即可

## 退出
```bash
deactivate
```
## 如何获取SESSDATA
```bash
  1.打开 https://www.bilibili.com/
  2.登录
  3.右键检查或F12
  4.F5/CTRL+R/CMD+R 刷新一下
    >>  4.1 network/网络
    >>  4.2 选择一个请求
    >>  4.3 Headers
    >>  4.4 cookie
    >>  4.5 找到中间"SESSDATA=xxxx;"
    >>  后面222位的值就是你的令牌
```
<img width="1962" alt="image" src="https://github.com/user-attachments/assets/52a4966d-2ced-4d58-8ace-918003c5b0ee">



一般为IEC结尾 例如:
```bash
b106234%2C1748070390%2C4cfd5%2Ab1CjAVsNIDKYDjQfJnua6M5Dd-ddkmRWoJwFgUuM53N3UQ6JegiIK0c-9o0fJQAzBMI3gSVlNGWkJJZjd1a2FtUDVjWnlVVS1NdjhpcmRval96aUdmUi01ZGNvdF8zVUVNMVFuRGJ3a....................nJ2oNS1UbVBoSFZyRVJjSHVnNWRnIIEC(这是假的)
```
SESSDATA一次输入后会记录在本地SESSDATA.txt文件内,如需更换,删除即可.

## 视频教程
```bash
https://www.bilibili.com/video/BV1rRqkYdEkm
```

