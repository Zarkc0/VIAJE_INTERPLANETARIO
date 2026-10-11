class Planeta:
    # Atributos de clase para conteo y almacenamiento global
    total_planetas = 0
    lista_planetas = []

    def __init__(self, nombre, distancia_sol_km):
        # Constructor
        self.nombre = nombre
        self.distancia_sol_km = distancia_sol_km
        Planeta.total_planetas += 1
        Planeta.lista_planetas.append(self)

    def __del__(self):
        # Destructor
        Planeta.total_planetas -= 1
        if self in Planeta.lista_planetas:
            Planeta.lista_planetas.remove(self)

    @classmethod
    def obtener_total_planetas(cls):
        # Método de clase
        return cls.total_planetas

    def __str__(self):
        return f"Planeta: {self.nombre} (Distancia al Sol: {self.distancia_sol_km:,.2f} km)"


class NaveEspacial:
    # Atributos de clase para conteo y almacenamiento global
    total_naves = 0
    lista_naves = []

    def __init__(self, nombre, velocidad_km_s, *misiones, **recursos):
        # Constructor con *args y **kwargs
        self.nombre = nombre
        self.velocidad_km_s = velocidad_km_s
        self.misiones = misiones          # Tupla de misiones (*args)
        self.recursos = recursos          # Diccionario de recursos (**kwargs)
        self.destino = None               # Instancia de Planeta asignada
        
        NaveEspacial.total_naves += 1
        NaveEspacial.lista_naves.append(self)

    def __del__(self):
        # Destructor
        NaveEspacial.total_naves -= 1
        if self in NaveEspacial.lista_naves:
            NaveEspacial.lista_naves.remove(self)

    @classmethod
    def obtener_total_naves(cls):
        # Método de clase
        return cls.total_naves

    def asignar_destino(self, planeta):
        # Método de instancia
        self.destino = planeta
        print(f"¡Destino '{planeta.nombre}' asignado con éxito a la nave {self.nombre}!")

    def calcular_tiempo_viaje(self):
        # Método de instancia para cálculo de tiempo
        if not self.destino:
            return "La nave no tiene un destino asignado."
        if self.velocidad_km_s <= 0:
            return "La velocidad de la nave debe ser mayor a 0."
        
        # Cálculo básico basado en distancia lineal y velocidad constante
        distancia = self.destino.distancia_sol_km
        tiempo_segundos = distancia / self.velocidad_km_s
        tiempo_horas = tiempo_segundos / 3600
        tiempo_dias = tiempo_horas / 24
        return tiempo_dias

    def mostrar_informacion(self):
        # Método de instancia
        info = f"\n--- Nave: {self.nombre} ---\n"
        info += f"Velocidad: {self.velocidad_km_s:,.2f} km/s\n"
        info += f"Destino actual: {self.destino.nombre if self.destino else 'Ninguno'}\n"
        info += f"Misiones (*args): {', '.join(self.misiones) if self.misiones else 'Ninguna'}\n"
        info += "Recursos (**kwargs):\n"
        if self.recursos:
            for clave, valor in self.recursos.items():
                info += f"  - {clave}: {valor}\n"
        else:
            info += "  - Ninguno\n"
        return info


def menu_interactivo():
    while True:
        print("\n========================================")
        print("    SIMULADOR DE VIAJES INTERPLANETARIOS")
        print("========================================")
        print(f"Planetas registrados: {Planeta.obtener_total_planetas()} | Naves registradas: {NaveEspacial.obtener_total_naves()}")
        print("1. Registrar planeta")
        print("2. Registrar nave espacial")
        print("3. Asignar destino")
        print("4. Calcular tiempo de viaje")
        print("5. Mostrar información")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()

        if opcion == "1":
            nombre = input("Nombre del planeta: ").strip()
            try:
                distancia = float(input("Distancia aproximada al Sol (en km): "))
                p = Planeta(nombre, distancia)
                print(f"¡Planeta '{nombre}' registrado correctamente!")
            except ValueError:
                print("Error: Ingresa un valor numérico válido para la distancia.")

        elif opcion == "2":
            nombre = input("Nombre de la nave: ").strip()
            try:
                velocidad = float(input("Velocidad de crucero (km/s): "))
                
                print("Introduce misiones adicionales separadas por coma (ej. Exploración, Escaneo, Minería):")
                misiones_input = input("Misiones: ")
                misiones = [m.strip() for m in misiones_input.split(",")] if misiones_input else []
                
                print("Introduce recursos en formato clave=valor (ej. combustible=5000 oxigeno=200 tripulantes=5). Presiona Enter si no deseas agregar:")
                recursos_input = input("Recursos: ").strip()
                recursos = {}
                if recursos_input:
                    for item in recursos_input.split():
                        if "=" in item:
                            k, v = item.split("=", 1)
                            recursos[k] = v

                n = NaveEspacial(nombre, velocidad, *misiones, **recursos)
                print(f"¡Nave '{nombre}' registrada con éxito!")
            except ValueError:
                print("Error: Asegúrate de ingresar números válidos en la velocidad.")

        elif opcion == "3":
            if not Planeta.lista_planetas or not NaveEspacial.lista_naves:
                print("Aviso: Debes tener al menos un planeta y una nave registrados.")
                continue
            
            print("\nNaves disponibles:")
            for i, n in enumerate(NaveEspacial.lista_naves):
                print(f"{i}. {n.nombre}")
            try:
                idx_nave = int(input("Selecciona el número de la nave: "))
                
                print("\nPlanetas disponibles:")
                for i, p in enumerate(Planeta.lista_planetas):
                    print(f"{i}. {p.nombre}")
                idx_planeta = int(input("Selecciona el número del planeta destino: "))
                
                NaveEspacial.lista_naves[idx_nave].asignar_destino(Planeta.lista_planetas[idx_planeta])
            except (ValueError, IndexError):
                print("Error: Selección numérica inválida.")

        elif opcion == "4":
            if not NaveEspacial.lista_naves:
                print("No hay naves registradas.")
                continue
            
            print("\nNaves disponibles:")
            for i, n in enumerate(NaveEspacial.lista_naves):
                print(f"{i}. {n.nombre}")
            try:
                idx_nave = int(input("Selecciona el número de la nave: "))
                nave = NaveEspacial.lista_naves[idx_nave]
                resultado = nave.calcular_tiempo_viaje()
                
                if isinstance(resultado, (int, float)):
                    print(f"\nEl viaje al planeta '{nave.destino.nombre}' tomará aproximadamente {resultado:,.2f} días.")
                else:
                    print(resultado)
            except (ValueError, IndexError):
                print("Error: Selección inválida.")

        elif opcion == "5":
            print("\n================ INFORMACIÓN GENERAL ================")
            print(f"Total de Planetas: {Planeta.obtener_total_planetas()}")
            for p in Planeta.lista_planetas:
                print(f" - {p}")
            
            print(f"\nTotal de Naves: {NaveEspacial.obtener_total_naves()}")
            for n in NaveEspacial.lista_naves:
                print(n.mostrar_informacion())
            print("=====================================================")

        elif opcion == "6":
            print("\nSaliendo del simulador. ¡Buen viaje, comandante!")
            break
        else:
            print("Opción inválida. Por favor, elige un número del 1 al 6.")


if __name__ == "__main__":
    menu_interactivo()
    