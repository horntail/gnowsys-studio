# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.



from django.http import HttpResponse
from django.shortcuts import render_to_response
import ox
import os
from gstudio.models import *
from objectapp.models import *
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from demo.settings import *
from gstudio.methods import *

def video(request):
	api=ox.api.API("http://wetube.gnowledge.org/api")
	p=Objecttype.objects.get(title="Video")
	q=p.get_nbh['contains_members']
	api.signin({'username':'nero','password':'nihar'})
	if request.method == 'POST':
		clip = request.FILES.getlist("clip[]","")
		svid = request.POST.get("svid","")
		sub1 = request.POST.get("norm","")
		sub2 = request.POST.get("spe","")
		rating = request.POST.get("star1","")
		vidid = request.POST.get("vidid","")
		user = request.POST.get("user","")
		sub3 = request.POST.get("mydropdown","")
		favid=request.POST.get("favid","")
		favusr=request.POST.get("favusr","")
		fav=request.POST.get("fav","")
		full=request.POST.get("full","")
		if full!="" :
			variables= RequestContext(request,{'id':full})
			template="gstudio/transcript.html"
			return render_to_response(template,variables)
		if fav != "" :
			list1=[]
			t=Gbobject.objects.get(title=user)
			for each in t.get_nbh['has_favourite']:
				d=each.right_subject_id
				x=Gbobject.objects.get(id=d)
				list1.append(x)
			variables = RequestContext(request,{'vids':list1,'val':svid})
			template = "gstudio/video.html"
			return render_to_response(template, variables)	

		if rating :
        	 	rate_it(int(vidid),request,int(rating))
		
		if favid!="":
                        e=0
                        r = Objecttype.objects.get(title="user")
                        for each in r.get_nbh['contains_members']:
                                if favusr == each.title:
                                        e=1
                        if e==0 :
                                t=Gbobject()
                                t.title=favusr
                                t.slug=favusr
                                t.content=' '
                                t.status=2
                                t.save()
                                t.objecttypes.add(Objecttype.objects.get(title="user"))
                                t.save()
                        t=Gbobject.objects.get(title=favusr)
                        rel=Relation()
                        rt=Relationtype.objects.get(title="has_favourite")
                        rel.relationtype_id=rt.id
                        f1=Gbobject.objects.get(id=favid)
                        rel.left_subject_id=t.id
                        rel.right_subject_id=f1.id
                        rel.save()
			t.save()
		if clip != "":
			api.signup({'username':user,'password':'wetube'})
			save_file(clip)
			clipname = clip._get_name()
			i=0
			dirname = ""
			while clipname[i] != ".":
				dirname = dirname + clipname[i]
				i=i+1
			y=str(dirname)
			os.system("pandora_client scan")
			os.system("pandora_client sync")
			os.system("pandora_client upload")
			wclip= api.find({'sort': [{'key': 'title','operator': '+'}],'query': {'conditions': [{'key': 'title','value': y,'operator': '='}],'operator': '&'},'keys': ['id', 'title','user','duration','sourcedescription','created'],'range': [0,100]})
			for each in wclip['data']['items']:
				m=Gbobject()
				m.title=each['title'].lower()
				m.rurl="http://wetube.gnowledge.org/"+each['id']+'/480p.webm'
				m.slug=each['id']
				m.content=' '
				m.status=2
				m.save()
				m.objecttypes.add(Objecttype.objects.get(id=p.id))
				m.save()
				a=Attribute()
				a.attributetype=Attributetype.objects.get(title="posted_by")
				a.subject=m
				a.svalue=user
				a.save()
				a1=Attribute()
				a1.attributetype=Attributetype.objects.get(title="time_limit")
				a1.subject=m
				a1.svalue=each['duration']
				a1.save()
				a2=Attribute()
				a2.attributetype=Attributetype.objects.get(title="creation_day")
				a2.subject=m
				a2.svalue=each['created']
				a2.save()
				a3=Attribute()
				a3.attributetype=Attributetype.objects.get(title="source")
				a3.subject=m
				a3.svalue=each['sourcedescription']
				a3.save()
				a4=Attribute()
				a4.attributetype=Attributetype.objects.get(title="map_link")
				a4.subject=m
				l=each['sourcedescription']
				final=''
				for each in l:
					if each==" ":
						final=final+'+'
					else:
						final=final+each
				a4.svalue=final
				a4.save()
				m.save()
		if sub3 != "":
			if svid != "":
				if sub2 == "":
					vidon = Objecttype.objects.get(title="Video")
					vido_new = vidon.get_nbh['contains_members']
					vido = vido_new.filter(title__contains=svid)
					if sub3 == 'title':
						vido2 = vido.order_by(sub3)
					else:
						vido2 = sort_video(vido)
					variables = RequestContext(request,{'vids':vido2,'val':svid})
					template = "gstudio/video.html"
					return render_to_response(template, variables)
				else:
					vidon = Objecttype.objects.get(title="Video")
					vido_new = vidon.get_nbh['contains_members']
					vido = vido_new.filter(slug__contains=svid)
					if sub3 == 'title':
						vido2 = vido.order_by(sub3)
					else:
						vido2 = sort_video(vido)
					variables = RequestContext(request,{'vids':vido2,'val':svid})
					template = "gstudio/video.html"
					return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Video")
				vido_new = vidon.get_nbh['contains_members']
				if sub3 == 'title':
					vido=vido_new.order_by(sub3)
				else:
					vido=sort_video(vido_new)
				variables = RequestContext(request,{'vids':vido,'val':svid})
				template = "gstudio/video.html"
				return render_to_response(template, variables)
	r= api.find({'sort': [{'key': 'title','operator': '+'}],'query': {'conditions': [{'key': 'title','value': '','operator': ''}],'operator': '&'},'keys': ['id', 'title','user','created','duration','sourcedescription'],'range': [0,100]})
	s=r['data']['items']
	for each in s:
		flag=0
		for vid in q:
			if vid.title==each['title'].lower():
				flag=1
		if flag==0:
			m=Gbobject()
			m.title=each['title'].lower()
			m.rurl="http://wetube.gnowledge.org/"+each['id']+'/480p.webm'
			m.slug=each['id']
			m.content=' '
			m.status=2
			m.save()
			m.objecttypes.add(Objecttype.objects.get(id=p.id))
			m.save()
			a=Attribute()
			a.attributetype=Attributetype.objects.get(title="posted_by")
			a.subject=m
			a.svalue=each['user']
			a.save()
			a1=Attribute()
			a1.attributetype=Attributetype.objects.get(title="time_limit")
			a1.subject=m
			a1.svalue=each['duration']
			a1.save()
			a2=Attribute()
			a2.attributetype=Attributetype.objects.get(title="creation_day")
			a2.subject=m
			a2.svalue=each['created']
			a2.save()
			a3=Attribute()
			a3.attributetype=Attributetype.objects.get(title="source")
			a3.subject=m
			a3.svalue=each['sourcedescription']
			a3.save()
			a4=Attribute()
			a4.attributetype=Attributetype.objects.get(title="map_link")
			a4.subject=m
			l=each['sourcedescription']
			final=''
			for each in l:
				if each==" ":
					final=final+'+'
				else:
					final=final+each
			a4.svalue=final
			a4.save()
			m.save()
	svid=""
	q=p.get_nbh['contains_members']
	variables = RequestContext(request,{'vids':q,'val':svid})
	template = "gstudio/video.html"
	return render_to_response(template, variables)	

def save_file(file, path=""):
	filename = file._get_name()
	i=0
	dirname = ""
	while filename[i] != ".":
		dirname = dirname + filename[i]
		i=i+1
	x=str(filename[0]).upper()
	y=str(dirname)
	z = ''
	for each1 in y:
		if each1==" ":
			z=z+'\ '
		else:
			z=z+each1
	os.system("mkdir "+MEDIA_ROOTNEW+"/"+x+"/"+z)
    	fd = open('%s/%s/%s/%s' % (MEDIA_ROOTNEW, str(filename[0]).upper(), str(dirname), str(path) + str(filename)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()

def sort_video(video):
	a = []
	i = 0
	for each in video:
		a.append(each)
	while i < video.count()-1:
    		min = i
    		j = i+1
    		while j < video.count():
			if a[min].get_nbh['creation_day'][0] > a[j].get_nbh['creation_day'][0] :
            			min = j
        		j = j+1
		temp = a[i]
		a[i] = a[min]
		a[min] = temp
		i = i+1
	return a
