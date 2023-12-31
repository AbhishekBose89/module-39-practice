# Generated by Django 4.1.9 on 2023-07-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('rating', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('authors', models.ManyToManyField(related_name='books', to='restapi.author')),
            ],
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['-price', 'title'], name='price-title-index'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['price'], name='price-index'),
        ),
    ]
