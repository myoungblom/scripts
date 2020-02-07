# =========================================================
# R script to generate pan-genome accumulation curves.
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
nr_iterations <- 100;#the number of iterations

#the matrix which will hold the results
core_results <- matrix(data=NA,nrow=nr_rows,ncol=nr_iterations);
#a vector the holds the updated results of each iteration
presence_line <- matrix(data=0,nrow=1,ncol=nr_cols);

# the times that we will run our calculation
for(times in 1: nr_iterations){

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
	  #if we find e new gene count it
      if(presence_line[1,j] || subset[i,j]){
        presence_line[1,j] <- 1;
      }
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

# stores first results
result3 <- t(core_results)
result3 <- as.data.frame(result3)

#read the SECOND input file - this one isnt subsampled. 
#The input file must have no header row and column.
#rows corespond to genes, columns corespond to isolates
data2 <- read.table("clade2_gpa_reduced_rarefaction.tsv", sep="\t");
transposed_data2 <- t(data2);#we transpose the table to run a for loop row-wise
nr_rows2 <- nrow(transposed_data2);# this file isn't sampled, just run as whole
nr_cols2 <- ncol(transposed_data2);
nr_iterations <- 100;#the number of iterations

#the matrix which will hold the results
core_results2 <- matrix(data=NA,nrow=nr_rows2,ncol=nr_iterations);
#a vector the holds the updated results of each iteration
presence_line2 <- matrix(data=0,nrow=1,ncol=nr_cols2);

# the times that we will run our calculation
for(times in 1: nr_iterations){
  
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
      #if we find e new gene count it
      if(presence_line2[1,j] || transposed_data2[i,j]){
        presence_line2[1,j] <- 1;
      }
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

# stores second results
result4 <- t(core_results2)
result4 <- as.data.frame(result4)

# plots first results
clade1 <- boxplot(result, data=result, xlab="Number of genomes", ylab="Number of genes in pangenome",
        varwidth=TRUE, outline=FALSE, ylim=c(2000,6000), col = alpha("pink2",0.8))
# adds grid for visibility
grid()
# plots first plot over grid
boxplot(result, data=result,varwidth=TRUE, outline=FALSE,col = alpha("pink2",0), add=TRUE)
# plots second plot
clade2<- boxplot(result2, data=result2, varwidth=TRUE, ylim=c(2000,6000), 
                 outline=FALSE, add = TRUE, col = alpha("Lightskyblue", 0.8))

# adds legend
legend("topleft", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15)
