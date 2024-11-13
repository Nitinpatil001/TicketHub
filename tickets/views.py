from django.shortcuts import render,redirect,get_object_or_404
from .models import Ticket
from django.shortcuts import render
from django. contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import TicketForm
from django.contrib.auth.decorators import user_passes_test
from .forms import TicketForm , CommentForm 


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')
        if password==conpassword:
            obj = User(username=username,email=email,password=password)
            obj.set_password(password)
            obj.save()
            return redirect('login')
        else:
            return HttpResponse('Password Does not Matched!!')
    return render(request,'register.html')

    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first() 

        if user is not None:
            
            obj = authenticate(request, username=user.username, password=password)

            if obj is not None:
                auth_login(request, obj)  
                return redirect('home')
            else:
                return HttpResponse('Invalid password!')
        else:
            return HttpResponse('User not found!')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request) 
    return redirect('login')

@login_required
def home(request):
    status = request.GET.get('status', '')

    if status:
        tickets = Ticket.objects.filter(status=status)
    else:
        tickets = Ticket.objects.filter(user=request.user)
    
    return render(request, 'home.html', {'tickets':tickets})
     

@login_required
def ticket(request):
    if request.method == 'POST':
        print("Form Data:", request.POST)  
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            print('ticket before ',ticket)
            form.save()
            print('ticket saved')
            return redirect('ticket_list')
        else:
            print("Form Errors:", form.errors) 
    else:
        form = TicketForm()
    
    return render(request, 'ticket.html', {'form': form})

def ticket_comments(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all()  # Assuming a related_name='comments' in Comment model
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_comments', pk=ticket.pk)
    else:
        form = CommentForm()
    return render(request, 'ticket_comment.html', {'ticket': ticket, 'comments': comments, 'form': form})

@login_required
def ticket_list(request):
    user = request.user
    
    # Get the status filter from the GET request (if provided)
    status_filter = request.GET.get('status', None)
    print("Requested Status:", status_filter)
    
    # Start by filtering tickets by the logged-in user
    tickets = Ticket.objects.filter(user=user)
    print("Tickets before filtering by status:", tickets) 

    # If a status filter is provided, apply it
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    return render(request, 'tickets.html', {'tickets': tickets})

def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'admin_tickets.html', {'tickets': tickets})


@user_passes_test(is_admin)
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Ticket.STATUS_CHOICES):
            ticket.status = status
            ticket.save()
            return redirect('admin_ticket_list')
    return render(request, 'admin_update_ticket.html', {'ticket': ticket})

def update(request,pk):
    data = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        priority = request.POST.get('priority')
        assigned_to = request.POST.get('assigned_to')
        data.title = title
        data.desc = desc
        data.desc = desc
        data.priority = priority
        data.assigned_to = assigned_to
        data.save()
        return redirect('home')

    ticket_data = {
        'data' : data
    }

    return render(request,'update.html',context=ticket_data)


def delete(request,pk):
    data = Ticket.objects.get(id=pk)
    data.delete()
    return redirect('home')
