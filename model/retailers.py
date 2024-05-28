from dataclasses import dataclass
@dataclass
class Retailer:
    Retailer_code:int
    Retailer_name:str
    Type:str
    Country:str

    def __hash__(self):
        return hash(self.Retailer_code)

    def __str__(self):
        return f'Code: {self.Retailer_code}, nome: {self.Retailer_name}'