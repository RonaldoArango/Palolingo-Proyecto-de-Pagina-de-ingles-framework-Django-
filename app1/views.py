from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importa el sistema de mensajes
from allauth.socialaccount.models import SocialApp
from django.db.models import Count
import speech_recognition as sr
from django.http import JsonResponse,HttpResponse, HttpRequest
from django.core.files.storage import FileSystemStorage
import os
from pydub import AudioSegment
from .forms import TextInputForm
import language_tool_python
from PyDictionary import PyDictionary
from .forms import DiccionarioForm
from .models import Diccionario, Forum, Discussion
from .models import * 
from .forms import *
from allauth.socialaccount.models import SocialAccount, SocialToken
import yaml
from nltk.corpus import wordnet as wn
from .models import Quiz, Question, Answer
from django.core.paginator import Paginator
from typing import Optional

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html', {'user': request.user})

def SignupPage(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya estás registrado y logueado. Haz clic para ir al inicio.")
        return redirect('home')  # Redirige al usuario a la página de inicio si ya está logueado

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Las contraseñas no son iguales.")
            return render(request, 'signup.html')  # Renderiza la misma página con el mensaje

        try:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Error al registrar el usuario: " + str(e))
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def LoginPage(request):
    messages.get_messages(request).used = True

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña son incorrectos.")
            return redirect('login')

    discord_app = None
    try:
        discord_app = SocialApp.objects.get(provider='discord')
    except SocialApp.DoesNotExist:
        messages.error(request, "")

    return render(request, 'login.html', {'discord_app': discord_app})

def LogoutPage(request):
    # Agregar un mensaje de éxito antes de cerrar sesión
    messages.success(request, "Has cerrado sesión exitosamente.")
    logout(request)
    
    # Limpiar los mensajes de sesión (opcional, pero puede ayudar)
    messages.get_messages(request).used = True
    
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')

#---------------- Speech recognition-------------------------

def reconocer_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audiofile']  # El archivo de audio subido
        fs = FileSystemStorage()
        filename = fs.save(audio_file.name, audio_file)
        file_path = fs.path(filename)

        try:
            # Convertir MP3 a WAV usando pydub
            audio = AudioSegment.from_mp3(file_path)  # Lee el archivo MP3
            wav_filename = os.path.splitext(file_path)[0] + '.wav'  # Crear el nombre del archivo WAV
            audio.export(wav_filename, format="wav")  # Exportar como WAV

            # Ahora usar speech_recognition para procesar el archivo WAV
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_filename) as source:
                audio_data = recognizer.record(source)  # Lee el archivo WAV
                text = recognizer.recognize_google(audio_data, language="es-ES")  # Reconocer el audio

            # Retornar la transcripción como JSON
            return JsonResponse({'transcripcion': text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def pagina_audio(request):
    return render(request,'audio.html')

#------------------------Corrector de textos---------

def correct_text(request):
    correction_result = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            tool = language_tool_python.LanguageTool('en-US')
            matches = tool.check(text)
            correction_result = tool.correct(text)
            tool.close()
    else:
        form = TextInputForm()

    return render(request, 'correct_text.html', {
        'form': form,
        'correction_result': correction_result
    })




#--------------------Diccionario

def input_word(request):
    if request.method == "POST":
        word = request.POST.get("word")
        return redirect('display_word', word=word)
    return render(request, 'input_word.html')

def display_word(request, word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    meaning = wn.synsets(word)[0].definition() if wn.synsets(word) else "No definition found."
    context = {
        'word': word,
        'meaning': meaning,
        'synonyms': list(synonyms)
    }
    return render(request, 'display_word.html', context)
#--------------------------Foro

def foro(request):
    forums = Forum.objects.all()
    count = forums.count()
    discussions = []
    for forum in forums:
        discussions.append(forum.discussion_set.all())
    
    context = {
        'forums': forums,
        'count': count,
        'discussions': discussions
    }
    return render(request, 'foro.html', context)

def addInForum(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            # No redirigir, solo volver a renderizar la página del foro
            return foro(request)  # Llama a la vista 'foro' para renderizarla de nuevo

    context = {'form': form}
    return render(request, 'addInForum.html', context)

def addInDiscussion(request):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/foro/')  # Redirigir a la página de foros después de agregar una discusión

    context = {'form': form}
    return render(request, 'addInDiscussion.html', context)


#---------------------------------quizz

def start_quiz_view(request) -> HttpResponse:
  topics = Quiz.objects.all().annotate(questions_count=Count('question'))
  return render(
    request, 'start.html', context={'topics': topics}
  )


def get_questions(request, is_start=False) -> HttpResponse:
  if is_start:
    request = _reset_quiz(request)
    question = _get_first_question(request)
  else:
    question = _get_subsequent_question(request)
    if question is None:
      return get_finish(request)

  answers = Answer.objects.filter(question=question)
  request.session['question_id'] = question.id  # Update session state with current question id.

  return render(request, 'partials/question.html', context={
    'question': question, 'answers': answers
  })


def _get_first_question(request) -> Question:
  quiz_id = request.POST['quiz_id']
  return Question.objects.filter(quiz_id=quiz_id).order_by('id').first()


def _get_subsequent_question(request) -> Optional[Question]:
  quiz_id = request.POST['quiz_id']
  previous_question_id = request.session['question_id']

  try:
    return Question.objects.filter(
      quiz_id=quiz_id, id__gt=previous_question_id
    ).order_by('id').first()
  except Question.DoesNotExist:  # I.e., there are no more questions.
    return None


def get_answer(request) -> HttpResponse:
  submitted_answer_id = request.POST['answer_id']
  submitted_answer = Answer.objects.get(id=submitted_answer_id)

  if submitted_answer.is_correct:
    correct_answer = submitted_answer
    request.session['score'] = request.session.get('score', 0) + 1
  else:
    correct_answer = Answer.objects.get(
      question_id=submitted_answer.question_id, is_correct=True
    )

  return render(
    request, 'partials/answer.html', context={
      'submitted_answer': submitted_answer,
      'answer': correct_answer,
    }
  )


def get_finish(request) -> HttpResponse:
  quiz = Question.objects.get(id=request.session['question_id']).quiz
  questions_count = Question.objects.filter(quiz=quiz).count()
  score = request.session.get('score', 0)
  percent = int(score / questions_count * 100)
  request = _reset_quiz(request)

  return render(request, 'partials/finish.html', context={
    'questions_count': questions_count, 'score': score, 'percent_score': percent
  })


def _reset_quiz(request) -> HttpRequest:
  """
  We reset the quiz state to allow the user to start another quiz.
  """
  if 'question_id' in request.session:
    del request.session['question_id']
  if 'score' in request.session:
    del request.session['score']
  return request

#-----------------topicos(temas)-----------------
from django.shortcuts import render, redirect


def temas(request):
    return render(request, 'temas.html')

def present_simple_exercises(request):
   yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'topics', 'present_simple.yaml')
   with open(yaml_path,'r') as file:
      config_data=yaml.safe_load(file)
   return render(request,'present_simple_exersices.html', {'config_data': config_data})
  

def present_simple(request):
    # Verifica si el tema está marcado como aprendido en la sesión
    aprendido = request.session.get('aprendidos', {}).get('present_simple', False)
    return render(request, 'present_simple.html', {'aprendido':aprendido})

def past_simple(request):
    aprendido = request.session.get('aprendidos', {}).get('past_simple', False)
    return render(request, 'past_simple.html', {'aprendido': aprendido})

def future_simple(request):
    aprendido = request.session.get('aprendidos', {}).get('future_simple', False)
    return render(request, 'future_simple.html', {'aprendido': aprendido})

def present_continuous(request):
    aprendido = request.session.get('aprendidos', {}).get('present_continuous', False)
    return render(request, 'present_continuous.html', {'aprendido': aprendido})

def past_continuous(request):
    aprendido = request.session.get('aprendidos', {}).get('past_continuous', False)
    return render(request, 'past_continuous.html', {'aprendido': aprendido})

def marcar_aprendido(request, tema):
    if request.method == 'POST':
        #esta linea crea un diccionario para almacenar temas aprendidos
        aprendidos = request.session.get('aprendidos', {})

        #este acciona el boton del aprendido
        aprendidos[tema] = not aprendidos.get(tema, False)

        #esta linea lo almacena en el diccionario creado
        request.session['aprendidos'] = aprendidos

    return redirect(f'/temas/{tema}/')
