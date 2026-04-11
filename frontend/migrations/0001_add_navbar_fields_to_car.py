from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.AddField(
            model_name='car',
            name='navbar_photo',
            field=models.ImageField(blank=True, null=True, upload_to='cars/navbar/', verbose_name='Фото для навбара'),
        ),
        migrations.AddField(
            model_name='car',
            name='navbar_position',
            field=models.PositiveIntegerField(default=0, verbose_name='Позиция в навбаре'),
        ),
    ]
