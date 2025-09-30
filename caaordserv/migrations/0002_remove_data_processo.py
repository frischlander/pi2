from django.db import migrations

def remove_data_processo(apps, schema_editor):
    OrdemServico = apps.get_model('caaordserv', 'OrdemServico')
    for ordem in OrdemServico.objects.all():
        # Extrai apenas o número do processo (remove a data)
        numero = ordem.processo.split('/')[0]
        ordem.processo = numero
        ordem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('caaordserv', '0006_ordemservico_ultimo_usuario_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_data_processo),
    ] 