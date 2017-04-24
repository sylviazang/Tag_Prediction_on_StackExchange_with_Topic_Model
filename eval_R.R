data <- read.csv('eval_result.csv')
data$result <- 30*data$result
library(ggplot2)

data_topic_1 = subset(data, topic==1)
data_topic_3 = subset(data, topic==3)


plot_data <- function(data){
  data$topic <- factor(data$topic)
  data$filter <- as.factor(data$filter)
  
  ggplot() + geom_point(data=data, mapping=aes(x=iters, y=result, shape=factor(topic))) + geom_line(data=data, mapping=aes(x=iters, y=result, color=field, linetype=filter)) + labs(x="# of Iterations", y="Accuracy", title="Parameter Tuning")   
}

plot_data(data_topic_1)
plot_data(data_topic_3)




ggplot() + geom_point(data=data_topic_3, mapping=aes(x=iters, y=result, shape=factor(topic))) + geom_line(data=data_topic_3, mapping=aes(x=iters, y=result, color=field, linetype=filter)) + geom_point(data=data_topic_1, mapping=aes(x=iters, y=result, shape=factor(topic))) + geom_line(data=data_topic_1, mapping=aes(x=iters, y=result, color=field, linetype=filter)) + labs(x="# of Iterations", y="Accuracy", title="Parameter Tuning") + labs(x="# of Iterations", y="Accuracy", title="Parameter Tuning") 


