from django.db import migrations, models





class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, choices=[
                    (0, 'Electric'),
                    (1, 'Petrol'),
                    (2, 'Gasoline'),
                    (3, 'CNG'),
                    (4, 'LPG'),
                ])),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('unit', models.CharField(max_length=5)),
            ],
        ),
    ]
