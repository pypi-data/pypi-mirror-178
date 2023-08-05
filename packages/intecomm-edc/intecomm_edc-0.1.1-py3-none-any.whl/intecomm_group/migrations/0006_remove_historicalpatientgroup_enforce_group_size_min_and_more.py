# Generated by Django 4.1.2 on 2022-11-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intecomm_group", "0005_patientfollowupcall_historicalpatientfollowupcall"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalpatientgroup",
            name="enforce_group_size_min",
        ),
        migrations.RemoveField(
            model_name="historicalpatientgroup",
            name="enforce_ratio",
        ),
        migrations.RemoveField(
            model_name="patientgroup",
            name="enforce_group_size_min",
        ),
        migrations.RemoveField(
            model_name="patientgroup",
            name="enforce_ratio",
        ),
        migrations.AddField(
            model_name="historicalpatientgroup",
            name="bypass_group_ratio",
            field=models.BooleanField(
                default=False,
                help_text="If ticked, you must have consulted with your study coordinator first",
                verbose_name="Bypass 2:1 NCD:HIV ratio",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatientgroup",
            name="bypass_group_size_min",
            field=models.BooleanField(
                default=False,
                help_text="If ticked, you must have consulted with your study coordinator first",
                verbose_name="Bypass group size minimum of 14",
            ),
        ),
        migrations.AddField(
            model_name="patientgroup",
            name="bypass_group_ratio",
            field=models.BooleanField(
                default=False,
                help_text="If ticked, you must have consulted with your study coordinator first",
                verbose_name="Bypass 2:1 NCD:HIV ratio",
            ),
        ),
        migrations.AddField(
            model_name="patientgroup",
            name="bypass_group_size_min",
            field=models.BooleanField(
                default=False,
                help_text="If ticked, you must have consulted with your study coordinator first",
                verbose_name="Bypass group size minimum of 14",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientgroup",
            name="confirm_randomize_now",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                verbose_name="If YES, please confirm by typing the word RANDOMIZE here",
            ),
        ),
        migrations.AlterField(
            model_name="patientgroup",
            name="confirm_randomize_now",
            field=models.CharField(
                blank=True,
                max_length=15,
                null=True,
                verbose_name="If YES, please confirm by typing the word RANDOMIZE here",
            ),
        ),
    ]
