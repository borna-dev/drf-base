# Generated by Django 4.2.2 on 2023-06-16 15:27
# make custom migration
# python manage.py makemigrations --empty --name <migration_name> <app_name>

from django.db import migrations, models
import django.db.models.deletion


def fix_data(apps, schema_editor):
    Article = apps.get_model("news", "Article")
    Journalist = apps.get_model("news", "Journalist")
    for article in Article.objects.all():
        name, *_, surname = article.author.split()
        journalist = Journalist(name=name, surname=surname)
        journalist.save()
        article.author_id = journalist
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_journalist_alter_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='news.journalist'),
        ),
        migrations.RunPython(fix_data),
        migrations.RemoveField(
            model_name='Article',
            name='author',
        ),
        migrations.RenameField(
            model_name='Article',
            old_name='author_id',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='news.journalist'),
        ),
    ]
