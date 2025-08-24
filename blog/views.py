from .models import Post
from account.models import User
from django.http import JsonResponse, Http404
import json
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import jwt_required


@csrf_exempt
def manage_post(request, post_id = None):
    if(post_id is None):        
        if request.method == "GET":
            return get_all_post(request)
        elif request.method == "POST":
            return jwt_required(create_post)(request)
    else:
        if request.method == "GET":
            return get_post(request, post_id)
        elif request.method == "PUT":
            return jwt_required(edit_post)(request, post_id)
        elif request.method == "DELETE":
            return jwt_required(delete_post)(request, post_id)
        
    return JsonResponse({"error": "Method not allowed"}, status=405)



def get_all_post(request): 
    """_summary_
    Gets all the available posts

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
       
    posts = Post.objects.all().values("id", "title", "content", "created_at", "author__username")
    return JsonResponse(list(posts), safe=False)
    
    
def get_post(request, post_id):
    try:
        post = Post.objects.values("id", "title", "content", "created_at", "author__username").get(id=post_id)
        return JsonResponse(post)
    except Post.DoesNotExist:
        raise Http404("Post not found")
            

def create_post(request):    
        try:
            data = json.loads(request.body)  # parse JSON body
            title = data.get("title")
            content = data.get("content")
            
            user = User.objects.get(id=request.user_id)
            
            post = Post.objects.create(
                title=title,
                content=content,
                author=user
            )
            
            return JsonResponse({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author.username,
                "created_at": post.created_at
            }, status=201)
            
        except:
            raise Http404("Post not found")
        

def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    
    # Check ownership
    if post.author.id != request.user_id:
        return JsonResponse({"error": "Not authorized"}, status=403)
    
    try:
        data = json.loads(request.body)  # parse JSON body
        title = data.get("title")
        content = data.get("content")
        
        # Update fields
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.save()
        
        return JsonResponse({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "created_at": post.created_at
        }, status=201)
        
    except:
        raise Http404("Post not found")
        

def delete_post(request, post_id):
    if request.method == "DELETE":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        # Check ownership
        if post.author.id != request.user_id:
            return JsonResponse({"error": "Not authorized"}, status=403)

        post.delete()
        return JsonResponse({"message": "Post deleted successfully"}, status=200)
        
    return JsonResponse({"error": "Method not allowed"}, status=405)