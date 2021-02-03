#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

# set working directory
setwd(args[1])
database = args[2]
metric = args[3]

# -- load libraries --
library(mongolite)
library(ggplot2)

# -- read data --
collections = readLines(paste0(database,".collections.txt"))
collections = collections[-1]

# creating empty dataframe for number of documents in each collection
number.docs = rep(0,length(collections))
df = data.frame(collections,number.docs)

# Iterating through the collections in the database
for (i in 1:length(collections)) 
{
  # connect to mongodb instance
  m = mongo(collection = collections[i], db = database, url = "mongodb://localhost:3306")
  # number of documents in collection 
  df[i,2] = m$count()
  # loading in all documents in the collection
  alldata <- m$find('{}')
  # extracting timestamps
  (times = alldata$timestamp)
  (times = gsub("T"," ",times))
  (times = gsub("Z","",times))
  (times <- strptime(times, "%Y-%m-%d %H:%M:%OS"))
  (times <- as.POSIXct(times, format="%H:%M:%S"))
  (delta.time <- diff(times))
  time.delta = as.numeric(delta.time)
  
  if ( metric == "cpu" ) {
    # extracting cpu data 
    cpu = alldata$cpu
    # extracting cpu usage 
    cpu.usage = cpu$usage
    # total cpu usage 
    cpu.usage.total = cpu.usage$total
    # differences between usages 
    delta = diff(cpu.usage.total, lag = 1) 
    # calculating core usage 
    cores = delta/time.delta
    cores = cores/1000000000
    
    # creating dataframe for ggplot
    dat = data.frame(cores,times[-1])
    names(dat) <- c("cores","time")
    
    # creating the plot object 
    g = ggplot(data=dat, aes(x=time,y=cores)) +
      ggtitle(paste("Total Usage of",collections[i]),subtitle=database) +
      geom_line(color=i+1) +
      theme(plot.subtitle = element_text(size=10, face="italic"))
  }
  else if (metric == "memory"){
    # extracting memory 
      memory = alldata$memory
      # extracting memory usage
      memory.usage = memory$usage
      # convert to megabytes
      memory.usage = memory.usage/1000000
      
      # creating dataframe for ggplot
      dat = data.frame(memory.usage,times)
      names(dat) <- c("memory","time")
      # creating the plot object
      g = ggplot(data=dat, aes(x=time,y=memory)) + 
            geom_line(color=i) +
              ggtitle(paste("Total Memory Usage of",collections[i]),subtitle=database) +
                ylab("megabytes") + geom_line(color=i+1) +
                  theme(plot.subtitle = element_text(size=10, face="italic"))
  }
  filepath <- file.path(paste0(args[1],"/graphics"),paste(database,"_",metric,"_",collections[i], ".png", sep = ""))
      
  png(file=filepath)

  print(g)
}
