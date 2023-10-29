# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 1: Data Analysis of Singapore Weather on Electricity Consumption

### Problem Statement
Housing pricing affects the decision making process of buyers in their assessment of the unit. This project attempts to build a linear regression model, using the data contain in the dataset folder. The goal is to have the model accurately predict the sales price of the houses in the test set, which will be evaluated based on common evaluation metrics such as R2 and RMSE.
This will give those who are impacted by housing prices, e.g. owners, buyers and agents additional data to inform their own decision making process. 

### Codebook / Data Dictionary
|        Feature Name       |                        Feature Description per data source                        |
|:-------------------------:|:---------------------------------------------------------------------------------:|
| resale_price              |  the property's sale price in Singapore dollars. This is the target variable that |
| flat_type                 |  type of the resale flat unit, e.g.   3 ROOM                                      |
| street_name               |  street name where the resale flat   resides, e.g. TAMPINES ST 42                 |
| floor_area_sqm            |  floor area of the resale flat unit   in square metres                            |
| lease_commence_date       |  commencement year of the flat   unit's 99-year lease                             |
| Tranc_Year                |  year of resale transaction                                                       |
| mid                       |  middle value of storey_range                                                     |
| commercial                |  boolean value if resale flat has   commercial units in the same block            |
| market_hawker             |  boolean value if resale flat has a   market or hawker centre in the same block   |
| multistorey_carpark       |  boolean value if resale flat has a   multistorey carpark in the same block       |
| precinct_pavilion         |  boolean value if resale flat has a   pavilion in the same block                  |
| planning_area             |  Government planning area that the   flat is located                              |
| Mall_Nearest_Distance     |  distance (in metres) to the   nearest mall                                       |
| Mall_Within_500m          |  number of malls within 500 metres                                                |
| Mall_Within_1km           |  number of malls within 1 kilometre                                               |
| Mall_Within_2km           |  number of malls within 2   kilometres                                            |
| Hawker_Nearest_Distance   |  distance (in metres) to the   nearest hawker centre                              |
| Hawker_Within_500m        |  number of hawker centres within   500 metres                                     |
| Hawker_Within_1km         |  number of hawker centres within 1   kilometre                                    |
| Hawker_Within_2km         |  number of hawker centres within 2   kilometres                                   |
| mrt_nearest_distance      |  distance (in metres) to the   nearest MRT station                                |
| bus_interchange           |  boolean value if the nearest MRT   station is also a bus interchange             |
| mrt_interchange           |  boolean value if the nearest MRT   station is a train interchange station        |
| bus_stop_nearest_distance |  distance (in metres) to the   nearest bus stop                                   |
| pri_sch_nearest_distance  |  distance (in metres) to the   nearest primary school                             |
| pri_sch_name              |  name of the nearest primary school                                               |
| pri_sch_affiliation       |  boolean value if the nearest   primary school has a secondary school affiliation |
| sec_sch_name              |  name of the nearest secondary   school                                           |
| cutoff_point              |  PSLE cutoff point of the nearest   secondary school                              |

### Analysis 
| Version | Score Description | Linear Regression | Ridge Regression | Lasso Regression |
|---------|-------------------|-------------------|------------------|------------------|
| V1      | Train Score       | 0.92618           | 0.92618          | 0.92615          |
| V1      | Test Score        | -6846639454563    | 0.92476          | 0.92473          |
| V1      | Train RMSE        | 38915.20          | 38915.67         | 38922.83         |
| V1      | Test RMSE         | 374737262352      | 39283.65         | 39291.22         |
|_________|___________________|___________________|__________________|__________________|
| V2      | Train Score       | 0.92618           | 0.92618          | 0.92615          |
| V2      | Test Score        | -267759160690952  | 0.92476          | 0.92473          |
| V2      | Train RMSE        | 38915.30          | 38915.67         | 38922.92         |
| V2      | Test RMSE         | 2343474971158     | 39283.65         | 39291.33         |
|_________|___________________|___________________|__________________|__________________|
| V3      | Train Score       | 0.92552           | 0.92551          | 0.92411          |
| V3      | Test Score        | -1564517453.13769 | 0.92415          | 0.92446          |
| V3      | Train RMSE        | 39089.89          | 39090.38         | 39097.75         |
| V3      | Test RMSE         | 5664718809        | 39443.09         | 39452.04         |
|_________|___________________|___________________|__________________|__________________|
| V4      | Train Score       | 0.917622034       | 0.917622         | 0.91758          |
| V4      | Test Score        | 0.91667287        | 0.916672         | 0.916558         |
| V4      | Train RMSE        | 41113.99025       | 41114.08         | 41124.49         |
| V4      | Test RMSE         | 41296.1161        | 41296.38         | 41324.48         |


