from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from django.http import JsonResponse

from .models import *
from .forms import *
# ─── HELPER ───────────────────────────────────────────────
# Checks if the logged in user is admin/staff
def is_admin(user):
    return user.is_staff


# ─── AUTH VIEWS ───────────────────────────────────────────

# Student registration page
def register(request):
    form = StudentRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            email = form.cleaned_data['email']

            # Check if roll number already exists
            if User.objects.filter(username=roll_number).exists():
                messages.error(request, 'Roll number already registered.')
                return render(request, 'allocation/register.html', {'form': form})

            # Check if email already exists
            if Student.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'allocation/register.html', {'form': form})

            # Create the login account (User)
            user = User.objects.create_user(
                username=roll_number,
                password=form.cleaned_data['password'],
                email=email
            )

            # Create the student profile linked to that user
            Student.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                roll_number=roll_number,
                gender=form.cleaned_data['gender'],
                course=form.cleaned_data['course'],
                year=form.cleaned_data['year'],
                contact=form.cleaned_data['contact'],
                email=email
            )

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

    return render(request, 'allocation/register.html', {'form': form})


# ─── REDIRECT AFTER LOGIN ─────────────────────────────────

# After login, redirect admin to admin dashboard and student to student dashboard
# Home view — redirects based on who is logged in
def home(request):
    # If not logged in, send to student login
    if not request.user.is_authenticated:
        return redirect('login')
    # If admin, go to admin dashboard
    if is_admin(request.user):
        return redirect('admin_dashboard')
    # If student, go to student dashboard
    return redirect('student_dashboard')


# ─── ADMIN VIEWS ──────────────────────────────────────────

# Admin dashboard — shows counts of everything
@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    active_allocations = Allocation.objects.filter(status='Active').count()
    waitlist_count = WaitlistEntry.objects.count()

    available_rooms = 0
    occupied_rooms = 0
    for room in Room.objects.all():
        occupied = Allocation.objects.filter(room=room, status='Active').count()
        if occupied < room.capacity:
            available_rooms += 1
        else:
            occupied_rooms += 1

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'active_allocations': active_allocations,
        'waitlist_count': waitlist_count,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'recent_allocations': Allocation.objects.select_related('student', 'room').order_by('-allocated_date')[:5],
    }
    return render(request, 'allocation/admin_dashboard.html', context)


