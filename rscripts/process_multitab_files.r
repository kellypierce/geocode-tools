#########################################################
# This script takes multi-tab excel files from TX DFPS  #
# and combines all the tabs into a single flat CSV file #
# with tab name as a new column.                        #
#########################################################

# set working dir to secure area
rm(list=ls())
setwd('/corral-secure/projects/Cooks-ProTX/working_dpfs_data/')
library(tidyverse)
library(readxl)
library(plyr)

# some dates are in Excel serial numbers; convert to normal dates
# this function needs debugging...
convert_serial_dates <- function(serial_date){
  print('Attempting to convert serial dates...')
  tryCatch(
    as.Date(as.numeric(serial_date), origin='1899-12-30'),
    error = function(c) {return(serial_date)}
  )
}

# draft 1 of a general method to iterate over tabs and combine into flat data structure
# missing generalized data validation and sanity checks
flatten_excel <- function(path, manual_dates=NULL){
  tabs <- excel_sheets(path)
  if(length(tabs) > 1){
    sheets <- NULL
    for(t in 1:length(tabs)){
      print(paste('Processing tab name ', tabs[t]))
      tab_data <- read_excel(path=path, sheet=tabs[t], skip=3, guess_max=70000)
      if(!is.null(manual_dates)){
        # a clunky workaround while I troubleshoot the tryCatch method
        if(tabs[t] == 'Fiscal Year 2014'){
          tab_data$`Date of Birth` <- as.Date(as.numeric(tab_data$`Date of Birth`), origin='1899-12-30')
        }
      }
      tab_data$tab_name <- tabs[t]
      sheets <- plyr::rbind.fill(sheets, tab_data)
      print('... tab successfully added to flat dataframe.')
      print(paste(tabs[t], ' ', setdiff(names(sheets), names(tab_data))))
      print(paste(tabs[t], ' ', setdiff(names(tab_data), names(sheets))))
    }
  }
  else{
    sheets <- read_excel(path=path, skip=3, guess_max=70000)
  }
  return(sheets)
}

inv_data_all <- flatten_excel('98692_Cook_Children_Confirmed_INV_FY10_FY19.xlsx')
vic_data_all <- flatten_excel('98692_Cook_Children_Confirmed_Victims_FY10_FY19.xlsx')
perp_data_all <- flatten_excel('98692_Cook_Children_Confirmed_Perpetrators_FY10_FY19.xlsx', manual_dates = 'Date of Birth')

write.csv(inv_data_all, 'FLATTENED_98692_Cook_Children_Confirmed_INV_FY10_FY19.csv')
write.csv(vic_data_all, 'FLATTENED_98692_Cook_Children_Confirmed_Victims_FY10_FY19.csv')
write.csv(perp_data_all, 'FLATTENED_98692_Cook_Children_Confirmed_Perpetrators_FY10_FY19.csv')

## debug dates in perp_2014

perp_2014 <- read_excel('98692_Cook_Children_Confirmed_Perpetrators_FY10_FY19.xlsx', sheet='Fiscal Year 2014', guess_max=70000, skip=3)
perp_2013 <- read_excel('98692_Cook_Children_Confirmed_Perpetrators_FY10_FY19.xlsx', sheet='Fiscal Year 2013', guess_max=70000, skip=3)

for(i in length(perp_2014$`Date of Birth`)){
  print(i)
  print(perp_2014$`Date of Birth`[i])
  result <- tryCatch()
  print(as.Date(perp_2014$`Date of Birth`[i], origin = "1899-12-30"))
}