In V1, modelling the data using linear regression, the test scored gave a discrepant result (-6846639454563) which is negative and large which does not make sense for as a coefficient of determination (R2) score. The RMSE for Linear regression in the test set (374737262352) is also oddly high. Likely, the splitting of the data set has resulted in an imbalance that skews the results of when the more simplistic linear regression model is used. Looking for alternatives, Ridge regression models and Lasso regression models were tested out as well (39283.65). While the scores were both similar, the cross-validation Lasso regression model gave convergence warning, indicating that the most optimal alpha value derived may not be the true optimum. Therefore, Ridge regression is preferred for now.

In V2, trying to account for a small feature does not really remove the discrepant results and the scores barely made any difference. In this iteration, in order to more aggressive reduce the features, an additional modelling in the form of Ordinary Least Squares (OLS) is done on the numeric features to determine if there is any that can be dropped in V3.

In V3, based on the OLS results, more features were dropped before modelling. However, there still seems to be some discrepant results (1564517453.13769) with the Linear regression model. Nevertheless, the Ridge regression models and Lasso regression models retain a consistent score (39443.09 & 39452.04 respectively) between the train and test sets as well as between the different version. As before, the convergence warning occurring with the Lasso regression mean there is likely some issues with the features, possibly too many or the features may be problematic.

In V4, after dropping further 2 features 'flat_model', and 'max_floor_lvl' which is suspected to be collinear with 'flat_type' and 'mid' of the floor range as well as removing 'Tranc_Month', there is an improvement.

The improvement is that the discrepant results with the Linear regression model is not as prevalent with the test score (0.91667287) indicating that the features are less overfitting and more generalised, avoiding the issues where the sectioning during cross validation leads to vastly different results. The results are also more consistent across the 3 different models. In fact, Linear regression and Ridge regression shows very high similarity in the R2 and RMSE scores. (0.91667287 vs 0.916672 and 41296.1161 vs respectively).

While the removal of the features led to a decrease in the R2 scores and the increased RMSE giving a larger variance in the predicted price, having the linear regression model align bodes well for the current variant of the model with less likelihood of overfitting, improving its robustness.

An interesting thing to note is the variables with the highest coefficients in the lasso models are those relating to streets, while the ones in ridge are a mix between schools and streets. This allows us to peek into the workings of the regression models with multiple encoded categories, being of a certain category either penalises or raises the price by the coefficient. This translates to location categories having a large impact on the resale prices even though it is not obvious which exactly is the key areas.


### Conclusion
The modelling process has shown a rather linear relation between the various features and price even though the model is not perfect. In fact, through the iterative process of versioning, the reduction of multiple features does not seem to impact the models score greatly. Thus, it is quite clear that a house price is determined not just by a single factor but rather quite a lot of factors combined together since there was no clear correlation between price resale_price and any one factor. 

While a common understanding is the per area price as evident in the EDA, looking at the coefficients of the models gives us a better understanding of the other drivers (such as street address) of resale prices. This advises us in which area we can possibly look to further refine the model to be as accurate and as simple as possible.

In the meantime, the current model version with the RMSE scores (which represent the pricing error) of around $41k, is less than 10% of the average resale price (\\$448,661), which gives it sufficient utility to gauge housing prices. This will give those who are impacted by housing prices, e.g. owners, buyers and agents additional avenue to gauge the prices of the house unit and aid their decision making process. 
