import os
import random

class Hasil:

    def __init__(self, namafolder, jumlah_karyawan, staycool) :
        # os.path.expanduser('~/Documents')
        # os.mkdir('hasil/'+namafolder)
        desktop = os.path.join(os.path.expanduser('~/Documents/'))+'Hkk_output/'
        try:
            os.mkdir(desktop+namafolder)
        except FileExistsError:
            a = [1,2,3,4,5,6,7,8,9,0]
            r = str(random.choice(a))
            os.mkdir(desktop+namafolder+r)

        for i in range(jumlah_karyawan):
            try : 
                hs = open(desktop+namafolder+r+'/'+staycool['nama_karyawan'][i] + '.txt', 'w')
            except:
                hs = open(desktop+namafolder+'/'+staycool['nama_karyawan'][i] + '.txt', 'w')
            hs.writelines('                                     PT. STAY COOL                                        \n')
            hs.writelines('Gaji Karyawan\n')
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Nama                 : {}\n'.format(staycool['nama_karyawan'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Jabatan              : {}\n'.format(staycool['jabatan'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Tunjangan            : {:,}\n'.format(staycool['tunjangan'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Pendidikan           : {}\n'.format(staycool['pendidikan'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Honor Lembur         : {:,}\n'.format(staycool['honor_lembur'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Pajak                : {}\n'.format(staycool['pajak'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('Pendapatan Bersih    : {:,}\n'.format(staycool['pendapatan_bersih'][i]))
            hs.writelines('-------------------------------------------------------------------------------------------------------------------\n')
            hs.writelines('\n                                                                    Total Gaji yang dikeluarkan Rp. : {:,}\n'.format(staycool['total_gaji_yang_keluar'][i]))
            hs.writelines('                                                                                                   PT. STAY COOL')