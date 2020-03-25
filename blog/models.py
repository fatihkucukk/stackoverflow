from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.title

    def get_oy_count(self):
        upvote = Oy.objects.filter(soru=self, vote_type=Oy.UP).count()
        downvote = Oy.objects.filter(soru=self, vote_type=Oy.DOWN).count()
        oysayisi = upvote - downvote
        return oysayisi

    def oy_ver(self, voter_user):
        oylar = Oy.objects.filter(kullanici=voter_user, soru=self, vote_type=Oy.UP)

        if not oylar.exists():
            Oy.objects.create(kullanici=voter_user, soru=self, vote_type=Oy.UP)
        else:
            oylar = Oy.objects.filter(kullanici=voter_user, soru=self, vote_type=Oy.DOWN)
            if oylar.exists():
                oylar.delete()
                Oy.objects.create(kullanici=voter_user, soru=self, vote_type=Oy.UP)
        return True



    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title



class Cevap(models.Model):

    vote_type = models.PositiveSmallIntegerField(null=True, blank=True)
    kullanici = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    icerik = models.TextField()
    soru = models.ForeignKey('blog.Post', related_name='cevaplar', on_delete=models.CASCADE)
    created_date = models.DateTimeField(
        default=timezone.now)


    def get_oy_count(self):
        upvote = Oy.objects.filter(cevap=self, vote_type=Oy.UP).count()
        downvote = Oy.objects.filter(cevap=self, vote_type=Oy.DOWN).count()
        oysayisi = upvote - downvote
        return oysayisi

    def oyver(self, answer_voter_user, vote_type):
        oylar = Oy.objects.filter(kullanici=answer_voter_user, cevap=self, vote_type=Oy.UP)
        if not oylar.exists():
            Oy.objects.create(kullanici=answer_voter_user, cevap=self, vote_type=Oy.UP)
        else:
            oylar = Oy.objects.filter(kullanici=answer_voter_user, cevap=self, vote_type=Oy.DOWN)
            if oylar.exists():
                oylar.delete()
                Oy.objects.create(kullanici=answer_voter_user, cevap=self, vote_type=Oy.UP)
        return True

    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return self.title


class Oy(models.Model):
    EMPTY = 0
    UP = 1
    DOWN = 2
    soru = models.ForeignKey('blog.Post', related_name='oyver', on_delete=models.CASCADE, null=True, blank=True)
    cevap = models.ForeignKey('blog.Cevap', related_name='oylar', on_delete=models.CASCADE, null=True, blank=True)
    kullanici = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    vote_type = models.PositiveSmallIntegerField()


