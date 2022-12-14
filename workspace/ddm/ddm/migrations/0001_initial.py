# Generated by Django 3.1.3 on 2022-09-18 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMember',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=50, unique=True)),
                ('pw', models.CharField(max_length=50)),
                ('nickname', models.CharField(default='관리자', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BoardMaincategory',
            fields=[
                ('bcmn_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('main_category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BoardMidcategory',
            fields=[
                ('bcmd_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('mid_category', models.CharField(max_length=50)),
                ('main_idx', models.ForeignKey(db_column='main_idx', on_delete=django.db.models.deletion.CASCADE, related_name='ma_idx', to='ddm.boardmaincategory')),
            ],
        ),
        migrations.CreateModel(
            name='BoardSelling',
            fields=[
                ('bs_idx', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('conditions', models.IntegerField(default=0)),
                ('trade', models.IntegerField(default=0)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('price_propose', models.IntegerField(default=0)),
                ('contents', models.CharField(max_length=1000)),
                ('jjim_count', models.IntegerField(blank=True, default=0, null=True)),
                ('board_location', models.CharField(max_length=50, null=True)),
                ('upload_time', models.DateField()),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('board_status', models.IntegerField(default=0)),
                ('board_coordinate_x', models.CharField(blank=True, max_length=50, null=True)),
                ('board_coordinate_y', models.CharField(blank=True, max_length=50, null=True)),
                ('board_maincategory_idx', models.ForeignKey(db_column='board_mainCategory_idx', on_delete=django.db.models.deletion.CASCADE, related_name='b_ma_idx', to='ddm.boardmaincategory')),
                ('board_midcategory_idx', models.ForeignKey(db_column='board_midCategory_idx', on_delete=django.db.models.deletion.CASCADE, related_name='b_mi_idx', to='ddm.boardmidcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('mem_idx', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=50, unique=True)),
                ('pw', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=30, unique=True)),
                ('ph_num', models.CharField(max_length=20, unique=True)),
                ('email', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('join_date', models.DateField(auto_now_add=True)),
                ('alarm_keyword', models.CharField(max_length=300)),
                ('alarm_agree', models.IntegerField()),
                ('bs_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Metro',
            fields=[
                ('met_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Qna',
            fields=[
                ('q_idx', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('status', models.IntegerField()),
                ('datetime', models.DateField(blank=True, null=True)),
                ('admin_idx', models.ForeignKey(db_column='admin_idx', on_delete=django.db.models.deletion.CASCADE, related_name='ad_idx', to='ddm.adminmember')),
                ('member_idx', models.ForeignKey(db_column='member_idx', on_delete=django.db.models.deletion.CASCADE, related_name='memb_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='QnaMainCategory',
            fields=[
                ('qmc_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('main_category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bs_idx', models.ForeignKey(db_column='bs_idx', on_delete=django.db.models.deletion.CASCADE, related_name='b_idx', to='ddm.boardselling')),
                ('user_idx', models.ForeignKey(db_column='user_idx', on_delete=django.db.models.deletion.CASCADE, related_name='u_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('re_idx', models.AutoField(primary_key=True, serialize=False)),
                ('contents', models.CharField(max_length=500)),
                ('upload_time', models.DateField()),
                ('manner_1', models.IntegerField(blank=True, null=True)),
                ('manner_2', models.IntegerField(blank=True, null=True)),
                ('manner_3', models.IntegerField(blank=True, null=True)),
                ('manner_4', models.IntegerField(blank=True, null=True)),
                ('manner_5', models.IntegerField(blank=True, null=True)),
                ('r_bs_idx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm.boardselling')),
                ('r_receive_idx', models.ForeignKey(db_column='r_receive_idx', on_delete=django.db.models.deletion.CASCADE, related_name='rec_idx', to='ddm.member')),
                ('r_send_idx', models.ForeignKey(db_column='r_send_idx', on_delete=django.db.models.deletion.CASCADE, related_name='sen_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('re_idx', models.AutoField(primary_key=True, serialize=False)),
                ('cotegory', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=1000)),
                ('datetime', models.DateField(blank=True, null=True)),
                ('member_idx', models.ForeignKey(db_column='member_idx', on_delete=django.db.models.deletion.CASCADE, related_name='re_mem_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='QnaSubCategory',
            fields=[
                ('qsc_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('sub_category', models.CharField(max_length=50)),
                ('aq_mcategory', models.ForeignKey(db_column='aq_mcategory', on_delete=django.db.models.deletion.CASCADE, related_name='aq_idx', to='ddm.qnamaincategory')),
            ],
        ),
        migrations.CreateModel(
            name='QnaFile',
            fields=[
                ('qf_idx', models.AutoField(primary_key=True, serialize=False)),
                ('upload_route', models.CharField(max_length=500)),
                ('filename', models.CharField(max_length=500)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('qna_idx', models.ForeignKey(blank=True, db_column='qna_idx', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qna_idx', to='ddm.qna')),
            ],
        ),
        migrations.AddField(
            model_name='qna',
            name='qa_kind_idx',
            field=models.ForeignKey(db_column='qa_kind_idx', on_delete=django.db.models.deletion.CASCADE, related_name='qna_cate_idx', to='ddm.qnamaincategory'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('ms_idx', models.AutoField(primary_key=True, serialize=False)),
                ('contents', models.CharField(max_length=500)),
                ('datetime', models.DateField()),
                ('status', models.IntegerField()),
                ('m_receive_idx', models.ForeignKey(db_column='m_receive_idx', on_delete=django.db.models.deletion.CASCADE, related_name='rece_idx', to='ddm.member')),
                ('m_send_idx', models.ForeignKey(db_column='m_send_idx', on_delete=django.db.models.deletion.CASCADE, related_name='se_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='MemberFile',
            fields=[
                ('mf_idx', models.AutoField(primary_key=True, serialize=False)),
                ('upload_file', models.FileField(upload_to='img/')),
                ('filename', models.CharField(max_length=500)),
                ('content_type', models.CharField(max_length=128)),
                ('size', models.IntegerField()),
                ('member_idx', models.ForeignKey(blank=True, db_column='member_idx', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memf_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='Manner',
            fields=[
                ('mn_idx', models.AutoField(primary_key=True, serialize=False)),
                ('manner_1', models.IntegerField(blank=True, null=True)),
                ('manner_2', models.IntegerField(blank=True, null=True)),
                ('manner_3', models.IntegerField(blank=True, null=True)),
                ('manner_4', models.IntegerField(blank=True, null=True)),
                ('manner_5', models.IntegerField(blank=True, null=True)),
                ('user_idx', models.ForeignKey(db_column='user_idx', on_delete=django.db.models.deletion.CASCADE, related_name='uss_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='Lacal',
            fields=[
                ('lac_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('full_code', models.CharField(max_length=10)),
                ('metro_idx', models.ForeignKey(db_column='metr_idx', on_delete=django.db.models.deletion.CASCADE, related_name='mete_idx', to='ddm.metro')),
            ],
        ),
        migrations.CreateModel(
            name='BoardSubcategory',
            fields=[
                ('bsb_idx', models.IntegerField(primary_key=True, serialize=False)),
                ('sub_category', models.CharField(max_length=50)),
                ('mid_idx', models.ForeignKey(db_column='mid_idx', on_delete=django.db.models.deletion.CASCADE, related_name='mi_idx', to='ddm.boardmidcategory')),
            ],
        ),
        migrations.AddField(
            model_name='boardselling',
            name='board_subcategory_idx',
            field=models.ForeignKey(db_column='board_subCategory_idx', null=b'I01\n', on_delete=django.db.models.deletion.CASCADE, related_name='b_su_idx', to='ddm.boardsubcategory'),
        ),
        migrations.AddField(
            model_name='boardselling',
            name='buy_idx',
            field=models.ForeignKey(blank=True, db_column='buy_idx', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bu_idx', to='ddm.member'),
        ),
        migrations.AddField(
            model_name='boardselling',
            name='sell_idx',
            field=models.ForeignKey(db_column='sell_idx', on_delete=django.db.models.deletion.CASCADE, related_name='sel_idx', to='ddm.member'),
        ),
        migrations.CreateModel(
            name='BoardNotice',
            fields=[
                ('bn_idx', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('contents', models.CharField(max_length=500)),
                ('upload_time', models.DateField()),
                ('notice_count', models.IntegerField(blank=True, null=True)),
                ('admin_idx', models.ForeignKey(db_column='admin_idx', on_delete=django.db.models.deletion.CASCADE, related_name='adm_idx', to='ddm.member')),
            ],
        ),
        migrations.CreateModel(
            name='BoardFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(upload_to='img/')),
                ('filename', models.CharField(max_length=64)),
                ('content_type', models.CharField(max_length=128)),
                ('size', models.IntegerField()),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddm.boardselling')),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('al_idx', models.AutoField(primary_key=True, serialize=False)),
                ('contents', models.CharField(max_length=500)),
                ('alarm_time', models.DateField()),
                ('alarm_status', models.IntegerField(default=0)),
                ('user_idx', models.ForeignKey(db_column='user_idx', on_delete=django.db.models.deletion.CASCADE, related_name='us_idx', to='ddm.member')),
            ],
        ),
    ]
