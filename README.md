# tcpreplay_GUI
tcpreplay的一个用户界面 使用pyqt实现
## 使用pyqt的原因：
  跨平台需求 c++版qt不太熟 java的GUI太丑
## 用到的一些东西：
- 自定义checkboxlist
- json的读取保存与使用
- 选择文件
- QScrollArea() QTabWidget() QSlider 多线程QThread
- pyinstaller打包安装
- 以sudo向shell发送指令：echo password |sudo -S command

## 遇到的一些坑：
- 使用anaconda配置路径：export PATH=/home/fd/anaconda3/bin:$PATH
- pyinstaller 需要配置库路径export LD_LIBRARY_PATH=/home/fd/anaconda3/lib:$LD_LIBRARY_PATH
- 通常情况下gui程序都建议使用多线程 否则主界面会卡死
- anaconda自带的spyder没有代码缩进 pycharm可以代码缩进但调试界面不如spyder
- pyqt也是可以用qtcreator画界面的 很多教程完全没有提到
- qt组件的一些方法的命名很反直觉 用的时候得确认一下

## 存在的一些问题：
- 使用了全局变量 应该避免
- 代码条理性不过好 太乱
