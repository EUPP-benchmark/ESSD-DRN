library(feather)
library(reshape2)

# specify path
new_path

probs = seq(1/52, 51/52, 1/52)
probs_order = c(probs[26], probs[1:25], probs[27:51])

for (n in 0:20) {
  
  print(n)
  
  path = paste0(new_path, "pred_leadtime", n, ".csv")
  preds = read.csv(path, header = T)
  
  pred_ens = as.data.frame(matrix(NA, nrow = nrow(preds), ncol = 51))
  colnames(pred_ens) = as.character(0:50)
  
  for (k in 1:51) {
    quantile_p = probs_order[k]
    pred_ens[,k] = qnorm(quantile_p, mean = preds$t2m_mean, sd = preds$t2m_std)
  }
  
  pred_all = cbind(preds[,1:3], pred_ens)
  
  pred_final = melt(pred_all, 
                    id.vars = c("station_id", "forecast_lead_time", 
                                "forecast_reference_time"), 
                    variable.name = "realization", 
                    value.name = "t2m")
  
  new_path0 = paste0(new_path, "fcst_leadtime", n, ".feather")
  write_feather(pred_final, new_path0)
  
}
