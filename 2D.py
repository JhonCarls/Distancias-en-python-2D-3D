import tkinter as tk
from tkinter import simpledialog
import math

class PlanoCartesiano(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Plano Cartesiano")
        self.geometry("800x800")
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.puntos = []
        self.lineas = []

        self.btn_agregar_puntos = tk.Button(self, text="Agregar Puntos", command=self.agregar_puntos)
        self.btn_agregar_puntos.pack()

        self.bind("<Configure>", self.crear_ejes)

    def crear_ejes(self, event=None):
        self.canvas.delete("ejes")
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        # Eje X
        self.canvas.create_line(0, alto/2, ancho, alto/2, fill="black", tags="ejes")
        # Eje Y
        self.canvas.create_line(ancho/2, 0, ancho/2, alto, fill="black", tags="ejes")

    def agregar_puntos(self):
        entrada = simpledialog.askstring("Entrada", "Ingrese las coordenadas de los puntos (formato x1,y1 x2,y2):")
        if entrada:
            try:
                puntos = [tuple(map(int, p.split(','))) for p in entrada.split()]
                for punto in puntos:
                    self.puntos.append(punto)
                    self.dibujar_punto(*punto)
                if len(self.puntos) >= 2:
                    self.dibujar_linea(self.puntos[-2], self.puntos[-1])
            except ValueError:
                print("Formato inválido. Ingrese las coordenadas como x1,y1 x2,y2")

    def dibujar_punto(self, x, y):
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        canvas_x = ancho / 2 + x
        canvas_y = alto / 2 - y

        self.canvas.create_oval(canvas_x-3, canvas_y-3, canvas_x+3, canvas_y+3, fill="black")
        self.canvas.create_text(canvas_x + 10, canvas_y, text=f"({x},{y})", anchor=tk.W)

    def dibujar_linea(self, p1, p2):
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        x1, y1 = p1
        x2, y2 = p2

        canvas_x1 = ancho / 2 + x1
        canvas_y1 = alto / 2 - y1
        canvas_x2 = ancho / 2 + x2
        canvas_y2 = alto / 2 - y2

        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue")

        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        self.lineas.append((p1, p2, distancia))
        self.actualizar_distancias()

    def actualizar_distancias(self):
        self.canvas.delete("distancia")
        for (p1, p2, distancia) in self.lineas:
            x1, y1 = p1
            x2, y2 = p2

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

            ancho = self.canvas.winfo_width()
            alto = self.canvas.winfo_height()
            canvas_mid_x = ancho / 2 + mid_x
            canvas_mid_y = alto / 2 - mid_y

            self.canvas.create_text(canvas_mid_x, canvas_mid_y, text=f"{distancia:.2f}", tags="distancia", fill="red")

if __name__ == "__main__":
    app = PlanoCartesiano()
    app.mainloop()
