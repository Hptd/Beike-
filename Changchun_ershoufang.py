import requests
from lxml import etree
import re
import openpyxl


class ChangchunErshoufangInformation(object):
    def __init__(self):
        self.page = 1
        self.url = f"https://cc.ke.com/ershoufang/pg{self.page}/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

    def beike_information(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet["A1"].value = "标题"
        sheet["B1"].value = "总价"
        sheet["C1"].value = "元/平米"
        sheet["D1"].value = "房屋面积"
        sheet["E1"].value = "小区名称"
        sheet["F1"].value = "所在区域"
        sheet["G1"].value = "房屋类型"
        sheet["H1"].value = "房屋楼层"
        sheet["I1"].value = "抵押信息"
        sheet["J1"].value = "交易权属"
        sheet["K1"].value = "房屋用途"

        column = 2
        for page in range(1, 1001):
            print(f"正在获取第{page}页数据.")
            ershoufang_result_src = []
            resp = requests.get(self.url, headers=self.header)
            main_tree = etree.HTML(resp.text)
            house_url_list = main_tree.xpath("/html/body/div[1]/div[4]/div[1]/div[4]/ul//div[1]/div[1]/a/@href")
            for src in house_url_list:
                ershoufang = src[18:28]
                if ershoufang == "ershoufang":
                    ershoufang_result_src.append(src)
                else:
                    continue
            print(f"第{page}页共有{len(ershoufang_result_src)}个数据.")
            for href in ershoufang_result_src:
                resp_two = requests.get(href)
                tree_two = etree.HTML(resp_two.text)

                title_l = tree_two.xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/h1/@title")
                title = title_l[0]
                price_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div/span[1]/text()")
                price = price_l[0] + "万"
                mean_price_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span/text()")
                mean_price = mean_price_l[0] + "元/平米"
                # 房屋面积
                acreage_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[3]/div[3]/div[1]/text()")
                acreage = acreage_l[0]
                # 小区名称
                xiaoqu_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[4]/div[1]/a[1]/text()")
                xiaoqu = xiaoqu_l[0]
                # 房屋所在区域
                area_l = tree_two.xpath("/html/body/div[1]/div[4]/div[1]/div[2]/div[4]/div[2]/span[2]/a[1]/text()")
                area = area_l[0]
                # 房屋类型
                house_type_l = tree_two.xpath("/html/body/div[1]/div[5]/div[1]/div/div/div[1]/div[2]/ul/li[1]/text()")
                house_type = re.sub('\s+', '', house_type_l[1]).strip()
                # 所在楼层
                house_flor_l = tree_two.xpath("/html/body/div[1]/div[5]/div[1]/div/div/div[1]/div[2]/ul/li[5]/text()")
                house_flor = re.sub('\s+', '', house_flor_l[1]).strip()
                # 抵押信息
                house_pledge_l = tree_two.xpath("/html/body/div[1]/div[5]/div[1]/div/div/div[2]/div[2]/ul/li[7]/span[2]/text()")
                house_pledge = re.sub('\s+', '', house_pledge_l[0]).strip()
                # 交易权属
                house_power_l = tree_two.xpath("/html/body/div[1]/div[5]/div[1]/div/div/div[2]/div[2]/ul/li[2]/text()")
                house_power = re.sub('\s+', '', house_power_l[0]).strip()
                # 房屋用途
                house_use_l = tree_two.xpath("/html/body/div[1]/div[5]/div[1]/div/div/div[2]/div[2]/ul/li[4]/text()")
                house_use = re.sub('\s+', '', house_use_l[0]).strip()

                for cow in "ABCDEFGHIJK":
                    cell_name = str(cow) + str(column)
                    if cow == "A":
                        sheet[cell_name].value = title
                    elif cow == "B":
                        sheet[cell_name].value = price
                    elif cow == "C":
                        sheet[cell_name].value = mean_price
                    elif cow == "D":
                        sheet[cell_name].value = acreage
                    elif cow == "E":
                        sheet[cell_name].value = xiaoqu
                    elif cow == "F":
                        sheet[cell_name].value = area
                    elif cow == "G":
                        sheet[cell_name].value = house_type
                    elif cow == "H":
                        sheet[cell_name].value = house_flor
                    elif cow == "I":
                        sheet[cell_name].value = house_pledge
                    elif cow == "J":
                        sheet[cell_name].value = house_power
                    elif cow == "K":
                        sheet[cell_name].value = house_use
                print(f"已经获取{column - 1}个数据")
                column += 1
            wb.save("贝壳网二手房数据集_1-1000页.xlsx")
        print("Done.")


if __name__ == '__main__':
    ChangchunErshoufangInformation().beike_information()
