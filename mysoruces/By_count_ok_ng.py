def count_ok_ng(path):
    ok_count = 0
    ng_count = 0
    with open(path, 'r') as f:
        txt = f.readlines()
        for i, t in enumerate(txt):
            flag = t[-2]
            if flag == "1":
                ok_count += 1
            else:
                ng_count += 1
    return ok_count, ng_count
