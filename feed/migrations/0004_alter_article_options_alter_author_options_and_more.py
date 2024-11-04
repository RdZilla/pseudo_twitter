# Generated by Django 5.1.2 on 2024-10-24 00:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_alter_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='comment',
            name='count_of_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.author', verbose_name='Автор записи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='Текст записи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='author',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='Полное имя автора'),
        ),
        migrations.AlterField(
            model_name='author',
            name='registration_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата регистрации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='feed.article', verbose_name='Запись'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.author', verbose_name='Автор комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.CharField(max_length=200, verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.CreateModel(
            name='LikeOnComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('&#128077;', 'like'), ('&#128557;', 'cry'), ('&#128562;', 'surprise'), ('&#128514;', 'laugh'), ('&#129505;', 'hearth')], max_length=50, verbose_name='Текстовый код эмоции')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.comment')),
            ],
            options={
                'verbose_name': 'Лайк на комментарии',
                'verbose_name_plural': 'Лайки на комментариях',
            },
        ),
    ]