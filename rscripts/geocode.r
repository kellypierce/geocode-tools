library(tidygeocoder)
library(tidyverse)

geocode_handler <- function(data_chunk){
  result <- {tryCatch(
    geocode(data_chunk, street=Address, city=City, postalcode=Zip.Code, method='census',
            full_results=TRUE, return_type='geographies'),
    error=function(c) c$message,
    warning=function(c) c$message,
    message=function(c) c$message
  )}
  return(result)
}

bind_rows_handler <- function(original, addition){
  result <- {tryCatch(
    bind_rows(original, addition),
    error=function(c) c$message,
    warning=function(c) c$message,
    message=function(c) c$message
  )}
  if(typeof(result)=='list'){
    # if no error, return the combined data structure
    return(result)
  }else{
    # else return the original chunk and print the error/warning/message
    message(result)
    return(original)
  }
}

geocode_chunker <- function(data, chunk_size){
  increments <- seq(1, length(data[,1]), chunk_size)
  chunk_list = list()
  for(i in 1:length(increments)){
    start <- increments[i]
    stop <- min(increments[i] + (chunk_size - 1), length(data[,1]))
    chunk_list[[i]] <- data[start:stop,]
  }
  return(chunk_list)
}

# todo: parallelize
geocode_launcher <- function(chunks){
  geocoded = NULL
  for(i in 1:length(chunks)){
    geocode_result <- geocode_handler(chunks[[i]])
    if(typeof(geocode_result)=="list"){
      geocoded <- bind_rows_handler(geocoded, geocode_result)
    }else{ #todo: retry these chunks instead of skipping
      start <- i * dim(chunks[[i]])[1]
      my_alert <- paste('Warning encountered while processing chunk starting at row', as.character(start), sep=' ')
      message(my_alert)
      message(geocode_result)
    }
    Sys.sleep(3)
  }
  return(geocoded)
}

if(!interactive()){
  
  # parse arguments
  library(optparse)
  option_list = list(
    make_option(c("-f", "--file",  type="character", 
      default=NULL,  help="Path to file with addresses for geocoding.",  metavar="character")),
    make_option(c("-o", "--output", type="character", 
        default=NULL, help="Output save path.", metavar="character")),
    make_option(c("-c", "--chunksize", type="integer",
        default=10000, help="Number of addresses to pass to geocoder at one time."))
  )
  opt_parser = OptionParser(option_list=option_list)
  opt = parse_args(opt_parser)
  addr <- read.csv(opt$file)
  outf <- opt$output
  cs <- as.numeric(as.character(opt$chunksize))
  # override user specified chunk size if it's greater than the max allowed by the us census bureau api
  if (cs > 10000) {cs <- 10000}
  
  # load in the file and geocode in chunks of no more than 10,000
  chunksize <- min(cs, dim(addr)[1])
  message(paste('Processing data in batches of', chunksize, sep=' '))
  fchunk <- geocode_chunker(addr, chunk_size=chunksize)
  geocodes <- geocode_launcher(fchunk)
  original <- basename(opt$file)
  savename <- file.path(outf, paste("geocoded_addresses_", original, sep=''))
  print(savename)
  write.csv(geocodes, savename, row.names=FALSE, quote=TRUE)
}

################################
## testing exception handling ##
################################

# an incorrectly formatted address tibble
#test_addr1 <- as_tibble(x=list('addr'='10100 Burnet Rd', 'city'='Austin', 'zip'=78758))
# a correctly formatted address tibble
#test_addr2 <- as_tibble(x=list('Address'='10100 Burnet Rd', 'City'='Austin', 'Zip.Code'=78758)

# returns a character string with the error/warning/message
#g1 <- geocode_handler(data_chunk=test_addr1)
# returns a tibble with the geocode result
#g2 <- geocode_handler(data_chunk=test_addr2)
