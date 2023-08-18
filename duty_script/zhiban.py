import csv
import requests
import time


def get_holiday_single(data):
    '''
    节假日判断单个日期版
    :param data: 日期参数20190803
    :return: (工作日-0, 法定节假日-1,节假日调休补班-2，休息日-3)
    '''
    url = r'http://api.goseek.cn/Tools/holiday?date='
    new_url = url + data
    r = requests.get(new_url)
    r.encoding = 'utf-8'
    # time.sleep(0.5)
    rjson = r.json()
    res = rjson["data"]
    return res


def get_schedule(origin_file, result_file, zhiban_person_wday, zhiban_person_wend):
    '''
    生成最终值班表
    :param origin_file: 源文件
    :param result_file: 结果文件
    :param zhiban_person_wday: 工作日值班人员
    :param zhiban_person_wend: 周末、节假日值班人员
    :return:
    '''
    with open(origin_file, encoding='gbk') as csvfile:
        rows = csv.reader(csvfile)
        headers = next(rows)
        print(headers)
        with open(result_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                row[1] = get_holiday_single(str(row[0]))
                if row[1] == 0 or row[1] == 2:
                    row[4] = next(zhiban_person_wday)
                else:
                    row[4] = next(zhiban_person_wend)
                print(row)
                writer.writerow(row)


if __name__ == '__main__':
    origin_file = r'E:\05-project_ding\zhiban\zhiban201908_.csv'
    result_file = r'E:\05-project_ding\zhiban\zhiban201908_zhiban2.csv'
    zhiban_person_wday = iter(['张三', '李四', '王五', '马六', '赵一', '钱二', '孙三', ] * 50)
    zhiban_person_wend = iter(['Tom', 'Jerry', 'Leo', 'Lily', 'John',] * 15)

    st_time = time.time()
    get_schedule(origin_file, result_file, zhiban_person_wday, zhiban_person_wend)

    sp_time = time.time() - st_time
    print('任务完成，花费时间{}s'.format(sp_time))
