

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
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *

def topicadd(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a title.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if not errors:
  	     title=request.POST['subject']
 	     content=request.POST['message']
	     idusr=request.POST['idusr']
             boolean = make_topic_object(title,int(idusr),content)
             if boolean :
              return HttpResponseRedirect('/betameta/Chatroom/')
    variables = RequestContext(request,{'errors' : errors })
    template = "gstudio/NewTopic.html"
    return render_to_response(template, variables)
 


    
