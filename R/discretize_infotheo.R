library(infotheo)
library(optparse)

option_list <- list(   
  make_option(c("-i", "--input"), type = "character", help = "input file for discretization", metavar = "path"),
  make_option(c("-o", "--output"), type = "character", help = "Output path for discretized file", metavar = "path"))

opt <- parse_args(OptionParser(option_list = option_list))

iname <- opt$input
fname <- opt$output

df <- read.table(iname, header = TRUE, sep = ",")
df_dis <- discretize(df, disc="equalfreq", nbins=NROW(df)^(1/3) )
write.csv(df_dis, file = fname, )   



