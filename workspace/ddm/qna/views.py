from dataclasses import dataclass
from distutils.command.upload import upload
import os
from xmlrpc.client import ResponseError
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.conf import settings
from ddm.models import  Qna,Member,QnaFile, QnaMainCategory
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def introduce(request):
    return render(request,'introduce_company.html')

def consumer(request):
    return render(request,'consumer_service.html')
    
def question(request):
    try:
        request.session['login']
    except:
        return redirect('/member/login')
    return render(request,'Question.html')

def fileUpload(request:HttpRequest):
    try:
        mem = request.session['login']
    except:
        return redirect('/member/login')

    qa_kind_idx = request.POST.get('qa_kind_idx')
    #파일같은경우는 FILES로 전달된다..
    content = request.POST.get('content')
    print(content) 
    # status = request.POST.get('status')

    dt=datetime.now()
    kind=QnaMainCategory.objects.get(qmc_idx=qa_kind_idx)

    mem = Member.objects.filter(mem_idx = mem) 
    mem1= mem[0]

    fileModel = Qna.objects.create(qa_kind_idx=kind,member_idx=mem1,content=content,datetime=dt,status=0)

    files = request.FILES.getlist('files')

    for file in files:
        print(file)
        uf = QnaFile(qna_idx=fileModel,upload_route=file,filename=file.name,size=file.size)
        uf.save()

    print(dt)


    print(fileModel)
    context = {
        'f' : fileModel,
    }


    return redirect('/member/mypage/qna')


# @login_message_required

def fileChange(request,no):
    print("들어옴")
    board = Qna.objects.get(q_idx=no)
    kind = QnaMainCategory.objects.all()
    mem = Member.objects.get(mem_idx=1)
    #no = board.q_idx
    files = QnaFile.objects.get(qna_idx = no)
    if request.method == "POST":
        board = Qna.objects.get(q_idx=no)
        #파일같은경우는 FILES로 전달된다..
        kind_idx = QnaMainCategory.objects.get(qmc_idx=int(request.POST['qa_kind_idx']))
        board.qa_kind_idx = kind_idx
        board.content = request.POST.get('content')
        get_files = request.FILES.getlist('files')

    # notice = Qna.objects.filter(q_idx = q_idx) 
    # notice = Member.objects.get(mem_idx = 1)
    
        # notice = Qna.objects.get(qa_kind_idx = qna) 
        # if board.qa_kind_idx != 0:
        #     notice.qa_kind_idx = board.qa_kind_idx
        # if board.content != "":
        #     notice.content = board.content
        
        files.delete()
        for file in get_files:
            uf = QnaFile(qna_idx=board,upload_route=file,filename=file.name,size=file.size)
            
            uf.save()
        board.save()

        return redirect('/member/mypage/qna')
    
    context = {
        'board' : board,
        'kind' : kind,
        'mem' : mem,
    }
    return render(request,'Question_fix.html', context)
    #     try:
    #         file.save()
    #         return redirect('/notice')
    #     except ValueError:
    #         return Response({"success":False,"msg":"사진이 없습니다."})
    # except ObjectDoesNotExist:
    #         return Response({"success":False,"msg":"게시글 없음."})




def fileDelete(request,no):
    print("no : ", no)
    board = Qna.objects.get(q_idx=no)
    print("====================================")
    print("board : ",board)
    board.delete()


    return redirect('/member/mypage/qna')
    

    #print(os.path.join(settings.MEDIA_ROOT,path))
    #print(os.path.exists(os.path.join(settings.MEDIA_ROOT,path)))
    # if os.path.exists(os.path.join(settings.MEDIA_ROOT,path)): # 해당 경로에 폴더가 있으면..
    #     try:
    #         os.rmdir(os.path.join(settings.MEDIA_ROOT,path))
    #         # rmdir - 비어있는 폴더 삭제
    #         # rmtree - 폴더와 그 안에 있는 파일 모두 삭제
    #     except:
    #         pass
        
    # return redirect('/')


# @receiver(post_delete,sender=QnaFile)
# def deleteFile(sender,**kwargs):
#     print('deleteFile')
#     files = kwargs.get('instance') 
#     files.upload_file.delete(save=False)
