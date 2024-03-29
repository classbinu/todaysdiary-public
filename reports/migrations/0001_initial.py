# Generated by Django 4.0.2 on 2022-03-19 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', '주제 신고'), ('2', '일기 신고'), ('3', '댓글 신고'), ('4', '주제 제안'), ('5', '기능 제안'), ('0', '기타')], max_length=10)),
                ('ref', models.CharField(blank=True, max_length=10)),
                ('content', models.TextField(blank=True, max_length=200)),
                ('state', models.CharField(choices=[('open', '접수'), ('closed', '완료')], default='open', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='report', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]