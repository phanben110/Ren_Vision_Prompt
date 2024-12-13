
# from gtts import gTTS
# import os

# def speak_text_in_vietnamese(text):
#     tts = gTTS(text=text, lang='vi')
#     tts.save("output.mp3")
#     os.system("afplay output.mp3")  # Chạy file âm thanh trên macOS


# import tkinter as tk
# from video_stream import VideoStreamHandler
# from content_description import ContentDescriber
# import threading
# import time

# # Hàm chờ cho đến khi text generation hoàn tất
# def wait_for_text_generation(content_describer, message_label):
#     while content_describer.message_var.get() == "":  # Chờ message_var có giá trị
#         time.sleep(0.1)  # Giảm tải CPU bằng cách chờ 100ms mỗi vòng lặp
#     text = content_describer.message_var.get().replace("\n", "").replace("\r", "").strip()
#     print("Text generation completed:", text )
#     speak_text_in_vietnamese(text)
#     message_label.config(text="Content description completed.")  # Cập nhật thông báo khi hoàn thành

# # Main GUI setup and button handlers
# root = tk.Tk()
# root.title("Webcam Stream")

# canvas = tk.Canvas(root, width=1920, height=1080)
# canvas.pack()

# video_handler = VideoStreamHandler(root, canvas)
# content_describer = ContentDescriber(root, None, video_handler)

# # Hàm xử lý khi nhấn phím Space
# def describe_and_wait(event=None):
#     # Cập nhật thông báo ban đầu
#     message_label.config(text="Describing content... Please wait.")
#     # Bắt đầu mô tả nội dung trong luồng phụ
#     threading.Thread(target=content_describer.threaded_describe_content).start()
#     # Chờ text generation hoàn tất
#     threading.Thread(target=wait_for_text_generation, args=(content_describer, message_label)).start()

# # Ràng buộc phím Space với hàm describe_and_wait
# root.bind("<space>", describe_and_wait)

# message_label = tk.Label(root, text="", wraplength=500)
# message_label.pack()

# video_handler.start_stream()

# root.mainloop()


from gtts import gTTS
import os
import tkinter as tk
from video_stream import VideoStreamHandler
from content_description import ContentDescriber
import threading
import time

# Hàm phát âm thanh bằng tiếng Việt
def speak_text_in_vietnamese(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("output.mp3")
    os.system("afplay output.mp3")  # Chạy file âm thanh trên macOS

# Hàm phát âm thanh và xóa nội dung sau khi phát
def speak_text_in_vietnamese_and_clear(content_describer, message_label):
    text = content_describer.message_var.get().replace("\n", "").replace("\r", "").strip()
    print("Text generation completed:", text)
    if text:  # Kiểm tra nếu có nội dung để nói
        speak_text_in_vietnamese(text)
        content_describer.message_var.set("")  # Làm trống nội dung sau khi phát
        message_label.config(text="")  # Làm trống nhãn sau khi hoàn tất

# Hàm chờ cho đến khi text generation hoàn tất
def wait_for_text_generation(content_describer, message_label):
    while content_describer.message_var.get() == "":  # Chờ message_var có giá trị
        time.sleep(0.1)  # Giảm tải CPU bằng cách chờ 100ms mỗi vòng lặp
    # Chạy hàm phát âm thanh và xóa nội dung
    speak_text_in_vietnamese_and_clear(content_describer, message_label)

# Cấu hình giao diện chính
root = tk.Tk()
root.title("Webcam Stream")

canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

# Khởi tạo VideoStreamHandler và ContentDescriber
video_handler = VideoStreamHandler(root, canvas)
content_describer = ContentDescriber(root, None, video_handler)

# Hàm xử lý khi nhấn phím Space
def describe_and_wait(event=None):
    # Cập nhật thông báo ban đầu
    message_label.config(text="Describing content... Please wait.")
    # Bắt đầu mô tả nội dung trong luồng phụ
    threading.Thread(target=content_describer.threaded_describe_content).start()
    # Chờ text generation hoàn tất
    threading.Thread(target=wait_for_text_generation, args=(content_describer, message_label)).start()

# Ràng buộc phím Space với hàm describe_and_wait
root.bind("<space>", describe_and_wait)

# Nhãn hiển thị thông báo
message_label = tk.Label(root, text="", wraplength=500)
message_label.pack()

# Bắt đầu luồng video
video_handler.start_stream()

# Chạy vòng lặp chính của GUI
root.mainloop()
