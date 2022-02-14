import datetime
import math
from typing import List


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

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]) -> None:
        self.pessoa = pessoa
        self.experiencias = experiencias
    
    @property
    def quantidade_experiencias(self) -> int:
        return len(self.experiencias)
    
    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, newExperience: str) -> None:
        self.experiencias.append(newExperience)
    
    def __str__(self) -> str:
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já " \
            f"trabalhou em {self.quantidade_experiencias} empresas e atualmente trabalha na empresa {self.empresa_atual}"


rafael = Pessoa(nome= 'Rafael', sobrenome='Filipake', data_de_nascimento=datetime.date(1995, 5, 17))
print(rafael)

curriculo_rafael = Curriculo(pessoa=rafael, experiencias=['Foursales', 'Esparta', 'Justen Advocacia'])

print(curriculo_rafael.pessoa)
print(curriculo_rafael)
curriculo_rafael.adiciona_experiencia('How Education')
print(curriculo_rafael)

class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date):
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

class PessoaHer(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos."

rafael2 = PessoaHer(nome='rafael', data_de_nascimento=datetime.date(1995, 5, 17))

class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str):
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def __str__(self) -> str:
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos."

dog = Cachorro(nome='estrela', data_de_nascimento=datetime.date(1995, 5, 17), raca = 'bordercollie')
print(dog)