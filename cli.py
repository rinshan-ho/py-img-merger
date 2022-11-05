import os
import cv2
import sys
import configparser

dir = os.path.dirname(sys.argv[0])
config_path = dir + '\\config.ini'
config_ini = configparser.ConfigParser()
config_ini.read(config_path, encoding = 'utf-8')

DEFAULT_NAME = config_ini.get('DEFAULT', 'name')
DEFAULT_EXT = config_ini.get('DEFAULT', 'ext')
DEFAULT_METHOD = config_ini.get('DEFAULT', 'method')
DEFAULT_SCALING = config_ini.get('DEFAULT' ,'scaling')
OUTPUT_PATH = config_ini.get('DEFAULT', 'path')

def hconcat(img_list, scaling):
    if(scaling=='0'):
        #最小pxを取得
        height = min(img.shape[0] for img in img_list)
    elif(scaling=='1'):
        #最大pxを取得
        height = max(img.shape[0] for img in img_list)
    #取得したサイズに拡大縮小
    img_list_resize = [cv2.resize(img, (int(img.shape[1] * height / img.shape[0]), height)) for img in img_list]
    return cv2.hconcat(img_list_resize)

def vconcat(img_list, scaling):
    if(scaling=='0'):
        #最小pxを取得
        width = min(img.shape[1] for img in img_list)
    elif(scaling=='1'):
        #最大pxを取得
        width = max(img.shape[1] for img in img_list)
    #取得したサイズに拡大縮小
    img_list_resize = [cv2.resize(img, (width, int(img.shape[0] * width / img.shape[1]))) for img in img_list]
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
    scaling = input('結合基準を選択してください(最小px:0, 最大px:1)\n(デフォルトは"0"です)\n>> ')


    #DEFAULT値の設定
    if(name==''):
        name = DEFAULT_NAME
    if(ext==''):
        ext = DEFAULT_EXT
    else:
        #先頭に”.”が付いていたら除去
        ext = ext.removeprefix('.')
    if(method=='' or method!='0' or method!='1'):
        method = DEFAULT_METHOD
    if(scaling=='' or scaling!='0' or scaling!='1'):
        scaling = DEFAULT_SCALING


    if(method=='0'):
        img = hconcat(imgs, scaling)
    
    if(method=='1'):
        img = vconcat(imgs, scaling)

    #OUTPUT_PATHに画像を出力
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    cv2.imwrite(f'{OUTPUT_PATH}\\{name}.{ext}', img)
    print(f'{OUTPUT_PATH}\\{name}.{ext}')
else:
    print("画像をD&Dしてください\n")