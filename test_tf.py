import tensorflow as tf
import dotenv

dotenv.load_dotenv()

# 1. 确认版本
print("TensorFlow 版本:", tf.__version__)
# 预期: 2.10.0

# 2. 确认 GPU 被识别
print("GPU 数量:", tf.config.list_physical_devices('GPU'))
# 预期: 1 或以上（如果是0说明失败）

# 3. 确认 CUDA 版本
print("CUDA 是否可用:", tf.test.is_built_with_cuda())
# 预期: True
