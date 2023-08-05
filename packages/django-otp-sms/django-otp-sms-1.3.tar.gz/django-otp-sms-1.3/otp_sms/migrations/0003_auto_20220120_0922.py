# Generated by Django 2.2.12 on 2022-01-20 06:22

from django.db import migrations, models
import otp_sms.models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_sms', '0002_auto_20161114_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsdevice',
            name='code',
            field=models.CharField(help_text='The code to verify call', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='smsdevice',
            name='key',
            field=models.CharField(default=otp_sms.models.default_key, help_text='A random key used to generate tokens (hex-encoded).', max_length=40, validators=[otp_sms.models.key_validator]),
        ),
        migrations.AlterField(
            model_name='smsdevice',
            name='last_t',
            field=models.BigIntegerField(default=-1, help_text='The t value of the latest verified token. The next token must be at a higher time step.'),
        ),
    ]
