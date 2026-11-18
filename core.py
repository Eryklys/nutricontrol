import os
import random
import shutil  # Biblioteca nativa para copiar arquivos
from openpyxl import Workbook, load_workbook

class NutriCore:
    def __init__(self, arquivo_excel="registro_pacientes.xlsx"):
        self.arquivo_excel = arquivo_excel
        self._inicializar_planilha()

    def _inicializar_planilha(self):
        """Cria a planilha com os cabeçalhos caso ela ainda não exista."""
        if not os.path.exists(self.arquivo_excel):
            wb = Workbook()
            ws = wb.active
            ws.title = "Pacientes"
            ws.append(["Matrícula", "Nome", "Idade", "Gênero", "Altura (m)", "Peso (kg)", "IMC", "Classificação"])
            wb.save(self.arquivo_excel)

    def calcular_imc(self, peso, altura):
        """Calcula o IMC e retorna o valor e a classificação."""
        imc = peso / (altura ** 2)
        
        if imc < 18.5:
            classificacao = "Abaixo do peso"
        elif imc < 25:
            classificacao = "Peso normal"
        elif imc < 30:
            classificacao = "Sobrepeso"
        else:
            classificacao = "Obesidade"
            
        return round(imc, 2), classificacao

    def gerar_matricula(self):
        """Gera uma matrícula aleatória de 5 dígitos."""
        return random.randint(10000, 99999)

    def salvar_paciente(self, nome, idade_str, genero, altura_str, peso_str):
        """Valida os dados, processa e salva diretamente no Excel."""
        nome = nome.strip()
        altura_str = altura_str.strip().replace(',', '.')
        peso_str = peso_str.strip().replace(',', '.')

        if not (nome and idade_str and genero and altura_str and peso_str):
            raise ValueError("Todos os campos devem ser preenchidos!")

        try:
            idade = int(idade_str)
            altura = float(altura_str)
            peso = float(peso_str)
        except ValueError:
            raise ValueError("Idade, Altura e Peso precisam ser valores numéricos válidos.")

        imc, classificacao = self.calcular_imc(peso, altura)
        matricula = self.gerar_matricula()

        wb = load_workbook(self.arquivo_excel)
        ws = wb.active
        ws.append([matricula, nome, idade, genero, altura, peso, imc, classificacao])
        wb.save(self.arquivo_excel)

        return {
            "matricula": matricula,
            "imc": imc,
            "classificacao": classificacao
        }

    def exportar_planilha(self, caminho_destino):
        """Copia a planilha atual para o caminho escolhido pelo usuário."""
        if not os.path.exists(self.arquivo_excel):
            raise FileNotFoundError("Ainda não existem dados registrados para exportar.")
        
        # Copia o arquivo local para o destino escolhido pela nutricionista
        shutil.copy(self.arquivo_excel, caminho_destino)

    # ==========================================
    # NOVAS FUNÇÕES ADICIONADAS AQUI NO FINAL!
    # ==========================================

    def deletar_paciente(self, matricula_str):
        """Busca um paciente pela matrícula e o remove da planilha Excel."""
        matricula_str = matricula_str.strip()
        
        if not matricula_str:
            raise ValueError("Por favor, insira uma matrícula para exclusão.")
        
        try:
            matricula_alvo = int(matricula_str)
        except ValueError:
            raise ValueError("A matrícula inserida deve conter apenas números.")

        if not os.path.exists(self.arquivo_excel):
            raise FileNotFoundError("Nenhum registro de pacientes foi encontrado ainda.")

        wb = load_workbook(self.arquivo_excel)
        ws = wb.active

        foi_deletado = False
        
        # Percorre as linhas do Excel (da última para a primeira)
        for linha in range(ws.max_row, 1, -1):
            if ws.cell(row=linha, column=1).value == matricula_alvo:
                ws.delete_rows(linha)
                foi_deletado = True
                break

        if foi_deletado:
            wb.save(self.arquivo_excel)
            return True
        else:
            raise ValueError(f"A matrícula {matricula_alvo} não foi encontrada no sistema.")

    def buscar_paciente(self, matricula_str):
        """Busca um paciente pela matrícula e retorna sua ficha completa."""
        matricula_str = matricula_str.strip()
        
        if not matricula_str:
            raise ValueError("Por favor, insira uma matrícula para buscar.")
        
        try:
            matricula_alvo = int(matricula_str)
        except ValueError:
            raise ValueError("A matrícula inserida deve conter apenas números.")

        if not os.path.exists(self.arquivo_excel):
            raise FileNotFoundError("Nenhum registro de pacientes foi encontrado ainda.")

        wb = load_workbook(self.arquivo_excel)
        ws = wb.active

        # Varre a planilha procurando a matrícula
        for linha in range(2, ws.max_row + 1):
            if ws.cell(row=linha, column=1).value == matricula_alvo:
                # Monta o "dicionário" de dados para a interface
                cliente = {
                    "nome": ws.cell(row=linha, column=2).value,
                    "idade": ws.cell(row=linha, column=3).value,
                    "genero": ws.cell(row=linha, column=4).value,
                    "altura": ws.cell(row=linha, column=5).value,
                    "peso": ws.cell(row=linha, column=6).value,
                    "imc": ws.cell(row=linha, column=7).value,
                    "classificacao": ws.cell(row=linha, column=8).value
                }
                return cliente
                
        # Se não encontrar ninguém
        raise ValueError(f"O ID {matricula_alvo} não foi encontrado no sistema.")
    
    def listar_historico_matriculas(self):
        """Retorna uma lista de dicionários contendo apenas Nome e Matrícula de todos os pacientes."""
        if not os.path.exists(self.arquivo_excel):
            raise FileNotFoundError("Nenhum registro de pacientes foi encontrado ainda.")

        wb = load_workbook(self.arquivo_excel)
        ws = wb.active

        lista_clientes = []
        
        # Percorre da linha 2 (pulando o cabeçalho) até a última linha preenchida
        for linha in range(2, ws.max_row + 1):
            matricula = ws.cell(row=linha, column=1).value
            nome = ws.cell(row=linha, column=2).value
            
            # Se a linha não estiver vazia, adiciona na lista
            if matricula and nome:
                lista_clientes.append({
                    "matricula": matricula,
                    "nome": nome
                })
                
        return lista_clientes