from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Document, Task, CustomUser
from .forms import DocumentForm, CustomUserCreationForm, CustomLoginForm, TaskForm
from datetime import datetime
from django.core.paginator import Paginator
from django.http import Http404
from .fields import get_document_fields
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(request):
    if request.user.is_authenticated:
        # Sadece okunmamış görevleri say
        unread_tasks_count = Task.objects.filter(
            assigned_to=request.user
        ).exclude(
            is_read=request.user
        ).count()
    else:
        unread_tasks_count = 0
    return render(request, "index.html", {'unread_tasks_count': unread_tasks_count})


def care(request):
    return render(request, "care.html")


def document_list(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if request.user.is_superuser:
        documents = Document.objects.all()
    else:

        if request.user.department == "otomasyon":
            if request.user.yetki == "yetki1":
                documents = Document.objects.all()
            elif request.user.yetki == "yetki2":
                documents = Document.objects.filter(device_type__icontains="otomasyon")
            elif request.user.yetki == "yetki3":
                documents = Document.objects.filter(
                    device_type__icontains="otomasyon",
                    created_at__gte=datetime.now().date() - datetime.timedelta(days=30),
                )
            elif request.user.yetki == "yetki4":
                documents = Document.objects.filter(
                    device_type__icontains="otomasyon",
                    created_at__gte=datetime.now().date() - datetime.timedelta(days=7),
                )
            else:  # yetki5
                documents = Document.objects.none()
        else:
            documents = Document.objects.none()

    if query:
        documents = documents.filter(
            Q(shipyard__icontains=query)
            | Q(boat__icontains=query)
            | Q(engine_name__icontains=query)
        )

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            documents = documents.filter(date__range=[start_date, end_date])
        except ValueError:
            pass

    paginator = Paginator(documents, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "care/list.html",
        {
            "documents": page_obj,
            "query": query,
            "start_date": start_date,
            "end_date": end_date,
        },
    )


def document_delete(request, id):
    try:
        document = Document.objects.get(id=id)
        document.delete()
    except Document.DoesNotExist:
        raise Http404("Document not found.")
    return redirect("document_list")


def document_edit(request, id):
    try:
        document = Document.objects.get(id=id)
    except Document.DoesNotExist:
        raise Http404("Document not found.")

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect("document_list")
    else:
        form = DocumentForm(instance=document)

    context = {
        "form": form,
        "document": document,
    }
    return render(request, "care/edit.html", context)


def document_add(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("document_list")
    else:
        form = DocumentForm()

    fields = get_document_fields(form.instance)

    return render(
        request,
        "care/add.html",
        {"form": form, "fields": fields, "error": "Form is invalid!"},
    )


def document_view(request, id):
    document = Document.objects.get(id=id)
    fields = get_document_fields(document)

    context = {
        "document": document,
        "fields": fields,
    }

    return render(request, "care/detail.html", context)


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Grupları oluştur
            group_names = {
                "otomasyon": "Otomasyon",
                "yeni_insa": "Yeni İnşa",
                "bakim": "Bakım",
                "kalite": "Kalite",
                "diger": "Diğer",
            }

            # Kullanıcının departmanına göre grubu oluştur veya al
            group_name = group_names.get(user.department, "Diğer")
            group, created = Group.objects.get_or_create(name=group_name)

            # Kullanıcıyı gruba ekle
            user.groups.add(group)

            messages.success(request, "Kullanıcı başarıyla oluşturuldu.")
            return redirect("document_list")
        else:
            messages.error(request, "Kullanıcı oluşturulurken bir hata oluştu.")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def notifications(request):
    # Kullanıcıya atanan tüm görevleri getir
    tasks = Task.objects.filter(assigned_to=request.user)
    
    # Görevleri okundu olarak işaretle
    for task in tasks:
        task.is_read.add(request.user)
    
    return render(request, 'notifications.html', {'tasks': tasks})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('document_list')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def institutional(request):
    return render(request, 'institutional.html')


@login_required
def task_list(request):
    # Filtreleme parametrelerini al
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')
    assigned_to = request.GET.get('assigned_to', '')

    # Temel sorguyu oluştur
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    # Departman filtresi
    if department:
        tasks = tasks.filter(department=department)

    # Durum filtresi
    if status:
        tasks = tasks.filter(status=status)

    # Atanan kişi filtresi
    if assigned_to:
        tasks = tasks.filter(assigned_to__id=assigned_to)

    # Kullanıcı listesini al (filtre için)
    users = CustomUser.objects.all()

    # Form nesnesini oluştur
    form = TaskForm()

    context = {
        'tasks': tasks,
        'users': users,
        'selected_department': department,
        'selected_status': status,
        'selected_assigned_to': assigned_to,
        'form': form,  # Form nesnesini context'e ekle
    }
    return render(request, 'tasks/list.html', context)


@login_required
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Many-to-many ilişkileri kaydet

            # Görev atanan kişilere mail gönder
            for assigned_user in task.assigned_to.all():
                # Mail içeriğini hazırla
                subject = f'Yeni Görev Atandı: {task.project_name}'
                html_message = render_to_string('tasks/email/task_assigned.html', {
                    'task': task,
                    'assigned_user': assigned_user,
                    'created_by': request.user
                })
                plain_message = strip_tags(html_message)

                # Maili gönder
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email='noreply@saygielectric.com',
                    recipient_list=[assigned_user.email],
                    html_message=html_message,
                    fail_silently=False,
                )

            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add.html', {'form': form})


@login_required
def task_edit(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404("Task not found.")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit.html', {'form': form, 'task': task})


@login_required
def task_delete(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
    except Task.DoesNotExist:
        raise Http404("Task not found.")
    return redirect('task_list')
