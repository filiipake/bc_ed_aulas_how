import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome  = sobrenome
        self.data_de_nascimento = data_de_nascimento
    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos."
# ------

rafael = Pessoa(nome= 'Rafael', sobrenome='Filipake', data_de_nascimento=datetime.date(1995, 5, 17))
print(rafael)
print(rafael.nome)
print(rafael.sobrenome)
print(rafael.data_de_nascimento)
print(rafael.idade)