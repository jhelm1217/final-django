from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.TextField()
    last_name = models.TextField()
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username 
    

class Trip(models.Model):
    user = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    destination = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_by = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='shared_trips', null=True, blank=True)
    # pending_requests = models.ManyToManyField(User, related_name='pending_trips', null=True, blank=True)

    # updated_at = models.DateTimeField(auto_now=True)
    # description = models.TextField()


    def __str__(self):
       return self.name



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.TextField(blank=True, null=True)
   
    def __str__(self):
        return f'{self.user.username}: {self.content}'
    
class Image(models.Model):
  title = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(upload_to='images/')

  def __str__(self):
    return self.title

    
class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # from_user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    # to_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)

    class Meta:
       unique_together = ('user', 'friend')
      #  unique_together = ('from_user', 'to_user')

    def __str__(self):
       return f'{self.from_user.username} friends with {self.to_user.username}'
    

class Group(models.Model):
   name = models.CharField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)
   members = models.ManyToManyField(User, through='GroupMember')
   trips = models.ManyToManyField(Trip, related_name='groups', blank=True)

   def __str__(self):
      return self.name
   
class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, choices=(('admin', 'Admin'), ('member', 'Member')))

    def __str__(self):
       return f'{self.user.username} is in {self.group.name}'
       
