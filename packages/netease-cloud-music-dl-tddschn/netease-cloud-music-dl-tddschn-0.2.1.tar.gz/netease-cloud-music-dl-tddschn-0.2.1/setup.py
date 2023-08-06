# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncm']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=4.3.0',
 'mutagen>=1.38.0',
 'pycryptodomex>=3.16.0,<4.0.0',
 'requests>=2.17.3']

entry_points = \
{'console_scripts': ['ncm = ncm.start:main']}

setup_kwargs = {
    'name': 'netease-cloud-music-dl-tddschn',
    'version': '0.2.1',
    'description': 'Netease cloud music song downloader, with full ID3 metadata!',
    'long_description': '# 网易云音乐下载器\n基于Python3.X编写的网易云音乐命令行下载器，自动下载专辑封面，记录歌手名、音乐标题、专辑名等元数据，并写入[ID3 Tags][1] metadata容器。在github上试了几个高星的下载器都没有写入专辑封面，对于强迫症患者简直不能忍，于是一怒之下决定自己写。\n\n## Preview\n![Preview](preview.gif)\n\n## Installation\n\n若没有安装Python3，请先到官网下载并安装：\n> https://www.python.org/download/releases/3.0/\n\n\n首先下载源码：\n```bash\n$ git clone https://github.com/codezjx/netease-cloud-music-dl.git\n```\n\n进入根目录，然后执行：\n```bash\n$ python3 setup.py install\n```\n\n最终显示以下log，表示顺利安装：\n```\nrunning install\nrunning bdist_egg\nrunning egg_info\n...\n...\nFinished processing dependencies for netease-cloud-music-dl==x.x.x\n```\n\n后续直接在命令行中通过`ncm`指令即可快速调用相关功能，**Warning: 目前只支持Python3.x版本**\n\n## Feature\n- 支持下载专辑封面并嵌入MP3文件\n- 支持写入歌手名、音乐标题、专辑名等信息至[ID3 Tags][1]\n- 支持跳过已下载的音频文件\n- 支持常见设置选项，如：保存路径、音乐命名格式、文件智能分类等\n- 默认下载比特率为320k的高品质音乐（若木有320k则会自动下载最高比特率）\n- 支持下载单首/多首歌曲\n- 支持下载歌手热门单曲（可配置最大下载数）\n- 支持下载专辑所有歌曲\n- 支持下载公开歌单所有歌曲\n\n**（注意：已下架的音乐暂时无法下载）**\n\n通过`ncm -h`即可查看所支持的参数列表：\n```\n$ ncm -h\nusage: ncm [-h] [-s song_id] [-ss song_ids [song_ids ...]] [-hot artist_id]\n           [-a album_id] [-p playlist_id]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s song_id            Download a song by song_id\n  -ss song_ids [song_ids ...]\n                        Download a song list, song_id split by space\n  -hot artist_id        Download an artist hot 50 songs by artist_id\n  -a album_id           Download an album all songs by album_id\n  -p playlist_id        Download a playlist all songs by playlist_id\n```\n\n## Usage\n\n### 下载单曲\n\n使用参数`-s`，后加歌曲id或者歌曲完整url，如：\n```bash\n$ ncm -s 123123\nor\n$ ncm -s http://music.163.com/#/song?id=123123\n```\n\n### 下载多首歌曲\n\n使用参数`-ss`，后加歌曲ids或者歌曲完整urls(id或url之间通过空格隔开)，如：\n```bash\n$ ncm -ss 123123 456456 789789\nor\n$ ncm -ss url1 url2 url3\n```\n\n### 下载某歌手的热门单曲(默认下50首，可配置)\n\n使用参数`-hot`，后加歌手id或者完整url，如：\n```bash\n$ ncm -hot 123123\nor\n$ ncm -hot http://music.163.com/#/artist?id=123123\n```\n\n### 下载某张专辑的所有歌曲\n\n使用参数`-a`，后加专辑id或者完整url，使用方法同上。\n\n### 下载某个公开的歌单\n\n使用参数`-p`，后加歌单id或者完整url，使用方法同上，必须确认是**公开**的歌单才能下载哦。\n\n## Settings\n\n配置文件在在用户目录下自动生成，路径如下：\n```\n/Users/yourUserName/.ncm/ncm.ini\n```\n\n目前支持以下几项设置：\n```\n[settings]\n\n#--------------------------------------\n# 热门音乐的最大下载数，默认50\n# Range: 0 < hot_max <= 50\n#--------------------------------------\ndownload.hot_max = 50\n\n#--------------------------------------\n# 音乐文件的下载路径，默认在用户目录.ncm/download目录下\n#--------------------------------------\ndownload.dir = /Users/yourUserName/.ncm/download\n\n#--------------------------------------\n# 音乐命名格式，默认1\n# 1: 歌曲名\n# 2: 歌手 - 歌曲名\n# 3: 歌曲名 - 歌手\n#--------------------------------------\nsong.name_type = 1\n\n#--------------------------------------\n# 文件智能分类，默认1\n# 1: 不分文件夹\n# 2: 按歌手分文件夹\n# 3: 按歌手/专辑分文件夹\n#--------------------------------------\nsong.folder_type = 1\n```\n\n**Warning:** 智能分类设置目前只针对`-s`和`-ss`参数有效，`-hot/-a/-p`分别会存于后缀为：`-hot50/-album/-playlist`的文件夹中，方便管理本地音乐。\n\n## Feedback\n\n如果遇到Bugs，欢迎提issue或者PR，谢谢各位支持~\n\n## License\n\nMIT License\n\nCopyright (c) 2017 codezjx <code.zjx@gmail.com>\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n[1]: https://zh.wikipedia.org/wiki/ID3\n',
    'author': 'codezjx',
    'author_email': 'code.zjx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/netease-cloud-music-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
