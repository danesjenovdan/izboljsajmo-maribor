# Generated by Django 3.1.5 on 2022-01-28 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0032_auto_20210920_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Ustvarjeno')),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Urejano')),
                ('initiative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_history', to='initiatives.initiative', verbose_name='Pobuda')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_history', to='initiatives.alladminuser', verbose_name='Reviewer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='initiative',
            name='reviewer_user_history',
            field=models.ManyToManyField(blank=True, null=True, through='initiatives.ReviewerHistory', to='initiatives.AllAdminUser', verbose_name='Reviewer history'),
        ),
    ]
