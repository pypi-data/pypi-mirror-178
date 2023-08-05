import requests
import time
from yyweaknet.stf import STFServer

class WeakNetworkConfig(object):
    """
        弱网配置工具类提供以下功能
        1、自动连接/断开弱网wifi
        2、为设备配置弱网配置
    """
    # ios切换网络app bundle_id
    IOS_APP_BUNDLE_ID = "com.yy.net.test"
    # atc 服务器
    ATC_HOST = "http://172.29.182.90:8000"
    ATC_AUTH_URI = "/api/v1/auth/{}/"
    ATC_SHAPE_URI = "/api/v1/shape/{}/"

    def __init__(self, devices_serial, stf_url=None, sft_token=None, platform='ios'):
        """
            :param devices_serial: 设备serial
            :param stf_url: sft服务器地址
            :param sft_token: sft服务token
            :param platform: 设备平台
        """
        self._platform = platform
        self._devices_serial = devices_serial
        self._stf = STFServer(url=stf_url, token=sft_token)
        self._devices = self._stf.get_device_info(self._devices_serial, self._platform)
        self._device_ip = None
        if self._devices_serial is None:
            raise Exception('No devices:{} found'.format(self._devices_serial))

    def connect_wifi(self):
        """
            连接弱网WIFI热点
        """
        if self._platform == 'ios':
            self._connect_ios()

    def disconnect_wifi(self):
        """
            断开弱网WIFI热点
        """
        if self._platform == 'ios':
            self._disconnect_ios()

    def _connect_ios(self):
        # 发送自动点击弹窗配置
        self._stf.watch_alert(self._devices['wda_url'])
        self._stf.stop_ios_app(self._devices['wda_url'], WeakNetworkConfig.IOS_APP_BUNDLE_ID)
        self._stf.launch_ios_app(self._devices['wda_url'], WeakNetworkConfig.IOS_APP_BUNDLE_ID)
        timeout = 5 * 60
        t1 = time.time()
        while True:
            if time.time() - t1 > timeout:
                raise Exception('get_device_ip:{} timeout:{}'.format(self._devices['wda_url'], timeout))
            self._device_ip = self._stf.get_device_ip(self._devices['wda_url'], self._platform)
            if self._device_ip:
                # 弱网断网现在是192.168.0 如果网段变化则需要修改下面的逻辑
                if self._device_ip.startswith('192.168.0'):
                    self._set_auth()
                    return True
                else:
                    return False

    def _disconnect_ios(self):
        self._stf.stop_ios_app(self._devices['wda_url'], WeakNetworkConfig.IOS_APP_BUNDLE_ID)
        self._stf.launch_ios_app(self._devices['wda_url'], WeakNetworkConfig.IOS_APP_BUNDLE_ID, args=['disconnect'])

    def _set_auth(self):
        url = "{host}{uri}".format(host=WeakNetworkConfig.ATC_HOST,
                                   uri=WeakNetworkConfig.ATC_AUTH_URI.format(self._device_ip))
        r = requests.post(url)
        try:
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    def set_net_config(self, config_json):
        """
        :param config_json: 弱网配置参数
        :return: True if successful
        """
        url = "{host}{uri}".format(host=WeakNetworkConfig.ATC_HOST,
                                   uri=WeakNetworkConfig.ATC_SHAPE_URI.format(self._device_ip))
        r = requests.post(url, json=config_json)
        try:
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False


if __name__ == '__main__':
    token = "24dc77b46c7542a28cc74888aed16d15fc0d0d3077ed48e5b68956e2668eef27"
    sft_url = "http://10.12.35.2:8086"
    config = WeakNetworkConfig("2834d69c9ee8c9c02280d7d8828697cde1920cd6", stf_url=sft_url, sft_token=token)
    config.connect_wifi()
