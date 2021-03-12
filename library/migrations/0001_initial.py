# Generated by Django 3.1.2 on 2021-03-12 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, null=True)),
                ('gender', models.CharField(max_length=16, null=True)),
                ('website', models.URLField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('genre', models.CharField(blank=True, max_length=32, null=True)),
                ('publisher', models.CharField(blank=True, max_length=64, null=True)),
                ('published_date', models.DateField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='library.author')),
            ],
        ),
        migrations.CreateModel(
            name='BookLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action_date', models.DateTimeField(null=True)),
                ('repayment_date', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField(default=0)),
                ('action_taken_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approve_book_loans', to='core.userprofile')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_loans', to='library.book')),
                ('request_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='req_book_loans', to='core.userprofile')),
            ],
        ),
    ]
