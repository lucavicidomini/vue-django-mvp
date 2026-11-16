from django.db import migrations, models





class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('unit', models.CharField(max_length=5)),
                ('inverted', models.BooleanField()),
            ],
        ),
    ]
