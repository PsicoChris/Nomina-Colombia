def calcular_nomina_colombia():
    print("=== SIMULADOR DE NÓMINA COLOMBIA 2026 ===\n")
    
    SMLMV = 1750905
    AUX_TRANSPORTE = 249095
    UVT = 52374
    
    salario = float(input("Ingresa tu salario mensual bruto (COP): "))
    tipo_de_salario = int(input("Ingresa:\n[1] Salario Nominal (Dependiente)\n[2] Prestación de Servicios (Independiente)\n> "))


    if tipo_de_salario == 2:
        ibc = salario * 0.40
        if ibc < SMLMV:
            ibc = SMLMV
        

        porcentaje_seguridad_social = 0.285
        cotizacion = ibc * porcentaje_seguridad_social
        auxilio_recibido = 0
    else:
        ibc = salario
        porcentaje_seguridad_social = 0.08
        cotizacion = ibc * porcentaje_seguridad_social

        auxilio_recibido = AUX_TRANSPORTE if salario <= (2 * SMLMV) else 0

    base_uvt = salario / UVT
    impuesto_uvt = 0.0

    if base_uvt <= 95:
        tarifa = "0%"
        impuesto_uvt = 0
    elif base_uvt <= 150:
        tarifa = "19%"
        impuesto_uvt = (base_uvt - 95) * 0.19
    elif base_uvt <= 360:
        tarifa = "28%"
        impuesto_uvt = (base_uvt - 150) * 0.28 + 10
    elif base_uvt <= 640:
        tarifa = "33%"
        impuesto_uvt = (base_uvt - 360) * 0.33 + 69
    elif base_uvt <= 945:
        tarifa = "35%"
        impuesto_uvt = (base_uvt - 640) * 0.35 + 162
    elif base_uvt <= 2300:
        tarifa = "37%"
        impuesto_uvt = (base_uvt - 945) * 0.37 + 268
    else:
        tarifa = "39%"
        impuesto_uvt = (base_uvt - 2300) * 0.39 + 770

    retencion_pesos = impuesto_uvt * UVT
    salario_final = (salario - cotizacion - retencion_pesos) + auxilio_recibido


    print("\n" + "="*40)
    print("        RESUMEN DE TU NÓMINA (2026)      ")
    print("="*40)
    print(f"Tipo de Contrato:     {'Nominal' if tipo_de_salario == 1 else 'Prestación de Servicios'}")
    print(f"Salario Bruto:        ${salario:,.2f}")
    print(f"IBC calculado:        ${ibc:,.2f}")
    print(f"Descuento Seg. Social:${cotizacion:,.2f}")
    print(f"Auxilio Transporte:   ${auxilio_recibido:,.2f}")
    print(f"Rango de Retención:   {tarifa}")
    print(f"Retención en Fuente:  ${retencion_pesos:,.2f}")
    print("-"*40)
    print(f"SALARIO NETO A PAGAR: ${salario_final:,.2f}")
    print("="*40)

if __name__ == "__main__":
    calcular_nomina_colombia()