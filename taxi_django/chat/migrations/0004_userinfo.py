# Generated by Django 4.2.13 on 2024-06-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
                ('kakaopay_deeplink', models.CharField(max_length=255)),
                ('preferred_conditions', models.CharField(blank=True, max_length=255, null=True)),
                ('average_review_score', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
            ],
        ),
    ]
