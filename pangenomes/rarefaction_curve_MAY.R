# =========================================================
# R script to generate core genome rarefaction curves.
# Script by Leonardos Mageiros, February 2014
# =========================================================
# The input format is shown in sample_input.csv included
# in this archive. 1=gene present/0=gene absent; 
# 1 column= 1 genome.
# =========================================================
# Requests should be made to s.k.sheppard@swansea.ac.uk 
# Visit our lab website: http://www.sheppardlab.com/
# =========================================================
# Associated publication: Meric et al. (2014) A reference 
# pan-genome approach to comparative bacterial genomics: 
# identification of novel epidemiological markers in 
# pathogenic Campylobacter
# =========================================================
# Edited by Madison Youngblom 08/2019
# =========================================================

#Define working directory
setwd("~/Desktop/Pepperell/saprophyticus/2019.07.31_saproRarefaction");

#read the FIRST input file - the one to be subsampled. 
#The input file must have no header row and column.
#rows corespond to genes, columns corespond to isolates
data <- read.table("clade1_gpa_reduced_rarefaction.tsv", sep="\t");
transposed_data <- t(data);#we transpose the table to run a for loop row-wise
subset <- transposed_data[sample(nrow(transposed_data), 17), ] # 17 == the number of isolates to be sampled from larger pop
nr_rows <- nrow(subset);
nr_cols <- ncol(subset);
nr_iterations <- 100; #the number of iterations 

#the matrix which will hold the results
core_results <- matrix(data=NA,nrow=nr_rows,ncol=nr_iterations);
#a vector the holds the updated results of each iteration
presence_line <- matrix(data=0,nrow=1,ncol=nr_cols);

# the times that we will run our calculation
for(times in 1:nr_iterations){

  #for all the rows of the table
  for (i in 1: nr_rows){
    sum <- 0;
   if(i==1){ #for the first row
     for(j in 1: nr_cols){#calculate the number of genes
       presence_line[1,j]<-subset[i,j]
       sum <- sum + subset[i,j]; 
     }
     #and store the first result
     core_results[i,times] <- sum
     next;
   }
    
   #for every consecutive row, for every gene  
   for(j in 1: nr_cols){
    #if the gene was and is present count it
    if(presence_line[1,j] && subset[i,j]){
      presence_line[1,j] <- 1;
    }# else dont
    else{presence_line[1,j] <- 0;}
   }
    #count the total number of present genes
   for(j in 1: nr_cols){
     sum <- sum + presence_line[1,j]; 
   }
    #store the result
   core_results[i,times] <- sum;
   
  }
  #suffle the matrix and repeat the procedure
  subset <- transposed_data[sample(nrow(transposed_data), 17), ]
}

# results from first file to be plotted
result <- t(core_results)
result <- as.data.frame(result)

#read the SECOND input file - this one is not subsampled. 
#The input file must have no header row and column.
#rows corespond to genes, columns corespond to isolates
data2 <- read.table("clade2_gpa_reduced_rarefaction.tsv", sep="\t");
transposed_data2 <- t(data2);#we transpose the table to run a for loop row-wise
nr_rows2 <- nrow(transposed_data2); # this file isn't sampled, just run as whole
nr_cols2 <- ncol(transposed_data2);
nr_iterations <- 100; #the number of iterations 

#the matrix which will hold the results
core_results2 <- matrix(data=NA,nrow=nr_rows2,ncol=nr_iterations);
#a vector the holds the updated results of each iteration
presence_line2 <- matrix(data=0,nrow=1,ncol=nr_cols2);

# the times that we will run our calculation
for(times in 1:nr_iterations){
  
  #for all the rows of the table
  for (i in 1: nr_rows2){
    sum <- 0;
    if(i==1){ #for the first row
      for(j in 1: nr_cols2){#calculate the number of genes
        presence_line2[1,j]<-transposed_data2[i,j]
        sum <- sum + transposed_data2[i,j]; 
      }
      #and store the first result
      core_results2[i,times] <- sum
      next;
    }
    
    #for every consecutive row, for every gene  
    for(j in 1: nr_cols2){
      #if the gene was and is present count it
      if(presence_line2[1,j] && transposed_data2[i,j]){
        presence_line2[1,j] <- 1;
      }# else dont
      else{presence_line2[1,j] <- 0;}
    }
    #count the total number of present genes
    for(j in 1: nr_cols2){
      sum <- sum + presence_line2[1,j]; 
    }
    #store the result
    core_results2[i,times] <- sum;
    
  }
  #suffle the matrix and repeat the procedure
  transposed_data2 <- transposed_data2[sample(nrow(transposed_data2), nrow(transposed_data2)), ]
}

