from cajero import iniciar_sesion, consultar_saldo, depositar, retirar
from inicializar_datos import inicializar_archivo_json
import json
import os


RUTA_DATOS = os.path.join(os.path.dirname(__file__), 'datos', 'cuentas.json')

def menu():
    print("\n--- Cajero Automático ---")
    print("1. Consultar saldo")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Transferir")
    print("5. Salir")
    return input("Seleccione una opción: ")

def crear_cuenta():
    # Se leen las cuentas y se guardan en una variable dentro del bucle
    try:
        with open(RUTA_DATOS, 'r') as archivo:
            cuentas = json.load(archivo)
    except FileNotFoundError:
        cuentas = []  # Si el archivo no existe, empezar con una lista vacía

    # Pedir al usuario los datos para la nueva cuenta
    print('')
    print('A continucacion le pediremos los datos para su nueva cuenta')
    numero = input("Ingrese un número de cuenta: ")
    pin = input("Ingrese un PIN para su cuenta: ")
    saldo = float(input("Ingrese el saldo inicial: "))

    # Crear un diccionario para la nueva cuenta
    nueva_cuenta = {
        "numero": numero,
        "pin": pin,
        "saldo": saldo
    }

    # Se agrega la cuenta a la lista de cuentas
    cuentas.append(nueva_cuenta)

    # Devolver la lista de cuentas al archovo Jeison
    with open(RUTA_DATOS, 'w') as archivo:
        json.dump(cuentas, archivo, indent=4)

    print("Cuenta creada exitosamente.")


def verify():
    try:
        opcion = input('¿Tiene una cuenta creada(si/no)?')
        if opcion == 'si':
            pass
        else:
            crear_cuenta()

    except ValueError:
        print('Error: Dato ingresado Incorrecto')

def transferir(cuenta_origen):
    # Se leen las cuentas y se guardan en una variable dentro del bucle
    try:
        with open(RUTA_DATOS, 'r') as archivo:
            cuentas = json.load(archivo)
    except FileNotFoundError:
        print("Error: No se encontraron cuentas registradas.")
        return

    # Solicitar numero de cuenta destino
    cuenta_destino_numero = input("Ingrese el número de cuenta destino: ")

    # Buscar la cuenta destino
    cuenta_destino = None
    for cuenta in cuentas:
        if cuenta['numero'] == cuenta_destino_numero:
            cuenta_destino = cuenta
            break

    if cuenta_destino is None:
        print("Error: La cuenta destino no existe.")
        return

    # Solicitar monto a transferir
    monto = float(input("Ingrese el monto a transferir: "))

    # Verificar que la cuenta origen tenga saldo suficiente
    if cuenta_origen['saldo'] < monto:
        print("Error: Saldo insuficiente para realizar la transferencia.")
        return

    # Realizar la transferencia
    cuenta_origen['saldo'] -= monto
    cuenta_destino['saldo'] += monto

    # Actualizar la lista de cuentas con las modificaciones
    for cuenta in cuentas:
        if cuenta['numero'] == cuenta_origen['numero']:
            cuenta['saldo'] = cuenta_origen['saldo']  # Actualizar saldo de la cuenta de origen
        elif cuenta['numero'] == cuenta_destino['numero']:
            cuenta['saldo'] = cuenta_destino['saldo']  # Actualizar saldo de la cuenta destino

    # Se devuelve la informacion al JSON
    with open(RUTA_DATOS, 'w') as archivo:
        json.dump(cuentas, archivo, indent=4)

    print(f"Transferencia de {monto} realizada exitosamente a la cuenta {cuenta_destino_numero}.")




def main():
    inicializar_archivo_json()
    verify()
    cuenta = iniciar_sesion()
    if not cuenta:
        print("No se pudo iniciar sesión. El programa se cerrará.")
        return

    while True:
        print(f'Bienvenido de nuevo')
        opcion = menu()
        if opcion == '1':
            consultar_saldo(cuenta)
        elif opcion == '2':
            monto = float(input("Ingrese el monto a depositar: "))
            depositar(cuenta, monto)
        elif opcion == '3':
            monto = float(input("Ingrese el monto a retirar: "))
            retirar(cuenta, monto)
        elif opcion == '4':
            transferir(cuenta)
        elif opcion == '5':
            print("Gracias por usar nuestro cajero automático.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")




if __name__ == "__main__":
    main()