# Generated by Django 4.2.4 on 2024-02-28 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0003_follow_follow_alter_comment_comment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="comment_time",
            field=models.DateField(auto_now=True),
        ),
    ]
