# Generated by Django 2.2.3 on 2019-08-10 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shoppingcart.UserCoupon'),
        ),
    ]
