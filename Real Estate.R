library(ggplot2)
library(data.table)
library(randomForest)
library(dplyr)
library(tidyr)
library(car)
library(tm)
library(visdat)
library(vip)
library(tidymodels)
library(stringr)
re_train = read.csv('housing_train.csv')
re_test = read.csv('housing_test.csv')
glimpse(re_train)
re_train[c('Address_1','Address_2')] <- str_split_fixed(re_train$Address,' ',2)
re_train[c('Address_3','Address_4')] <- str_split_fixed(re_train$Address_2,' ',2)
re_test[c('Address_1','Address_2')] <- str_split_fixed(re_test$Address,' ',2)
re_test[c('Address_3','Address_4')] <- str_split_fixed(re_test$Address_2,' ',2)
re_train$age_of_house = 2023 - re_train$YearBuilt
re_train$age_of_house
re_test$age_of_house = 2023 - re_test$YearBuilt
vis_dat(re_train)
re_train$Price= as.numeric(re_train$Price)
dp_pipe = recipe(Price~ .,data = re_train) %>%
  update_role(Address,YearBuilt,Address_1,Address_2,Address_3,new_role = 'drop_vars') %>%
  update_role(Suburb,Type,Method,SellerG,Postcode,CouncilArea,Address_4,new_role = 'to_dummies') %>%
  update_role(Rooms,Distance,Bedroom2,Bathroom,Car,Landsize,BuildingArea,age_of_house,new_role='to_numeric') %>%
  step_rm(has_role('drop_vars'))%>%
  #step_unknown(has_role('to_dummies'),new_meaning ='__missing__') %>%
  step_other(has_role('to_dummies'),threshold = 0.02,other = '__other__') %>%
  step_dummy(has_role('to_dummies')) %>%
  step_mutate_at(has_role('to_numeric'),fn=as.numeric) %>%
  step_mutate_at(Price,fn = as.numeric,skip=TRUE)%>%
  step_impute_median(all_numeric(),-all_outcomes())
#train1 = subset(train,select = -c(Postcode_X3073,Postcode_X3165))
dp_pipe = prep(dp_pipe)
train = bake(dp_pipe,new_data=NULL)
test = bake(dp_pipe,new_data = re_test)
vis_dat(train,warn_large_data = FALSE)
train1 = subset(train,select = -c(Postcode_X3073,Postcode_X3165))
tree_model = decision_tree(cost_complexity = tune(),tree_depth = tune(),min_n = tune()) %>%
  set_engine('rpart') %>%
  set_mode('regression')
folds = vfold_cv(train,v=10)
tree_grid = grid_regular(cost_complexity(),tree_depth(),min_n(),levels = 4)
tree_grid
doParallel::registerDoParallel()
my_res = tune_grid(tree_model,Price~.,resamples=folds,grid=tree_grid,metrics=metric_set(rmse,mae),control = control_grid(verbose = TRUE))
autoplot(my_res)+theme_light()
fold_metrices=collect_metrics(my_res)

fold_metrices
final_tree_fit = tree_model %>%
  finalize_model(select_best(my_res,'rmse')) %>%
  fit(Price~.,data=train)

final_tree_fit %>%
  vip(geom='col',aethetics=list(fill = 'midnightblue',alpha=0.8)) + scale_y_continuous(expand = c(0,0))

rpart.plot::rpart.plot(final_rf$fit)
train_pred = predict(final_tree_fit,new_data = train)
test_pred = predict(final_tree_fit,new_data = test)
##RANDOM_FOREST
rf_model = rand_forest(mtry = tune(),trees = tune(), min_n = tune()) %>%
  set_mode('regression') %>%
  set_engine('ranger')
folds = vfold_cv(train,v=10)
rf_grid = grid_regular(mtry(c(5,30)),trees(c(100,500)),min_n(c(2,10)),levels = 3)
doParallel::registerDoParallel()
my_res_rf = tune_grid(rf_model, Price ~.,resamples = folds, grid = rf_grid,metrics = metric_set(rmse,mae),control = control_grid(verbose = TRUE))
autoplot(my_res_rf)+theme_light()
fold_metrices=collect_metrics(my_res_rf)
my_res_rf %>% show_best()
final_rf = rf_model %>%
  set_engine('ranger',importance='permutation') %>%
  finalize_model(select_best(my_res_rf,'rmse')) %>%
  fit(Price ~.,data = train)
