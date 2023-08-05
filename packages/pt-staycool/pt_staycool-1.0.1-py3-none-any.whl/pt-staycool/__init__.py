try : 
    from Main import Main
except ModuleNotFoundError:
    import os
    print('installing requirements.txt')
    os.system('pip install -r requirements.txt || pip3 install -r requirements.txt') #install module yang diperlukan
    from Main import Main

import os
from time import sleep
import sys

desktop = os.path.join(os.path.expanduser('~/Documents/'))+'Hkk_output/'

try :
    os.mkdir(desktop)
except FileExistsError:
    pass

def help():
    print("Usage :")
    print("python start.py [command]\n")
    print("Command :")
    for s in range(len(tostart)):
        print(tostart[s], end =', ')
    print(' | Memulai program')
    for a in range(len(toanggota)):
        print(toanggota[a], end =', ')
    print(' | Melihat anggota kelompok')
    for l in range(len(tolangsung)):
        print(tolangsung[l], end =', ')
    print('[jumlah karyawan] | Menjalankan program')


def mulai():
    #printout
    print('Program Hitung Honor Karyawan Kontrak\nPT. STAY COOL')
    input('Press Enter to start')
    os.system('cls||clear') #clear terminal
    #printout pake animasi
    kata1 = "-------------------Program Hitung Honor Karyawan Kontrak-------------------\n"
    kata2 = "-------------------------------PT. STAY COOL-------------------------------\n"
    for char in kata1:
        sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()
    for char in kata2:
        sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()
    #jalankan program
    Main()

#variasi
tostart = ('start', 'mulai', 'run', '-r', '-m', '-s')
toanggota = ('anggota', 'credit', '-a', '-c')
toclass = ('Main')
tolangsung = ('karyawan', '-k')
tohelp = ('h', 'help', '-h')

if len(sys.argv) > 1:

    if sys.argv[1] in toclass:
        Main()
    elif sys.argv[1] in tostart:
        try:
            mulai()
        except KeyboardInterrupt:
            print('\nSee you!!')
            sys.exit()
        except IndexError :
            print('Completed but ada yang salah')
        except ValueError :
            print('Harus pake Integer')
    elif sys.argv[1] in toanggota :
        print('\n')
        print('Muhamad Dafa Prasetya')
        print('Devi Alvandi')
        print('Dimas Ajie')
        print('Chairil Fajri')
        print('Arie Sutiawan')
        print('\n')
    elif sys.argv[1] in tolangsung:
        try :
            Main(int(sys.argv[2]))
        except IndexError:
            print('Tidak komplit')
        except ValueError :
            print('Masukan value dalam bentuk angka!')
    elif sys.argv[1] in tohelp :
        print('--------------Program Hitung Honor Karyawan Kontrak--------------')
        print('--------------------------PT. Stay Cool--------------------------\n')
        help()

    else:
        for i in range(len(sys.argv[1:])):
            print(sys.argv[i+1],end=' ')
        print('\n')

else :
    help()

