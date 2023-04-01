def is_overlap(a1, a2, b1, b2):
    return (a1 <= b2) and (a2 >= b1)

# 测试数据
a1, a2 = 1.0, 4.0
b1, b2 = 1.5, 3.5

# 判断是否有重叠
if is_overlap(a1, a2, b1, b2):
    print("区间[{}, {}]和区间[{}, {}]有重叠".format(a1, a2, b1, b2))
else:
    print("区间[{}, {}]和区间[{}, {}]没有重叠".format(a1, a2, b1, b2))