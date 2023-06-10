from mpi4py import MPI
import os
import time
import re




y = ['20000','40000','60000','80000','100000','120000','140000','160000','180000','200000','220000','240000','260000','280000','300000','320000','340000','360000','380000','400000','420000','440000','460000','480000','500000','520000','540000','560000','580000','600000','620000','640000','660000','680000','700000','720000','740000', '760000','780000','800000','820000','840000','860000','880000','900000','920000','940000','960000','980000','1000000','1020000','1040000','1060000','1080000','1100000','1120000','1140000','1160000','1180000','1200000','1220000','1240000','1260000','1280000','1300000','1320000','1340000','1360000','1380000','1400000','1420000','1440000','1460000','1480000','1500000','1520000','1540000','1560000','1580000','1600000','1620000','1640000','1660000','1680000','1700000','1720000','1740000','1760000','1780000','1800000','1820000','1840000','1860000','1880000','1900000','1920000','1940000','1960000','1980000','2000000','2020000','2040000','2060000','2080000','2100000','2120000','2140000','2160000','2180000','2200000','2220000','2240000','2260000','2280000','2300000','2320000','2340000','2360000','2380000','2400000','2420000','2440000','2460000','2480000','2500000','2520000','2540000','2560000','2580000','2600000','2620000','2640000','2660000','2680000','2700000','2720000','2740000','2760000','2780000','2800000','2820000','2840000','2860000','2880000','2900000','2920000','2940000','2960000','2980000','3000000','3020000','3040000','3060000','3080000','3100000','3120000','3140000','3160000']
z = ['20001','40001','60001','80001','100001','120001','140001','160001','180001','200001','220001','240001','260001','280001','300001','320001','340001','360001','380001','400001','420001','440001','460001','480001','500001','520001','540001','560001','580001','600001','620001','640001','660001','680001','700001','720001','740001', '760001','780001','800001', '820001','840001','860001','880001','900001','920001','940001','960001','980001','1000001','1020001','1040001','1060001','1080001','1100001','1120001','1140001','1160001','1180001','1200001','1220001','1240001','1260001','1280001','1300001','1320001','1340001','1360001','1380001','1400001','1420001','1440001','1460001','1480001','1500001','1520001','1540001','1560001','1580001','1600001','1620001','1640001','1660001','1680001','1700001','1720001','1740001','1760001','1780001','1800001','1820001','1840001','1860001','1880001','1900001','1920001','1940001','1960001','1980001','2000001','2020001','2040001','2060001','2080001','2100001','2120001','2140001','2160001','2180001','2200001','2220001','2240001','2260001','2280001','2300001','2320001','2340001','2360001','2380001','2400001','2420001','2440001','2460001','2480001','2500001','2520001','2540001','2560001','2580001','2600001','2620001','2640001','2660001','2680001','2700001','2720001','2740001','2760001','2780001','2800001','2820001','2840001','2860001','2880001','2900001','2920001','2940001','2960001','2980001','3000001','3020001','3040001','3060001','3080001','3100001','3120001','3140001','3160001']
a = ['6000','12000','18000','24000']
y2 = ['760000','720000', '460000', '2300000','2080000','2000000', '1920000', '1620000','1220000','1040000']
z2 = ['760001','720001', '460001', '2300001','2080001','2000001', '1920001', '1620001','1220001','1040001']
#y = range (20000,3160000,20000)
# Starting the job process
#

# Job starting  
start_t = time.time()

# STAGE 1 : Making VCF FIle
# Load module plink2

def stage1(int):
        for i in range(161):
                os.system("time mkdir " +s_path+"/"+z[i])

# STAGE 2 : Filtering vcf tools
# Load bcftools

def stage2(int):
        for i in range(161):
                os.system("time mv " +s_path+"small_file_"+z[int]+".vcf.gz "+s_path+"z[int]")

# STAGE 3 : Making chunkspp
#

def stage3(int):
        lines_per_file = 6000
        smallfile = None   
        for i in range(161):
                with open(""+s_path+"/"+str(z[i])+"/small_file_"+str(z[i])+".vcf") as bigfile:
                        for lineno, line in enumerate(bigfile):
                                if lineno % lines_per_file == 0:
                                        if smallfile:
                                                smallfile.close()
                                        small_filename = ""+s_path+"/"+z[i]+"/small_file_"+z[i]+"_{}.vcf".format(lineno + lines_per_file)
                                        smallfile = open(small_filename, "w")
                                smallfile.write(line)
                if smallfile:
                        smallfile.close()
# STAGE 4 : Seperate file named
#
'''
def stage4(int):
        for i in range(161):
                for j in range(3):
                        os.system("time cat /gpfs/data/user/aditya/PED_files/VCF_chunk/chr15/chr15_head.vcf " +s_path+"/"+str(z[i])+"/small_file_"+str(z[i])+"_"+str(a[j])+".vcf >" +s_path+"/"+str(z[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+".vcf")
# STAGE 5 : Merging the files
#
'''
def stage5(int):
        for i in range(161):
                os.system("mkdir "+epacts_path+"/"+str(y[i])+"/")


# STAGE 6 : BGZIP on Each files
# Load BGZIP

def stage6(int):
       # os.system("mkdir "+d_path+"/"+x[int]+"/")
        for i in range(161):
                for j in range(4):
                        os.system("time bgzip -c " +s_path+"/"+str(z[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+".vcf > " +d_path+"/"+str(y[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+".vcf.gz")


# STAGE 7 : FOR TABIX
#

def stage7(int):
        for i in range(161):
                for j in range(4):
                        os.system("time tabix -pvcf -f "+d_path+"/"+str(y[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+".vcf.gz" )

# STAGE 8 : FOR EPACTS
# Load naveen/epacts-3.3.2 naveen/R-4.0.0

def stage8(int):
       # os.system("mkdir "+s_path+"/"+x[int]+"/")
        for i in range(161):
                for j in range(4):
                        os.system("time epacts single --vcf "+d_path+"/"+str(y[i])+"/small_file_"+y[i]+"_"+str(a[j])+".vcf.gz --ped "+ped_path+"/fluid_intelligence_ei.ped --min-maf 0.000016 --chr 15 --pheno X30710.0.1 --inv-norm --cov X6138.0.0 --cov SEX --cov X21022.0.0 --cov PC1 --cov PC2 --cov PC3 --cov PC4 --cov PC5 --cov PC6 --cov PC7 --cov PC8 --cov PC9 --cov PC10 --test q.linear --out "+epacts_path+"/"+str(y[i])+"/"+str(y[i])+"_"+str(a[j])+"_chunk --run 72")
#os.system("time epacts single --vcf "+d_path+"/"+x[int]+"/"small_file_"+z[i]+".vcf.gz --ped "+ped_path+"/Phenotype.ped --min-maf 0.001 --chr "+x1[int]+" --pheno X20133.0.0 --cov X6138.0.0 --cov SEX --cov X21022.0.0 --test b.score --out "+s_path+"/"+x[int]+"/"+z[i]+"_chunk --run 2"")
def stage9(int):
        for i in range(161):
                for j in range(4):
                        os.system("time plink2 --vcf "+d_path+"/"+str(y[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+".vcf.gz --freq --out "+d_path+"/"+str(y[i])+"/small_file_"+str(y[i])+"_"+str(a[j])+"")
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank < 25:
        #stage1(rank)
        #stage2(rank)
        #stage3(rank)
        stage8(rank)
else:
  print('Rank outside of range , given rank was: ' + str(rank))

# End time

end_t = time.time()
elapsed = end_t - start_t

#print(f"Total Time take :\n{elapsed}")
