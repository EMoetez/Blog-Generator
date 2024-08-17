from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
from pytubefix import YouTube
from pytubefix.cli import on_progress
import ollama
from .models import Blogpost
from dotenv import load_dotenv
load_dotenv()
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

 
@csrf_exempt
def generate_blog(request):
    if request.method =='POST':
        try:
            data = json.loads(request.body)
            yt_link= data['link']
            
        except(KeyError, json.JSONDecodeError):
             return JsonResponse({'error': 'Invalid data sent' }, status=400)  
         
        # get yt title
        title = yt_title(yt_link)
        
        # get transcript
        transcription = get_transcription(yt_link,title)
        if not transcription:
            return JsonResponse({'error':"Failed to get transcript"}, status= 500)
          
        # use OpenAI to generate the blog
        blog_content=generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error':"Failed to generate blog"}, status= 500) 
        
        
        # save blog article to database
        new_blog_article= Blogpost.objects.create(
        
            user = request.user,
            youtube_title = title,
            youtube_link =yt_title ,
            generated_content = blog_content,
             
        )
        new_blog_article.save()
        
        
        # return blog article as response
        return JsonResponse({'content': blog_content}) 
     
    else:
        return JsonResponse({'error':'Invalid request method'}, status=405) 
   
   
def yt_title(link):
    yt= YouTube(link)
    title=yt.title
    return title 

def download_audio(link):
    yt = YouTube(link, on_progress_callback = on_progress)
    ys = yt.streams.get_audio_only()
    out_file=ys.download(mp3=True,output_path=settings.MEDIA_ROOT)
    base, ext= os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file
    
    
def get_transcription(link,title):
    audio_file= download_audio(link)
    aai.settings.api_key= "YOUR_ASSEMBLYAI_API_KEY"
    transcriber= aai.Transcriber()
    transcript= transcriber.transcribe(audio_file)
    # Specify the file name and path
    file_name = title +'.txt'

    # Open the file in write mode ('w') and save the text
    with open(file_name, 'w') as file:
        file.write(transcript.text)

    print(f"Text saved to {file_name}")
    return transcript.text

# Generate blog from transcript using Llama2 from Ollama API(you can use any model of your choice)
def generate_blog_from_transcription(transcription):
    
    prompt=f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, please do it in 200 words approximately, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    Answer=ollama.chat(
    
    model="llama2",
    messages=[{"role":"user","content":prompt}],
    
    stream=False,
)

    ##For dubbuging
    #print(Answer['message']['content'],end='',flush=True)
    
    
    generated_content = Answer['message']['content']
    
    return generated_content  


def blog_list(request):
     blog_articles= Blogpost.objects.filter(user= request.user)
     return render(request, "All-blogs.html", {'blog_articles':blog_articles})
 
def BlogDetails(request, pk):
    blog_article_details=Blogpost.objects.get(id=pk)
    if request.user == blog_article_details.user:
        return render(request, "BlogDetails.html", {'blog_article_details':blog_article_details})
    else:
        return redirect('/')

def user_login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message='Invalid username or password'
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')
    


def user_signup(request):
    if request.method =='POST':
        
        username = request.POST['username']
        Email = request.POST['email']
        password = request.POST['password']
        repeatPassword= request.POST['repeatPassword']
        if password == repeatPassword:
            try:
                
                user= User.objects.create_user(username, Email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message='Error creating user'
                render (request, 'signup.html', {'error_message':error_message})
        else:
            error_message='Password does not match'
            render (request, 'signup.html', {'error_message':error_message})
    
    return render(request, 'signup.html')
     
    

def user_logout(request):
    logout(request) 
    return redirect('/')
    
