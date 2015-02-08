
#####Success is balance of worker efficiency and vendor satisfaction.  

	My Intent: Meet or exceed satisfactory standards and maximize efficiency.

#####Truths?
1. Worker efficiency is most orders delivered per hour.
2. Goal is for each DG to deliver most number of orders.
3. Goal may not be (or cannot be?) to take the shortest distance. 

######Why can't #3 be a goal? 

	Because the only goal is to optimize return and a DG who takes less orders in order to travel less is not optimizing return. Therefore, since traveling least does not optimize return, then 
	Because the goal is to optimize return, and because traveling less does not optimize return, then traveling less cannot be a goal.
	what if goal




####Optimizing DG Routes:


	Return Rate per DG route = (order/minute) per DG route

When the opportunity arises for a DG to change route, the return rates can be compared between the changed route the existing route.

#####Example:

Before `this_DG` starts heading to a `first_pickup`, a `second_pickup` enters the system where:

	Distance(this_DG,second_pickup)  >>  Distance(this_DG,first_pickup)

######What is better?  
Should `this_DG` either (A) change course and substitute the closer `second_order` with the further `first_order`, or (B) continue to `first_order` as planned? 

	Comparing the return rate for each instance (A) and (B) is informative.

#####(A) Stay on course	
Based on the existing route, the return rate for this instance (A) is the sum of:

	(i) the already-defined return rate for "this_dg"
	  				
	  				and
	  				
	(ii) the change (+/-) in return rate for the "other_DG" who is to pickup/deliver the "second_order"

Before the change in the return rate for the `other_DG` can be determined, the `other_DG` must selected.  There is already an algorithm in place to select the DG with the most increased return rate among a group of DG.

	Result:  	The "other_DG" is selected based on the optimum change
				in the return rate, and, this return rate (for the
				"other_DG") is now defined.

By adding (i) the change in the return rate for the `other_DG` and (ii) `this_DG`'s return rate for the existing route, the return rate for the first instance can be quantified.

#####(B) Change course and substitute the further for the closer
Based on `this_DG` deciding to ignore the first_order and head to the closer, second_order, the return rate for this instance (B) is the sum of:

	(i) the modified return rate of "this_DG"
	  				
	  				and
	  				
	(ii) the change (+/-) in return rate for "another_DG" who is to pickup the "first_order"


A modified return rate is ascertained by `this_DG`'s modified route now optimized including possible additional orders and ***FLEX-ORDERS***.

Similar to instance (A), `another_DG` is selected based on the optimum change in the return rate as from a number of DG, and, this return rate (for the `another_DG`) is now defined.

The return rate for this instance (B) is the sum of (i) the change in the return rate of `another_DG` and (ii) `this_DG`'s modified return rate.

####Conclusion:		
			To evaluate whether "this_DG" should change his route
			   or stay on course, "this_DG" should 
			   choose the instance with the greatest return rate.


