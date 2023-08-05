import os
import shutil
from algorithm_mic_sdk.algorithms.check_photo_classic import CheckPhotoClassic
from algorithm_mic_sdk.auth import ClassicAuthInfo
from algorithm_mic_sdk.tools import FileInfo
import requests
import base64
filename = '14.jpg'

url = 'http://172.24.74.132:8002/api/check_pic'

host = 'http://mars.leqi.us:17012'  # 算法host地址
user_name = 'panso'
password = '0bdca2d8-4a3d-11eb-addb-0242c0a80006'
classic_password = 'rongsuo'
classic_user_name = 'pan'
files = os.listdir('src/检测/模糊检测/')
auth_info = ClassicAuthInfo(classic_user_name=classic_user_name, classic_password=classic_password,
                                user_name=user_name,
                                password=password, host=host, gateway_cache=True, extranet=True)
for file in files:
    filename = 'src/检测/模糊检测/' + file
    file_info = FileInfo.for_file_bytes(open(filename, 'rb').read())
    try:
        check_photo = CheckPhotoClassic(auth_info, file_info, result_matches=True)
        resp = check_photo.synchronous_request(timeout=30)
    except Exception as e:
        print(filename, e)
        continue
    algo_image_blur = resp.result['check_original_result']['face_blur']
    data = {
        'spec_id': 440,
        'file': base64.b64encode(open(filename, 'rb').read()).decode()
    }
    resp = requests.post(url, json=data)
    pingan_image_blur =resp.json()['check_raw_parameter']['image_blur']
    print(file, algo_image_blur, pingan_image_blur)
    save_name = f'src/save/{file.split(".")[0]}-{algo_image_blur}-{pingan_image_blur}.jpg'
    shutil.copy(filename, save_name)

    # if 'check_original_result' not in resp.result:
    #     print(filename, resp.json)
    #     continue
    # check_original_result = resp.result['check_original_result']
    # decoration_occlusion = check_original_result['decoration_occlusion']
    # if decoration_occlusion>90:
    #     s = '不通过'
    # else:
    #     s ='通过'
    # shutil.copy(filename, f'src/save/{file.split(".")[0]}-新-{s}-{decoration_occlusion}.png')



    # eye_left = check_original_result['facial_feature_points'][39]
    # eye_right = check_original_result['facial_feature_points'][42]
    # eye_length = (eye_right[0] - eye_left[0])
    # model_coordinate = {
    #     'left_eye': eye_left,  # 左眼的坐标
    #     'eye_length': eye_length  # 眼睛宽度
    # }
    # print(file, model_coordinate)
