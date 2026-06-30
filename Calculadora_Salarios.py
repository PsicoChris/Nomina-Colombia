import os

def calcular_retencion_dian_2026(salario_bruto, tipo_contrato, dependientes=False, 
                                 medicina_prepagada=0, intereses_vivienda=0, 
                                 pension_voluntaria_afc=0):
    """
    Calcula la retención en la fuente real en Colombia (2026) aplicando la depuración de base.
    """
    # 1. Datos Legales para 2026
    UVT = 52374
    SMLMV = 1750905
    AUX_TRANSPORTE = 249095
    
    # Tipo de salário + lógica según salario
    es_integral = tipo_contrato == 1 and salario_bruto >= (13 * SMLMV)
    ingreso_base_calculo = salario_bruto * 0.70 if es_integral else salario_bruto

    # 2. Ingresos No Constitutivos de Renta (Seguridad Social Obligatoria)
    if tipo_contrato == 1:  # Nominal / Dependiente
        ibc = min(ingreso_base_calculo, 25 * SMLMV)
        salud_obligatoria = ibc * 0.04
        pension_obligatoria = ibc * 0.04
        solidaridad = ibc * 0.01 if salario_bruto >= (4 * SMLMV) else 0
        total_ingresos_no_renta = salud_obligatoria + pension_obligatoria + solidaridad
        auxilio_recibido = AUX_TRANSPORTE if salario_bruto <= (2 * SMLMV) else 0
    else:  # Prestación de Servicios / Independiente
        ibc = max(min(salario_bruto * 0.40, 25 * SMLMV), SMLMV)
        total_ingresos_no_renta = ibc * 0.285
        auxilio_recibido = 0

    # Subtotal 1: Base sobre la cual se calcula el límite del 40%
    subtotal_1 = salario_bruto - total_ingresos_no_renta

    # 3. Deducciones Certificadas (Con sus respectivos topes mensuales en UVT)
    deduccion_dependientes = min(ingreso_base_calculo * 0.10, 32 * UVT) if dependientes else 0
    deduccion_prepagada = min(medicina_prepagada, 16 * UVT)
    deduccion_vivienda = min(intereses_vivienda, 100 * UVT)
    
    total_deducciones = deduccion_dependientes + deduccion_prepagada + deduccion_vivienda

    # 4. Rentas Exentas
    renta_exenta_afc = min(pension_voluntaria_afc, ingreso_base_calculo * 0.30, 316.6 * UVT)
    
    base_para_exenta_25 = subtotal_1 - total_deducciones - renta_exenta_afc
    renta_exenta_25 = min(base_para_exenta_25 * 0.25, 65.8 * UVT) if base_para_exenta_25 > 0 else 0

    # 5. Aplicación del Límite Global del 40%
    total_beneficios_solicitados = total_deducciones + renta_exenta_afc + renta_exenta_25
    limite_40_porciento = subtotal_1 * 0.40
    tope_maximo_40 = 111.6 * UVT
    limite_global_permitido = min(limite_40_porciento, tope_maximo_40)

    beneficios_reales = min(total_beneficios_solicitados, limite_global_permitido)

    # 6. Base Gravable Final (En Pesos y convertida a UVT)
    base_gravable_pesos = subtotal_1 - beneficios_reales
    base_gravable_uvt = max(0.0, base_gravable_pesos / UVT)

    # 7. Tabla de Retención en la Fuente (Art. 383 del Estatuto Tributario)
    if base_gravable_uvt <= 95:
        tarifa = "0%"
        impuesto_uvt = 0
    elif base_gravable_uvt <= 150:
        tarifa = "19%"
        impuesto_uvt = (base_gravable_uvt - 95) * 0.19
    elif base_gravable_uvt <= 360:
        tarifa = "28%"
        impuesto_uvt = (base_gravable_uvt - 150) * 0.28 + 10
    elif base_gravable_uvt <= 640:
        tarifa = "33%"
        impuesto_uvt = (base_gravable_uvt - 360) * 0.33 + 69
    elif base_gravable_uvt <= 945:
        tarifa = "35%"
        impuesto_uvt = (base_gravable_uvt - 640) * 0.35 + 162
    elif base_gravable_uvt <= 2300:
        tarifa = "37%"
        impuesto_uvt = (base_gravable_uvt - 945) * 0.37 + 268
    else:
        tarifa = "39%"
        impuesto_uvt = (base_gravable_uvt - 2300) * 0.39 + 770

    retencion_final_pesos = impuesto_uvt * UVT
    salario_neto = (salario_bruto - total_ingresos_no_renta - retencion_final_pesos) + auxilio_recibido

    return {
        "salario_bruto": salario_bruto,
        "es_integral": es_integral,
        "tipo_contrato": "Nominal" if tipo_contrato == 1 else "Prestación de Servicios",
        "seguridad_social": total_ingresos_no_renta,
        "auxilio_transporte": auxilio_recibido,
        "deducciones_aplicadas": total_deducciones,
        "rentas_exentas_aplicadas": renta_exenta_afc + renta_exenta_25,
        "limite_40_activado": total_beneficios_solicitados > limite_global_permitido,
        "base_uvt": base_gravable_uvt,
        "tarifa_retencion": tarifa,
        "retencion_fuente": round(retencion_final_pesos),
        "salario_neto": round(salario_neto)
    }

