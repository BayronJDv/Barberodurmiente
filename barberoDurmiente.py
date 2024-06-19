import threading
import time
import sys

MAX_CLIENTES = 17 #Se puede definir un numero máximo de clientes para atender

numeroAyuda = 0 #Se define un numero de ayuda para ver evidente el uso de semaforos

def cliente(num):
    global numeroAyuda # Etso no se debe hacer porque entran de manera descontrolada, pero como solo se hace un corte al mismo tiempo
    print(f"El cliente {num + 1} llegó a la barbería")
    
    sillaEspera.acquire() #Decrementa el semaforo para usar la sillita
    print(f"El cliente {num + 1} se sienta en la sala de espera")
    
    sillaBarbero.acquire() #Decrementa el semaforo para sentarse en la silla "principal"
    
    sillaEspera.release() #Incrementa el semaforo para liberar la sillita
    
    print(f"El cliente {num + 1} levanta al barbero")
    barberoZZZ.release() #Incrementa el semaforo de barbero para despertarlo y que trabaje
    
    corte.acquire() #Decrementa el semaforo de corte para hacer el corte

    numeroAyuda = numeroAyuda+1 #se refiere al numero de cortes que realizó el barbero, debe ser igual al num de clientes

    sillaBarbero.release() #Libera la silla del barbero para que otro pueda ocuparla
    print(f"El cliente {num + 1} se fue")
    
def barbero():
    global numeroAyuda
    while not atendiTodos:
        print("El barbero está durmiendo")
        barberoZZZ.acquire() #Se duerme un poco zzz (inicia dormido)
        if not atendiTodos:
            print("El barbero está cortando cabello")            
            time.sleep(1) # toma un momento para "Cortar"
            print("Ya termino de cortar el cabello")
            corte.release() #Incrementa el semaforo de corte para terminar el corte

    print("El barbero cierra la barberia.") #Se refiere a que la ejecucion finalizó
    print(f'Se atendieron {numeroAyuda} clientes.')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Asi se usa: barberoDurmiente.py <Num clientes> <Num sillas>")
        sys.exit(-1)
    
    numclientes = int(sys.argv[1])
    numsillas = int(sys.argv[2])
    
    if numclientes > MAX_CLIENTES:
        print(f"El número máximo de clientes es {MAX_CLIENTES}.")
        sys.exit(-1)
    
    sillaEspera = threading.Semaphore(numsillas)
    sillaBarbero = threading.Semaphore(1) # inicia con una silla totalmente libre disponible para que un personae la use y la deseche
    barberoZZZ = threading.Semaphore(0) # inicia dormidisimo
    corte = threading.Semaphore(0) #inicia sin corte
    
    atendiTodos = False #Inicia si atender a todos pues
    
    barbero_thread = threading.Thread(target=barbero) # crea un hilo para ejecutar barbero
    barbero_thread.start()
    
    clientes_threads = []
    for i in range(numclientes):
        cliente_thread = threading.Thread(target=cliente, args=(i,)) #crea un hilo para ejecutar cliente
        clientes_threads.append(cliente_thread)
        cliente_thread.start()
    
    for cliente_thread in clientes_threads:
        cliente_thread.join()
    
    atendiTodos = True # despues de hacer todos los ciclos en teoria ya se atendieron todos los socios
    barberoZZZ.release()  # Despierta al barbero para cerrar la barbería
    barbero_thread.join()
