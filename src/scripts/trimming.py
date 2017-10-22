# coding:utf-8
import cv2

# @brief 画像を正方形にトリミングする
#
# @param[in] image         画像情報を扱うnumpy.ndarray
# @param[in] top           トリミングしたい矩形の左上の頂点のy座標
# @param[in] left          トリミングしたい矩形の左上の頂点のx座標
# @param[in] width         トリミングしたい矩形の幅
# @param[in] height        トリミングしたい矩形の高さ
# @param[in] file_name     トリミングする画像の名前
# @param[in] serial_number トリミングする画像の通し番号
#
# @return    image_name トリミング後の画像のファイル名
def trimming(image, top, left, width, height, file_name, serial_number):
    image_name = file_name+str(serial_number)+".png"

    # 矩形を正方形に変換
    if(height > width):
        height -= (height - width) / 2
        top += (height - width) / 2
    else:
        width -= (width - height) / 2
        left += (width - height) / 2

    # 画像を256*256にトリミング
    trim = image[top:top+height, left:left+width]    
    size = (256, 256)
    trim = cv2.resize(trim, size)

    cv2.imwrite(image_name,trim)

    return image_name
