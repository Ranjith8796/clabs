from django.db import models

class account(models.Model):
    email_id = models.EmailField(unique=True, blank=False)
    account_id = models.AutoField(primary_key=True, auto_created= True)
    account_name = models.CharField(max_length=200, blank=False)
    token = models.CharField(max_length=200)
    website = models.CharField(max_length=200)


class destination(models.Model):
    id = models.AutoField(primary_key=True, auto_created= True)
    account_id = models.ForeignKey(account, on_delete=models.CASCADE, unique=False)
    distination_url = models.CharField(max_length=200, blank=False)
    http_method = models.CharField(max_length=100, blank=False)
    headers = models.JSONField(max_length=400, blank=False)