# Room list page
@login_required
def room_list(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    rooms = Room.objects.all()

    # Add occupancy info to each room
    room_data = []
    for room in rooms:
        occupied = Allocation.objects.filter(room=room, status='Active').count()
        room_data.append({
            'room': room,
            'occupied': occupied,
            'available': room.capacity - occupied,
            'is_full': occupied >= room.capacity,
        })

    return render(request, 'allocation/room_list.html', {'room_data': room_data})


# Add room page
@login_required
def room_add(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Room added successfully.')
        return redirect('room_list')

    return render(request, 'allocation/room_form.html', {'form': form, 'title': 'Add Room'})


# Delete room
@login_required
def room_delete(request, pk):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted.')
        return redirect('room_list')

    return render(request, 'allocation/confirm_delete.html', {'object': room, 'type': 'Room'})


# Student list page (admin only)
@login_required
def student_list(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    students = Student.objects.all()
    return render(request, 'allocation/student_list.html', {'students': students})


# Allocation list page
@login_required
def allocation_list(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    allocations = Allocation.objects.all().order_by('-allocated_date')
    return render(request, 'allocation/allocation_list.html', {'allocations': allocations})


# Add allocation page
@login_required
def allocation_add(request):
    
    if not is_admin(request.user):
        return redirect('student_dashboard')

    form = AllocationForm(request.POST or None)

    if form.is_valid():

        allocation = form.save()

        # Remove student from waiting list
        WaitlistEntry.objects.filter(
            student=allocation.student
        ).delete()

        messages.success(
            request,
            'Room allocated successfully.'
        )

        return redirect('allocation_list')

    return render(
        request,
        'allocation/allocation_form.html',
        {'form': form}
    )


# Vacate a room
@login_required
def allocation_vacate(request, pk):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    allocation = get_object_or_404(Allocation, pk=pk)
    if request.method == 'POST':
        allocation.status = 'Vacated'
        allocation.save()
        messages.success(request, f'{allocation.student.name} has vacated the room.')
        return redirect('allocation_list')

    return render(request, 'allocation/confirm_delete.html', {'object': allocation, 'type': 'Vacate'})


# Waitlist page
@login_required
def waitlist(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    entries = WaitlistEntry.objects.all().order_by('requested_date')
    return render(request, 'allocation/waitlist.html', {'entries': entries})


# Add to waitlist
@login_required
def waitlist_add(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    form = WaitlistForm(request.POST or None)
    if form.is_valid():
        student = form.cleaned_data['student']
        if WaitlistEntry.objects.filter(student=student).exists():
            messages.warning(request, f'{student.name} is already on the waitlist.')
        else:
            form.save()
            messages.success(request, f'{student.name} added to waitlist.')
        return redirect('waitlist')

    return render(request, 'allocation/waitlist_form.html', {'form': form})


# Remove from waitlist
@login_required
def waitlist_remove(request, pk):
    if not is_admin(request.user):
        return redirect('student_dashboard')

    entry = get_object_or_404(WaitlistEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Removed from waitlist.')
        return redirect('waitlist')

    return render(request, 'allocation/confirm_delete.html', {'object': entry, 'type': 'Waitlist Entry'})


# ─── STUDENT VIEWS ────────────────────────────────────────

# Student dashboard — shows their own info, room or waitlist status
@login_required
def student_dashboard(request):
    # Admin should not see this page
    if is_admin(request.user):
        return redirect('admin_dashboard')

    # Get the student profile linked to the logged in user
    student = get_object_or_404(Student, user=request.user)

    # Check if student has an active allocation
    allocation = Allocation.objects.filter(student=student, status='Active').first()

    # Check if student is on the waitlist
    waitlist_entry = WaitlistEntry.objects.filter(student=student).first()

    context = {
        'student': student,
        'allocation': allocation,
        'waitlist_entry': waitlist_entry,
    }
    return render(request, 'allocation/student_dashboard.html', context)

# Student applies for a room — adds them to waitlist
@login_required
def apply_for_room(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')

    student = get_object_or_404(Student, user=request.user)

    # Check if already allocated
    already_allocated = Allocation.objects.filter(student=student, status='Active').exists()
    if already_allocated:
        messages.warning(request, 'You already have a room allocated.')
        return redirect('student_dashboard')

    # Check if already applied
    already_applied = WaitlistEntry.objects.filter(student=student).exists()
    if already_applied:
        messages.warning(request, 'You have already applied. Please wait for the admin.')
        return redirect('student_dashboard')

    # GET request → show confirmation page
    if request.method == 'GET':
        return render(request, 'allocation/apply_confirm.html', {'student': student})

    # POST request → confirmed, add to waitlist
    WaitlistEntry.objects.create(student=student)
    messages.success(request, 'Your room application has been submitted successfully!')
    return redirect('student_dashboard')

from django.contrib.auth import authenticate, login as auth_login

# Separate admin login view
def admin_login(request):
    # If already logged in, go to dashboard
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # Check if user exists and is admin
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin account.')

    return render(request, 'allocation/admin_login.html')



# Admin — view all fees
@login_required
def fee_list(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')
    fees = Fee.objects.select_related('student').all().order_by('due_date')
    return render(request, 'allocation/fee_list.html', {'fees': fees})


# Admin — add a fee
@login_required
def fee_add(request):
    if not is_admin(request.user):
        return redirect('student_dashboard')
    form = FeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fee added successfully.')
        return redirect('fee_list')
    return render(request, 'allocation/fee_form.html', {'form': form})


# Admin — mark fee as paid or unpaid
@login_required
def fee_toggle(request, pk):
    if not is_admin(request.user):
        return redirect('student_dashboard')
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        # Toggle status
        fee.status = 'Paid' if fee.status == 'Unpaid' else 'Unpaid'
        fee.save()
        messages.success(request, f'Fee marked as {fee.status}.')
    return redirect('fee_list')


# Student — view their own fees
@login_required
def my_fees(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    student = get_object_or_404(Student, user=request.user)
    fees = Fee.objects.filter(student=student).order_by('due_date')
    return render(request, 'allocation/my_fees.html', {'fees': fees})

@login_required
def load_rooms(request):
    
    student_id = request.GET.get('student')

    rooms = []

    if student_id:

        student = Student.objects.get(id=student_id)

        rooms_data = Room.objects.filter(
            gender_type=student.gender
        )

        rooms = list(
            rooms_data.values(
                'id',
                'room_number',
                'block'
            )
        )

    return JsonResponse(rooms, safe=False)