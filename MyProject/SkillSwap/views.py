from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import UserProfile, Skill, SkillExchange, Message, Review
import json

def index(request):
    """Home page showing recent skill exchanges and featured skills"""
    # For now, show basic content - we'll add more when models are ready
    context = {
        'recent_exchanges': [],
        'popular_skills': [],
    }
    return render(request, 'index.html', context)

def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# @login_required
def dashboard(request):
    # """User dashboard showing their exchanges and activities"""
    # user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # # Get user's exchanges
    # my_requests = SkillExchange.objects.filter(requester=request.user).order_by('-created_at')
    # my_offers = SkillExchange.objects.filter(provider=request.user).order_by('-created_at')
    
    # # Get available skill exchanges (excluding user's own)
    # available_exchanges = SkillExchange.objects.filter(
    #     status='pending'
    # ).exclude(requester=request.user).order_by('-created_at')[:10]
    
    # context = {
    #     'user_profile': user_profile,
    #     'my_requests': my_requests,
    #     'my_offers': my_offers,
    #     'available_exchanges': available_exchanges,
    # }
    # return render(request, 'dashboard.html', context)
    return render(request, 'dashboard.html')

# @login_required
def profile(request):
    """User profile view and edit"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update
        user_profile.bio = request.POST.get('bio', '')
        user_profile.location = request.POST.get('location', '')
        user_profile.phone = request.POST.get('phone', '')
        user_profile.skills_offered = request.POST.get('skills_offered', '')
        user_profile.skills_wanted = request.POST.get('skills_wanted', '')
        
        # Handle file upload
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    # Get user's reviews
    reviews = Review.objects.filter(reviewed_user=request.user).order_by('-created_at')
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    context = {
        'user_profile': user_profile,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 2),
    }
    return render(request, 'profile.html', context)

# @login_required
def chat(request, exchange_id):
    """Chat interface for a specific skill exchange"""
    exchange = get_object_or_404(SkillExchange, id=exchange_id)
    
    # Check if user is part of this exchange
    if request.user not in [exchange.requester, exchange.provider]:
        messages.error(request, 'You are not authorized to view this chat.')
        return redirect('dashboard')
    
    # Get messages for this exchange
    messages_list = Message.objects.filter(exchange=exchange).order_by('timestamp')
    
    # Mark messages as read
    Message.objects.filter(
        exchange=exchange,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Handle new message
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                exchange=exchange,
                sender=request.user,
                content=content
            )
            return redirect('chat', exchange_id=exchange_id)
    
    context = {
        'exchange': exchange,
        'messages': messages_list,
    }
    return render(request, 'chat.html', context)

# @login_required
def accept_exchange(request, exchange_id):
    """Accept a skill exchange request"""
    exchange = get_object_or_404(SkillExchange, id=exchange_id)
    
    if request.user != exchange.provider:
        messages.error(request, 'You are not authorized to accept this exchange.')
        return redirect('dashboard')
    
    exchange.status = 'accepted'
    exchange.save()
    messages.success(request, 'Skill exchange accepted!')
    return redirect('dashboard')

# @login_required
def complete_exchange(request, exchange_id):
    """Mark exchange as completed"""
    exchange = get_object_or_404(SkillExchange, id=exchange_id)
    
    if request.user not in [exchange.requester, exchange.provider]:
        messages.error(request, 'You are not authorized to complete this exchange.')
        return redirect('dashboard')
    
    exchange.status = 'completed'
    exchange.save()
    messages.success(request, 'Skill exchange marked as completed!')
    return redirect('dashboard')

# @login_required
def cancel_exchange(request, exchange_id):
    """Cancel a skill exchange"""
    exchange = get_object_or_404(SkillExchange, id=exchange_id)
    
    if request.user not in [exchange.requester, exchange.provider]:
        messages.error(request, 'You are not authorized to cancel this exchange.')
        return redirect('dashboard')
    
    exchange.status = 'cancelled'
    exchange.save()
    messages.success(request, 'Skill exchange cancelled!')
    return redirect('dashboard')

# @login_required
def delete_exchange(request, exchange_id):
    """Delete a skill exchange (only for requesters)"""
    exchange = get_object_or_404(SkillExchange, id=exchange_id)
    
    if request.user != exchange.requester:
        messages.error(request, 'You can only delete your own exchange requests.')
        return redirect('dashboard')
    
    if exchange.status != 'pending':
        messages.error(request, 'You can only delete pending exchanges.')
        return redirect('dashboard')
    
    exchange.delete()
    messages.success(request, 'Skill exchange deleted successfully!')
    return redirect('dashboard')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

# API endpoints for AJAX requests
@csrf_exempt
# @login_required
def get_messages(request, exchange_id):
    """Get messages for an exchange (AJAX endpoint)"""
    if request.method == 'GET':
        exchange = get_object_or_404(SkillExchange, id=exchange_id)
        
        if request.user not in [exchange.requester, exchange.provider]:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        messages_list = Message.objects.filter(exchange=exchange).order_by('timestamp')
        messages_data = []
        
        for message in messages_list:
            messages_data.append({
                'id': message.id,
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'is_own_message': message.sender == request.user,
            })
        
        return JsonResponse({'messages': messages_data})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
# @login_required
def send_message(request, exchange_id):
    """Send a message (AJAX endpoint)"""
    if request.method == 'POST':
        exchange = get_object_or_404(SkillExchange, id=exchange_id)
        
        if request.user not in [exchange.requester, exchange.provider]:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if not content:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            message = Message.objects.create(
                exchange=exchange,
                sender=request.user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                    'is_own_message': True,
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)