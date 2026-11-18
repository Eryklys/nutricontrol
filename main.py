import customtkinter as ctk
from core import NutriCore
from gui import NutriInterface

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    backend = NutriCore()
    app = NutriInterface(core_backend=backend)
    app.mainloop()

if __name__ == "__main__":
    main()