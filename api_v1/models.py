from django.db import models


# Create your models here.
# class CompanyManager(models.Manager):
#     def create(self, city, c_name, social_code, reg_address, c_address, c_tel, info_url, pc_url):
#         company_obj = self.model()
#         # 属性赋值
#         company_obj.city = city
#         company_obj.c_name = c_name
#         company_obj.social_code = social_code
#         company_obj.reg_address = reg_address
#         company_obj.c_address = c_address
#         company_obj.c_tel = c_tel
#         company_obj.info_url = info_url
#         company_obj.pc_url = pc_url

# def get_queryset(self):
#     # 默认查询没有删除的公司信息
#     return super().get_queryset().filter(isdelete=False)


class Company(models.Model):
    # 逻辑主键
    cid = models.CharField(max_length=36, unique=True)
    # 城市
    city = models.CharField(max_length=10)
    # 公司名称
    c_name = models.CharField(max_length=60, null=True)
    # 统一社会代码
    social_code = models.CharField(max_length=30, null=True)
    # 组织机构代码
    org_code = models.CharField(max_length=10, null=True)
    # 注册地址
    reg_address = models.CharField(max_length=80, null=True)
    # 公司地址
    c_address = models.CharField(max_length=80, null=True)
    # 公司电话
    c_tel = models.CharField(max_length=50, null=True)
    # 信息来源
    info_url = models.CharField(max_length=80)
    # pc端数据来源
    pc_url = models.CharField(max_length=80, null=True)
    # 是否可以删除
    isdelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'company'

        # company = CompanyManager()


class Job(models.Model):
    # 逻辑外键,关联company表的逻辑主键cid,通过两者相等做联合查询
    cid = models.CharField(max_length=36)
    # 职位名称
    job_name = models.CharField(max_length=100, null=True)
    # 职位地址
    job_address = models.CharField(max_length=60, null=True)
    # 工资
    salary = models.CharField(max_length=30, null=True)
    # 招聘人数
    recruit_num = models.CharField(max_length=10, null=True)
    # 学历
    edu = models.CharField(max_length=10, null=True)
    # 更新时间
    update_time = models.CharField(max_length=25, null=True)
    # update_time = models.CharField(max_length=25, null=True)
    # 联系人
    contact_person = models.CharField(max_length=15, null=True)
    # 联系电话
    job_tel = models.CharField(max_length=50, null=True)
    # 职位链接
    job_url = models.CharField(max_length=150)
    # 是否可以删除
    isdelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'recruit'
