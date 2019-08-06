#!/usr/bin/env Rscript
# ABSTRACT: Create R plots
# PODNAME: create_plots.R
# Take the output files from the pan genome pipeline and create nice plots.
# Edited by Madison Youngblom 07/2019
library(ggplot2)

setwd("/Users/madi/Desktop/07.28.2019_roaryPlots")

# boxplot of number of new genes
mydata1 = read.table("clade1/number_of_new_genes.Rtab")
colnames(mydata1) <- c(1:148)
mydata2 = read.table("clade2/number_of_new_genes.Rtab")
colnames(mydata2) <- c(1:17)
boxplot(mydata1, data=mydata1, main="Number of new genes",
         xlab="Number of genomes", ylab="Number of genes",varwidth=TRUE, ylim=c(0,max(mydata1)), outline=FALSE, col = "pink2", xaxt = "n")
boxplot(mydata2, data=mydata2, varwidth=TRUE, ylim=c(0,max(mydata2)), outline=FALSE, add = TRUE, col = "Lightskyblue",
        legend("topright", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15), xaxt = "n", 
        axis(1, at = seq(0, 150, by = 10), las=2))

# boxplot of number of conserved genes
mydata1 = read.table("clade1/number_of_conserved_genes.Rtab")
colnames(mydata1) <- c(1:148)
mydata2 = read.table("clade2/number_of_conserved_genes.Rtab")
colnames(mydata2) <- c(1:17)
boxplot(mydata1, data=mydata1, main="Number of conserved genes",
          xlab="Number of genomes", ylab="Number of genes",varwidth=TRUE, ylim=c(1800,max(mydata1)), outline=FALSE, col = "pink2", xaxt = "n")
boxplot(mydata2, data=mydata2, varwidth=TRUE, ylim=c(1800,max(mydata2)), outline=FALSE, add = TRUE, col = "Lightskyblue",
        legend("topright", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15), xaxt = "n", 
        axis(1, at = seq(0, 150, by = 10), las=2))


# boxplot of number of genes in pan-genome
mydata1 = read.table("clade1/number_of_genes_in_pan_genome.Rtab")
colnames(mydata1) <- c(1:148)
mydata2 = read.table("clade2/number_of_genes_in_pan_genome.Rtab")
colnames(mydata2) <- c(1:17)
boxplot(mydata1, data=mydata1, main="No. of genes in the pan-genome",
          xlab="Number of genomes", ylab="Number of genes",varwidth=TRUE, ylim=c(2000,max(mydata1)), outline=FALSE, col = "pink2", xaxt = "n")
boxplot(mydata2, data=mydata2, varwidth=TRUE, ylim=c(1500,max(mydata2)), outline=FALSE, add = TRUE, col = "Lightskyblue",
        legend("topleft", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15), xaxt = "n", 
        axis(1, at = seq(0, 150, by = 10), las=2))


# boxplot of number of unique genes
mydata1 = read.table("clade1/number_of_unique_genes.Rtab")
colnames(mydata1) <- c(1:148)
mydata2 = read.table("clade2/number_of_unique_genes.Rtab")
colnames(mydata2) <- c(1:17)
boxplot(mydata1, data=mydata1, main="Number of unique genes",
         xlab="Number of genomes", ylab="Number of genes",varwidth=TRUE, ylim=c(0,max(mydata1)), outline=FALSE, col = "pink2", xaxt = "n")
boxplot(mydata2, data=mydata2, varwidth=TRUE, ylim=c(0,max(mydata2)), outline=FALSE, add = TRUE, col = "Lightskyblue",
        legend("topleft", legend = c("Clade 1", "Clade 2"), col = c("pink2", "lightskyblue"), pch = 15), xaxt = "n", 
        axis(1, at = seq(0, 150, by = 10), las=2))

# plotting blastp hits with different percentage identity
mydata1 = read.table("clade1/blast_identity_frequency.Rtab")
mydata2 = read.table("clade2/blast_identity_frequency.Rtab")
ggplot(NULL, aes(x = V1, y = V2)) + ggtitle("Number of blastp hits with \n different percentage identity")+
xlab("Blast percentage identity") + ylab("Number of blast results")+
geom_point(data = mydata1, aes(color = "Clade 1")) + geom_point(data = mydata2, aes(color = "Clade 2"))+
scale_color_manual("", breaks = c("Clade 1", "Clade 2"), values = c("Pink2", "Lightskyblue"))+
ggsave(filename="blastp_hits.png", scale=1)

