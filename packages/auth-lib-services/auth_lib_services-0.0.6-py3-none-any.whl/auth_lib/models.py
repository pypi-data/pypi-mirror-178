from django.contrib.auth.models import AbstractBaseUser

class Rol():
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

class Facultad():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Program():
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def set_facultad_from_dict(self, data):
        self.facultad = Facultad(data['id'], data['name'])

class TokenUser(AbstractBaseUser):
    def from_json(self, data):
        self.id = data['id']
        self.is_active = data['is_active']
        if 'program' in data:
            self.program = Program(data['program']['id'], data['program']['name'])
            self.program.set_facultad_from_dict(data['program']['facultad'])

        self.roles = []
        for rol in data['roles']:
            self.roles.append(Rol(id=rol['id'], name=rol['name']))

    class Meta:
        managed = False