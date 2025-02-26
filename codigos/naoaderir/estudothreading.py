import threading

contador = 0
lock = threading.Lock()  # Cria um lock

def incrementar():
    global contador
    for _ in range(1000000):
        with lock:  # Adquire o lock automaticamente
            contador += 1
        # O lock é liberado automaticamente ao sair do bloco `with`

# Cria duas threads
thread1 = threading.Thread(target=incrementar)
thread2 = threading.Thread(target=incrementar)

# Inicia as threads
thread1.start()
thread2.start()

# Aguarda as threads terminarem
thread1.join()
thread2.join()

print(f"Contador final: {contador}")