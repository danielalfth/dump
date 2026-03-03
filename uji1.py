import pandas as pd
import time
import random
import sys

# Batas rekursi untuk menghindari error recursion limit pada Quick Sort
sys.setrecursionlimit(10000)

# ==========================================
# 1. ALGORITMA SORTING
# ==========================================

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# ==========================================
# 2. ALGORITMA SEARCHING
# ==========================================

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# ==========================================
# 3. FUNGSI PENGUJIAN
# ==========================================

if __name__ == "__main__":
    
    # Menentukan file yang akan diuji dan kolom sasarannya
    # Disini kita menambahkan movies.csv dengan kolom 'title' (Judul Film)
    datasets_to_test = {
        'movies.csv': 'title',
        'ratings.csv': 'rating',
        'links.csv': 'imdbId',
        'tags.csv': 'timestamp'
    }

    # Melakukan loop/perulangan untuk mengeksekusi semua file CSV
    for file_name, col_name in datasets_to_test.items():
        print(f"\n=========================================")
        print(f"MENGUJI DATASET: {file_name} (Kolom: {col_name})")
        print(f"=========================================")
        
        try:
            # Memuat dataset
            df = pd.read_csv(file_name)
            
            # Ekstrak data, buang data yg kosong, jadikan list biasa
            data = df[col_name].dropna().tolist()
            
            # Acak dan ambil sampel 2000 data agar pengujian Bubble Sort tidak menghabiskan waktu terlalu lama
            random.shuffle(data)
            data = data[:10000] 
            
            print(f"Banyak sampel data: {len(data)} items\n")
            
            # 1. Bubble Sort
            arr_copy = data.copy()
            start = time.time()
            bubble_sort(arr_copy)
            end = time.time()
            print(f"Kecepatan Bubble Sort    : {end - start:.5f} detik")
            
            # 2. Selection Sort
            arr_copy = data.copy()
            start = time.time()
            selection_sort(arr_copy)
            end = time.time()
            print(f"Kecepatan Selection Sort : {end - start:.5f} detik")
            
            # 3. Merge Sort
            arr_copy = data.copy()
            start = time.time()
            merge_sort(arr_copy)
            end = time.time()
            print(f"Kecepatan Merge Sort     : {end - start:.5f} detik")
            
            # 4. Quick Sort
            arr_copy = data.copy()
            start = time.time()
            sorted_arr = quick_sort(arr_copy)
            end = time.time()
            print(f"Kecepatan Quick Sort     : {end - start:.5f} detik")
            
            # Ambil sebuah angka acak/data dari tengah array yang sudah terurut untuk dijadikan target pencarian
            target = sorted_arr[len(sorted_arr)//2]
            
            # 5. Linear Search (mencari dalam array yg masih acak / belum disort)
            start = time.time()
            linear_search(data, target)
            end = time.time()
            print(f"\nKecepatan Linear Search  : {end - start:.7f} detik")
            
            # 6. Binary Search (mencari dalam array yg sudah disort)
            start = time.time()
            binary_search(sorted_arr, target)
            end = time.time()
            print(f"Kecepatan Binary Search  : {end - start:.7f} detik")
            
        except FileNotFoundError:
            print(f"File {file_name} tidak ditemukan. Pastikan satu folder dengan program ini.")