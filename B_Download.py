import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import threading
import datetime

def download_video():
    # 禁用输入和下载按钮
    entry.config(state='disabled')
    button.config(state='disabled')

    # 获取用户输入的视频URL
    url = entry.get()
    # 弹出文件选择对话框，选择保存路径和文件名
    save_path = filedialog.askdirectory()

    # 获取当前日期时间
    current_datetime = datetime.datetime.now()

    # 将日期时间格式化为字符串
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # 使用格式化后的日期时间作为视频名称
    file_name = formatted_datetime

    # 创建进度条
    progress_bar = ttk.Progressbar(window, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=10)

    # 创建下载线程
    def download_thread():
        # 构建you-get命令
        command = ['you-get', '-o', save_path, '-O', file_name + '.mp4', url]

        # 启动子进程执行命令
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                                   encoding='utf-8',executable='E:\\pythonProject3\\venv\\Scripts\\you-get.exe')
        # 循环检查子进程是否结束
        while process.poll() is None:
            # 获取命令输出
            output = process.stdout.readline().strip()
            if output.startswith('[download]'):
                # 提取下载百分比
                percentage = int(output.split()[1].strip('%'))
                # 更新进度条
                progress_bar['value'] = percentage
                window.update()

        # 弹出消息框提示下载完成
        messagebox.showinfo('下载完成', '视频下载完成！')

        # 启用输入和下载按钮
        entry.config(state='normal')
        button.config(state='normal')

    # 创建并启动下载线程
    download_thread = threading.Thread(target=download_thread)
    download_thread.start()

# 创建主窗口
window = tk.Tk()
window.title('视频下载')
window.geometry('300x150')

# 创建标签和输入框
label = tk.Label(window, text='请输入视频URL：')
label.pack(pady=10)
entry = tk.Entry(window)
entry.pack(pady=5)

# 创建下载按钮
button = tk.Button(window, text='下载', command=download_video)
button.pack(pady=10)

# 进入主循环
window.mainloop()

