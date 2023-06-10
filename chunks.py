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
