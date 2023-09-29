from django.db import models
import smtplib
from email.mime.text import MIMEText

class ScreenRecording(models.Model):
    content = models.FileField(upload_to='screen_recordings/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content.name

    def share(self, attributes=None):
        if attributes is None:
            attributes = {'url': self.get_absolute_url(), 'filename': self.content.name, 'email': 'user@example.com'}

        smtp_server = smtplib.SMTP('smtp.example.com', 587)
        smtp_server.starttls()
        smtp_server.login('username', 'password')

        msg = MIMEText('This is the screen recording you requested.')
        msg['Subject'] = 'Screen recording'
        msg['From'] = 'sender@example.com'
        msg['To'] = attributes['email']

        with open(self.content.path, 'rb') as f:
            msg.add_attachment(f.read(), filename=self.content.name)

        smtp_server.sendmail('sender@example.com', attributes['email'], msg.as_string())
        smtp_server.quit()

        return 'Screen recording shared successfully!'

class SavedSharedVideo(models.Model):
    email = models.EmailField()
    filename = models.CharField(max_length=255)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