def ejecutar_interfaz():
    print("=============================================")
    print("   CALCULADORA DE NÓMINA COLOMBIA (2026)    ")
    print("=============================================\n")
    
    try:
        # Captura de datos básicos
        salario = float(input("1. Ingresa tu salario mensual bruto: $"))
        print("\n2. Selecciona el tipo de contrato:")
        print("   [1] Salario Nominal (Empleado dependiente)")
        print("   [2] Prestación de Servicios (Independiente)")
        tipo_contrato = int(input("   > Elige (1 o 2): "))
        
        if tipo_contrato not in [1, 2]:
            print("Opción inválida. Saliendo...")
            return

        print("\n--- CASOS ESPECIALES (DEDUCCIONES) ---")
        
        # Caso especial 1: Dependientes
        dep_input = input("¿Tienes dependientes económicos? (s/n): ").strip().lower()
        tiene_dependientes = dep_input == 's'
        
        # Caso especial 2: Medicina Prepagada (¡Modificado!)
        pag_prepagada = input("¿Pagas medicina prepagada o planes privados de salud? (s/n): ").strip().lower()
        if pag_prepagada == 's':
            prepagada = float(input("   > ¿Cuánto pagas mensualmente?: $"))
        else:
            prepagada = 0.0  # Si dice que no, automáticamente es cero
        
        # Caso especial 3: Intereses Vivienda
        pag_vivienda = input("¿Pagas intereses por crédito de vivienda o leasing? (s/n): ").strip().lower()
        if pag_vivienda == 's':
            vivienda = float(input("   > ¿Cuánto pagas mensualmente en intereses?: $"))
        else:
            vivienda = 0.0
            
        # Caso especial 4: AFC / Pensión voluntaria
        hace_afc = input("¿Haces aportes mensuales a cuentas AFC o Pensión Voluntaria? (s/n): ").strip().lower()
        if hace_afc == 's':
            afc = float(input("   > ¿Cuánto aportas mensualmente?: $"))
        else:
            afc = 0.0

        # Procesar cálculos
        res = calcular_retencion_dian_2026(
            salario_bruto=salario,
            tipo_contrato=tipo_contrato,
            dependientes=tiene_dependientes,
            medicina_prepagada=prepagada,
            intereses_vivienda=vivienda,
            pension_voluntaria_afc=afc
        )

        # Mostrar resultados formateados
        print("\n" + "="*45)
        print("              RESULTADOS DEL CÁLCULO          ")
        print("="*45)
        print(f"Tipo de Contrato:      {res['tipo_contrato']}")
        if res['es_integral']:
            print("⚠️ Nota: Aplica Ley de Salario Integral (Base al 70%)")
        print(f"Salario Bruto Inicial: ${res['salario_bruto']:,.2f}")
        print(f"Auxilio de Transporte: ${res['auxilio_transporte']:,.2f}")
        print(f"Descuento Seg. Social: ${res['seguridad_social']:,.2f}")
        print("-"*45)
        print(f"Deducciones Aplicadas: ${res['deducciones_aplicadas']:,.2f}")
        print(f"Rentas Exentas Real:   ${res['rentas_exentas_aplicadas']:,.2f}")
        
        if res['limite_40_activado']:
            print("⚠️ ¡Tope Ley del 40% superado! Las deducciones se limitaron al máximo legal.")
            
        print(f"Base Líquida en UVT:   {res['base_uvt']:.2f} UVT")
        print(f"Rango de Impuesto:     {res['tarifa_retencion']}")
        print(f"RETENCIÓN EN FUENTE:   ${res['retencion_fuente']:,.2f}")
        print("="*45)
        print(f"💰 NETO A RECIBIR:     ${res['salario_neto']:,.2f}")
        print("="*45)

    except ValueError:
        print("\n❌ Error: Por favor ingresa valores numéricos válidos en los montos.")

if __name__ == "__main__":
    ejecutar_interfaz()