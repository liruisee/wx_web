import requests
from common_util.redis_util.redis_conn import RedisUtil
import json

app_name = '盛世爱游'
app_secret = 'b13e4dfa82a531a43f3447b6a2b9286c'
app_id = 'wxd915430b4a523911'
token = 'douban_book'
encoding_aes_key = '5s8OZFOIB2xexF8yhHHhCEPP3mIk4o7qfyF6KyrMJbm'

# 自定义菜单配置文件
menu_conf_dic = {
        "button": [
            {
                "name": "菜单1",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "teacher_list",
                        "url": "http://118.89.222.232/wx_app/teacher_list?teacher_type=A"
                    },
                    {
                        "type": "view",
                        "name": "teacher_info",
                        "url": "http://118.89.222.232/wx_app/teacher_info?teacher_id=1"
                    }]
            },
            {
                "name": "菜单2",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "type_list",
                        "url": "http://118.89.222.232/wx_app/type_list/"
                    },
                    {
                        "type": "view",
                        "name": "type_list",
                        "url": "http://118.89.222.232/wx_app/type_list/"
                    }]
            }]
    }


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


if __name__ == '__main__':
    app_name = '盛世爱游'
    app_secret = 'b13e4dfa82a531a43f3447b6a2b9286c'
    app_id = 'wxd915430b4a523911'
    token = 'douban_book'
    encoding_aes_key = '5s8OZFOIB2xexF8yhHHhCEPP3mIk4o7qfyF6KyrMJbm'
    acc_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (app_id, app_secret)
    response = requests.get(acc_url).text
    print(response)

    access_token = json.loads(response)['access_token']
    menu_conf = json.dumps(menu_conf_dic, ensure_ascii=False).encode('utf-8')
    print(access_token)

    menu_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
    response = requests.post(menu_url, menu_conf).text
    print(response)
