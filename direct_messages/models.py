from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    content = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # creating the two instances of one message in the DB and save it to both users (sender, receiver)
    def send_message(sender, to_user, content):
        from_message = Message(
            user = sender,
            from_user = sender,
            to_user = to_user,
            content = content,
            is_read = True)
        from_message.save()

        to_message = Message(
            user = to_user,
            from_user = sender,
            content = content,
            to_user = sender)

        to_message.save()

        return from_message

    # getting the messages owned by user(param)
    def get_messages(user):
        users = []
        messages = Message.objects.filter(user=user).values('to_user').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['to_user']),
                #'last': message['last'],
                'unread': Message.objects.filter(user=user, to_user__pk=message['to_user'], is_read=False).count()
            })
        return users