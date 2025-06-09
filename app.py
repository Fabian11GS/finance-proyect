from tkinter import messagebox
from datetime import timedelta
from datetime import datetime
import customtkinter as ctk
import json
import threading
import time


ARCHIVO_DATOS = "finanzas.json"

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"planes": [], "gastos": []}

class ControlGastosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Control de Gastos")
        self.geometry("800x600")
        self.datos = cargar_datos()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frames principales
        self.frame_izquierdo = ctk.CTkFrame(self, width=400)
        self.frame_izquierdo.pack(side="left", fill="both", expand=True)

        self.frame_derecho = ctk.CTkFrame(self, width=400)
        self.frame_derecho.pack(side="right", fill="both", expand=True)

        # Botones principales
        self.btn_crear_plan = ctk.CTkButton(self.frame_derecho, text="Crear Plan de Ahorro", command=self.crear_plan)
        self.btn_crear_plan.pack(pady=10, padx=20)

        self.btn_registrar_gasto = ctk.CTkButton(self.frame_derecho, text="Registrar Gasto", command=self.registrar_gasto)
        self.btn_registrar_gasto.pack(pady=10, padx=20)

        self.btn_ver_reportes = ctk.CTkButton(self.frame_derecho, text="Ver Reportes", command=self.ver_reportes)
        self.btn_ver_reportes.pack(pady=10, padx=20)

        self.btn_guardar = ctk.CTkButton(self.frame_derecho, text="Guardar Datos", command=self.guardar_datos)
        self.btn_guardar.pack(pady=10, padx=20)
        
        
        self.btn_guardar = ctk.CTkButton(self.frame_derecho, text="Eliminar Plan", command=self.eliminar_plan)
        self.btn_guardar.pack(pady=10, padx=20)

        # Menú desplegable para filtros
        ctk.CTkLabel(self.frame_derecho, text="Filtrar Planes").pack(pady=10)
        self.filtro_selector = ctk.CTkComboBox(
            self.frame_derecho,
            values=["Todos", "Próximos a Vencer"],
            command=self.aplicar_filtro
        )
        self.filtro_selector.pack(pady=10, padx=20)
        
        self.mostrar_planes()
        
        # Iniciar el sistema de monitoreo en segundo plano
        self.iniciar_monitoreo()
    
    def aplicar_filtro(self, filtro):
        if filtro == "Próximos a Vencer":
            self.mostrar_planes(filtro="proximos_a_vencer")
        else:
            self.mostrar_planes()

    def iniciar_monitoreo(self):
        # Crear un hilo para ejecutar el monitoreo en segundo plano
        hilo_monitoreo = threading.Thread(target=self.monitorear_planes, daemon=True)
        hilo_monitoreo.start()

    def guardar_datos(self):
        guardar_datos(self.datos)
        messagebox.showinfo("Guardar Datos", "Datos guardados correctamente.")

    def monitorear_planes(self):
        while True:
            for plan in self.datos["planes"]:
                # Verificar si el plan ha alcanzado su fecha de fin
                fecha_actual = datetime.now().date()
                fecha_fin = datetime.strptime(plan["fecha_fin"], "%Y-%m-%d").date()
                if fecha_actual >= fecha_fin:
                    self.mostrar_alerta(f"El plan '{plan['nombre']}' ha alcanzado su fecha de fin.")

                # Verificar si el monto ahorrado ha alcanzado el objetivo
                if plan["ahorrado"] >= plan["objetivo"]:
                    self.mostrar_alerta(f"¡Felicidades! Has alcanzado el objetivo del plan '{plan['nombre']}'.")

            time.sleep(10)  # Esperar 10 segundos antes de volver a verificar

    def mostrar_alerta(self, mensaje):
        # Mostrar una alerta en la interfaz gráfica
        messagebox.showinfo("Alerta", mensaje)
    
    def crear_plan(self):
        ventana_plan = ctk.CTkToplevel(self)
        ventana_plan.title("Crear Plan de Ahorro")
        ventana_plan.geometry("400x400")

        nombre = ctk.CTkEntry(ventana_plan, placeholder_text="Nombre del Plan")
        nombre.pack(pady=10, padx=20)

        objetivo = ctk.CTkEntry(ventana_plan, placeholder_text="Objetivo Monetario")
        objetivo.pack(pady=10, padx=20)

        fecha_fin = ctk.CTkEntry(ventana_plan, placeholder_text="Fecha de Fin (YYYY-MM-DD)")
        fecha_fin.pack(pady=10, padx=20)

        def guardar_plan():
            nuevo_plan = {
                "id": datetime.now().timestamp(),
                "nombre": nombre.get(),
                "objetivo": float(objetivo.get()),
                "fecha_fin": fecha_fin.get(),
                "ahorrado": 0.0
            }
            self.datos["planes"].append(nuevo_plan)
            self.mostrar_planes()
            ventana_plan.destroy()

        btn_guardar = ctk.CTkButton(ventana_plan, text="Guardar Plan", command=guardar_plan)
        btn_guardar.pack(pady=20)
    

    # def mostrar_planes(self):
    #     for widget in self.frame_izquierdo.winfo_children():
    #         widget.destroy()

    #     for plan in self.datos["planes"]:
    #         plan_frame = ctk.CTkFrame(self.frame_izquierdo)
    #         plan_frame.pack(pady=10, padx=20, fill="x")

    #         ctk.CTkLabel(plan_frame, text=f"Plan: {plan['nombre']}").pack(anchor="w")
    #         ctk.CTkLabel(plan_frame, text=f"Objetivo: ${plan['objetivo']:.2f}").pack(anchor="w")
    #         ctk.CTkLabel(plan_frame, text=f"Ahorrado: ${plan['ahorrado']:.2f}").pack(anchor="w")
    #         ctk.CTkLabel(plan_frame, text=f"Fecha Fin: {plan['fecha_fin']}").pack(anchor="w")

    #         # Botón para añadir ahorro
    #         btn_ahorro = ctk.CTkButton(plan_frame, text="Añadir Ahorro", command=lambda p=plan: self.añadir_ahorro(p))
    #         btn_ahorro.pack(side="left", padx=5)

    #         # Botón para editar plan
    #         btn_editar = ctk.CTkButton(plan_frame, text="Editar", command=lambda p=plan: self.editar_plan(p))
    #         btn_editar.pack(side="left", padx=5)
    def mostrar_planes(self, filtro=None):
        for widget in self.frame_izquierdo.winfo_children():
            widget.destroy()

        # Aplicar filtro si se proporciona
        planes = self.datos["planes"]
        if filtro == "proximos_a_vencer":
            fecha_actual = datetime.now().date()
            planes = list(filter(lambda p: datetime.strptime(p["fecha_fin"], "%Y-%m-%d").date() <= fecha_actual + timedelta(days=7), planes))

        for plan in planes:
            plan_frame = ctk.CTkFrame(self.frame_izquierdo)
            plan_frame.pack(pady=10, padx=20, fill="x")

            ctk.CTkLabel(plan_frame, text=f"Plan: {plan['nombre']}").pack(anchor="w")
            ctk.CTkLabel(plan_frame, text=f"Objetivo: ${plan['objetivo']:.2f}").pack(anchor="w")
            ctk.CTkLabel(plan_frame, text=f"Ahorrado: ${plan['ahorrado']:.2f}").pack(anchor="w")
            ctk.CTkLabel(plan_frame, text=f"Fecha Fin: {plan['fecha_fin']}").pack(anchor="w")

            # Botón para añadir ahorro
            btn_ahorro = ctk.CTkButton(plan_frame, text="Añadir Ahorro", command=lambda p=plan: self.añadir_ahorro(p))
            btn_ahorro.pack(side="left", padx=5)

            # Botón para editar plan
            btn_editar = ctk.CTkButton(plan_frame, text="Editar", command=lambda p=plan: self.editar_plan(p))
            btn_editar.pack(side="left", padx=5)
            
            # Botón para eliminar plan
            btn_editar = ctk.CTkButton(plan_frame, text="Eliminar", command=lambda p=plan: self.eliminar_plan(p))
            btn_editar.pack(side="left", padx=5)
        
    def eliminar_plan(self, plan):
        """
        Elimina el plan seleccionado directamente.
        """
        if not self.datos["planes"]:
            messagebox.showwarning("Eliminar Plan", "No hay planes disponibles para eliminar.")
            return

        # Verificar si el plan existe en la lista
        if plan in self.datos["planes"]:
            self.datos["planes"].remove(plan)  # Eliminar el plan directamente
            messagebox.showinfo("Eliminar Plan", f"Plan '{plan['nombre']}' eliminado correctamente.")
            self.mostrar_planes()  # Actualizar la lista de planes
        else:
            messagebox.showerror("Eliminar Plan", "El plan seleccionado no se encuentra en la lista.")

    def mostrar_planes_proximos_a_vencer(self):
        self.mostrar_planes(filtro="proximos_a_vencer")

    def editar_plan(self, plan):
        ventana_editar = ctk.CTkToplevel(self)
        ventana_editar.title("Editar Plan de Ahorro")
        ventana_editar.geometry("400x400")

        # Campos para editar el plan
        nombre = ctk.CTkEntry(ventana_editar, placeholder_text="Nombre del Plan")
        nombre.insert(0, plan["nombre"])
        nombre.pack(pady=10, padx=20)

        objetivo = ctk.CTkEntry(ventana_editar, placeholder_text="Objetivo Monetario")
        objetivo.insert(0, str(plan["objetivo"]))
        objetivo.pack(pady=10, padx=20)

        fecha_fin = ctk.CTkEntry(ventana_editar, placeholder_text="Fecha de Fin (YYYY-MM-DD)")
        fecha_fin.insert(0, plan["fecha_fin"])
        fecha_fin.pack(pady=10, padx=20)

        def guardar_cambios():
            try:
                # Validar y actualizar los datos del plan
                plan["nombre"] = nombre.get()
                plan["objetivo"] = float(objetivo.get())
                plan["fecha_fin"] = fecha_fin.get()
                self.mostrar_planes()
                ventana_editar.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        btn_guardar = ctk.CTkButton(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
        btn_guardar.pack(pady=20)
    
    def añadir_ahorro(self, plan):
        ventana_ahorro = ctk.CTkToplevel(self)
        ventana_ahorro.title("Añadir Ahorro")
        ventana_ahorro.geometry("300x200")

        ctk.CTkLabel(ventana_ahorro, text=f"Plan: {plan['nombre']}").pack(pady=10)

        monto = ctk.CTkEntry(ventana_ahorro, placeholder_text="Monto a añadir")
        monto.pack(pady=10, padx=20)

        def guardar_ahorro():
            try:
                monto_ahorro = float(monto.get())
                if monto_ahorro <= 0:
                    raise ValueError("El monto debe ser mayor a 0.")
                plan["ahorrado"] += monto_ahorro
                self.mostrar_planes()
                ventana_ahorro.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        btn_guardar = ctk.CTkButton(ventana_ahorro, text="Guardar", command=guardar_ahorro)
        btn_guardar.pack(pady=20)
    
    def registrar_gasto(self):
        ventana_gasto = ctk.CTkToplevel(self)
        ventana_gasto.title("Registrar Gasto")
        ventana_gasto.geometry("400x400")

        # Selección del plan de ahorro
        ctk.CTkLabel(ventana_gasto, text="Selecciona un Plan").pack(pady=10)
        plan_seleccionado = ctk.CTkComboBox(
            ventana_gasto,
            values=[plan["nombre"] for plan in self.datos["planes"]]
        )
        plan_seleccionado.pack(pady=10, padx=20)

        # Campos para el gasto
        descripcion = ctk.CTkEntry(ventana_gasto, placeholder_text="Descripcion del Gasto")
        descripcion.pack(pady=10, padx=20)

        monto = ctk.CTkEntry(ventana_gasto, placeholder_text="Monto del Gasto")
        monto.pack(pady=10, padx=20)

        def guardar_gasto():
            try:
                # Validar entrada
                monto_gasto = float(monto.get())
                if monto_gasto <= 0:
                    raise ValueError("El monto debe ser mayor a 0.")
                
                # Buscar el plan seleccionado
                nombre_plan = plan_seleccionado.get()
                plan = next((p for p in self.datos["planes"] if p["nombre"] == nombre_plan), None)
                if not plan:
                    raise ValueError("Debes seleccionar un plan válido.")

                # Verificar si hay suficiente dinero ahorrado
                if plan["ahorrado"] < monto_gasto:
                    raise ValueError("No hay suficiente dinero ahorrado en este plan para cubrir el gasto.")

                # Registrar el gasto y actualizar el plan
                nuevo_gasto = {
                    "id": datetime.now().timestamp(),
                    "descripcion": descripcion.get(),
                    "monto": monto_gasto,
                    "categoria": "General",  # Puedes agregar un campo para categorías si es necesario
                    "fecha": datetime.now().isoformat(),
                    "plan": nombre_plan
                }
                self.datos["gastos"].append(nuevo_gasto)
                plan["ahorrado"] -= monto_gasto  # Restar el gasto del ahorro
                self.mostrar_planes()
                ventana_gasto.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        btn_guardar = ctk.CTkButton(ventana_gasto, text="Guardar Gasto", command=guardar_gasto)
        btn_guardar.pack(pady=20)

    def ver_reportes(self):
        ventana_reportes = ctk.CTkToplevel(self)
        ventana_reportes.title("Reportes Detallados")
        ventana_reportes.geometry("600x600")

        # Crear un marco para los reportes
        frame_reportes = ctk.CTkFrame(ventana_reportes)
        frame_reportes.pack(fill="both", expand=True, padx=10, pady=10)

        # Agrupar los gastos por plan
        gastos_por_plan = {}
        for gasto in self.datos["gastos"]:
            plan_nombre = gasto.get("plan", "Sin Plan")
            if plan_nombre not in gastos_por_plan:
                gastos_por_plan[plan_nombre] = []
            gastos_por_plan[plan_nombre].append(gasto)

        # Mostrar los reportes por plan
        for plan_nombre, gastos in gastos_por_plan.items():
            ctk.CTkLabel(frame_reportes, text=f"Plan: {plan_nombre}", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)

            if not gastos:
                ctk.CTkLabel(frame_reportes, text="No hay gastos registrados para este plan.", font=("Arial", 12)).pack(anchor="w", padx=10)
            else:
                total_gastos = sum(g["monto"] for g in gastos)
                ctk.CTkLabel(frame_reportes, text=f"Gastos Totales: ${total_gastos:.2f}", font=("Arial", 12)).pack(anchor="w", padx=10)

                for gasto in gastos:
                    descripcion = gasto["descripcion"]
                    monto = gasto["monto"]
                    fecha = gasto["fecha"]
                    ctk.CTkLabel(frame_reportes, text=f"- {descripcion}: ${monto:.2f} (Fecha: {fecha})", font=("Arial", 11)).pack(anchor="w", padx=20)

            ctk.CTkLabel(frame_reportes, text="").pack()

if __name__ == "__main__":
    app = ControlGastosApp()
    app.mainloop()