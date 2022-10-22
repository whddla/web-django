from pickle import TRUE
from django.db import models

class Member(models.Model):
    mem_idx = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=50)
    pw = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    nickname = models.CharField(unique=True, max_length=30)
    ph_num = models.CharField(unique=True, max_length=20)
    email = models.CharField(max_length=100)
    birth_date = models.DateField()
    join_date = models.DateField(auto_now_add=True)
    alarm_keyword = models.CharField(max_length=300)
    alarm_agree = models.IntegerField()
    bs_count = models.IntegerField(default=0,null=True)

class MemberFile(models.Model):
    mf_idx = models.AutoField(primary_key=True)
    member_idx = models.ForeignKey(Member,on_delete=models.CASCADE,related_name='memf_idx', db_column='member_idx', blank=True, null=True)
    upload_file = models.FileField(upload_to='img/')
    filename = models.CharField(max_length=500)
    content_type = models.CharField(max_length=128)
    size = models.IntegerField()

class BoardMaincategory(models.Model):
    bcmn_idx = models.IntegerField(primary_key=True)
    main_category = models.CharField(max_length=50)


class BoardMidcategory(models.Model):
    bcmd_idx = models.IntegerField(primary_key=True)
    main_idx = models.ForeignKey(BoardMaincategory, db_column='main_idx',on_delete=models.CASCADE,related_name='ma_idx')
    mid_category = models.CharField(max_length=50)


class BoardSubcategory(models.Model):
    bsb_idx = models.IntegerField(primary_key=True)
    mid_idx = models.ForeignKey(BoardMidcategory, db_column='mid_idx',on_delete=models.CASCADE,related_name='mi_idx')
    sub_category = models.CharField(max_length=50)


class BoardSelling(models.Model):
    bs_idx = models.AutoField(primary_key=True)
    board_maincategory_idx = models.ForeignKey(BoardMaincategory, on_delete=models.CASCADE,related_name='b_ma_idx', db_column='board_mainCategory_idx')  # Field name made lowercase.
    board_midcategory_idx = models.ForeignKey(BoardMidcategory, on_delete=models.CASCADE,related_name='b_mi_idx', db_column='board_midCategory_idx')  # Field name made lowercase.
    board_subcategory_idx = models.ForeignKey(BoardSubcategory,null=TRUE ,on_delete=models.CASCADE,related_name='b_su_idx', db_column='board_subCategory_idx')  # Field name made lowercase.
    sell_idx = models.ForeignKey(Member, db_column='sell_idx',on_delete=models.CASCADE, related_name='sel_idx')
    buy_idx = models.ForeignKey(Member, db_column='buy_idx', blank=True, null=True ,on_delete=models.CASCADE, related_name='bu_idx')
    title = models.CharField(max_length=50)
    conditions = models.IntegerField(default=0)
    trade = models.IntegerField(default=0)
    price = models.IntegerField(blank=True, null=True)
    contents = models.CharField(max_length=1000)
    jjim_count = models.IntegerField(default=0, blank=True, null=True)
    board_location = models.CharField(max_length=50,null=True)
    upload_time = models.DateField()
    count = models.IntegerField(blank=True, null=True, default=0)
    board_status = models.IntegerField(default=0)
    board_coordinate_x = models.CharField(max_length=50, blank=True, null=True)
    board_coordinate_y = models.CharField(max_length=50, blank=True, null=True)


class BoardFile(models.Model):
    upload = models.ForeignKey(BoardSelling, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to='img/')
    filename = models.CharField(max_length=64)
    content_type = models.CharField(max_length=128)
    size = models.IntegerField()

class Message(models.Model):
    ms_idx = models.AutoField(primary_key=True)
    m_send_idx = models.ForeignKey(Member, db_column='m_send_idx',on_delete=models.CASCADE, related_name='se_idx')
    m_receive_idx = models.ForeignKey(Member, db_column='m_receive_idx',on_delete=models.CASCADE, related_name='rece_idx')
    contents = models.CharField(max_length=500)
    datetime = models.DateField()
    status = models.IntegerField()


class QnaMainCategory(models.Model):
    qmc_idx = models.IntegerField(primary_key=True)
    main_category = models.CharField(max_length=50)

class Qna(models.Model):
    q_idx = models.AutoField(primary_key=True)
    qa_kind_idx = models.ForeignKey(QnaMainCategory, on_delete=models.CASCADE, related_name='qna_cate_idx', db_column='qa_kind_idx')
    member_idx = models.ForeignKey(Member, db_column='member_idx',on_delete=models.CASCADE, related_name='memb_idx')
    content = models.CharField(max_length=1000)
    status = models.IntegerField()
    datetime = models.DateField(blank=True, null=True)


class QnaFile(models.Model):
    qf_idx = models.AutoField(primary_key=True)
    qna_idx = models.ForeignKey(Qna, on_delete=models.CASCADE,related_name='qna_idx', db_column='qna_idx', blank=True, null=True)
    upload_route = models.CharField(max_length=500)
    filename = models.CharField(max_length=500)
    size = models.IntegerField(blank=True, null=True)


class Reviews(models.Model):
    re_idx = models.AutoField(primary_key=True)
    r_send_idx = models.ForeignKey(Member, db_column='r_send_idx',on_delete=models.CASCADE,related_name='sen_idx')
    r_receive_idx = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='r_receive_idx',related_name='rec_idx')
    r_bs_idx = models.ForeignKey(BoardSelling, on_delete=models.CASCADE)
    contents = models.CharField(max_length=500)
    upload_time = models.DateField()
    manner_1 = models.IntegerField(blank=True, null=True)
    manner_2 = models.IntegerField(blank=True, null=True)
    manner_3 = models.IntegerField(blank=True, null=True)
    manner_4 = models.IntegerField(blank=True, null=True)
    manner_5 = models.IntegerField(blank=True, null=True)


class Manner(models.Model):
    mn_idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='uss_idx', db_column='user_idx')
    manner_1 = models.IntegerField(blank=True, null=True)
    manner_2 = models.IntegerField(blank=True, null=True)
    manner_3 = models.IntegerField(blank=True, null=True)
    manner_4 = models.IntegerField(blank=True, null=True)
    manner_5 = models.IntegerField(blank=True, null=True)


class Alarm(models.Model):
    al_idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey(Member,on_delete=models.CASCADE,related_name='us_idx', db_column='user_idx')
    contents = models.CharField(max_length=500)
    alarm_time = models.DateField()
    alarm_status = models.IntegerField(default=0)

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey(Member,on_delete=models.CASCADE,related_name='u_idx', db_column='user_idx')
    bs_idx = models.ForeignKey(BoardSelling,on_delete=models.CASCADE,related_name='b_idx', db_column='bs_idx')