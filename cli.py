import os
import cv2
import sys

DEFAULT_NAME = 'merged'
DEFAULT_EXT = 'png'
DEFAULT_METHOD = '0'
DEFAULT_OUTPUT_DIR = os.environ['USERPROFILE']+'\\Pictures\\output_img-merging'

def hconcat(img_list):
    #最も小さい高さを取得
    min_height = min(img.shape[0] for img in img_list)
    print(img.shape[0] for img in img_list)
    #最も小さい高さに合わせてサイズの変更
    img_list_resize = [cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height)) for img in img_list]
    return cv2.hconcat(img_list_resize)

def vconcat(img_list):
    #最も小さい幅を取得
    min_width = min(img.shape[1] for img in img_list)
    #最も小さい幅に合わせてサイズの変更
    img_list_resize = [cv2.resize(img, (min_width, int(img.shape[0] * min_width / img.shape[1]))) for img in img_list]
    return cv2.vconcat(img_list_resize)

#config.txtより設定を反映
with open('config.txt', 'r', encoding='UTF-8') as file:
    settings = file.readlines()
for i, setting in enumerate(settings):
    if(setting.startswith('#')):
        continue
    elif(setting.startswith('<path>\n')):
        if(i+1<len(settings) and settings[i+1]!=''):
            OUTPUT_DIR = settings[i+1]
            # print(OUTPUT_DIR)



#画像の読み込み
imgs = []
img_paths = sys.argv[1:]
for path in img_paths:
    imgs.append(path)
#大小関係なしにAtoZソート
imgs.sort(key=str.casefold)

for i, img in enumerate(imgs):
    imgs[i] = cv2.imread(img)

if(imgs!=[]):
    name = input('結合した画像の名前を入力してください\n(デフォルトは"merged"です)\n>> ')
    ext = input('拡張子を入力してください\n(デフォルトは".png"です)\n>> .')
    method = input('結合方法を選択してください(縦:0, 横:1)\n(デフォルトは"0"です)\n>> ')

    if(name==''):
        name = DEFAULT_NAME
    if(ext==''):
        ext = DEFAULT_EXT

    #先頭に”.”が付いていたら除去
    ext = ext.removeprefix('.')

    if(method==''):
        method = DEFAULT_METHOD


    if(method=='0'):
        img = hconcat(imgs)
    elif(method=='1'):
        img = vconcat(imgs)

    #OUTPUT_DIRが存在すればそこに結合した画像を出力
    if os.path.exists(OUTPUT_DIR):
        cv2.imwrite(f'{OUTPUT_DIR}\\{name}.{ext}', img)
    #なければDEFAULT_OUTPUT_DIRに出力
    else:
        if not os.path.exists(DEFAULT_OUTPUT_DIR):
            os.makedirs(DEFAULT_OUTPUT_DIR)
        cv2.imwrite(f'{DEFAULT_OUTPUT_DIR}\\{name}.{ext}', img)
        print(f'{DEFAULT_OUTPUT_DIR}\\{name}.{ext}')
else:
    print("画像をD&Dしてください\n")