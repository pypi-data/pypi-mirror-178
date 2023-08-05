
import pandas #import module pandas
from Hasil import Hasil #import file Hasil.py

#class main
class Main:

    #function menghitung lembur
    def lembur(self, jam_kerja):
        self.total_fix = 0
        if jam_kerja >= 240:
            self.total = jam_kerja - 240
            self.total_fix = self.total * 2500
            self.jumlah_jam_kerja.append(jam_kerja)
            self.list_honor_lembur.append(self.total_fix)
        else :
            self.jumlah_jam_kerja.append(jam_kerja)
            self.list_honor_lembur.append(0)
        return 0
    #end lembur

    #function menghitung tunjangan jabatan
    def tunjangan_jabatan(self, golongan):
        tunjangan = 0
        if golongan == 1:
            tunjangan = 5/100
        elif golongan == 2:
            tunjangan = 10/100
        elif golongan == 3:
            tunjangan = 15/100
        else:
            tunjangan = 5/100
        self.total_tunjangan = self.gaji_tetap * (tunjangan)
        return self.list_tunjangan.append(self.total_tunjangan)
    #end tunjangan

    #funciton menentukan pendidikan
    def pendidikan(self, pddkn):
        sekolah = 'SMU'
        if pddkn == 1:
            sekolah = 'SMU'
        elif pddkn == 2:
            sekolah = 'D3'
        elif pddkn == 3:
            sekolah = 'S1'
        return self.list_pendidikan.append(sekolah)
    #end pendidikan

    #function menghitung pajak
    def pajak(self):
        self.total_pajak = self.gaji_tetap * (5/100)
        self.total_pajak_fix = self.gaji_tetap - self.total_pajak
        return self.list_pajak.append('5%')
    #end pajak

    #function menghitung total gaji keluar
    def total_gaji_keluar(self):
        gaji = self.total_pajak_fix + (self.total_fix) + self.total_tunjangan
        self.total_gaji_yang_dikeluarkan.append(gaji)
    #end total gaji keluar


    def mulaii(self, argv):
        for i in range(argv):
            try :
                print('karyawan ke - {}'.format(i+1))
                #input nama karyawan
                nama = input('Nama Karyawan : ')
                self.list_nama.append(nama)
                #end input nama karyawan

                #input golongan
                golongan = int(input('Golongan(1/2/3) : '))
                    
                self.list_golongan.append(golongan)
                self.tunjangan_jabatan(golongan)
                #end input golongan
                #input pendidikan
                pddkn = int(input('Pendidikan (1=SMU/2=D3/3=S1) :'))
                self.pendidikan(pddkn)
                #end input pendidikan

                #input jam kerja
                jam_kerja = int(input('Jumlah Jam Kerja : '))
                self.lembur(jam_kerja)
                #end input jam kerja

                self.list_gaji.append(self.gaji_tetap)

                self.pajak()
                self.total_gaji_keluar()
            except ValueError:
                print('Ups ada kesalahan')
                break
            except KeyboardInterrupt:
                print('\nAnda memaksa untuk keluar, data belum di save')
                break
            
            
        #dictionary staycool
        staycool = {
            'nama_karyawan' : self.list_nama,
            'jabatan' : self.list_golongan,
            'tunjangan' : self.list_tunjangan,
            'pendidikan' : self.list_pendidikan,
            # 'jam_kerja' : self.jumlah_jam_kerja,
            'honor_lembur' : self.list_honor_lembur,
            'pajak' : self.list_pajak,
            'pendapatan_bersih' : self.list_gaji,
            'total_gaji_yang_keluar' : self.total_gaji_yang_dikeluarkan
        }
        #output pandas dataframe
        try: #jika value dalam list komplit
            pd = pandas.DataFrame(staycool)
            print(pd)
        except: #jika value dalam list tidak komplit
            pd = pandas.DataFrame.from_dict(staycool, orient='index')
            print(pd)


        #menentukan file di save atau tidak dalam bentuk .txt
        saveornot = input('Apakah anda ingin penyimpan file? [Y/n] : ')

        if saveornot == 'Y' or saveornot == 'y' :
            namafolder = input('Nama Folder : ')
            Hasil(namafolder,argv, staycool)   
            print('Data disimpan di folder Documents/Hkk_output/{}'.format(namafolder))
            print('Terima kasih sudah menggunakan program kami!')
        else :
            print('Terima kasih sudah menggunakan program kami!')
            exit()

    #function __init__
    def __init__(self,argv=None):
        
        self.gaji_tetap = 2500000
        self.list_gaji = []
        self.list_nama = []
        self.list_golongan = []
        self.list_pendidikan = []
        self.jumlah_jam_kerja = []
        self.list_tunjangan = []
        self.list_honor_lembur = []
        self.list_pajak = []
        self.total_gaji_yang_dikeluarkan = []
        self.jumlah_karyawan = 0
        print('\n')
        
        if argv is None :
            self.jumlah_karyawan = int(input('Masukan Jumlah Karyawan : '))
            if self.jumlah_karyawan == '':
                print('Masukan Value dalam bentuk angka!')
            self.mulaii(self.jumlah_karyawan)
        else:
            print('Jumlah Karyawan : {}'.format(argv))
            self.mulaii(argv)

    #end __init__