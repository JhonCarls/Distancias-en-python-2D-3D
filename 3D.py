import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tkinter import Tk, simpledialog

class PlanoCartesiano3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.puntos = []
        self.lineas = []

        self.root = Tk()
        self.root.withdraw()  # Ocultar la ventana principal de Tkinter
        self.agregar_puntos()

    def agregar_puntos(self):
        while True:
            entrada = simpledialog.askstring("Entrada", "Ingrese las coordenadas de los puntos (formato x1,y1,z1 x2,y2,z2), o 'salir' para terminar:")
            if entrada.lower() == 'salir':
                break
            if entrada:
                try:
                    puntos = [tuple(map(float, p.split(','))) for p in entrada.split()]
                    for punto in puntos:
                        self.puntos.append(punto)
                        self.dibujar_punto(*punto)
                    if len(self.puntos) >= 2:
                        self.dibujar_linea(self.puntos[-2], self.puntos[-1])
                except ValueError:
                    print("Formato inválido. Ingrese las coordenadas como x1,y1,z1 x2,y2,z2")

        plt.show()

    def dibujar_punto(self, x, y, z):
        self.ax.scatter(x, y, z, color='black')
        self.ax.text(x, y, z, f"({x},{y},{z})")

    def dibujar_linea(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2

        self.ax.plot([x1, x2], [y1, y2], [z1, z2], color='blue')

        distancia = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        self.lineas.append((p1, p2, distancia))

        mid_x, mid_y, mid_z = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
        self.ax.text(mid_x, mid_y, mid_z, f"{distancia:.2f}", color='red')

if __name__ == "__main__":
    app = PlanoCartesiano3D()
