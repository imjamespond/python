import os
import tensorflow as tf
import dotenv

dotenv.load_dotenv()

backends = [
    'opencv', 'ssd', 'dlib', 'mtcnn', 'fastmtcnn',
    'retinaface', 'mediapipe', 'yolov8n', 'yolov8m',
    'yolov8l', 'yolov11n', 'yolov11s', 'yolov11m',
    'yolov11l', 'yolov12n', 'yolov12s', 'yolov12m',
    'yolov12l', 'yunet', 'centerface',
]
detector = os.getenv("DETECTOR", backends[3])
align = True

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def config_gpu():

    # ==========================================
    # 第一步：限制 TensorFlow 显存增长 (最重要)
    # ==========================================
    # 必须在初始化 GPU 之前设置
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                # 开启显存按需增长，而不是一开始就占满
                tf.config.experimental.set_memory_growth(gpu, True)

                # 可选：设置显存硬性上限 (例如只允许使用 4GB)
                # 如果你的显卡是 8G，建议设置 4096；如果是 12G，可以设 6144 或 8192
                tf.config.set_logical_device_configuration(
                    gpu,
                    [tf.config.LogicalDeviceConfiguration(memory_limit=4096)]
                )
                print("✅ GPU 显存配置成功：按需分配，上限 4GB", gpu)
        except RuntimeError as e:
            # 异常通常发生在程序启动后试图修改物理设备时
            print(f"⚠️ GPU 配置失败: {e}")
