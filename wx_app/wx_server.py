from django.http import HttpResponse, JsonResponse
import hashlib
import requests
import json
from common_util.redis_util.redis_conn import RedisUtil


app_name = '盛世爱游'
app_secret = 'b13e4dfa82a531a43f3447b6a2b9286c'
app_id = 'wxd915430b4a523911'
token = 'douban_book'
encoding_aes_key = '5s8OZFOIB2xexF8yhHHhCEPP3mIk4o7qfyF6KyrMJbm'


# 验证token，用于连接到微信服务器
def check_signature(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = 'douban_book'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()
        print(hashstr)
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("field")
    else:
        return HttpResponse("error")


# 获取access_token，获取之后会存到redis数据库中，并设置过期时间是7150秒，过期后重新获取
def get_access_token():
    r = RedisUtil.get_conn('txy_db')
    access_token = r.get('wx_access_token')
    if access_token is None:
        # 如果发现access_token已经过过期，重新请求access_token
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (app_id, app_secret)
        response = requests.get(url).text
        access_token = json.loads(response)['access_token']

        # 将请求后的access_token重新写入到redis中，并设置过期时间
        r.set('wx_access_token', access_token, ex=7150)
    else:
        # 如果没有过期，用utf-8解码并返回
        access_token = access_token.decode('utf-8')
    print('access_token', access_token)
    return access_token


def create_menu(menu_conf_dic):
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    response = requests.post(url, menu_conf_dic).text
    return response

