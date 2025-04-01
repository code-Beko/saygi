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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def home(request):
    if request.user.is_authenticated:

        unread_tasks = Task.objects.filter(assigned_to=request.user).exclude(
            is_read=request.user
        )
        unread_tasks_count = unread_tasks.count()
    else:
        unread_tasks = []
        unread_tasks_count = 0

    context = {
        "unread_tasks_count": unread_tasks_count,
        "unread_tasks": unread_tasks,
    }
    return render(request, "index.html", context)


def care(request):
    return render(request, "care.html")


def document_list(request):
    query = request.GET.get("q", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    documents = Document.objects.all()

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
            "can_edit": request.user.is_superuser,
        },
    )


def document_delete(id):

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


@login_required
def document_add(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.created_by = request.user
                document.save()
                return redirect("document_list")
            except Exception as e:
                messages.error(
                    request, f"Döküman oluşturulurken bir hata oluştu: {str(e)}"
                )
        else:
            messages.error(request, "Form geçersiz. Lütfen tüm alanları kontrol edin.")
    else:
        form = DocumentForm()

    fields = get_document_fields(form.instance)
    return render(request, "care/add.html", {"form": form, "fields": fields})


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
            return redirect("user_list")
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

    tasks = Task.objects.filter(assigned_to=request.user)

    unread_tasks = tasks.exclude(is_read=request.user)

    for task in tasks:
        task.is_read.add(request.user)

    context = {
        "tasks": tasks,
        "unread_count": unread_tasks.count(),
    }
    return render(request, "notifications.html", context)


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("document_list")
    else:
        form = CustomLoginForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def task_list(request):
    # Filtreleme parametrelerini al
    department = request.GET.get("department", "")
    status = request.GET.get("status", "")
    assigned_to = request.GET.get("assigned_to", "")

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
        "tasks": tasks,
        "users": users,
        "selected_department": department,
        "selected_status": status,
        "selected_assigned_to": assigned_to,
        "form": form,  # Form nesnesini context'e ekle
    }
    return render(request, "tasks/list.html", context)


@login_required
def task_add(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.created_by = request.user
                task.save()
                form.save_m2m()  # Many-to-many ilişkileri kaydet

                # Görev atanan kişilere mail gönder
                for assigned_user in task.assigned_to.all():
                    try:
                        # Mail içeriğini hazırla
                        subject = f"Yeni Görev Atandı: {task.project_name}"
                        html_message = render_to_string(
                            "tasks/email/task_assigned.html",
                            {
                                "task": task,
                                "assigned_user": assigned_user,
                                "created_by": request.user,
                                "request": request,
                            },
                        )
                        plain_message = strip_tags(html_message)

                        # Maili gönder
                        send_mail(
                            subject=subject,
                            message=plain_message,
                            from_email="noreply@saygielectric.com",
                            recipient_list=[assigned_user.email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                        messages.success(
                            request,
                            f"{assigned_user.username} kullanıcısına bildirim gönderildi.",
                        )
                    except Exception as e:
                        messages.warning(
                            request,
                            f"{assigned_user.username} kullanıcısına bildirim gönderilemedi: {str(e)}",
                        )

                messages.success(request, "Görev başarıyla oluşturuldu.")
                return redirect("task_list")
            except Exception as e:
                messages.error(
                    request, f"Görev oluşturulurken bir hata oluştu: {str(e)}"
                )
                return redirect("task_list")
        else:
            messages.error(request, "Form geçersiz. Lütfen tüm alanları kontrol edin.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/add.html", {"form": form})


def task_edit(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404("Task not found.")

    # Kullanıcı göreve atanmış mı kontrol et
    is_assigned_user = request.user in task.assigned_to.all()

    # Kullanıcı giriş yapmamışsa sadece görüntüleme yetkisi ver
    if request.user.is_authenticated:
        if not is_assigned_user and request.user != task.created_by:
            messages.error(request, "Bu görevi düzenleme izniniz yok.")
            return redirect("task_list")
    else:
        # Üye girişi yapmamış kullanıcıya formu readonly yap
        is_assigned_user = False  # Her durumda atanmış kullanıcı olarak kabul edilmesin

    if request.method == "POST":
        if is_assigned_user:
            # Atanan kullanıcı sadece status'ü değiştirebilir
            new_status = request.POST.get("status")
            if new_status:
                task.status = new_status
                task.save()
                messages.success(request, "Görev durumu başarıyla güncellendi.")
                return redirect("task_list")
            else:
                messages.error(request, "Durum alanı boş bırakılamaz.")
        else:
            # Normal kullanıcı tüm alanları değiştirebilir
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, "Görev başarıyla güncellendi.")
                return redirect("task_list")
            else:
                messages.error(
                    request, "Form geçersiz. Lütfen tüm alanları kontrol edin."
                )
    else:
        form = TaskForm(instance=task)
        if not is_assigned_user:
            # Atanmamış kullanıcı ise formu sadece okuma modunda göster
            for field in form.fields.values():
                field.disabled = (
                    True  # Formu readonly yapmak için tüm alanları devre dışı bırak
                )

    context = {"form": form, "task": task, "is_assigned_user": is_assigned_user}
    return render(request, "tasks/edit.html", context)


@login_required
def task_delete(request, id):  # request eklenmeli
    try:
        task = Task.objects.get(id=id)
        task.delete()
    except Task.DoesNotExist:
        raise Http404("Task not found.")
    return redirect("task_list")


@user_passes_test(is_superuser)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "users/list.html", {"users": users})


@user_passes_test(is_superuser)
def user_edit(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        raise Http404("User not found.")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Kullanıcı başarıyla güncellendi.")
            return redirect("user_list")
        else:
            messages.error(request, "Kullanıcı güncellenirken bir hata oluştu.")
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, "users/edit.html", {"form": form, "user": user})


@user_passes_test(is_superuser)
def user_delete(request, id):
    try:
        user = CustomUser.objects.get(id=id)
        user.delete()
        messages.success(request, "Kullanıcı başarıyla silindi.")
    except CustomUser.DoesNotExist:
        raise Http404("User not found.")
    return redirect("user_list")
