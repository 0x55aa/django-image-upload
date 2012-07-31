# coding:utf-8

from django.shortcuts import render_to_response,get_object_or_404,render
from django.template import RequestContext
from image.forms import UploadImageForm
from image.models import Images
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect



MAX_FILE_SIZE = 7 * 2 ** 10	# 2 Mb
MIX_FILE_SIZE = 3 * 2 ** 10	# 1 Kb

#允许的文件类型
ACCEPTED_FORMATS = (
            "image/pjpeg",
            "image/jpeg",
            "image/png",
            )

def uploadimage(request):
    if request.method == 'POST':

        file = request.FILES[u'files[]']
        error = False
        #文件是否合法
        if file.size > MAX_FILE_SIZE:
            error = "maxFileSize"
        if file.size < MIX_FILE_SIZE:
            error = "minFileSize"
        if file.content_type not in ACCEPTED_FORMATS:
            error = "acceptFileTypes"
        if request.session["is_allow_upload"] == 0:
            error = "maxNumberOfFiles"
        else:
            request.session["is_allow_upload"] -= 1
                
        response_data = {
            "name": file.name,
            "size": file.size,
            "type": file.content_type,
            #"url":'static/'+image.image_url.url,
            }
        if error:
            response_data["error"] = error
            response_data = simplejson.dumps([response_data])
            return HttpResponse(response_data, mimetype='text/html')

        #保存文件
        image = Images(
            image_url = file,
            )
        image.save()
        response_data["url"] = 'static/'+image.image_url.url
        #删除链接
        response_data["delete_url"] = request.path + "del/" + str(image.id)

        response_data["delete_type"] = "GET"
        response_data = simplejson.dumps([response_data])
        response_type = "text/html"
        if "application/json" in request.META["HTTP_ACCEPT"]:
            response_type = "application/json"
        return HttpResponse(response_data, mimetype=response_type)

        
        
    else:
        #上传图片数量
        maxnumberoffiles = 3
        request.session["is_allow_upload"] = maxnumberoffiles
        print request.session["is_allow_upload"]
        return render_to_response('index.html',
                    {"open_tv":u'{%',"close_tv": u'%}',"maxfilesize": MAX_FILE_SIZE,
                     "minfilesize": MIX_FILE_SIZE,"maxnumberoffiles":maxnumberoffiles,},
                          context_instance=RequestContext(request))
    
def delimage(request,image_id):
    image = get_object_or_404(Images,id=image_id)
    print image_id
    image.delete()
    response_data = simplejson.dumps(True)
    return HttpResponse(response_data, mimetype="application/json")
        
