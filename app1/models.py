from django.db import models
from django.contrib.auth.models import User
    
class Pregunta(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Word(models.Model):
    english_word = models.CharField(max_length=100)
    spanish_translation = models.CharField(max_length=100)

    def __str__(self):
        return self.english_word

class Forum(models.Model):  # Asegúrate de que la clase se llame Forum
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="DESCONOCIDO")
    email = models.CharField(max_length=200, null=True)
    topic = models.CharField(max_length=300)
    description = models.TextField()
    link = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Discussion(models.Model):
    forum = models.ForeignKey(Forum, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.forum)


#------------- QUIZ MODELS ---------------------

class Quiz(models.Model):
  name = models.CharField(max_length=300)


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_correct = models.BooleanField(default=False)


#---------------DICCIONARIO----------------------

class Diccionario(models.Model):
    # Define los campos aquí
    nombre = models.CharField(max_length=100)
    significado = models.TextField()
    # Otros campos que necesites

    def __str__(self):
        return self.nombre

class Palabra(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    definicion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
