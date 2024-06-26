# Generated by Django 4.1.7 on 2023-03-16 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policymanagement', '0002_rename_evidence_date_evidencedata_evidence_data_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorePolicy',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('fields_info', models.TextField()),
                ('blockly_json', models.TextField()),
                ('generated_code', models.TextField(default='')),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyVerificationReport',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('network_name', models.CharField(max_length=255)),
                ('submitted_policy_details', models.TextField()),
                ('verification_result', models.TextField()),
                ('status', models.CharField(choices=[('submitted', 'submitted'), ('running', 'running'), ('completed', 'completed'), ('failed', 'failed')], default='submitted', max_length=255)),
                ('passed', models.BooleanField(default=False)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('completed_on', models.DateTimeField(null=True)),
                ('log_from_timestamp', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredPolicyDetails',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('network_name', models.CharField(max_length=255)),
                ('core_policy_label', models.CharField(max_length=255)),
                ('core_policy_type', models.CharField(max_length=255)),
                ('policy_description', models.TextField()),
                ('policy_config', models.TextField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='evidencedata',
            name='selected_controller_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='evidencedata',
            name='selected_host_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='evidencedata',
            name='selected_switch_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
