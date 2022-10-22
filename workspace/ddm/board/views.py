from datetime import datetime
import os
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.conf import settings
from ddm.models import BoardSelling,BoardFile,BoardMaincategory, BoardMidcategory, BoardSubcategory,Member,Wishlist
from django.core.paginator import Paginator # 장고에서 페이지네비게이션을 하기위해 만들어진 클래스.
import simplejson as json

# Create your views here.
def new(request:HttpRequest):
    try:
        request.session['login']
    except:
        return redirect('/member/login/')
    main = BoardMaincategory.objects.all()
    mid = BoardMidcategory.objects.all()
    sub = BoardSubcategory.objects.all()
    context ={
        'main' : main,
        'mid' : mid,
        'sub' : sub,
    }
    return render(request,'board/new.html',context)

def fileUpload1(request:HttpRequest):
    try:
        no = request.session['login']
    except:
        return redirect('/member/login/')
    if no != None:
        mem = Member.objects.get(mem_idx=no)
        print("----------------count---------------")
        print(mem.bs_count)
        count = mem.bs_count
        count += 1
        Member.objects.update(bs_count = count)
        print("----------------count---------------")
        sell_idx = Member.objects.filter(mem_idx=no)[0]
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        contents = contents.replace('\r\n','<br>')
        board_location = request.POST.get('location')
        x = request.POST.get('x')
        y = request.POST.get('y')
        conditions = int(request.POST.get('conditions'))
        price = int(request.POST.get('price'))
        trade = int(request.POST.get('trade'))
        bcmn_idx  = int(request.POST.get('main_cate'))
        bcmd_idx = int(request.POST.get('mid_cate'))
        bsb_idx = request.POST.get('sub_cate')
        if bsb_idx == '':
            board_maincategory = BoardMaincategory.objects.get(bcmn_idx=bcmn_idx)
            board_midcategory = BoardMidcategory.objects.get(bcmd_idx=bcmd_idx)
            nowtime= datetime.now() 
            upload = BoardSelling.objects.create(title=title,price=price,board_status=0,trade=trade,contents=contents,conditions=conditions ,board_location=board_location,sell_idx=sell_idx,board_maincategory_idx=board_maincategory,board_midcategory_idx=board_midcategory,upload_time=nowtime,board_coordinate_x=x,board_coordinate_y=y)
            files = request.FILES.getlist('files')

            for file in files:
                uf = BoardFile(upload=upload,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
                uf.save()

            files = BoardFile.objects.filter(upload=upload)

            context = {
                'c' : upload,
                'fs' : files
            }
            return redirect('/board/manage',context)
        elif bsb_idx != None:
            bsb_idx = int(bsb_idx)
            board_maincategory_idx = BoardMaincategory.objects.get(bcmn_idx=bcmn_idx)
            board_midcategory_idx = BoardMidcategory.objects.get(bcmd_idx=bcmd_idx)
            board_subcategory_idx = BoardSubcategory.objects.get(bsb_idx=bsb_idx)
            nowtime= datetime.now() 
            upload = BoardSelling.objects.create(title=title,price=price,board_status=0,trade=trade,contents=contents,conditions=conditions ,board_location=board_location,sell_idx=sell_idx,board_maincategory_idx=board_maincategory_idx,board_midcategory_idx=board_midcategory_idx,board_subcategory_idx=board_subcategory_idx,upload_time=nowtime,board_coordinate_x = x ,board_coordinate_y=y)
        #-----------------------------------------------------------------
            
            files = request.FILES.getlist('files')

            for file in files:
                uf = BoardFile(upload=upload,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
                uf.save()

            files = BoardFile.objects.filter(upload=upload)

            context = {
                'c' : upload,
                'fs' : files
            }
            return redirect('/board/manage',context)

def remove(request, idx):
    try:
        no = request.session['login']
    except:
        return redirect('/member/login/')
    mem = Member.objects.get(mem_idx=no)
    print("----------------count---------------")
    print(mem.bs_count)
    count = mem.bs_count
    count -= 1
    Member.objects.update(bs_count = count)
    board = BoardSelling.objects.get(bs_idx=idx)
    board.delete()
    return redirect('/board/manage/')


def update(request,idx):
    try:
        request.session['login']
    except:
        return redirect('/member/login/')
    main = BoardMaincategory.objects.all()
    mid = BoardMidcategory.objects.all()
    sub = BoardSubcategory.objects.all()
    board = BoardSelling.objects.get(bs_idx=idx)
    idx = board.bs_idx
    print('------------------------------------------')
    print(idx)
    files = BoardFile.objects.filter(upload_id = idx)
    print(files)
    print('------------------------------------------')
    if request.method =="POST":
        get_files = request.FILES.getlist('files')
        board.title = request.POST['title']
        board.contents = request.POST['contents']
        board.contents = board.contents.replace('\r\n','<br>')
        # board.board_location = request.POST['location']
        board.conditions = int(request.POST['conditions'])
        board.board_coordinate_x = request.POST['x']
        board.board_coordinate_y = request.POST['y']
        board.price = int(request.POST['price'])
        board.trade = int(request.POST['trade'])
        board.nowtime= datetime.now() 
        main_idx  = int(request.POST['main_cate'])
        mid_idx = int(request.POST['mid_cate'])
        sub_idx = request.POST['sub_cate']
        print('----------------sub----------------')
        if sub_idx == '':
            print('----------------sub----------------')
            board.board_maincategory_idx= BoardMaincategory.objects.get(bcmn_idx=main_idx)
            board.board_midcategory_idx = BoardMidcategory.objects.get(bcmd_idx=mid_idx)
            board.board_subcategory_idx = None
            for i in files:
                files.delete()
            for file in get_files:
                uf = BoardFile(upload=board,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
                uf.save()
            board.save()

            return redirect('/board/manage/')
        sub_idx = int(sub_idx)
        print(sub_idx)
        print('----------------hi----------------')
        board.board_maincategory_idx= BoardMaincategory.objects.get(bcmn_idx=main_idx)
        board.board_midcategory_idx = BoardMidcategory.objects.get(bcmd_idx=mid_idx)
        board.board_subcategory_idx = BoardSubcategory.objects.get(bsb_idx = sub_idx)
        print('--------------hi2------------------')
        for i in files:
            files.delete()
        for file in get_files:
            uf = BoardFile(upload=board,upload_file=file,filename=file.name,content_type=file.content_type,size=file.size)
            uf.save()
        board.save()

        return redirect('/board/manage/')
    context = {
        'main': main,
        'mid': mid,
        'sub': sub,
    }
    return render(request,'board/update.html',context)


def sell(request):
    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 2
    page = request.GET.get('page','1')# page 파라미터가 있으면 값을 가져오고 없으면 1을 반환하겟다..

    # 정산
    cost = 0 
    # 구매자도 같이 보내주기 그래야 구매자 이름뽑음 
    try:
        no = request.session['login']
    except:
        return redirect('/member/login/')
    boardfile = []
    # sell_idx = sesstion
    board = BoardSelling.objects.filter(sell_idx=no)
    for i in board:
        boardNo = i.bs_idx
        print(boardNo)
        boardfile.append(BoardFile.objects.filter(upload_id=boardNo))
        if i.board_status == 1:
            cost += i.price
        # print(b_file)
        print('------------------------------------------------------')
        # print(boardfile)
        # boardfile.append(b_file)
    print(boardfile)

    #페이징처리
    paginator = Paginator(board,MAX_LIST_CNT)
    # Paginator 객체 생성할때 리스트값이랑 한페이지당 띄울 글개수
    page_obj = paginator.get_page(page)
    # 해당페이지에 해당하는 글을 저장....
    
    #끝페이지.
    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    #페이지그룹의 블록...
    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1

    end_page = start_page + MAX_PAGE_CNT - 1
    context = {
        'b' : board,
        'bf' : boardfile,
        'cost' : cost,
        'list' : page_obj,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }

    return render(request,'board/sell.html',context)

def manage(request):

    try:
        sell_idx = Member.objects.get(mem_idx = int(request.session['login']))
    except:
        return redirect('/member/login/')


    boardList = BoardSelling.objects.filter(sell_idx=sell_idx).order_by()

    print('--------------------boardlist for문--------------------------')
    imagelist = []
    for b in range(len(boardList)):
        print(boardList[b])
        print('--------------------list--------------------------')
        # 게시글의 idx 목록
        list = boardList[b].bs_idx
        print(list,end='')
        print(" 번째 글입니다.")
        
        # 게시글 번호에 맞는 이미지
        try: 
            boardImage = BoardFile.objects.filter(upload_id=list)
            print(boardImage)
            image = boardImage[0]
            print(image)
            imagelist.append(image)
        except:
            print("사진 없슴둥")
        
        # for i in range(len(boardImage)):
        #     print('-----------------------boardImage for문 들어옴-------------------------')
        #     print(boardImage[i])
        #     if boardImage[i].upload_file != None:
        #         file = boardImage[i].upload_file
        #         print(file)
        #         continue
    print('-----------------------끝-------------------------')
    context = {
        'boardList' : boardList,
        'boardImage' : imagelist,
    }
    return render(request,'board/manage.html',context)

def buy(request):

    try:
        no = request.session['login']
    except:
        return redirect('/member/login/')

    boardfile = []
    board = BoardSelling.objects.filter(board_status=1, buy_idx = no)
    for i in board:
        boardNo = i.bs_idx
        print(boardNo)
        boardfile.append(BoardFile.objects.filter(upload_id=boardNo))
        # print(b_file)
        print('------------------------------------------------------')
        # print(boardfile)
        # boardfile.append(b_file)
    print(boardfile)

    context = {
        'b' : board,
        'bf' : boardfile,
    }

    return render(request,'board/buy.html',context)



def detail(request:HttpRequest):        # 판매상세페이지
    try:
        wishlist = Wishlist.objects.filter(user_idx=request.session['login'],bs_idx=int(request.GET.get('no')))
        wishlist = wishlist[0]
        selling = wishlist.bs_idx   # 위시리스트를 필터로 쿼리문 돌리면 그 안에 포린키로 연결된 테이블도 같이 넘어옴.
        # 같이 넘어온 테이블을 해당 컬럼명으로 불러올수있음.
        # 그래서 wishlist.bs_idx = BoardSelling 이기때문에 따로 BoardSelling 할필요없이 이걸 가져다 게시물을 뿌려주면됨.
        # 일단 여기까지 실행했다는거 자체가 해당 게시물을 찜했다는거니까 여기서 찜 ♥ 하트를 표시해줄 값을 날려야함.
        heart = True
    except:
        selling = BoardSelling.objects.get(bs_idx=int(request.GET.get('no')))
        # 찜목록이 아닌경우는 게시물을 쿼리문돌려서 가져와서 뿌려줘야함.
        heart = False

    no = selling.bs_idx # no = selling[0]
    count = selling.count + 1
    BoardSelling.objects.filter(bs_idx=int(request.GET.get('no'))).update(count = count)
    files = BoardFile.objects.filter(upload_id=no)

    context = { 
        'selling' : selling,
        'files' : files,
        'heart' : heart,
        'member' : selling.sell_idx,    # member object()
    }

    return render(request,'board/detail.html', context)

def heart(request:HttpRequest):
    selling = BoardSelling.objects.get(bs_idx = int(request.GET['no']))
    try:
        if 'True' == request.GET['heart']:
            Wishlist.objects.get(bs_idx = int(request.GET['no']), user_idx = request.session['login']).delete()
            selling.jjim_count = selling.jjim_count - 1
            selling.save()
            heart = False
        else :
            Wishlist.objects.create(bs_idx = selling, user_idx = Member.objects.get(mem_idx=request.session['login']))
            selling.jjim_count = selling.jjim_count + 1
            selling.save()
            heart = True
    except:
        print('찜 에러발생')
    context = {
        'heart' : heart,
        'jjim' : selling.jjim_count,
        }
    return HttpResponse(json.dumps(context), content_type="application/json")       
    # 이렇게 값을 주면 페이지 새로고침없이 값을 리턴할수 있음.
    # pip install simplejson        - 인스톨 해줘야함.
    # import simplejson as json     - import 해줘야함.

def purchase(request:HttpRequest):
    selling = BoardSelling.objects.get(bs_idx = int(request.GET['no']))
    sell = selling.sell_idx
    no = request.session['login']
    buy = Member.objects.get(mem_idx = no)

    if sell.mem_idx != no:          # 구매 누른 사람이 게시글 작성자와 같지 않으면.
        selling.buy_idx = buy       # 거래id 변경.
        selling.board_status = 1    # 거래중 표시 컬럼
        selling.save()
        result = True
    else :
        result = False
    context = {
        'result' : result,
    }
    
    print(context)
    return HttpResponse(json.dumps(context), content_type="application/json") 