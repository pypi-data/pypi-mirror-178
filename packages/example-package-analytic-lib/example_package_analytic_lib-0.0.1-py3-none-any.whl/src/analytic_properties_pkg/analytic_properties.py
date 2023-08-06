class AnalyticProperties:
   
    def average(self, count_of_numbers,sum_of_numbers):
        average= sum_of_numbers/count_of_numbers
        return average
    
    def percentage(self, total_of_particular_entity,total_of_whole_entity):
        percentage=(total_of_particular_entity/total_of_whole_entity)*100
        
        return percentage
   
            
if __name__ == '__main__':
    ap = AnalyticProperties()
    sum_of_numbers=678
    count_of_numbers=67
    total_of_particular_entity=499
    total_of_whole_entity=50000
    
    print('\n the average of the count of {} entries  to the total sum of all entries {}  is   : {}'.format(count_of_numbers,sum_of_numbers, ap.average(count_of_numbers,sum_of_numbers)))
    print('The percentage of {}  to {} is : {}%'.format(total_of_particular_entity,total_of_whole_entity, ap.percentage(total_of_particular_entity,total_of_whole_entity)))
   