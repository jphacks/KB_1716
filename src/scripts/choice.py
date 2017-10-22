
# coding:utf-8
import cv2

# @brief カクテルをレコメンドする
#
# @param[in] A Aさんの顔の位置と感情、露出度が入ったdict
# @param[in] B Bさんの顔の位置と感情、露出度が入ったdict
# @return sake 左側の人にsake[0]、右側の人にsake[1]をレコメンドする文字列配列
def choice(A, B):
    if A['x'] < B['x']:
        sake = [recommend(A),recommend(B)]
    else:
        sake = [recommend(B),recommend(A)]
    return sake

# @brief 最も数値の高い感情を求める
#
# それぞれの感情の番号
#  * anger     ->  0
#  * neutral   ->  1
#  * sadness   ->  2
#  * surprise  ->  3
#  * exposure  ->  4
#  * others    -> -1 (負の感情を持たれていた場合)
#
# @param[in] emt　それぞれの感情と数値を表すdict
# @return max_emt 最大の数値を持った感情の番号
def max_emotion(emt):
    max_val = 0.0
    for key, value in emt.iteritems():
        if key == 'x':
            continue
        if key == 'drunk':
            continue
        if value > max_val:
            max_val = value
            if key == 'anger':
                max_emt = 0
            elif key == 'neutral':
                max_emt = 1
            elif key == 'sadness':
                max_emt = 2
            elif key == 'surprise':
                max_emt = 3
            elif key == 'exposure':
                max_emt = 4
            else:
                max_emt = -1
    return max_emt

# @brief おすすめのカクテルの色を求める
#
# すでに酔っている場合は、感情に関わらず水が選択される
#
# @param[in] emt ある人の感情
# return sake おすすめのカクテルの色
def recommend(emt):
    max_emt = max_emotion(emt)
    
    # 感情に合わせたカクテルを選ぶ
    if emt['drunk'] < 0:
        sake = u'water'
    elif max_emt < 0:
        sake = u'izakaya'
    elif max_emt == 0:
        sake = u'red'
    elif max_emt == 1:
        sake = u'clear'
    elif max_emt == 2:
        sake = u'blue'
    elif max_emt == 3:
        sake = u'yellow'
    elif max_emt == 4:
        sake = u'pink'

    return sake
