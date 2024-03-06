from uuid import uuid4

from django.db import models


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid4, db_index=True)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    company_logo = models.URLField(null=True, blank=True)
    date = models.DateField()
    ago_date = models.CharField(max_length=255, null=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)
    deleted = models.BooleanField(default=False)
    url = models.URLField(unique=True, max_length=400)

    class Meta:
        db_table = "job"
        ordering = ["-date"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self) -> str:
        return f"{self.position} at {self.company}"
