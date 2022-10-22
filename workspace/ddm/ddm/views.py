from django.shortcuts import render
from django.http import HttpRequest
from ddm.models import BoardSelling,BoardFile,BoardMaincategory, BoardMidcategory, BoardSubcategory,Member
from collections import Counter

def letter(request):
    return render(request,'letter.html')

def index(request):
    checkNum = 0
    recentlist=[]
    re_file=[]
    recent = BoardSelling.objects.filter(board_status =0).order_by('-upload_time')
    for i in recent:
        recentlist.append(i)
        checkNum += 1
        if checkNum == 5:
            break;
    print('-------------------최신글 5개 ------------------------')
    print(recentlist)
    for j in recentlist:
        print(j)
        board_idx = j.bs_idx
        re_file.append(BoardFile.objects.filter(upload_id = board_idx))
        print(re_file)

    main_cate = []
    board_list = BoardSelling.objects.all()
    for k in board_list:
        print(k)
        print('-------------------존재하는 maincate------------------------')
        num = k.board_maincategory_idx
        main_cate.append(num)
        print(main_cate)
    
    board_file = []
    
    for l in board_list:
        num = l.bs_idx
        board_file.append(BoardFile.objects.filter(upload_id = num))
    print('-------------------보드파일------------------------')
    print(board_file)
    count_items = Counter(main_cate)
    print(count_items)
    max_items = count_items.most_common(n=1)

    context = {
        'r' : recentlist,
        'rf' : re_file,
        'bl' : board_list,
        'c' : max_items,
        'bf' : board_file,
    }
        


    return render(request, 'index.html',context)

def category(request):
    main = BoardMaincategory.objects.all()
    mid = BoardMidcategory.objects.all()
    sub = BoardSubcategory.objects.all()
    board = BoardSelling.objects.all()
    boardFile= BoardFile.objects.all()

    if request.GET.get('recent') == '1':
            board = board.order_by('-upload_time')
    elif request.GET.get('rowprice') == '1':
        board = board.order_by('price')
    elif request.GET.get('highprice') == '1':
        board = board.order_by('-price')
    elif request.GET.get('most') == '1':
        board = board.order_by('-count')
    else:
        pass
    context = {
        'main': main,
        'mid': mid,
        'sub': sub,
        'b' : board,
        'bf' : boardFile
    }

    return render(request, 'category.html',context)


