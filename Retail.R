library(tidymodels)
library(stringr)
library(randomForest)
library(vip)
library(visdat)


ret_train = read.csv('store_train.csv')
ret_test = read.csv('store_test.csv')


ret_train1 = tidyr::extract(ret_train, storecode, c('Letter', 'Number'), '(\\d+)(.*)', convert = TRUE)
ret_test1 = tidyr::extract(ret_test, storecode, c('Letter', 'Number'), '(\\d+)(.*)', convert = TRUE)

ret_train$Number = ret_train1$Number
ret_test$Number = ret_test1$Number


ret_train$store = as.factor(ret_train$store)

dp_pipe = recipe(store ~.,data = ret_train) %>%
  update_role(Id,storecode,Areaname,new_role = 'drop_vars')%>%
  update_role(country,State,countyname,Number,countytownname,state_alpha,store_Type,new_role = 'to_dummies') %>%
  update_role(sales0,sales1,sales2,sales3,sales4,CouSub,population,new_role = 'as.numeric') %>%
  step_rm(has_role('drop_vars'))%>%
  step_other(has_role('to_dummies'),threshold = 0.05, other = '__other__') %>%
  step_dummy(has_role('to_dummies'))%>%
  step_mutate_at(has_role('to_numeric'),fn=as.numeric) %>%
  step_mutate_at(store,fn=as.factor,skip=TRUE)%>%
  step_impute_median(all_numeric(),-all_outcomes())

dp_pipe = prep(dp_pipe)


train = bake(dp_pipe,new_data = NULL)
test = bake(dp_pipe,new_data = ret_test)

colSums(is.na(test))


rf_model = rand_forest(mtry = tune(),trees = tune(), min_n = tune()) %>%
  set_mode('classification') %>%
  set_engine('ranger')


folds = vfold_cv(train,v=10)

rf_grid = grid_regular(mtry(c(5,40)),trees(c(100,500)),min_n(c(2,10)),levels = 10)
#rf_grid = grid_regular(mtry(c(5,10,15,20,25,30)),trees(c(50,100,150,200,300)),min_n(c(2,5,10,15,20,25,30)),levels = 3)
doParallel::registerDoParallel()

my_res_rf = tune_grid(rf_model, store ~.,resamples = folds, grid = rf_grid,metrics = metric_set(roc_auc),control = control_grid(verbose = TRUE))

# autoplot(my_res_rf)+theme_light()

fold_metrices=collect_metrics(my_res_rf)

my_res_rf %>% show_best()

final_rf = rf_model %>%
  set_engine('ranger',importance='permutation') %>%
  finalize_model(select_best(my_res_rf,'roc_auc')) %>%
  fit(store ~.,data = train)

test_pred_rf = predict(final_rf,new_data = test,type='prob')
test_pred_rf_1 = predict(final_rf,new_data = test)
test_pred_rf_1
test_pred_rf_main = test_pred_rf$.pred_1
write.csv(test_pred_rf_main,'Retail probability2.csv',row.names = FALSE)
train_pred_rf = predict(final_rf,new_data = train)
train_pred_rf
write.csv(train_pred_rf,'Retail probability train2.csv',row.names = FALSE)
