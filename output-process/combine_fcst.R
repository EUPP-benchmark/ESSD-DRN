library(feather)

pred_all = read_feather("/Data/eumetnet/eumetnet_temp/new/orog_fcst_leadtime0.feather")

for (n in 1:20) {
  
  print(n)
  
  path_new = paste0("/Data/eumetnet/eumetnet_temp/new/orog_fcst_leadtime", n, ".feather")
  preds = read_feather(path_new)
  
  pred_all = rbind(pred_all, preds)
  
}

write_feather(pred_all, "/Data/eumetnet/eumetnet_temp/fcst_all_leadtime_v5.feather")