import math

import requests
from tabulate import tabulate

URL_API = "https://dolarapi.com/v1/dolares"
CASAS = ("oficial", "blue")


def pedir_monto() -> float:
    """Pide por consola un monto en ARS y lo valida.

    Vuelve a pedirlo hasta que el usuario ingrese un número positivo.

    Returns:
        El monto ingresado, como float mayor a 0.
    """
    while True:
        try:
            monto = float(input("Ingresá monto en ARS: "))
        except ValueError:
            print("Poné solo números")
            continue
        if math.isfinite(monto) and monto > 0:
            return monto
        print("Tiene que ser un número mayor a 0")


def obtener_cotizaciones() -> list[dict]:
    """Consulta DolarApi y devuelve las cotizaciones de oficial y blue.

    Returns:
        Lista de diccionarios con las cotizaciones filtradas, o una
        lista vacía si falló la consulta o los datos son inválidos.
    """
    try:
        respuesta = requests.get(URL_API, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return [
            cotizacion for cotizacion in datos
            if cotizacion["casa"] in CASAS and cotizacion["venta"]
        ]
    except requests.RequestException as error:
        print(f"Error de red: {error}")
    except (KeyError, ValueError) as error:
        print(f"Datos inesperados de la API: {error}")
    return []


def main() -> None:
    """Pide un monto en ARS y muestra cuántos USD se obtienen por casa."""
    monto = pedir_monto()
    cotizaciones = obtener_cotizaciones()
    if not cotizaciones:
        print("No hay cotizaciones disponibles.")
        return

    tabla = [
        [
            cotizacion["casa"].capitalize(),
            cotizacion["compra"],
            cotizacion["venta"],
            round(monto / cotizacion["venta"], 2),
        ]
        for cotizacion in cotizaciones
    ]
    tabla.sort(key=lambda fila: fila[3], reverse=True)

    print(tabulate(
        tabla,
        headers=["Dólar", "Compra", "Venta", f"USD por {monto:,.2f} ARS"],
        tablefmt="grid",
    ))


if __name__ == "__main__":
    main()