# results from second file
result2 <- t(core_results2)
result2 <- as.data.frame(result2)
avg2 <- col
# this plots the first results
clade1 <- boxplot(result, data=result, xlab="Number of genomes", ylab="Number of genes in core genome",
                  varwidth=TRUE, outline=FALSE, ylim=c(2000,2800), col = alpha("pink2",0.8))
clade_colors <- c("pink2", "lightskyblue")

# plotting conserved and total genes for each clade
library(ggplot2)
conserved1 = apply(result, 2, median) # rarefaction results from clade 1
conserved2 = apply(result2, 2, median) # rarefaction results from clade 2
total1 = apply(result3, 2, median) # accumulation results from clade 1
total2 = apply(result4, 2, median) # accumulation results from clade 2

genes1 = data.frame( genes_to_genomes1 = c(conserved1,total1),
                     genomes1 = c(c(1:length(conserved1)),c(1:length(conserved1))),
                     Key = c(rep("Core genes",length(conserved1)), rep("Total genes",length(total1))) )
genes2 = data.frame( genes_to_genomes2 = c(conserved2,total2),
                     genomes2 = c(c(1:length(conserved2)),c(1:length(conserved2))),
                     Key = c(rep("Core genes",length(conserved2)), rep("Total genes",length(total2))) )

setwd("~/Desktop/2019_MWPG/figures/rarefaction/")

rarefaction <- ggplot() +geom_line(data = genes1, aes(x = genomes1, y = genes_to_genomes1, group = Key, linetype=Key, color = "Clade 1"), size = 1.5, alpha = 0.8) +
  geom_line(data = genes2, aes(x = genomes2, y = genes_to_genomes2, group = Key, linetype=Key, color = "Clade 2"), size = 1.5, alpha = 0.8)+
  scale_color_manual("Clade", breaks = c("Clade 1", "Clade 2"), values = c("Pink2", "Lightskyblue"))+
  theme_classic() +
  labs(linetype = "Genes")+
  ylim(c(2000,max(total1)))+
  xlim(c(1,length(total1)))+
  xlab("\nNumber of genomes") +
  ylab("Number of genes\n")+ theme_bw(base_size = 10) +
  theme(legend.justification=c(0,1),legend.position=c(0.01,.99), legend.box = "vertical",
        legend.text = element_text(color = "grey27", size = 12), 
        legend.title = element_text(color = "grey27", face = "bold"),
        axis.text = element_text(color = "grey27", face = "bold"),
        axis.title = element_text(color = "grey27", face = "bold", size = 12))+
  guides( color = guide_legend(order = 1), linetype = guide_legend(order = 2))

#function to export plot
ExportPlot <- function(gplot, filename, width=2, height=1.5) {
  # Export plot in PDF and EPS.
  # Notice that A4: width=11.69, height=8.27
  ggsave(paste(filename, '.pdf', sep=""), gplot, width = width, height = height)
  postscript(file = paste(filename, '.eps', sep=""), width = width, height = height, family = "sans")
  print(gplot)
  dev.off()
  png(file = paste(filename, '_.png', sep=""), width = width * 100, height = height * 100)
  print(gplot)
  dev.off()
}

#export plot
setwd("/Users/madi/Desktop/2019_MWPG/figures/rarefaction/")
ExportPlot(rarefaction, "conserved_vs_total_genes_median", width=6, height=8)



# adds a grid for visibility
grid()
# replots the first plot over the grid
boxplot(result, data=result,varwidth=TRUE, outline=FALSE,col = alpha("pink2",0), add=TRUE)
# plots the second results
clade2<- boxplot(result2, data=result2, varwidth=TRUE, ylim=c(2000,max(result2)), 
                 outline=FALSE, add = TRUE, col = alpha("Lightskyblue", 0.8))
# makes a legend
legend("topright", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15)

