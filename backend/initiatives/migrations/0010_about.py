# Generated by Django 3.1.5 on 2021-02-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0009_auto_20210210_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('order', models.IntegerField(default=1, verbose_name='Order')),
                ('type', models.CharField(choices=[('TITLE', 'Title'), ('TXT', 'Text'), ('IMG', 'Image'), ('YT', 'YoutubeEmbed')], default='TITLE', max_length=5, verbose_name='About type status')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
