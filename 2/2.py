import torch

A = torch.arange(24, dtype=torch.float32).reshape(2, 3, 4)
B = A.clone()  # 通过分配新内存，将A的一个副本分配给B
print(A,'\n', A + B)

A_sum_axis0 = A.sum(axis=0)
A_sum_axis0, A_sum_axis0.shape

A_sum_axis1 = A.sum(axis=1)
A_sum_axis1, A_sum_axis1.shape

print(A.sum(axis=[0])) # 结果和A.sum()相同

print("foobar")