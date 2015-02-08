# INTRODUCTION

Created on Nov 2, 2013

GENERAL MODELING STRATEGY/OUTLINE

    for each order,
        l=travel_time
        can any DG arrive by (40-l):
            if none available,
                add new DG to order_q
                send out on delivery
            for all DG who can arrive:
                pick best DG by ...
                    shortest order_time
                    **most even DG distribution
                    *most deliveries per person (= chaos method)
                    DG ranking

*   used in FIRST IMPLEMENTATION
**  used in SECOND IMPLEMENTATION

(based on company history, may be best to consider potential for new orders during travel to vendor.
 -- this can be based on probability of (order per minute) * (minutes to vendor)
    -->>--  the longer it takes to get to a location, the more likely there will be another order,
            and the more important it is to send DG with more available time)

(OR, rely on chaos theory and make decisions based on what information is available, not what is
predicted! --> in which case, pack as many deliveries per DG as possible) --> FIRST IMPLEMENTATION.


In the FIRST IMPLEMENTATION, orders were distributed in round robin fashion to DG capable of satisfying
condition and making delivery (provided it was determinable within the combination of 5 pickups/deliveries.
Simple robin distribution is inadequate as the distribution is made blindly without any considerations of whether
 another DG is better positioned to take order.

 - numerous ways could be used to make the first implemention better, but a second branch was started to
 explore a SECOND IMPLEMENTATION based on practical business reasons.

 - one such way to improve FIRST IMPLEMENTATION:
    -identify most inconvenient deliveries (and best combo without it, which can be calculated concurrently
    with c_best_combo method. a subprocess could re-distribute orders based on the outlier delivery center point
     and inlier center points of each DG route. this method could the "Bohr approach" after Neils Bohr

 - other strategies include:
    - least number of orders
    - weighted least number of orders
    - weighted round robin
    - most amount of time
    - centered around a (static or dynamic) point
    - work-stealing approach
    - ant colony optimization
    - swarm intelligence
    - clustering, generalized assignment problem
        make clusters limited by number of nodes


The SECOND IMPLEMENTATION attempts to prove/disprove a hypothesis.

PURPOSE:  In the most practical sense, this business will begin best if delivery guys
continue to work with restaurants with whom they have experience.  This means the delivery system
should start out with maximizing deliveries in particular areas, where a delivery guy covers a single
area and continues to serve the same restaurant.  Although the system may metamorphose into one based
on a level of chaos if more efficient, for now, the system should mirror practical business concerns.
In doing so, it is necessary to predict the minimum coverage required to satisfy delivery conditions
with a certain margin of safety.  Once a formula is identified for predicting the necessary coverage,
a two week period of monitoring a restaurant is assumed to be enough time to calibrate the initial
system.  Adding new restaurants to an active system will be based on the same premise (though the
transition time will likely be shorter).  Therefore, this calibration system should scale well with
the business.

HYPOTHESIS: Assuming a lattice of circles bound by the delivery radii of all restaurants, where the
circles' center points are:

X             Y
0              0,2,4,...2n
1              1,3,5,...2n+1
2              0,2,4,...2n
.
.
n


and where the areas of the circles are pi*((40-r)**2)*C*D
---> C will be a constant approximately proportional to the number of deliveries per hour.
---> D will be a constant approximately proportional to the density of restaurants.

OBJECTIVES:
- determine the maximum radii (95% confidence) for randomized pickup/drop-off locations
    and constant # of deliveries per hour for a constant density of restaurants where all
    deliveries satisfy all conditions.
- determine C by applying the above process to a range of deliveries per hour.
- determine D by applying the two above processes to a range of restaurant densities.

VERIFICATION:
- use density variable to predict deliveries per hour.
- use deliveries per hour to predict restaurant density.
- randomize deliveries per hour and restaurant densities, predict results, and verify accuracy of constants.

METHOD:
    1. Identify [x,y] ranges for vendors and expand based on delivery radii --> Xmax,Ymax,Xmin,Ymin
    2. Use monte carlo method to determine radii (as later identified)
      -starting points: max radii == pi*(40**2), min radii == 0
    3. (number of circles) n == (along X) : (Xmax-Xmin)/r,  (along Y) : (Ymax-Ymin)/r
    4. (center points) C == (along X) : 2*n,  (along Y) : 2*(n+1)
    5. All DG[i] start at C[i] and move back to C[i] during downtime.
    6. Start simulation. When an order comes in, check if primary DG for that area can deliver order.
      -this check includes taking last 5 pts of [current route + new delivery] and checking for availability.
      -(the above and other small steps could have significant impacts)
    7. If primary DG unavailable, apply same process for secondary DG, and the tertiary DGs.
    8. If still not available, save as undelivered and move on.
    9. If count of undelivered exceeds 7% of total deliveries -- end simulation.
    10. If end process, redefine radius as midway length between failed and successful radii
    ----
    Use above process to:
        a. find max radii within undeliverable limit
        b. find max radii with 0 undeliverables
        c. randomize vendor and delivery locations & run again until 95% confidence level

Possible Business Names:
-orcabee

@author: sethchase
