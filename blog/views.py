from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allposts = Post.objects.all()

    context = {'allposts': allposts}
    return render(request,'blog/blogHome.html', context) 
    
def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    context={"post":post,"comments":comments,'user':request.user}
    return render(request, "blog/blogPost.html", context)


def postcomment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postsno = request.POST.get('postsno')
        
        
        try:
            post = Post.objects.get(sno=postsno)
        except Post.DoesNotExist:
            return HttpResponse("Post not found")

        # Save the comment
        new_comment = BlogComment(comment=comment, user=user, post=post)
        new_comment.save()

        messages.success(request, "Your comment has been posted successfully.")
        return redirect(f"/blog/{post.slug}")   # Redirect to the blog post page
    else:
        return HttpResponse("404 - Page not found")  