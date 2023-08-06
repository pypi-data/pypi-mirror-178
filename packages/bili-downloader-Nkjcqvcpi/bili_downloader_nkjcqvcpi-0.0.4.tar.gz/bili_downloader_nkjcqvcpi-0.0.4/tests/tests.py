pics = {}
with open('train_list.txt') as f:
    for line in f.readlines():
        img, pid = line.rstrip().split()
        if pid in pics.keys():
            pics[pid].append(img)
        else:
            pics[pid] = [img]

avl = [len(v) for k, v in pics.items()]
cnt_old = sum(avl)
avg = int(cnt_old / len(avl))
cnt = 0
for k, v in pics.items():
    pics[k] = v[:avg]
    cnt += len(pics[k])

result = []
for k, v in pics.items():
    for p in v:
        result.append(f'{p} {k}\n')

with open('new_train_list.txt', 'w') as f:
    f.writelines(result)
