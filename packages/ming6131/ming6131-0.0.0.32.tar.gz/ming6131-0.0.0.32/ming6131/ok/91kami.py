
import time
import requests
import hashlib
class obj:
    def __init__(self,AppId,AppSecret,token):
        self.AppId = AppId
        self.AppSecret = AppSecret
        self.token = token
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'ApiVersion': '1'
        }
    def post(self,url,data,params):
        data['sign'] = self.get_sign(params, self.AppSecret)
        res = requests.post(url=url, data=data, headers=self.headers)
        res = res.json()
        return res

    def get_card(self,
                 cpkId,                 # 卡种Id
                 num=1,                   # 提卡数量
                 handPickOrderId=None,       # 接入方订单编号
                 buyer=None,                 # 买家名称
                 buildCpd=False,              # 生成完整卡券提取链接
                 usePriority=False,           # 优先出库标识为“优先出售”的卡密，默认True
                 ):

        t = int(time.time())
        if not handPickOrderId:
            handPickOrderId = str(t)

        # api业务参数
        params = []
        data = {}
        item_dic = {"timestamp":t, "cpkId": cpkId, "num": num, "handPickOrderId": handPickOrderId, "buyer": buyer, "buildCpd": buildCpd, "usePriority": usePriority}
        for k,v in item_dic.items():
            if v:
                params.append(f'{k}{v}')
                data[k] = v


        url = 'http://gw.api.agiso.com/acpr/CardPwd/HandPick'

        res = self.post(url, data, params)["Data"]["CardPwdArr"]
        res_data = {"col": ["卡号", "密码"]}
        index = 0
        for item in res:
            res_data[index] = [item["c"], item["p"]]
            index += 1
        return res_data

    def get_list(self,
        pageIndex=None,      # 页码默认 1
        pageSize=None,       # 默认100，最大100
        filterName=None,     # 卡种名称，支持模糊匹配
        classId=None):       # 卡种分类Id

        count = pageIndex + 1 if pageIndex else 2
        res_data = {"cols": ["ID", "类型", "名称","库存","已用数量","总数量","创建时间"]}
        index = 0
        start = pageIndex
        if not pageIndex and not pageSize and not filterName and not classId:
            start = 1
            count = 10000

        pageIndex = 1 if not pageIndex else pageIndex
        pageSize = 100 if not pageSize else pageSize
        start = pageIndex if not start else start

        for pageIndex in range(start,count):

            t = int(time.time())
            # api业务参数
            params = []
            data = {}
            item_dic = {"timestamp": t, "pageIndex": pageIndex, "pageSize": pageSize, "filterName": filterName, "classId": classId}
            for k, v in item_dic.items():
                if v:
                    params.append(f'{k}{v}')
                    data[k] = v


            url = 'http://gw.api.agiso.com/acpr/CardPwd/GetList'
            res = self.post(url, data,params)['Data']['List']
            card_type_dic = {700: "循环卡", 800: "套卡", 820: "唯一卡", 840: "重复卡", 850: "图片卡"}
            for item in res:
                IdNo = item["IdNo"]                         # Id
                CardType = card_type_dic[item["CardType"]]  # 卡种类型
                Title = item["Title"]                       # 卡种名称
                RemainingCount = item["RemainingCount"]     # 库存
                UsedCount = item["UsedCount"]               # 已用数量
                TotalCount = item["TotalCount"]             # 总数量
                CreateTime = item["CreateTime"]             # 创建时间
                res_data[index] = [IdNo, CardType, Title, RemainingCount, UsedCount, TotalCount, CreateTime]
                index += 1

            if index % pageSize != 0:
                break
        return res_data

    def get_sign(self,arge,AppSecret):

        # 对所有API请求参数（包括公共参数和业务参数，但除去sign参数和byte[]类型的参数），
        # 根据参数名称的ASCII码表的顺序排序。如：foo = 1, bar = 2, foo_bar = 3, foobar = 4
        # 排序后的顺序是bar = 2, foo = 1, foo_bar = 3, foobar = 4。
        # 将排序好的参数名和参数值拼装在一起，根据上面的示例得到的结果为：bar2foo1foo_bar3foobar4。
        # 把拼装好的字符串采用utf - 8编码，
        # 在拼装的字符串前后加上app的secret后，使用MD5算法进行摘要，如：md5(secret + bar2foo1foo_bar3foobar4 + secret)

        arge = sorted(arge)
        x = AppSecret + ''.join(arge) + AppSecret
        md5_arge = self.get_md5(x)
        return md5_arge

    def get_md5(self,x):
        m = hashlib.md5()
        m.update(x.encode("utf-8"))
        x = m.hexdigest()
        return x

'''
AppId = '-----'
AppSecret = '-----'
token = '-----'

kami = obj(AppId,AppSecret,token)

res = kami.get_list(filterName="UG")
#res = kami.get_card(77288)

print(res)

'''


