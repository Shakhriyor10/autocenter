from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('short_description', models.CharField(max_length=255, verbose_name='Короткое описание')),
                ('image', models.ImageField(upload_to='banners/', verbose_name='Фото')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ('sort_order', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название бренда')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180, verbose_name='Название')),
                ('model_name', models.CharField(max_length=180, verbose_name='Название модели')),
                ('engine_type', models.CharField(choices=[('turbo', 'Турбина'), ('electric', 'Электрический'), ('hybrid', 'Гибрид'), ('atmospheric', 'Атмосферный'), ('diesel', 'Дизель')], default='atmospheric', max_length=20, verbose_name='Тип двигателя')),
                ('engine_volume', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='Объем двигателя (л)')),
                ('transmission_type', models.CharField(choices=[('automatic', 'Автомат'), ('manual', 'Механика'), ('robot', 'Робот'), ('cvt', 'Вариатор')], default='automatic', max_length=20, verbose_name='Коробка передач')),
                ('photo_1', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото 1')),
                ('photo_2', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото 2')),
                ('photo_3', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото 3')),
                ('photo_4', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото 4')),
                ('photo_5', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Фото 5')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена со скидкой')),
                ('discount_until', models.DateField(blank=True, null=True, verbose_name='Скидка до')),
                ('is_hot', models.BooleanField(default=False, verbose_name='Горячий продукт')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cars', to='frontend.brand', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
                'ordering': ('-created_at',),
            },
        ),
    ]
