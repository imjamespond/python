import torch
print(torch.cuda.is_available())  # 应返回 True
print(torch.cuda.get_device_name(0))  # 显示显卡型号