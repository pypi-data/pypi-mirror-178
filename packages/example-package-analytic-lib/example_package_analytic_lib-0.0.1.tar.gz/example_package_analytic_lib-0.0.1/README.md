To use this Average and percentage library,input the following parameters.

#for "Average"  of set of numbers,
"sum_of_numbers": means the total sum of all numbers that you are about getting the average
"count_of_numbers":means the count of the total numbers you are summing

#for "percentage of set nof numbers"

"total_of_particular_entity": this is the particular entity you are about getting the percentage out of the whole entities

total_of_whole_entity": this is the value of the whole entities.

# you are to use the instance this way:

if __name__ == '__main__':
    ap = AnalyticProperties()
    sum_of_numbers=678
    count_of_numbers=67
    total_of_particular_entity=499
    total_of_whole_entity=50000
    
    print('\n the average of the count of {} entries  to the total sum of all entries {}  is   : {}'.format(count_of_numbers,sum_of_numbers, ap.average(count_of_numbers,sum_of_numbers)))
    print('The percentage of {}  to {} is : {}%'.format(total_of_particular_entity,total_of_whole_entity, ap.percentage(total_of_particular_entity,total_of_whole_entity)))
   