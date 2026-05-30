import tkinter as tk
from estructuras.arbol_decision import ArbolDecision
from logica.juego import ControladorJuego
from interfaz.ventana_principal import VentanaTotito

if __name__ == "__main__":
    root = tk.Tk()
    ai = ArbolDecision()
    game_control = ControladorJuego(ai)
    app = VentanaTotito(root, game_control)
    root.mainloop()
