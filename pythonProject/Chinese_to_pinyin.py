import os
from xpinyin import Pinyin

resume_rootdir = r'F:\Target_detection\datasets\HEU_Month1\HEU_Season1'


def rename(rootdir):
    print(u'重命名开始！')
    pin = Pinyin()
    for path in os.listdir(rootdir):
        if not os.path.isdir(os.path.join(rootdir, path)):
            continue
        llist = os.listdir(os.path.join(rootdir, path))
        for i in range(0, len(llist)):
            print(u'现在进行第{}个'.format(i))
            resume = os.path.join(os.path.join(rootdir, path), llist[i])
            obj = os.path.basename(resume)
            if obj[0] == '.':
                continue
            print(u'开始处理  {}'.format(obj))
            pinyin_name = pin.get_pinyin(obj, "")
            print(u'{} 新名字是:{}'.format(obj, pinyin_name))
            Newdir = os.path.join(os.path.join(rootdir, path), pinyin_name)  # 新的文件路径
            if os.path.exists(Newdir):
                print(u'{} 已经存在'.format(Newdir))
                continue
            else:
                os.rename(resume, Newdir)  # 重命名
        print(u'重命名结束！')


for dir in os.listdir(resume_rootdir):
    if os.path.isdir(os.path.join(resume_rootdir, dir)):
        rename(os.path.join(resume_rootdir, dir))
