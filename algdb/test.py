import sys, os,django

projectPath=r"D:\MasterDissert\algdb"
sys.path.append(projectPath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'algdb.settings'
django.setup()

import core.models as models

for i in sys.argv:
	print(i)

for i in models.Slot.objects.all():
	print(i.name+'\n');