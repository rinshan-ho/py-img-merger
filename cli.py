import os
import cv2
import sys
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding = 'utf-8')

DEFAULT_NAME = config_ini.get('DEFAULT','name')
DEFAULT_EXT = config_ini.get('DEFAULT','ext')
DEFAULT_METHOD = config_ini.get('DEFAULT','method')
OUTPUT_PATH = config_ini.get('DEFAULT','path')

def hconcat(img_list):
    #最も小さい高さを取得
    min_height = min(img.shape[0] for img in img_list)
    #最も小さい高さに合わせてサイズの変更
    img_list_resize = [cv2.resize(img, (int(img.shape[1] * min_height / img.shape[0]), min_height)) for img in img_list]
    return cv2.hconcat(img_list_resize)

def vconcat(img_list):
    #最も小さい幅を取得
    min_width = min(img.shape[1] for img in img_list)
    #最も小さい幅に合わせてサイズの変更
    img_list_resize = [cv2.resize(img, (min_width, int(img.shape[0] * min_width / img.shape[1]))) for img in img_list]
    return cv2.vconcat(img_list_resize)


#画像の取得
imgs = []
img_paths = sys.argv[1:]
for path in img_paths:
    imgs.append(path)
#大小関係なしにAtoZソート
imgs.sort(key=str.casefold)

#画像が存在するとき
if(imgs!=[]):
    #imgsをimreadし再格納
    for i, img in enumerate(imgs):
        imgs[i] = cv2.imread(img)

    name = input('結合した画像の名前を入力してください\n(デフォルトは"merged"です)\n>> ')
    ext = input('拡張子を入力してください\n(デフォルトは".png"です)\n>> .')
    method = input('結合方法を選択してください(縦:0, 横:1)\n(デフォルトは"0"です)\n>> ')

    #DEFAULT値の設定
    if(name==''):
        name = DEFAULT_NAME
    if(ext==''):
        ext = DEFAULT_EXT
    else:
        #先頭に”.”が付いていたら除去
        ext = ext.removeprefix('.')
    if(method==''):
        method = DEFAULT_METHOD


    if(method=='0'):
        img = hconcat(imgs)
    elif(method=='1'):
        img = vconcat(imgs)

    #OUTPUT_PATHに画像を出力
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    cv2.imwrite(f'{OUTPUT_PATH}\\{name}.{ext}', img)
    print(f'{OUTPUT_PATH}\\{name}.{ext}')
else:
    print("画像をD&Dしてください\n")