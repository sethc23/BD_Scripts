# NOTES
UPDATES + NOTES
Done -- 1. problem with picking right del_ID.  it should be based on first occurences in dynamic_dg_q.deliv_id

Done -- 2. figure out to fully reverse effect of checking combos for partial trips

Done -- 3.  Why is id==32 starting at 11 with order_time=4 at T=5 ?
    Why does dg_q_group not have destination for 1351 ?

Done -- 4. add option to verify clean_order_results

5. re-work dg_pool to:
    -only have purposeful information in rows
    -keep totalDeliveries column
    -to be updated on each access point (newDG,re-pool,new order assignment)
    -use sorted dg_pool to provide order for bestCombo
    -should be up-to-date with all location information(or at least be accessible)

Done -- 6. change graph 3 to combine plots with mean of Orders aligned and scaled right

Done -- isolate/consolidate changes to global data vars to single function (for simplicity and debugging)

Done -- 7. re-do delivery count on remove order

Done -- 8. change function that creates dg_q data from order_q data to start at certain point in time.
            -This seemed required when presented with the case of a second order completing before a first order,
                which left a gap of time in the order_q_i and thus the pulled dg_q.

9. QUERY: Should pull dg_q order function always include row from dg_X/Y to first point?
    - this is posed in light of dg_X/Y always being up-to-date.

10. re-implement dictionary for time-to-position for each DG in dg_pool.

Done -- 11. changed getComboInfo to uniformly select static orders and dg_q

Done -- 12. checked all index sorting to confirm that ascending=True was intended to mean [0,4,4]

Done -- 13. created function to re-order dg_q points based on mock_pt so points are always paired, A1,A2,B1,B2, etc..

company name -- BC, BC Delivery, BCD,

why is there a marked feature that the number of active DG first begins to closely follow number of Active Deliveries
    at t=40?  40 is of course the number that also corresponds with the maximum delivery time.

but why is the mean number of orders per DG continuous decline at t<20 maybe t<10?

----

    driver of this system is the orders.
    ??  the total travel time/dist for all DG  x  speed == the number of used DG  x  total number of minutes

    if each DG is working for total_time, and DG travels at 1 point per minute, then each DG will travel total_time points.
    if all DG are working for total_time, then (number of DG * total_time) should equal total dist traveled by DG.
    --at the very least, the numbers should be the same for all results.

    re-pool should start small and build out as necessary in increments (e.g., 20). the increment size could be based on times of the day.

    group selection for checking availability should be based segmentations of most deliveries, i.e., five equal segments based on count of
    totalDG_pool but ordered most-to-least deliveries.


        (timing could also be changed to be at the moment DG needs to make the decision)

    group selection could be secondarily re-analyzed at decision times.

    i can say at any given point in time, an attractive force in one direction and magnitude is acting on an object.
    what is that direction and magnitude at time Z ?

        that direction will unlikely be a straight line.


    total_time * No. of DG

    1 pt per minute


    dg_pool needs to be the source of available DG
    (as opposed to those DG on the order_q being selected,
    which works early on but not later when smaller pool)

        -

