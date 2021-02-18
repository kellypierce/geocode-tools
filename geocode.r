library(tidygeocoder)
library(tidyverse)
library(optparse)

option_list = list(
  make_option(
    c(
      "-f", 
      "--file", 
      type="character", 
      default=NULL, 
      help="Path to file with addresses for geocoding.", 
      metavar="character"
      )
    ),
  make_option(
    c(
      "-o", 
      "--output", 
      type="character", 
      default=NULL, 
      help="Output save path.", 
      metavar="character"
    )
  )
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

addr <- read.csv(opt$file)
outf <- opt$output

# grab the data in chunks and incrementally save
chunk_size = 1000
save_chunks = 10
increments <- seq(1, length(addr[,1]), chunk_size)
counter = 1

geocoded <- NULL
for(i in increments){
  start <- i
  stop <- min(i + (chunk_size - 1), length(addr[,1]))
  submit <- addr[start:stop,]
  geocoded <- bind_rows(
    geocoded, 
    geocode(submit, street=Address, city=City, postalcode=Zip.Code, method='census',
            full_results=TRUE, return_type='geographies') # this is the part that makes the query
    )
  # todo: this will not save the last chunk
  if(counter %% save_chunks == 0){
    savename = file.path(outf, paste("geocoded_addr_", i, ".csv", sep=''))
    print(savename)
    write.csv(geocoded, savename)
    geocoded=NULL
  }
  # pause between query chunks
  counter = counter + 1
  Sys.sleep(10)
}

# NOT RUN

#addr <- read.csv('/corral-secure/projects/Cooks-ProTX/working_dpfs_data/complete_vic_perp_addr.csv')
#head(addr)

#test_addr <- addr[1,]
#test_gc1 <- geocode(test_addr, street=Address, city=City, postalcode=Zip.Code, method='osm')
#test_gc2 <- geo(street=test_addr$Address, city=test_addr$City, postalcode=test_addr$Zip.Code, method='osm')

#test_gc1_census <- geocode(test_addr, street=Address, city=City, postalcode=Zip.Code, method='census')

#test_block <- addr[1:100,]
#start_t <- Sys.time()
#start <- 1
#stop <- min(1 + (chunk_size - 1), length(addr[,1]))
#submit <- addr[start:stop,]
#test_block_census <- geocode(submit, street=Address, city=City, postalcode=Zip.Code, method='census',
#                             full_results=TRUE, return_type='geographies')
#stop_t <- Sys.time()
#print(stop_t - start_t)
