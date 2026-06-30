import customtkinter as ctk

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

class AppNomina(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("Calculadora de Nómina Profesional Colombia (2026)")
        self.geometry("850x620")
        self.resizable(False, False)

        self.tipo_contrato = ctk.IntVar(value=1)
        self.tiene_dependientes = ctk.BooleanVar(value=False)
        self.tiene_prepagada = ctk.BooleanVar(value=False)
        self.tiene_vivienda = ctk.BooleanVar(value=False)
        self.tiene_afc = ctk.BooleanVar(value=False)

        self.texto_salario_var = ctk.StringVar()
        self.texto_salario_var.trace_add("write", self.formatear_salario_en_vivo)

        # interfaz
        self.titulo = ctk.CTkLabel(self, text="SIMULADOR DE NÓMINA Y RETENCIÓN 2026", font=ctk.CTkFont(size=20, weight="bold"))
        self.titulo.pack(pady=15)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.crear_columna_izquierda()
        self.crear_columna_derecha()

    def crear_columna_izquierda(self):
        self.frame_inputs = ctk.CTkFrame(self.main_container, width=420)
        self.frame_inputs.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Sección 1: Datos Básicos
        ctk.CTkLabel(self.frame_inputs, text="1. Datos Básicos", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(self.frame_inputs, text="Salario Mensual Bruto ($):").pack(anchor="w", padx=25)
        
        # Asignamos la variable con rastreo al Entry de salario
        self.entry_salario = ctk.CTkEntry(self.frame_inputs, textvariable=self.texto_salario_var, placeholder_text="Ej: 3'000.000", width=350)
        self.entry_salario.pack(anchor="w", padx=25, pady=(0, 10))

        ctk.CTkLabel(self.frame_inputs, text="Tipo de Contrato:").pack(anchor="w", padx=25)
        self.radio_nominal = ctk.CTkRadioButton(self.frame_inputs, text="Salario Nominal (Dependiente)", variable=self.tipo_contrato, value=1)
        self.radio_nominal.pack(anchor="w", padx=35, pady=2)
        self.radio_servicios = ctk.CTkRadioButton(self.frame_inputs, text="Prestación de Servicios (Independiente)", variable=self.tipo_contrato, value=2)
        self.radio_servicios.pack(anchor="w", padx=35, pady=(2, 15))

        # Sección 2: Casos Especiales / Deducciones
        ctk.CTkLabel(self.frame_inputs, text="2. Casos Especiales (Deducciones)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(5, 5))

        self.switch_dep = ctk.CTkSwitch(self.frame_inputs, text="¿Tiene dependientes económicos?", variable=self.tiene_dependientes)
        self.switch_dep.pack(anchor="w", padx=25, pady=5)

        self.switch_prep = ctk.CTkSwitch(self.frame_inputs, text="¿Paga Medicina Prepagada?", variable=self.tiene_prepagada, command=self.toggle_prepagada)
        self.switch_prep.pack(anchor="w", padx=25, pady=5)
        self.entry_prep = ctk.CTkEntry(self.frame_inputs, placeholder_text="Monto mensual pagado", width=350, state="disabled")
        self.entry_prep.pack(anchor="w", padx=45, pady=(0, 5))

        self.switch_viv = ctk.CTkSwitch(self.frame_inputs, text="¿Paga intereses de Vivienda/Leasing?", variable=self.tiene_vivienda, command=self.toggle_vivienda)
        self.switch_viv.pack(anchor="w", padx=25, pady=5)
        self.entry_viv = ctk.CTkEntry(self.frame_inputs, placeholder_text="Monto mensual de intereses", width=350, state="disabled")
        self.entry_viv.pack(anchor="w", padx=45, pady=(0, 5))

        self.switch_afc = ctk.CTkSwitch(self.frame_inputs, text="¿Aporta a cuentas AFC / Pensión Voluntaria?", variable=self.tiene_afc, command=self.toggle_afc)
        self.switch_afc.pack(anchor="w", padx=25, pady=5)
        self.entry_afc = ctk.CTkEntry(self.frame_inputs, placeholder_text="Monto mensual aportado", width=350, state="disabled")
        self.entry_afc.pack(anchor="w", padx=45, pady=(0, 15))

        self.btn_calcular = ctk.CTkButton(self.frame_inputs, text="Calcular Nómina con 1 Clic", font=ctk.CTkFont(size=14, weight="bold"), height=40, command=self.procesar_calculo)
        self.btn_calcular.pack(fill="x", padx=25, pady=10)

    def crear_columna_derecha(self):
        self.frame_resultados = ctk.CTkFrame(self.main_container, width=390, fg_color=("#EAEAEA", "#2B2B2B"))
        self.frame_resultados.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(self.frame_resultados, text="Resumen de Liquidación", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        self.lbl_contrato = self.crear_item_resultado("Tipo Contrato:", "-")
        self.lbl_bruto = self.crear_item_resultado("Salario Bruto:", "$0")
        self.lbl_ss = self.crear_item_resultado("Seguridad Social:", "$0")
        self.lbl_transporte = self.crear_item_resultado("Auxilio Transporte:", "$0")
        self.lbl_deduc = self.crear_item_resultado("Deducciones Aplicadas:", "$0")
        self.lbl_exent = self.crear_item_resultado("Rentas Exentas:", "$0")
        self.lbl_retencion = self.crear_item_resultado("RETENCIÓN FUENTE:", "$0", resaltar_valor=True)
        
        ctk.CTkFrame(self.frame_resultados, height=2, fg_color="gray").pack(fill="x", padx=30, pady=15)

        self.lbl_neto_titulo = ctk.CTkLabel(self.frame_resultados, text="NETO ESTIMADO A RECIBIR:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_neto_titulo.pack()
        self.lbl_neto_valor = ctk.CTkLabel(self.frame_resultados, text="$0", font=ctk.CTkFont(size=24, weight="bold"), text_color="green")
        self.lbl_neto_valor.pack(pady=5)

        self.lbl_alerta = ctk.CTkLabel(self.frame_resultados, text="", text_color="orange", font=ctk.CTkFont(size=11, weight="bold"))
        self.lbl_alerta.pack(pady=10, padx=20)

    def crear_item_resultado(self, texto_izq, valor_der, resaltar_valor=False):
        f = ctk.CTkFrame(self.frame_resultados, fg_color="transparent")
        f.pack(fill="x", padx=30, pady=3)
        ctk.CTkLabel(f, text=texto_izq, font=ctk.CTkFont(size=12)).pack(side="left")
        
        font_valor = ctk.CTkFont(size=12, weight="bold") if resaltar_valor else ctk.CTkFont(size=12)
        color_valor = "#FF5555" if resaltar_valor else None
        
        lbl_val = ctk.CTkLabel(f, text=valor_der, font=font_valor, text_color=color_valor)
        lbl_val.pack(side="right")
        return lbl_val
# formato número

    def formatear_salario_en_vivo(self, *args):
        texto_original = self.texto_salario_var.get()
        solo_numeros = "".join([c for c in texto_original if c.isdigit()])
        
        if not solo_numeros:
            return
        solo_numeros = solo_numeros[:12]
        valor_int = int(solo_numeros)
        formato_comas = f"{valor_int:,}"
        formato_final = formato_comas.replace(",", ".")
        

        if len(solo_numeros) >= 7:
            partes = formato_final.split(".")
            if len(partes) == 3:
                formato_final = f"{partes[0]}'{partes[1]}.{partes[2]}"
            elif len(partes) == 4:
                formato_final = f"{partes[0]}.{partes[1]}'{partes[2]}.{partes[3]}"

        # 3. Guardar temporalmente la posición del cursor para que no brinque al inicio
        posicion_cursor = self.entry_salario.index(ctk.INSERT)
        
        # Desactivar el rastreo un segundo para evitar bucles infinitos al setear el valor corregido
        self.texto_salario_var.trace_remove("write", self.texto_salario_var.trace_info()[0][1])
        self.texto_salario_var.set(formato_final)
        self.texto_salario_var.trace_add("write", self.formatear_salario_en_vivo)

    def toggle_prepagada(self):
        self.entry_prep.configure(state="normal" if self.tiene_prepagada.get() else "disabled")
        if not self.tiene_prepagada.get(): self.entry_prep.delete(0, 'end')

    def toggle_vivienda(self):
        self.entry_viv.configure(state="normal" if self.tiene_vivienda.get() else "disabled")
        if not self.tiene_vivienda.get(): self.entry_viv.delete(0, 'end')

    def toggle_afc(self):
        self.entry_afc.configure(state="normal" if self.tiene_afc.get() else "disabled")
        if not self.tiene_afc.get(): self.entry_afc.delete(0, 'end')


    def procesar_calculo(self):
        try:
            salario_limpio = self.entry_salario.get().replace("'", "").replace(".", "")
            if not salario_limpio:
                self.lbl_alerta.configure(text="❌ Error: Ingresa un salario válido.")
                return
            
            salario_bruto = float(salario_limpio)
            
            prepagada = float(self.entry_prep.get()) if (self.tiene_prepagada.get() and self.entry_prep.get()) else 0.0
            vivienda = float(self.entry_viv.get()) if (self.tiene_vivienda.get() and self.entry_viv.get()) else 0.0
            afc = float(self.entry_afc.get()) if (self.tiene_afc.get() and self.entry_afc.get()) else 0.0
            dependientes = self.tiene_dependientes.get()
            tipo_contrato = self.tipo_contrato.get()

            # --- ALGORITMO LEY DE COLOMBIA 2026 ---
            UVT = 52374
            SMLMV = 1750905
            AUX_TRANSPORTE = 249095

            es_integral = tipo_contrato == 1 and salario_bruto >= (13 * SMLMV)
            ingreso_base_calculo = salario_bruto * 0.70 if es_integral else salario_bruto

            if tipo_contrato == 1:
                ibc = min(ingreso_base_calculo, 25 * SMLMV)
                total_ingresos_no_renta = (ibc * 0.04) + (ibc * 0.04) + (ibc * 0.01 if salario_bruto >= (4 * SMLMV) else 0)
                auxilio_recibido = AUX_TRANSPORTE if salario_bruto <= (2 * SMLMV) else 0
            else:
                ibc = max(min(salario_bruto * 0.40, 25 * SMLMV), SMLMV)
                total_ingresos_no_renta = ibc * 0.285
                auxilio_recibido = 0

            subtotal_1 = salario_bruto - total_ingresos_no_renta
            deduccion_dependientes = min(ingreso_base_calculo * 0.10, 32 * UVT) if dependientes else 0
            deduccion_prepagada = min(prepagada, 16 * UVT)
            deduccion_vivienda = min(vivienda, 100 * UVT)
            total_deducciones = deduccion_dependientes + deduccion_prepagada + deduccion_vivienda

            renta_exenta_afc = min(afc, ingreso_base_calculo * 0.30, 316.6 * UVT)
            base_para_exenta_25 = subtotal_1 - total_deducciones - renta_exenta_afc
            renta_exenta_25 = min(base_para_exenta_25 * 0.25, 65.8 * UVT) if base_para_exenta_25 > 0 else 0

            total_beneficios_solicitados = total_deducciones + renta_exenta_afc + renta_exenta_25
            limite_global_permitido = min(subtotal_1 * 0.40, 111.6 * UVT)
            beneficios_reales = min(total_beneficios_solicitados, limite_global_permitido)

            base_gravable_uvt = max(0.0, (subtotal_1 - beneficios_reales) / UVT)

            # Rangos de la DIAN Art. 383
            if base_gravable_uvt <= 95:
                tarifa, imp_uvt = "0%", 0
            elif base_gravable_uvt <= 150:
                tarifa, imp_uvt = "19%", (base_gravable_uvt - 95) * 0.19
            elif base_gravable_uvt <= 360:
                tarifa, imp_uvt = "28%", (base_gravable_uvt - 150) * 0.28 + 10
            elif base_gravable_uvt <= 640:
                tarifa, imp_uvt = "33%", (base_gravable_uvt - 360) * 0.33 + 69
            elif base_gravable_uvt <= 945:
                tarifa, imp_uvt = "35%", (base_gravable_uvt - 640) * 0.35 + 162
            elif base_gravable_uvt <= 2300:
                tarifa, imp_uvt = "37%", (base_gravable_uvt - 945) * 0.37 + 268
            else:
                tarifa, imp_uvt = "39%", (base_gravable_uvt - 2300) * 0.39 + 770

            retencion_pesos = imp_uvt * UVT
            salario_neto = (salario_bruto - total_ingresos_no_renta - retencion_pesos) + auxilio_recibido

           
            self.lbl_contrato.configure(text="Nominal" if tipo_contrato == 1 else "Prestación Servicios")
            self.lbl_bruto.configure(text=f"${salario_bruto:,.0f}".replace(",", "."))
            self.lbl_ss.configure(text=f"${total_ingresos_no_renta:,.0f}".replace(",", "."))
            self.lbl_transporte.configure(text=f"${auxilio_recibido:,.0f}".replace(",", "."))
            self.lbl_deduc.configure(text=f"${total_deducciones:,.0f}".replace(",", "."))
            self.lbl_exent.configure(text=f"${(renta_exenta_afc + renta_exenta_25):,.0f}".replace(",", "."))
            self.lbl_retencion.configure(text=f"${retencion_pesos:,.0f} ({tarifa})".replace(",", "."))
            self.lbl_neto_valor.configure(text=f"${salario_neto:,.0f}".replace(",", "."))

            if total_beneficios_solicitados > limite_global_permitido:
                self.lbl_alerta.configure(text="⚠️ Alerta: Se superó el tope legal del 40%\nde exenciones y fue recortado por ley.")
            else:
                self.lbl_alerta.configure(text="")

        except ValueError:
            self.lbl_alerta.configure(text="❌ Error: Revisa que los datos ingresados sean correctos.")

if __name__ == "__main__":
    app = AppNomina()
    app.mainloop()