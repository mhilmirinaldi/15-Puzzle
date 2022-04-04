import time
import copy
import heapq as hq

def convert_matriks(nama_file):
    with open("../test/" + nama_file, "r") as f:
        matriks = [[int(num) for num in line.split(' ')] for line in f]
    return matriks
    
def print_matriks(matriks):
    print("+----+----+----+----+")
    for i in range(4):
        print("", end='| ')
        for j in range(4):
            if(matriks[i][j] < 10 and matriks[i][j]>0):
                print(matriks[i][j],end='  | ')
            elif(matriks[i][j] == 0):
                print(" ",end='  | ')
            else:
                 print(matriks[i][j],end=' | ')
        print()
        print("+----+----+----+----+")

def kurang(matriks, i):
    kurang = 0
    x_null,y_null = cari_null(matriks)

    # Jika yang dicari fungsi Kurang(16) maka nilai pada matriks bernilai 0
    if(i == 16):
        i = 0

    x_titik,y_titik = cari_titik(matriks, i)

    # Menset matriks yang bernilai 0 menjadi 16
    matriks[x_null][y_null] = 16
    
    # Menghitung nilai fungsi kurang
    for y in range(y_titik+1,4):
        if(matriks[x_titik][y_titik] > matriks[x_titik][y]):
                kurang += 1

    for x in range(x_titik+1,4):
        for y in range(0,4):
            if(matriks[x_titik][y_titik] > matriks[x][y]):
                kurang += 1

    # Menset matriks yang bernilai 16 menjadi 0
    matriks[x_null][y_null] = 0
    
    return kurang

def total_sumkurang_X(matriks):
    total = 0
    x_null,y_null = cari_null(matriks)

    # Total dari fungsi kurang
    for i in range(0,4):
        for j in range(0,4):
            total += kurang(matriks, matriks[i][j])
        
    # Mencari nilai X
    X = (x_null + y_null) % 2

    return total + X

def cari_null(matriks):
    for i in range(0,4):
        for j in range(0,4):
            if(matriks[i][j] == 0):
                return i,j

def cari_titik(matriks, x):
    for i in range(0,4):
        for j in range(0,4):
            if(matriks[i][j] == x):
                return i,j

def cost(matriks, target, kedalaman):
    ctr = 0
    for i in range(0,4):
        for j in range(0,4):
            if(matriks[i][j] != 0 and matriks[i][j] != target[i][j]):
                ctr += 1
    return ctr + kedalaman

def cek_kesamaan_matriks(matriks, target):
    for i in range(0,4):
        for j in range(0,4):
            if(matriks[i][j] != target[i][j]):
                return False
    return True

def cek_matriks_sudah_ada(matriks, list_matriks):
    for i in range(0,len(list_matriks)):
        if(cek_kesamaan_matriks(matriks, list_matriks[i])):
            return True
    return False

def geser_matriks(matriks, x_null, y_null, i):
    if(i == 0 and x_null != 0): # geser ke atas
        swap_matriks(matriks, x_null-1, y_null)
        return True
    elif(i == 1 and x_null != 3): # geser ke bawah
        swap_matriks(matriks, x_null+1, y_null)
        return True
    elif(i == 2 and y_null != 0): # geser ke kiri
        swap_matriks(matriks, x_null, y_null-1)
        return True
    elif(i == 3 and y_null != 3): # geser ke kanan
        swap_matriks(matriks, x_null, y_null+1)
        return True

def swap_matriks(matriks, x, y):
    x_null,y_null = cari_null(matriks)
    matriks_temp = matriks[x][y]
    matriks[x][y] = matriks[x_null][y_null]
    matriks[x_null][y_null] = matriks_temp

def masukan_node(node, list_node, list_node_expand):
    for i in range(len(list_node)):
        list_node_expand.append(list_node[i])
    list_node_expand.append(node)

def print_langkah(list_matriks):
    for i in range(1, len(list_matriks)):
        print("\nLangkah ke-"+str(i)+" :")
        print_matriks(list_matriks[i])


# Algoritma 15 Puzzle
print("  __ _____       _____               _  ")
print(" /_ | ____|     |  __ \             | | ")
print("  | | |__ ______| |__) |   _ _______| | ___ ")
print("  | |___ \______|  ___/ | | |_  /_  / |/ _ \\ ")
print("  | |___) |     | |   | |_| |/ / / /| |  __/")
print("  |_|____/      |_|    \__,_/___/___|_|\___|")
print("\n")

# Proses file txt
print("Masukkan nama file (tanpa .txt) : ")
nama_file = input()
path = nama_file + ".txt"

matriks = convert_matriks(path)

print("\nMatriks awal yang akan diselesaikan : ")
print_matriks(matriks)

# Mencari fungsi kurang
print("\nNilai dari Fungsi Kurang(i) :")
for i in range(1,17):
    print("Kurang("+str(i)+") = "+str(kurang(matriks,i)))

print("\nSumKurang + X = "+str(total_sumkurang_X(matriks)))

matriks_target = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
start = time.time()
if(total_sumkurang_X(matriks) % 2 == 0): # Jika SumKurang + X = genap
    print("\nPuzzle bisa diselesaikan")
    print("\nMatriks awal :")
    print_matriks(matriks)

    ctr_node = 0

    # Membuat Priority Queue dengan Heap
    matriks_langkah = [matriks]
    PQueue = [(cost(matriks, matriks_target, 0),matriks,matriks_langkah,0)]    # Cost, matriks_awal, list_matriks_langkah, kedalaman
    hq.heapify(PQueue)

    ketemu = cek_kesamaan_matriks(matriks, matriks_target)

    # Algoritma Branch and Bound
    while(len(PQueue) != 0 and not ketemu):
        matriks_tmp = hq.heappop(PQueue)
        x_null, y_null = cari_null(matriks_tmp[1])

        # Mengexpand node 
        for i in range(0,4):
            children = copy.deepcopy(matriks_tmp[1])
            # Menggeser nilai null matriks (0)
            gerak = geser_matriks(children, x_null, y_null, i)
            if(gerak): # Jika gerakan bisa dilakukan
                if(not cek_matriks_sudah_ada(children, matriks_tmp[2])):
                    matriks_solusi = []
                    masukan_node(children, matriks_tmp[2], matriks_solusi)
                    ctr_node += 1
                    # Jika sudah mencapai target maka print langkah untuk mencapai matriks target
                    if(cek_kesamaan_matriks(children, matriks_target)): 
                        ketemu = True
                        end = time.time()
                        print_langkah(matriks_solusi)
                        print("\nWaktu eksekusi program : " + str((end-start) ) + " detik")
                        print("Jumlah simpul yang dibangkitkan : "+ str(ctr_node))
                        break
                    # Jika belum mencapai target maka masukkan ke Priority Queue
                    else:
                        hq.heappush(PQueue, (cost(children, matriks_target, matriks_tmp[3]+1), children, matriks_solusi, matriks_tmp[3]+1))

else: # Jika SumKurang + X = ganjil
    print("\nPuzzle tidak bisa diselesaikan")