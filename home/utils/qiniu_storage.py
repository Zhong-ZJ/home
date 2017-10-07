#coding=utf-8

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'zvMX9Z5KEDOGpEKG7tUjiHbgRh4d5IWRuLGxGjq4'
secret_key = 'CzuMspAyuh4XQS7M_AJhTe32_Jg-E27ugaQCFIZe'

def storage(image_data):
    # 构建鉴权对象
    if not image_data:
        return None
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'home'

    # 上传到七牛后保存的文件名  (文件名七牛解决所以关闭他)
    # key = 'my-python-logo.png';

    # 要上传文件的本地路径(不用上传文件路径直接上传文件)
    # localfile = './sync/bbb.jpg'

    # 生成上传Token凭证(空间名,文件名,过去时间)
    token = q.upload_token(bucket_name, None, 3600)

                #put_data上传数据#凭证,文件名,二进制
    ret,info = put_data(token, None, image_data)
    print(info)
    return ret['key']

if __name__ == '__main__':
    file_name = raw_input('输入文件名：')
    file = open(file_name,'rb')
    file_data = file.read()
    key = storage(file_data)
    print key
    file.close()