train_pred_rf = predict(final_rf,new_data = train)
test_pred_rf = predict(final_rf,new_data = test)
errors = train1$Price-train_pred
sqrt(mean((train$Price - train_pred)**2))
write.csv(test_pred_rf,'random_forest_result_test.csv',row.names = FALSE)
set.seed(3)
s = sample(1:nrow(train1),0.8*nrow(train1))
t1 = train1[s,]
t2 = train1[-s,]
fit = lm(Price~.-Postcode_X__other__-Suburb_Richmond-Suburb_X__other__,data = t1)
sort(vif(fit),decreasing = T)
fit = stats::step(fit)
summary(fit)
formula(fit)
fit = lm(Price ~ Rooms + Distance + Bedroom2 + Bathroom + Car + Landsize + 
  BuildingArea + age_of_house + Suburb_Reservoir + Type_t + 
  Type_u + Method_S + Method_SP + Method_VB + SellerG_Buxton + 
  SellerG_Jellis + SellerG_Marshall + SellerG_X__other__ + 
  Postcode_X3032 + Postcode_X3040 + Postcode_X3046 + Postcode_X3058 + 
  Postcode_X3163 + Postcode_X3204 + CouncilArea_Banyule + CouncilArea_Bayside + 
  CouncilArea_Boroondara + CouncilArea_Brimbank + CouncilArea_Darebin + 
  CouncilArea_Glen.Eira + CouncilArea_Hobsons.Bay + CouncilArea_Manningham + 
  CouncilArea_Maribyrnong + CouncilArea_Melbourne + CouncilArea_Moonee.Valley + 
  CouncilArea_Moreland + CouncilArea_Port.Phillip + CouncilArea_Stonnington + 
  CouncilArea_Yarra,data=t1)
summary(fit)
t2_pred = predict(fit,newdata=t2)
errors = t2$Price-t2_pred
rmse = errors**2 %>% mean() %>% sqrt()
mae = mean(abs(errors))
fit_final = lm(Price~.-Postcode_X__other__-Suburb_Richmond-Suburb_X__other__-SellerG_X__other__,data = train1)
#fit_final = lm(Price.~ , data= train1)
sort(vif(fit_final),decreasing = T)
fit_final = stats::step(fit_final)
formula(fit_final)
summary(fit_final)
fit_final = lm(Price ~ Rooms + Distance + Bedroom2 + Bathroom + Car + Landsize + 
  BuildingArea + age_of_house + Suburb_Reservoir + Type_t + 
  Type_u + Method_S + Method_SP + Method_VB + 
  SellerG_Biggin + SellerG_Buxton + SellerG_hockingstuart + 
  SellerG_Jellis + SellerG_Marshall + SellerG_Nelson + SellerG_Ray + 
  Postcode_X3032 + Postcode_X3040 + Postcode_X3046 + Postcode_X3058 + Postcode_X3204 + CouncilArea_Banyule + 
  CouncilArea_Bayside + CouncilArea_Boroondara + CouncilArea_Brimbank + 
  CouncilArea_Darebin + CouncilArea_Glen.Eira + CouncilArea_Hobsons.Bay + 
  CouncilArea_Manningham + CouncilArea_Maribyrnong + CouncilArea_Melbourne + 
  CouncilArea_Moonee.Valley + CouncilArea_Moreland + CouncilArea_Port.Phillip + 
  CouncilArea_Stonnington + CouncilArea_Yarra + CouncilArea_X__other__,data=train1)
summary(fit_final)
test_pred =predict(fit_final,newdata=test)
test_pred
plot(fit_final)
error_test = re_train$Price - test_pred
rmse = error_test**2 %>% mean() %>% sqrt()
test_pred
View(re_test)
write.csv(test_pred,'Real Estate Project.csv',row.names = FALSE)
var(test_pred)
vec = is.na(re_train$YearBuilt)
vec
count = sum(vec)
count
x = re_train[re_train$Type =='h',]
y = re_train[re_train$Type == 't',]
x_price = x$Price
y_price = y$Price
x_mean = mean(x_price)
y_mean = mean(y_price)
x_mean - y_mean
seller = c(unique(re_train$SellerG))

var(re_train$Price)
re_train[re_train$SellerG == 'hockingstuart']
re_train$SellerG == 'hockingstuart'
table(re_train$SellerG)
