#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 9:22
# @Author  : lj
# @File    : parse.py

def urlparse(url_string:str):
    '''url解析'''
    data = {
        'scheme':'',
        'netloc':'',
        'path':[],
        'query':[]
    }

    if url_string.startswith('https://'):
        data['scheme'] = 'https'
        url_string = url_string.replace('https://','')

    elif url_string.startswith('http://'):
        data['scheme'] = 'http'
        url_string = url_string.replace('http://', '')


    url_is_split_ = url_string.split('?',1)
    url_is_split_path = url_is_split_[0].split('/')

    data['netloc'] = url_is_split_path[0]

    for i in url_is_split_path[1:]:
        data['path'].append(i)

    query_path_list = url_is_split_[-1].split('?')

    query_list = query_path_list[-1].split('&')

    for i in query_list:
        v = i.split('=')
        data['query'].append([v[0],v[-1]])

    return data
if __name__ == '__main__':
    # url_string = 'https://www.amazon.es/product-reviews/B095NLTZNF/?OrderPlus.isNewOrder=2&isSyncVal=&isSyncValIsVirtual=&isSyncLogisticsOrder=&isPackOrder=&isDeliverOrder=&isOutOfStockOrder=&outOfStockOrderDay=&isSyncLogistics=&logisStatus=&isExpireOrder=&isWindControlOrder=&isShipmentOrderC=&isToDayOrder=&isResendOrderC=&noTrackOnlineDay=&quickPickType=&smtflag=&fbaFlag=&platformIdFbw=&shopeeAbnormal=&abnormalType=&cloudStatus=&isTuotou=&platformId=&getCompanyCloudStorageHtmlForJson=%5B%5D&supplierCompanyId_v=&orderBys%5B%5D=&postDta=%5B%5D&isshowordercombosku=2&title_Json=%7B%22title_salesRecordNumber%22%3A%22{order_number}%22%2C%22title_stocksku%22%3A%22%22%2C%22title_stockskuTitle%22%3A%22%22%2C%22title_countryCode%22%3A%22%22%2C%22title_province%22%3A%22%22%2C%22title_postCode%22%3A%22%22%2C%22title_surplus_delivery%22%3A%22%22%2C%22title_platformId%22%3A%22%22%7D&platformTracknumberSearchInput=&platformTracknumberSearchtextarea=&orderSearchHistory=&OrderLogisticsSearch=&failureYiSearch=&view-hidden=&statusButton=&Order.orderStatus=2&orderTypeButton=&labelMultipleChoiceWhere=cross&OrderPlus.isTrackOnline=&OrderSearch.fuzzySearchKey=Order.platformOrderId&OrderSearchFuSKey=a.platformOrderId&daysOperator=%3D&OrderSearch.fuzzySearchValue=&orderPageKey=c0451283d474f89286fdb174982adede&goPaypalRefundStatus=1&page=1&rowsPerPage=100&Order_isCloud=2&m=order&a=list&isNewOrderPage=1&post_tableBase=1&showError=undefined&pageListC=undefined&1=1'
    url_string = 'https://www.google.com/search?q=python+%E5%85%83%E7%BB%84%E6%9C%89%E5%BA%8F%E5%90%97&ei=usd-Y6jyHMmKhwON7Z6IDQ&ved=0ahUKEwiot_SY1MX7AhVJxWEKHY22B9EQ4dUDCA8&uact=5&oq=python+%E5%85%83%E7%BB%84%E6%9C%89%E5%BA%8F%E5%90%97&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECAAQHjoKCAAQRxDWBBCwAzoFCAAQogQ6BwgAEB4QogQ6CAghEMMEEKABSgQIQRgASgQIRhgAUKEIWJcoYLspaAZwAXgAgAFLiAHcBZIBAjExmAEAoAEByAEHwAEB&sclient=gws-wiz-serp'
    print(urlparse(url_string))