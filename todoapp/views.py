from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import TASK
from .forms import todoforms
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy

class TaskListView(ListView):
    model = TASK
    template_name ='home.html'
    context_object_name = 'obj1'

class TaskDetailView(DetailView):
    model = TASK
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model=TASK
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = TASK
    template_name ='delete.html'
    success_url= reverse_lazy('cbvhome')

def add(request):
    obj1=TASK.objects.all()
    if request.method=='POST':
        name=request.POST.get('name')
        priority = request.POST.get('priority')
        date=request.POST.get('date')
        obj=TASK(name=name,priority=priority, date=date)
        obj.save()

    return render(request,"home.html",{'obj1':obj1})

#    return render(request,"task.html")
def delete(request,taskid):

    task=TASK.objects.get(id=taskid)
    if request.method=="POST":
        task.delete()
        return redirect('/')

    return render(request,'delete.html',{"task":task})


def update(request,id):
    task=TASK.objects.get(id=id)
    form=todoforms(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'task':task,'form':form})
