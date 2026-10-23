import requests
from tabulate import tabulate

def pedir_monto() -> float:
    while True:
        try:
            monto = float(input("Ingresá monto en ARS: "))
            if monto > 0:
                return monto
            print("Tiene que ser mayor a 0")
        except ValueError:
            print("Poné solo números")

def obtener_cotizaciones() -> list:
    try:
        r = requests.get("https://dolarapi.com/v1/dolares", timeout=10)
        r.raise_for_status()
        datos = r.json()
        return [d for d in datos if d["casa"] in ["oficial", "blue"]]
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    monto = pedir_monto()
    cotizaciones = obtener_cotizaciones()
    if not cotizaciones:
        return
    tabla = []
    for c in cotizaciones:
        tabla.append([c["casa"].capitalize(), c["compra"], c["venta"], round(monto / c["venta"], 2)])
    tabla.sort(key=lambda x: x[0])
    print(tabulate(tabla, headers=["Dolar", "Compra", "Venta", f"Con {monto} ARS"], tablefmt="grid"))

if __name__ == "__main__":
    main()