from random import randint
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from ddm.models import Member, MemberFile, BoardSelling, BoardFile,Reviews, Manner, Wishlist, Qna, QnaMainCategory
from datetime import datetime
from django.core.paginator import Paginator
#from cryptography.fernet import Fernet

#pip install coolsms_python_sdk
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

#비밀번호 암호화 복호화
#pip install cryptography
#key = Fernet.generate_key()
#key = b'yl2djXTGp9DoiIW6bzysZv2kSIE5y7NjqAlZF6lctDs='

def agreements (request):
    return render(request,'join/agreement.html')

def join (request:HttpRequest):
    alarm = request.POST.getlist('agree')

    if len(alarm) == 3 :
        alarm = 0
    else:
        alarm = 1

    content = {
        'alarm' : alarm,
        'month' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
    
    return render(request,'join/join.html', content)

def idDuplicateCheck (request):
    print("Ajax 들어옴?")
    userid = request.GET.get('userid')
    try:
        id_checked = Member.objects.get(id=userid)
    except:
        id_checked = None

    if id_checked is None:
        checkresult = "pass"
    else:
        checkresult = "fail"

    print("checkresult : ", checkresult)
    context = {
        'checkresult' : checkresult
    }

    return JsonResponse(context)

def nickDuplicateCheck (request):
    usernick = request.GET.get('usernick')
    try:
        nick_checked = Member.objects.get(nickname=usernick)
    except:
        nick_checked = None

    if nick_checked is None:
        checkresult = "pass"
    else:
        checkresult = "fail"

    print("checkresult : ", checkresult)
    context = {
        'checkresult' : checkresult
    }

    return JsonResponse(context)

def phnumDuplicateCheck (request):
    userphnum = request.GET.get('userphnum')
    try:
        phnum_checked = Member.objects.get(ph_num=userphnum)
        print(phnum_checked.ph_num)
    except:
        phnum_checked = None

    if phnum_checked is None:
        checkresult = "pass"
    else:
        checkresult = "fail"

    print("checkresult : ", checkresult)
    context = {
        'checkresult' : checkresult
    }

    return JsonResponse(context)

def selfPhoneCheck (request):
    userphnum = str(request.GET.get('userphnum'))
    resultCode = str(randint(1000, 10000))
    # set api key, api secret
    api_key = "NCSMURQ0QM47OCSV"
    api_secret = "S5ABL3TKGR4QV5EIPPA46QUAC6SQQ8DG"

    ## 4 params(to, from, type, text) are mandatory. must be filled
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = userphnum # Recipients Number '01000000000,01000000001'
    params['from'] = '01029821368' # Sender number
    params['text'] = '인증번호 : ' + resultCode + "\n위 번호를 정확하게 입력해주세요" # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
    context = {
        'resultcode' : resultCode
    }
    return JsonResponse(context)

'''
def encryptPw (pw:str):
    global key
    print('key : ', key)
    print('pw : ', pw)

    fernet = Fernet(key)
    print("fernet 까지 옴!")
    encrypt_pw = fernet.encrypt(pw.encode('utf-8'))
    print("복호화 성공함?")
    print(encrypt_pw.decode('utf-8'))

    return encrypt_pw
'''

def createMember(request:HttpRequest):
    #print('pw : ', request.POST.get("pw"))
    year = request.POST.get("year")
    month = request.POST.get("month")

    if month.__len__() <=1:
        month = '0' + month

    date = request.POST.get("date")
    day = year + '-' + month + '-' + date

    id = request.POST.get("id")
    pw = request.POST.get("pw")
    name = request.POST.get("name")
    nickname = request.POST.get("nick")
    ph_num = request.POST.get("phnum")
    email = request.POST.get("email")
    birth_date = datetime.strptime (day, "%Y-%m-%d")
    alarm_agree = request.POST.get('alarmagree')

    try:
        Member.objects.create(
            id = id,
            pw = pw,
            name = name,
            nickname = nickname,
            ph_num = ph_num,
            email = email,
            birth_date = birth_date,
            alarm_agree = alarm_agree
        )
    except Exception as e:
        print(e)
        return redirect('/member/join/')

    return render(request,'login.html')

def login(request:HttpRequest):
    id = request.GET.get("id")
    #result = request.GET.get("result")
    print('login/id : ', id)
    check = False
    if id == None:
        print('login/id : ', id)
        id = request.COOKIES.get("checkedid")
        if id != None:
            check = True

    print('login/check : ', check)
    context = {
        'id' : id,
        "check" : check,
    }

    return render(request,'login.html',context);

def checkLogin(request:HttpRequest):
    id = request.POST.get("id")
    pw = request.POST.get("pw")
    
    result = None

    try:
        member = Member.objects.get(id=id,pw=pw)
    except Exception as e:
        result = True
        return redirect('/member/login/?result=' + result)
    else:
        request.session['login'] = member.mem_idx
    
    response = render(request,'index.html')

    if result:
        checkedid = request.POST.get("checkedid")
        print("checkLogin/checkedid : ", checkedid)

        cookieid = request.COOKIES.get('checkedid')
        print("checkLogin/cookieid : ", cookieid)
        
        if checkedid != None:
            if cookieid == None:
                response.set_cookie("checkedid",id,max_age=60*60*48)
            elif cookieid != id:
                response.set_cookie("checkedid",id,max_age=60*60*48)
        else:
            if cookieid == id:
                response.delete_cookie("checkedid")

    return redirect('/')

def logout(request:HttpRequest):
    request.session.pop('login')
    return redirect('/')

def cal_temper (user_idx):

    manner = Manner.objects.get(user_idx=user_idx)

    temper = 36.5 +  (manner.manner_1*0.5) + (manner.manner_2*0.1) + (manner.manner_3*0.2) + (manner.manner_4*0.5) + (manner.manner_5*0.3)
    
    return round(temper, 2)

def mypage_sellProducts (request:HttpRequest):
    user_idx = request.session['login']
    boardlist = []
    boardfile = []
    filefirst = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    sell_products = BoardSelling.objects.filter(sell_idx=user_idx)

    if sell_products.exists():
        board_check = True
        for i in sell_products:
            boardlist.append(i)
            idx = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=idx))
        for i in boardfile:
            temp = i[0]
            filefirst.append(temp)
    else :
        board_check = False


    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(boardlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    context = {
        'member' : member,
        'member_img' : member_img,
        'boardList' : page_obj,
        'boardCheck' : board_check,
        'boardFile' : filefirst,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'mypage/mypage.html', context);

def mypage_buyProducts (request:HttpRequest):
    user_idx = request.session['login']
    boardlist = []
    boardfile = []
    fileFirst = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    sell_products = BoardSelling.objects.filter(buy_idx=user_idx)

    if sell_products.exists():
        board_check = True
        for i in sell_products:
            boardlist.append(i)
            idx = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=idx))
            print(idx)
        for i in boardfile:
            temp = i[0]
            fileFirst.append(temp)
    else :
        board_check = False


    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(boardlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    print("===============", board_check)

    context = {
        'member' : member,
        'member_img' : member_img,
        'boardList' : page_obj,
        'boardCheck' : board_check,
        'boardFile' : fileFirst,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'mypage/buyproducts.html', context);

def mypage_reviews (request:HttpRequest):
    user_idx = request.session['login']
    reviewlist = []
    userimges = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    # review = Reviews.objects.filter(r_send_idx=user_idx)

    # if review.exists():
    #     review_check = True
    #     for i in review:
    #         reviewlist.append(i)
    #         userimges.append(MemberFile.objects.get(member_idx=i.r_receive_idx))
    #         print(userimges)

    # else :
    #     review_check = False


    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(reviewlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    # print("===============", review_check)

    context = {
        'member' : member,
        'member_img' : member_img,
        'reviewList' : page_obj,
        'userImges' : userimges,
        'reviewCheck' : False,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'mypage/reviews.html', context);

def mypage_wishList (request:HttpRequest):
    user_idx = request.session['login']
    wishlist = []
    wishfile = []
    filefirst = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    wish = Wishlist.objects.filter(user_idx=user_idx)

    if wish.exists():
        wish_check = True
        
        for i in wish:
            idx = i.bs_idx.bs_idx
            wishlist.append(BoardSelling.objects.get(bs_idx=idx))
            wishfile.append(BoardFile.objects.filter(upload=idx))
        for i in wishfile:
            temp = i[0]
            filefirst.append(temp)
    else :
        wish_check = False


    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(wishlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    context = {
        'member' : member,
        'member_img' : member_img,
        'wishList' : page_obj,
        'wishCheck' : wish_check,
        'wishFile' : filefirst,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'mypage/wishes.html', context);

def one_on_one(request:HttpRequest):
    no = request.session['login']
    member = Member.objects.get(mem_idx=no)

    try:
        member_img= MemberFile.objects.get(member_idx=no)
    except:
        member_img = True

    qna = Qna.objects.filter(member_idx=no)
    qna_cate = QnaMainCategory.objects.all()

    context = {
        'member' : member,
        'member_img' : member_img,
        'qna' : qna,
        'qna_cate' : qna_cate,
    }

    return render(request, 'mypage/one-on-one_qt.html', context)
    
def mypage_alarm (request:HttpRequest):
    user_idx = request.session['login']

    member = Member.objects.get(mem_idx=user_idx)
    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    context = {
        'member' : member,
        'member_img' : member_img,
    }
    return render(request,'mypage/alarm.html', context)

def mypage_alarmSet (request:HttpRequest):
    user_idx = request.session['login']
    alarm = request.POST.get("alarmagree")

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member.alarm_agree = int(alarm)
        Member.save(member)
    except Exception as e:
        print("e")

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
        print(member_img)
    except:
        member_img = True

    context = {
            'member' : member,
            'member_img' : member_img,
    }
    return render(request,'mypage/alarm.html', context)

def mypage_update (request):
    user_idx = request.session['login']

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    context = {
        'member' : member,
        'member_img' : member_img,
    }
    return render(request, 'mypage/update.html', context)

def mypage_updateForm (request:HttpRequest):
    user_idx = request.session['login']
    result = None

    pw = request.POST.get("pw")

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
        print(member_img)
    except:
        member_img = True

    try:
        member = Member.objects.get(mem_idx=user_idx,pw=pw)
    except Exception as e:
        result = True
        
        context = {
        'member' : member,
        'member_img' : member_img,
        'result' : result
        }

        return render(request, 'mypage/update.html', context)
    else:
        context = {
            'member' : member,
            'member_img' : member_img,
        }
        return render(request, 'mypage/updateform.html', context)

def mypage_updateMember (request:HttpRequest):
    user_idx = request.session['login']
    member = Member.objects.get(mem_idx=user_idx)
    m_idx = member.mem_idx
    
    try :
        member_files = MemberFile.objects.filter(member_idx=user_idx)
    except Exception as e :
        get_files = request.FILES.getlist('files')
        for file in get_files:
            mf = MemberFile(member_idx=member,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
            mf.save()
    else:
        for i in member_files:
            member_files.delete()
        get_files = request.FILES.getlist('files')
        for file in get_files:
            mf = MemberFile(member_idx=member,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
            mf.save()

        member_img = MemberFile.objects.get(member_idx=m_idx)

    try:
        new_pw = request.POST.get("pw")
        if new_pw != '':
            member.pw = new_pw
            
        new_name = request.POST.get("name")
        if new_name != '':
            member.name = new_name

        new_nickname = request.POST.get("nick")
        if new_nickname != '':
            member.nickname = new_nickname
        
        new_email = request.POST.get("email")
        if new_email != '':
            member.email = new_email

        new_ph_num = request.POST.get("phnum")
        if new_ph_num != '':
            member.ph_num = new_ph_num

        Member.save(member)
    except Exception as e:
        print(e)
        return redirect('/member/mypage/updateform')

    member = Member.objects.get(mem_idx=user_idx)

    context = {
        'member' : member,
        'member_img' : member_img
    }

    return render(request, 'mypage/update.html', context)

def profile_products (request):
    user_idx = request.session['login']
    boardlist = []
    boardfile = []
    filefirst = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    m_temper = cal_temper(user_idx)

    sell_products = BoardSelling.objects.filter(sell_idx=user_idx)

    if sell_products.exists():
        board_check = True
        for i in sell_products:
            boardlist.append(i)
            idx = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=idx))
        for i in boardfile:
            temp = i[0]
            filefirst.append(temp)
    else :
        board_check = False

    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(boardlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    context = {
        'member' : member,
        'member_img' : member_img,
        'mTemper' : m_temper,
        'boardList' : page_obj,
        'boardCheck' : board_check,
        'boardFile' : filefirst,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'profiles/profile.html', context);

def profile_reviews (request):
    user_idx = request.session['login']
    reviewlist = []
    userimges = []

    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    m_temper = cal_temper(user_idx)

    review = Reviews.objects.filter(r_receive_idx=user_idx)

    if review.exists():
        review_check = True
        for i in review:
            reviewlist.append(i)
            userimges.append(MemberFile.objects.get(member_idx=i.r_send_idx))
            print(userimges)

    else :
        review_check = False


    #================ 페이징 ================

    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 30

    page = request.GET.get('page','1')

    paginator = Paginator(reviewlist,MAX_LIST_CNT)
    page_obj = paginator.get_page(page)

    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1
    end_page = start_page + MAX_PAGE_CNT - 1

    context = {
        'member' : member,
        'member_img' : member_img,
        'mTemper' : m_temper,
        'reviewList' : page_obj,
        'userImges' : userimges,
        'reviewCheck' : review_check,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'profiles/reviews.html', context);

def profile_manner (request:HttpRequest):
    user_idx = request.session['login']
    
    member = Member.objects.get(mem_idx=user_idx)

    try:
        member_img= MemberFile.objects.get(member_idx=user_idx)
    except:
        member_img = True

    m_temper = cal_temper(user_idx)

    manner = Manner.objects.get(user_idx=user_idx)

    context = {
        'member' : member,
        'member_img' : member_img,
        'mTemper' : m_temper,
        'manner' : manner,
    }
    return render(request,'profiles/manner.html', context);

def memberout (request):
    user_idx = request.session['login']

    member = Member.objects.get(mem_idx=user_idx)
    member.delete()
    request.session.pop('login')
    return redirect('/');

def one_on_one(request:HttpRequest):
    no = request.session['login']
    member = Member.objects.get(mem_idx=no)
    qna = Qna.objects.filter(member_idx=no)
    qnaList = []
    try:
        member_img= MemberFile.objects.get(member_idx=no)
        print(member_img)
    except:
        member_img = True
    print(qna.exists())
    for i in qna:
        qnaList.append(i)
        
    context = {
        'member' : member,
        'qnaList' : qnaList,
        'member_img' : member_img
    }

    return render(request, 'mypage/one-on-one_qt.html', context)