import requests
import json
import logging
logging.basicConfig(level=logging.INFO)

# 答案列表
Answers = [
    'WPS会员全文检索',
    'WPS会员数据恢复',
    'WPS会员图片转PDF',
    '100G',
    'WPS会员拍照转文字',
    '使用WPS会员修复',
    '金山PDF转WORD',
    '有，且无限次',
    'WPS全文检索功能',
    'WPS会员PDF转doc',
    'PDF转图片',
    'WPS图片转PDF插件',
    'WPS会员PDF转图片',
    '文档修复'
]

# 邀请好友列表
InvitedIds = [
    'V02SvlCVht41UTSNfXSSbYmOrconVo400a74926d002e51a8b5',
    'V02S2UBSfNlvEprMOn70qP3jHPDqiZU00a7ef4a800341c7c3b',
    'V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f',
    'V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828',
    'V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97',
    'V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579',
    'V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6',
    'V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96',
    'V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c',
    'V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1',
    'V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526',
    'V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c',
    'V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17',
    'V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f',
    'V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d'
]

class AutoClockIn(object):
    def __init__(self,wpdId=None,clockinId=None):
        self.wpdId = wpdId
        self.clockinId = clockinId
        self.headers = {"sid": self.clockinId}

    def auto_clockin(self) -> None:
        '''
        @summary 请求打卡问题，如果是多选则继续请求
        :return: None
        '''
        multi_select = 1
        logging.info('开始答题...')
        while(multi_select):
            res = requests.get(url='http://zt.wps.cn/2018/clock_in/api/get_question',
                               params={"member":"wps"},
                               headers=self.headers)
            data = json.loads(res.text)['data']
            logging.info(data)
            multi_select = data['multi_select']
            if(multi_select):
                continue
            else:
                logging.info('匹配答案中...')
                chooseList = data.get('options',[])
                for index,ans in enumerate(chooseList):
                    if ans in Answers:
                        # index为正确答案序号
                        logging.info('开始答题')
                        res_ans = requests.post(url='http://zt.wps.cn/2018/clock_in/api/answer?member=wps',
                                                json={"answer":index+1},
                                                headers=self.headers)
                        res_ans = json.loads(res_ans.text)
                        if(res_ans['result'] == 'ok'):
                            logging.info('答题正确,尝试进行打卡')
                            # 进行打卡
                            res_clockin = requests.get(url='http://zt.wps.cn/2018/clock_in/api/clock_in?member=wps',
                                                        headers=self.headers)
                            res_clockin = json.loads(res_clockin.text)
                            if(res_clockin['result'] == 'ok'):
                                logging.info("{0},{1}".format(res_clockin,'打卡成功!'))
                            else:
                                logging.info("{0},{1}".format(res_clockin,'打卡失败！'))
                                if(res_clockin['msg'] == '前一天未报名'):
                                    res_enroll = requests.get(url='http://zt.wps.cn/2018/clock_in/api/sign_up',
                                                              headers=self.headers)
                                    logging.info('进行报名,{0}'.format(res_enroll.text))
                        else:
                            logging.info('答题错误')
                            multi_select = 1
                        break
                    else:
                        logging.info('非正确答案或无法匹配答案，重试中...')

    def invited(self) -> None:
        '''
        @summary 打卡后邀请用户，则明天打卡可获得基础奖励*倍数
        :return: None
        '''
        invitedurl = 'http://zt.wps.cn/2018/clock_in/api/invite'
        for index,id in enumerate(InvitedIds):
            try:
                self.headers = {"sid":id}
                data = {"invite_userid":self.wpdId}
                res_inv = requests.post(url=invitedurl,json=data,headers=self.headers)
                if(res_inv.status_code == 200 and json.loads(res_inv.text)['result'] == 'ok'):
                    logging.info('邀请第{0}个好友成功！'.format(index))
            except Exception as e:
                continue

def wps_main(*args,**kwargs):
    ac = AutoClockIn("215609570","V02SK4wRb50dhJ40r748LAg8lXVohfQ00abe3c2c000cd9f0e2")
    ac.auto_clockin()
    ac.invited()

if(__name__ == '__main__'):
    wps_main()