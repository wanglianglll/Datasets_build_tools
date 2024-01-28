import cv2
import os

video_name = f'F:/Target_detection/datasets/blbl/videos/8.mp4'  # 视频路径
interval = 0.5  # 抽帧间隔(单位秒)


def extract_frames(video_path, interval_second=0.5):
    # 确保视频文件存在
    if not os.path.exists(video_path):
        print(f"Video file {video_path} does not exist.")
        return

    # 获取视频所在目录和视频名称
    video_dir, video = os.path.split(video_path)
    base_name = os.path.splitext(video)[0]

    # 创建images文件夹（如果不存在）
    images_dir = os.path.join(video_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # 读取视频
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    frame_interval = int(fps * interval_second)  # 每隔interval秒抽取一帧

    current_frame = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 如果没有获取到帧，说明视频读取完毕

        # 每隔frame_interval帧进行一次抽帧
        if current_frame % frame_interval == 0:
            frame_file = os.path.join(images_dir, f"{base_name}_frame{frame_count}.jpg")
            cv2.imwrite(frame_file, frame)
            print(f"Extracted {frame_file}")
            frame_count += 1

        current_frame += 1

    cap.release()
    print("Done extracting frames.")


if __name__ == "__main__":
    extract_frames(video_name, interval)