######################

# plotting conserved and total genes for each clade
library(ggplot2)
conserved1 = colMeans(read.table("clade1/number_of_conserved_genes.Rtab"))
conserved2 = colMeans(read.table("clade2/number_of_conserved_genes.Rtab"))
total1 = colMeans(read.table("clade1/number_of_genes_in_pan_genome.Rtab"))
total2 = colMeans(read.table("clade2/number_of_genes_in_pan_genome.Rtab"))

genes1 = data.frame( genes_to_genomes1 = c(conserved1,total1),
                    genomes1 = c(c(1:length(conserved1)),c(1:length(conserved1))),
                    Key = c(rep("Conserved genes",length(conserved1)), rep("Total genes",length(total1))) )
genes2 = data.frame( genes_to_genomes2 = c(conserved2,total2),
                     genomes2 = c(c(1:length(conserved2)),c(1:length(conserved2))),
                     Key = c(rep("Conserved genes",length(conserved2)), rep("Total genes",length(total2))) )

                    
ggplot() +geom_line(data = genes1, aes(x = genomes1, y = genes_to_genomes1, group = Key, linetype=Key, color = "Clade 1"), size = 1.3, alpha = 0.8) +
geom_line(data = genes2, aes(x = genomes2, y = genes_to_genomes2, group = Key, linetype=Key, color = "Clade 2"), size = 1.3, alpha = 0.8)+
scale_color_manual("Clade", breaks = c("Clade 1", "Clade 2"), values = c("Pink2", "Lightskyblue"))+
theme_classic() +
labs(linetype = "Genes")+
ylim(c(1800,max(total1)))+
xlim(c(1,length(total1)))+
xlab("Number of genomes") +
ylab("Number of genes")+ theme_bw(base_size = 10) +
theme(legend.justification=c(0,1),legend.position=c(0.01,.99), legend.box = "vertical")+
guides( color = guide_legend(order = 1), linetype = guide_legend(order = 2))+
ggsave(filename="conserved_vs_total_genes.png", scale=1)

######################

# plotting new and unique genes for each clade
unique_genes1 = colMeans(read.table("clade1/number_of_unique_genes.Rtab"))
unique_genes2 = colMeans(read.table("clade2/number_of_unique_genes.Rtab"))
new_genes1 = colMeans(read.table("clade1/number_of_new_genes.Rtab"))
new_genes2 = colMeans(read.table("clade2/number_of_new_genes.Rtab"))

genes1 = data.frame( genes_to_genomes1 = c(unique_genes1,new_genes1),
                    genomes1 = c(c(1:length(unique_genes1)),c(1:length(unique_genes1))),
                    Key = c(rep("Unique genes",length(unique_genes1)), rep("New genes",length(new_genes1))) )
genes2 = data.frame( genes_to_genomes2 = c(unique_genes2,new_genes2),
                    genomes2 = c(c(1:length(unique_genes2)),c(1:length(unique_genes2))),
                    Key = c(rep("Unique genes",length(unique_genes2)), rep("New genes",length(new_genes2))) ) 
                   
ggplot() + geom_line(data = genes1, aes(x = genomes1, y = genes_to_genomes1, group = Key, linetype=Key, color = "Clade 1"), size = 1.3, alpha = 0.8, show.legend = TRUE) +
geom_line(data = genes2, aes(x = genomes2, y = genes_to_genomes2, group =Key, linetype =Key, color = "Clade 2"), size = 1.3, alpha = 0.8, show.legend = TRUE)+
scale_color_manual("Clade", breaks = c("Clade 1", "Clade 2"), values = c("Pink2", "Lightskyblue"))+
theme_classic() +
labs(linetype = "Genes") +
ylim(c(1,max(unique_genes1)))+
xlim(c(1,length(unique_genes1)))+
xlab("Number of genomes") +
ylab("Number of genes")+ theme_bw(base_size = 10) +
theme(legend.justification=c(0,1),legend.position=c(0.01,0.99), legend.box = "vertical")+
guides( color = guide_legend(order = 1), linetype = guide_legend(order = 2))+
ggsave(filename="unique_vs_new_genes.png", scale=1)
