from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.CharField(max_length=500)),
                ('creator_introduction', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'creator',
            },
        ),
        migrations.CreateModel(
            name='SNS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'sns',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, null=True)),
                ('password', models.IntegerField(default=0)),
                ('phone_number', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50, null=True)),
                ('nickname', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.creator')),
            ],
            options={
                'db_table': 'hashtag',
            },
        ),
        migrations.CreateModel(
            name='CreatorSNS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sns_account', models.CharField(max_length=50, null=True)),
                ('sns_address', models.CharField(max_length=50, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.creator')),
                ('sns', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.sns')),
            ],
            options={
                'db_table': 'creator_sns',
            },
        ),
        migrations.AddField(
            model_name='creator',
            name='sns_name',
            field=models.ManyToManyField(null=True, through='user.CreatorSNS', to='user.SNS'),
        ),
        migrations.AddField(
            model_name='creator',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
