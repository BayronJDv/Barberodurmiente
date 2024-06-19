import threading
import time
import sys
# Se llama sin luz porque los semaforos estan dañados

MAX_CLIENTES = 17  # Se puede definir un número máximo de clientes para atender

numeroAyuda = 0  # Se define un número de ayuda para ver evidente el uso de semáforos

def cliente(num):
    global numeroAyuda  # Esto no se debe hacer porque entran de manera descontrolada, pero como solo se hace un corte al mismo tiempo
    print(f"El cliente {num + 1} llegó a la barbería")
    
    # sillaEspera.acquire()

    print(f"El cliente {num + 1} se sienta en la sala de espera")
    
    # sillaBarbero.acquire()
    
    print(f"El cliente {num + 1} levanta al barbero")
    # barberoZZZ.release()
    
    # Simulamos el tiempo que espera a que el barbero termine
    time.sleep(1)

    # Se quiere forzar condiciones de carrera
    time.sleep(1)
    numeroAyuda += 1  # Se refiere al número de cortes que realizó el barbero, debe ser igual al número de clientes
    '''
    Despues de ejecutarlo varias veces nos dimos cuenta que el numero
    no cambiaba a pesar de que en teoria el acceso descontrolado puede
    llevar a condiciones de carrera, se asume que la razon de la
    correcta ejecucion se debe a que python administra de cierta
    manera los hilos de ejecucion automaticamente
    '''
    time.sleep(1)

    # sillaBarbero.release()
    print(f"El cliente {num + 1} se fue")
    
def barbero():
    global numeroAyuda
    while not atendiTodos:
        print("El barbero está durmiendo")
        
        # barberoZZZ.acquire()
        
        if not atendiTodos:
            print("El barbero está cortando cabello")
            time.sleep(1)  # Toma un momento para "Cortar"
            print("Ya terminó de cortar el cabello")
            # corte.release()

    print("El barbero cierra la barbería.")  # Se refiere a que la ejecución finalizó
    print(f'Se atendieron {numeroAyuda} clientes.')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Así se usa: barberoDurmiente.py <Num clientes> <Num sillas>")
        sys.exit(-1)
    
    numclientes = int(sys.argv[1])
    numsillas = int(sys.argv[2])
    
    if numclientes > MAX_CLIENTES:
        print(f"El número máximo de clientes es {MAX_CLIENTES}.")
        sys.exit(-1)
    
    # Malo usar semaforos
    # sillaEspera = threading.Semaphore(numsillas)
    # sillaBarbero = threading.Semaphore(1)
    # barberoZZZ = threading.Semaphore(0)
    # corte = threading.Semaphore(0)
    
    atendiTodos = False  # Inicia sin atender a todos
    
    barbero_thread = threading.Thread(target=barbero)  # Crea un hilo para ejecutar barbero
    barbero_thread.start()
    
    clientes_threads = []
    
    for i in range(numclientes):
        cliente_thread = threading.Thread(target=cliente, args=(i,))  # Crea un hilo para ejecutar cliente
        cliente_thread.start()
        clientes_threads.append(cliente_thread)        
    
    for cliente_thread in clientes_threads:
        cliente_thread.join()
    
    atendiTodos = True  # Después de hacer todos los ciclos en teoría ya se atendieron todos los socios
    # barberoZZZ.release()
    barbero_thread.join()
