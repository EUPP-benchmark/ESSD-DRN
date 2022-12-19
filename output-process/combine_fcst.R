library(feather)

# specify path
new_path

pred_all = read_feather(paste0(new_path, "fcst_leadtime0.feather"))

for (n in 1:20) {
  
  print(n)
  
  path_new = paste0(new_path, "fcst_leadtime", n, ".feather")
  preds = read_feather(path_new)
  
  pred_all = rbind(pred_all, preds)
  
}

write_feather(pred_all, paste0(new_path, "fcst_all_leadtime.feather"))
