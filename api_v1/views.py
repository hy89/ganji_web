import uuid
import django
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from api_v1.models import Company, Job


def get_token(request):
    """
    用户必须经过首页，才能得到csrf所需要的token值
    :param request:
    :return:
    """
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})


def company(request):
    """
    前后分离,公司信息的查询及返回,ajax请求/table/company?page=1&limit=10
    :param request: 请求
    :return: 返回公司相关信息的json格式数据
    """
    arg = request.GET
    current_page = arg.get('page')  # 当前页码
    limit = arg.get('limit')  # 限制条目数
    keyword = arg.get('keyword')  # 搜索关键字
    city = arg.get('city')  # 是否请求的是城市

    if keyword:
        # 按指定关键字进行查询
        all_c = Company.objects.filter(c_name__icontains=keyword, isdelete=False).order_by('pk')
    elif city:
        # 依据城市进行查询
        all_c = Company.objects.filter(isdelete=False, city=city).order_by('pk')
    else:
        # 直接进入页面，没有keyword
        all_c = Company.objects.filter(isdelete=False).order_by('pk')
    count = all_c.count()
    if count > 0:  # 有数据,返回数据
        code = 0
        # 创建分页对象
        paginator = Paginator(all_c, limit)
        # 得到当前页的数据,返回
        page = paginator.page(current_page)
        data = []
        for i, c in enumerate(page.object_list):
            item = {}
            item['id'] = i + 1
            item['c_name'] = c.c_name
            item['city'] = c.city
            item['social_code'] = c.social_code if c.social_code else '暂无'
            item['org_code'] = c.org_code if c.org_code else '暂无'
            item['reg_address'] = c.reg_address if c.reg_address else '暂无'
            item['c_address'] = c.c_address if c.c_address else '暂无'
            item['c_tel'] = c.c_tel if c.c_tel else '暂无'
            item['info_url'] = c.info_url if c.info_url else None
            item['pc_url'] = c.pc_url if c.pc_url else None
            item['cid'] = c.cid
            # 查看是否有招聘信息
            j = Job.objects.filter(cid=c.cid, isdelete=False)
            if len(j) > 0:
                item['recruit'] = True
            else:
                item['recruit'] = False
            data.append(item)
        resp = {"code": code, "count": count, "data": data}
    else:  # 没有数据,返回一句话
        code = 1
        msg = '没有符合条件的数据!'
        resp = {'code': code, 'msg': msg}
    return JsonResponse(resp)


def recruit(request):
    """
    处理请求对应公司的招聘职位数据
    :param request: 请求
    :return: 返回对应公司的招聘信息的json格式数据
    """
    arg = request.GET
    cid = arg.get('cid')
    # print(cid)
    current_page = arg.get('page')  # 当前页码
    limit = arg.get('limit')  # 限制条目数
    # 判断招聘表中是否有此cid,断定此公司有无招聘信息
    jobs = Job.objects.filter(isdelete=False, cid=cid)
    # print(jobs)
    count = jobs.count()
    if count > 0:
        # 根据cid在招聘表中查找对应的数据
        data = []
        code = 0
        # 创建分页对象
        paginator = Paginator(jobs, limit)
        # 得到当前页的数据,返回
        page = paginator.page(current_page)
        for i, j in enumerate(page.object_list):
            item = {}
            item['b_id'] = i + 1
            item['job_name'] = j.job_name if j.job_name else '暂无'
            item['job_address'] = j.job_address if j.job_address else '暂无'
            item['salary'] = j.salary if j.salary else '暂无'
            item['recruit_num'] = j.recruit_num if j.recruit_num else '暂无'
            item['edu'] = j.edu if j.edu else '暂无'
            item['update_time'] = j.update_time if j.update_time else '暂无'
            item['contact_person'] = j.contact_person if j.contact_person else '暂无'
            item['job_tel'] = j.job_tel if j.job_tel else '暂无'
            item['job_url'] = j.job_url if j.job_url else '暂无'
            item['id'] = j.id
            data.append(item)
        resp = {"code": code, "count": count, "data": data}
    else:
        code = 1
        msg = '该公司暂无招聘信息!'
        resp = {'code': code, 'msg': msg}
    return JsonResponse(resp)


def delete_c(request):
    """逻辑删除一条公司记录"""
    arg = request.GET
    cid = arg.get('cid')
    # 从公司表中找到对应的信息,然后逻辑删除
    c = Company.objects.filter(cid=cid, isdelete=False)
    if len(c) == 1:
        c[0].isdelete = True
        c[0].save()
        code = 0
        msg = '删除成功'
    else:
        msg = '操作异常'
        code = 1
    resp = {'code': code, 'msg': msg}
    return JsonResponse(resp)


def delete_j(request):
    """逻辑删除一条公司记录"""
    arg = request.GET
    id = arg.get('id')
    print(id)
    # 从公司表中找到对应的信息,然后逻辑删除
    j = Job.objects.filter(pk=id, isdelete=False)
    print(j)
    if len(j) == 1:
        j[0].isdelete = True
        j[0].save()
        code = 0
        msg = '删除成功'
    else:
        msg = '操作异常'
        code = 1
    resp = {'code': code, 'msg': msg}
    return JsonResponse(resp)


@transaction.atomic
def add_company(request):
    """添加新的公司及编辑已有公司"""
    arg = request.POST
    cid = arg.get('cid', None)
    if cid is None:  # 新公司
        c = Company()
        reg_address = arg.get('rec_pro') + arg.get('reg_city') + arg.get('reg_district') + arg.get('reg_detail')
        c_address = arg.get('rec_pro') + arg.get('rec_city') + arg.get('rec_district') + arg.get('rec_detail')
        c.cid = uuid.uuid1()  # 新的公司需要新的uuid
    else:  # 已存在的公司进行修改操作
        c = Company.objects.get(cid=cid)
        reg_address = arg.get('reg_detail')
        c_address = arg.get('rec_detail')
    sp = transaction.savepoint()
    try:
        c.c_name = arg.get('c_name')
        c.city = arg.get('city')
        c.reg_address = reg_address
        c.c_address = c_address
        c.c_tel = arg.get('c_tel')
        c.org_code = arg.get('org_code')
        c.social_code = arg.get('social_code')
        c.info_url = arg.get('info_url')
        c.pc_url = arg.get('pc_url')
        c.save()
        msg = '添加成功'
        transaction.savepoint_commit(sp)
    except Exception as e:
        msg = '添加失败'
        transaction.savepoint_rollback(sp)
    return JsonResponse({'msg': msg})


def company_info(request):
    """公司数据回显"""
    arg = request.GET
    cid = arg.get('cid')
    item = dict()
    try:
        c = Company.objects.get(cid=cid)  # cid是必然存在的
        item['c_name'] = c.c_name
        item['city'] = c.city
        item['social_code'] = c.social_code
        item['org_code'] = c.org_code
        item['reg_address'] = c.reg_address
        item['c_address'] = c.c_address
        item['c_tel'] = c.c_tel
        item['info_url'] = c.info_url
        item['pc_url'] = c.pc_url
        item['code'] = 0
    except Exception as e:
        item['code'] = 1
        item['msg'] = '数据获取异常'
    return JsonResponse(item)


def add_job(request):
    arg = request.POST
    print(arg)
    return JsonResponse({'msg': '成功'})
