import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog

class NutriInterface(ctk.CTk):
    def __init__(self, core_backend):
        super().__init__()
        
        self.core = core_backend  
        
        # Aumentamos para 640px para caber o novo botão de histórico
        self.title("Sistema de Nutrição - Controle de IMC")
        self.geometry("460x640")
        self.resizable(False, False)
        
        self.grid_columnconfigure(1, weight=1)
        
        # --- Componentes Visuais (Cadastro) ---
        
        self.label_titulo = ctk.CTkLabel(self, text="Cadastro de Pacientes", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, padx=20, pady=15)

        self.label_nome = ctk.CTkLabel(self, text="Nome do Cliente:", font=ctk.CTkFont(size=14))
        self.label_nome.grid(row=1, column=0, padx=20, pady=8, sticky="w")
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Ex: João Silva")
        self.entry_nome.grid(row=1, column=1, padx=20, pady=8, sticky="ew")

        self.label_idade = ctk.CTkLabel(self, text="Idade:", font=ctk.CTkFont(size=14))
        self.label_idade.grid(row=2, column=0, padx=20, pady=8, sticky="w")
        self.entry_idade = ctk.CTkEntry(self, placeholder_text="Ex: 28")
        self.entry_idade.grid(row=2, column=1, padx=20, pady=8, sticky="ew")

        self.label_genero = ctk.CTkLabel(self, text="Gênero:", font=ctk.CTkFont(size=14))
        self.label_genero.grid(row=3, column=0, padx=20, pady=8, sticky="w")
        self.combo_genero = ctk.CTkComboBox(self, values=["Feminino", "Masculino", "Outro"], state="readonly")
        self.combo_genero.grid(row=3, column=1, padx=20, pady=8, sticky="ew")
        self.combo_genero.set("Feminino")

        self.label_altura = ctk.CTkLabel(self, text="Altura (m):", font=ctk.CTkFont(size=14))
        self.label_altura.grid(row=4, column=0, padx=20, pady=8, sticky="w")
        self.entry_altura = ctk.CTkEntry(self, placeholder_text="Ex: 1.75")
        self.entry_altura.grid(row=4, column=1, padx=20, pady=8, sticky="ew")

        self.label_peso = ctk.CTkLabel(self, text="Peso (kg):", font=ctk.CTkFont(size=14))
        self.label_peso.grid(row=5, column=0, padx=20, pady=8, sticky="w")
        self.entry_peso = ctk.CTkEntry(self, placeholder_text="Ex: 72.3")
        self.entry_peso.grid(row=5, column=1, padx=20, pady=8, sticky="ew")

        self.btn_gerar = ctk.CTkButton(self, text="GERAR IMC", font=ctk.CTkFont(size=15, weight="bold"), command=self.acao_gerar_imc)
        self.btn_gerar.grid(row=6, column=0, columnspan=2, padx=20, pady=12, sticky="ew")

        self.btn_baixar = ctk.CTkButton(
            self, text="BAIXAR PLANILHA (EXCEL)", font=ctk.CTkFont(size=14, weight="bold"), 
            fg_color="transparent", border_width=2, text_color=("black", "white"), command=self.acao_baixar_planilha
        )
        self.btn_baixar.grid(row=7, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        # --- SEÇÃO DE BUSCA E EXCLUSÃO (GERENCIAMENTO) ---
        
        self.separador = ctk.CTkLabel(self, text="──────────────────────────────────────────", text_color="gray")
        self.separador.grid(row=8, column=0, columnspan=2, pady=5)

        self.label_titulo_gerencia = ctk.CTkLabel(self, text="Consultar ou Remover Paciente", font=ctk.CTkFont(size=15, weight="bold"))
        self.label_titulo_gerencia.grid(row=9, column=0, columnspan=2, pady=5)

        self.label_gerencia_mat = ctk.CTkLabel(self, text="Matrícula (5 dígitos):", font=ctk.CTkFont(size=13))
        self.label_gerencia_mat.grid(row=10, column=0, padx=20, pady=5, sticky="w")
        self.entry_gerencia_matricula = ctk.CTkEntry(self, placeholder_text="Ex: 12345")
        self.entry_gerencia_matricula.grid(row=10, column=1, padx=20, pady=5, sticky="ew")

        # NOVO BOTÃO: Para ver a lista de matrículas caso tenha esquecido
        self.btn_esqueci_mat = ctk.CTkButton(
            self, text="Esqueceu a matrícula? Ver Histórico", font=ctk.CTkFont(size=11, underline=True),
            fg_color="transparent", text_color="gray", hover=False, command=self.acao_ver_historico_matriculas
        )
        self.btn_esqueci_mat.grid(row=11, column=0, columnspan=2, padx=20, pady=2, sticky="e")

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=12, column=0, columnspan=2, pady=10, sticky="ew")
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

        self.btn_buscar = ctk.CTkButton(self.frame_botoes, text="BUSCAR", font=ctk.CTkFont(size=13, weight="bold"), command=self.acao_buscar_paciente)
        self.btn_buscar.grid(row=0, column=0, padx=(20, 5), sticky="ew")

        self.btn_deletar = ctk.CTkButton(self.frame_botoes, text="APAGAR", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#c0392b", hover_color="#962d22", command=self.acao_deletar_paciente)
        self.btn_deletar.grid(row=0, column=1, padx=(5, 20), sticky="ew")

    # --- FUNÇÕES DE AÇÃO DOS BOTÕES ---

    def acao_gerar_imc(self):
        try:
            resultado = self.core.salvar_paciente(
                nome=self.entry_nome.get(), idade_str=self.entry_idade.get(),
                genero=self.combo_genero.get(), altura_str=self.entry_altura.get(), peso_str=self.entry_peso.get()
            )
            messagebox.showinfo("Paciente Registrado", f"Dados salvos!\n\nMatrícula: {resultado['matricula']}\nIMC: {resultado['imc']} ({resultado['classificacao']})")
            self.limpar_campos()
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))

    def acao_baixar_planilha(self):
        try:
            caminho_escolhido = filedialog.asksaveasfilename(title="Escolha onde baixar a planilha", initialfile="relatorio_pacientes.xlsx", defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
            if caminho_escolhido:
                self.core.exportar_planilha(caminho_escolhido)
                messagebox.showinfo("Sucesso!", "Planilha salva com sucesso!")
        except Exception as erro:
            messagebox.showerror("Erro ao Exportar", str(erro))

    def acao_buscar_paciente(self):
        matricula = self.entry_gerencia_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Campo Vazio", "Por favor, digite a matrícula para buscar.")
            return
        try:
            cliente = self.core.buscar_paciente(matricula)
            ficha = (
                f"--- FICHA DO CLIENTE ---\n\nNome: {cliente['nome']}\nIdade: {cliente['idade']} anos\nGênero: {cliente['genero'].upper()}\nAltura: {cliente['altura']} m\nPeso: {cliente['peso']} kg\n\n"
                f"--- RESULTADO ---\nIMC Calculado: {cliente['imc']}\nClassificação: {cliente['classificacao']}"
            )
            messagebox.showinfo(f"Matrícula {matricula}", ficha)
            self.entry_gerencia_matricula.delete(0, 'end')
        except Exception as erro:
            messagebox.showerror("Erro na Busca", str(erro))

    def acao_deletar_paciente(self):
        matricula = self.entry_gerencia_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Campo Vazio", "Por favor, digite a matrícula para apagar.")
            return
        confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Deseja remover a matrícula {matricula}?\nEsta ação não pode ser desfeita.")
        if confirmacao:
            try:
                self.core.deletar_paciente(matricula)
                messagebox.showinfo("Sucesso!", f"Paciente {matricula} removido.")
                self.entry_gerencia_matricula.delete(0, 'end')
            except Exception as erro:
                messagebox.showerror("Erro na Exclusão", str(erro))

    def acao_ver_historico_matriculas(self):
        """Busca no Excel todos os clientes e exibe uma lista rápida de Nomes e Matrículas."""
        try:
            historico = self.core.listar_historico_matriculas()
            
            if not historico:
                messagebox.showinfo("Histórico", "Nenhum paciente cadastrado até o momento.")
                return
            
            # Monta o texto que vai aparecer no pop-up
            texto_lista = "--- LISTA DE MATRÍCULAS ---\n\n"
            for cliente in historico:
                texto_lista += f"ID: {cliente['matricula']}  ->  Nome: {cliente['nome']}\n"
                
            messagebox.showinfo("Histórico do Consultório", texto_lista)
            
        except Exception as erro:
            messagebox.showerror("Erro ao carregar histórico", str(erro))

    def limpar_campos(self):
        self.entry_nome.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_altura.delete(0, 'end')
        self.entry_peso.delete(0, 'end')
        self.combo_genero.set("Feminino")