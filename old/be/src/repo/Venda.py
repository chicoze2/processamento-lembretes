class Venda:
    def __init__(self, chassi, modelo, nome, contato, local, data):
        self.chassi = chassi
        self.modelo = modelo
        self.nome = nome
        self.contato = contato
        self.local = local
        self.data = data

    def __str__(self):
        return f"Chassi: {self.chassi}\nModelo: {self.modelo}\nNome: {self.nome}\nContato: {self.contato}\nLocal: {self.local}\nData: {self.data}"
    
    def padronizar_dados(self):
        self.modelo = self.modelo.strip()
        self.nome = self.nome.strip()
        self.contato = self.contato.strip().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        self.local = self.local.strip()
        self.data = self.data.strftime("%d/%m/%Y")
