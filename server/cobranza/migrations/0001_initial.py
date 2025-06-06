from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListaCobroDetalle2022',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idListaCobro', models.IntegerField()),
                ('idCredito', models.IntegerField()),
                ('consecutivoCobro', models.CharField(max_length=20)),
                ('idBanco', models.IntegerField()),
                ('montoExigible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fechaCobroBanco', models.DateTimeField(blank=True, null=True)),
                ('idRespuestaBanco', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'ListaCobroDetalle2022',
            },
        ),
        migrations.CreateModel(
            name='ListaCobroDetalle2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idListaCobro', models.IntegerField()),
                ('idCredito', models.IntegerField()),
                ('consecutivoCobro', models.CharField(max_length=20)),
                ('idBanco', models.IntegerField()),
                ('montoExigible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fechaCobroBanco', models.DateTimeField(blank=True, null=True)),
                ('idRespuestaBanco', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'ListaCobroDetalle2023',
            },
        ),
        migrations.CreateModel(
            name='ListaCobroDetalle2024',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idListaCobro', models.IntegerField()),
                ('idCredito', models.IntegerField()),
                ('consecutivoCobro', models.CharField(max_length=20)),
                ('idBanco', models.IntegerField()),
                ('montoExigible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fechaCobroBanco', models.DateTimeField(blank=True, null=True)),
                ('idRespuestaBanco', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'ListaCobroDetalle2024',
            },
        ),
        migrations.CreateModel(
            name='ListaCobroDetalle2025',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idListaCobro', models.IntegerField()),
                ('idCredito', models.IntegerField()),
                ('consecutivoCobro', models.CharField(max_length=20)),
                ('idBanco', models.IntegerField()),
                ('montoExigible', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montoCobrado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fechaCobroBanco', models.DateTimeField(blank=True, null=True)),
                ('idRespuestaBanco', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'ListaCobroDetalle2025',
            },
        ),
    ]