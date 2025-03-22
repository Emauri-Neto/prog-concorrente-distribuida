import random
import threading
import time

def quicksort(arr, res):
    if len(arr) <= 1:
        res.extend(arr)
        return
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot] # Elementos menores ou iguais ao pivô
    right = [x for x in arr[:-1] if x > pivot] # Elementos maiores que o pivô

    left_part = []
    right_part = []

    thread1 = threading.Thread(target=quicksort, args=(left, left_part))
    thread2 = threading.Thread(target=quicksort, args=(right, right_part))

    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()

    return res.extend(left_part + [pivot] + right_part)


def gerar_numeros_aleatorios(n=100, min_val=1, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(n)]

def measure_time(fn, num):
    start = time.time()
    if fn == quicksort:
        order = []
        fn(num, order)
    else:
        order = fn(num)
    end = time.time()
    return order, end - start

def original_quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot] # Elementos menores ou iguais ao pivô
    right = [x for x in arr[:-1] if x > pivot] # Elementos maiores que o pivô
    return original_quicksort(left) + [pivot] + original_quicksort(right)


def main():
    numeros = gerar_numeros_aleatorios(random.randint(100, 1000))

    print("Utilizando threads")
    print("---------")
    print("Primeiros 20 números antes da ordenação:", numeros[:20])
    nums, timestamp = measure_time(fn=quicksort, num=numeros)
    print("Primeiros 20 números após a ordenação:", nums[:20])
    print(f"Tempo com threads: {timestamp:.4f}s")
    print("---------\n")
    print("Sem utilizar threads")
    print("---------")
    print("Primeiros 20 números antes da ordenação:", numeros[:20])
    original_nums, timestamp_no_threads = measure_time(fn=original_quicksort, num=numeros)
    print("Primeiros 20 números após a ordenação:", original_nums[:20])
    print(f"Tempo sem threads: {timestamp_no_threads:.4f}s")
    print("---------")

if __name__ == "__main__":
    main()