def cate(request:HttpRequest):
    boardlist = []
    boardfile = []
    d = []
    # 값이 없을 시 int로 받으면 오류발생
    # 그래서 형변환 없이 string형태로 받아옴
    mn = request.GET.get('main_cate')
    md = request.GET.get('mid_cate')
    sb = request.GET.get('sub_cate')
    print('-------------------------------------------------')
    print(mn)
    print(md)
    print(sb)
    # 메인 카테고리 값 입력 안했을때
    
    if mn == '':
        # 전체 필터 적용
        # 판매중인 게시글 모두 가져옴
        board = BoardSelling.objects.filter(board_status = 0)
        main_cate = BoardMaincategory.objects.all()
        mid_cate = BoardMidcategory.objects.all()
        sub_cate = BoardSubcategory.objects.all()
        for i in board:
            boardlist.append(i)
            no = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=no))
            print(no)
        for j in boardfile:
            print('-------------------------------------------------------------')
            print(j)
            e = j[0]
            print(e)
            d.append(e)
        if request.GET.get('recent') == '1':
            board = board.order_by('-upload_time')
        elif request.GET.get('rowprice') == '1':
            board = board.order_by('price')
        elif request.GET.get('highprice') == '1':
            board = board.order_by('-price')
        elif request.GET.get('most') == '1':
            board = board.order_by('-count')
        else:
            pass
        context = {
            'b' : board,
            'bf' : d,
            'main' : main_cate,
            'mid' : mid_cate,
            'sub' : sub_cate,
        }
        return render(request, 'cate.html',context)
    
    # 메인은 입력하고 
    # 중간 카테고리 값 입력 안했을 때 
    elif md == '':
        main = int(mn)
        # 메인필터만 적용
        # 메인 카테고리값을 적용시키고 게시글을 가져옴
        board = BoardSelling.objects.filter(board_status = 0,board_maincategory_idx = int(mn))
        main_cate = BoardMaincategory.objects.all()
        mid_cate = BoardMidcategory.objects.all()
        sub_cate = BoardSubcategory.objects.all()
        for i in board:
            boardlist.append(i)
            no = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=no))
            print(no)
        for j in boardfile:
            print('-------------------------------------------------------------')
            print(j)
            e = j[0]
            print(e)
            d.append(e)
        if request.GET.get('recent') == '1':
            board = board.order_by('-upload_time')
        elif request.GET.get('rowprice') == '1':
            board = board.order_by('price')
        elif request.GET.get('highprice') == '1':
            board = board.order_by('-price')
        elif request.GET.get('most') == '1':
            board = board.order_by('-count')
        else:
            pass
        context = {
            'b' : board,
            'bf' : d,
            'main' : main_cate,
            'mid' : mid_cate,
            'sub' : sub_cate,
            'm1' : main,
        }
        return render(request, 'cate.html',context)
    # 서브 카테고리 값 입력 안했을 때
    elif sb == '':
        print(sb)
        main = int(mn)
        mid = int(md)
        # 메인,중간 필터까지 적용
        board = BoardSelling.objects.filter(board_status = 0,board_maincategory_idx = int(mn),board_midcategory_idx = int(md))
        print("나왔졍")
        main_cate = BoardMaincategory.objects.all()
        mid_cate = BoardMidcategory.objects.all()
        sub_cate = BoardSubcategory.objects.all()
        for i in board:
            boardlist.append(i)
            no = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=no))
            print(no)
        for j in boardfile:
            print('-------------------------------------------------------------')
            print(j)
            e = j[0]
            print(e)
            d.append(e)
        if request.GET.get('recent') == '1':
            board = board.order_by('-upload_time')
        elif request.GET.get('rowprice') == '1':
            board = board.order_by('price')
        elif request.GET.get('highprice') == '1':
            board = board.order_by('-price')
        elif request.GET.get('most') == '1':
            board = board.order_by('-count')
        else:
            pass
        context = {
            'b' : board,
            'bf' : d,
            'main' : main_cate,
            'mid' : mid_cate,
            'sub' : sub_cate,
            'm1' : main,
            'm2' : mid,
        }
        return render(request, 'cate.html',context)
    else:
        # 모두 카테고리 입력했을때
        # 정수형으로 형변환 해주고
        main = int(mn)
        mid = int(md)
        sub = int(sb)
        # 필터 적용 후 가져옴
        board = BoardSelling.objects.filter(board_maincategory_idx=main,board_midcategory_idx=mid,board_subcategory_idx=sub,board_status = 0)
        main_cate = BoardMaincategory.objects.all()
        mid_cate = BoardMidcategory.objects.all()
        sub_cate = BoardSubcategory.objects.all()
        for i in board:
            boardlist.append(i)
            no = i.bs_idx
            boardfile.append(BoardFile.objects.filter(upload=no))
            print(no)
        for j in boardfile:
            print('-------------------------------------------------------------')
            print(j)
            e = j[0]
            print(e)
            d.append(e)
        if request.GET.get('recent') == '1':
            board = board.order_by('-upload_time')
        elif request.GET.get('rowprice') == '1':
            board = board.order_by('price')
        elif request.GET.get('highprice') == '1':
            board = board.order_by('-price')
        elif request.GET.get('most') == '1':
            board = board.order_by('-count')
        else:
            pass
        context = {
            'b' : board,
            'bf' : d,
            'main' : main_cate,
            'mid' : mid_cate,
            'sub' : sub_cate,
            'm1' : main,
            'm2' : mid,
            'm3' : sub,
        }
        return render(request, 'cate.html',context)

def banner_cate(request):
    board = BoardSelling.objects.get(BoardMaincategory=int(request.GET.get('no')))

    context = {
        'b' : board
    }

    return render(request,'board/category.html',context)


def search(request:HttpRequest):
    
    main = BoardMaincategory.objects.all()  # 대 카테고리
    mid = BoardMidcategory.objects.all()    # 중 카테고리
    sub = BoardSubcategory.objects.all()    # 소 카테고리
    board = BoardSelling.objects.filter(title__contains=request.GET.get('search'))      # 보드 셀링

    boardList = []
    for i in board:         # 필터링한 검색결과의 게시물번호로 게시물 파일(img)를 뽑아냄.
        board_file = BoardFile.objects.filter(upload_id = i.bs_idx)
        boardList.append(board_file[0])     # 리스트[0]번째 대표 이미지를 담아냄.
    
    context = {
        'main': main,
        'mid': mid,
        'sub': sub,
        'b' : board,
        'bf' : boardList
    }

    return render(request, 'category.html',context)
