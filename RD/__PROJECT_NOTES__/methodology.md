# METHODOLOGY
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


MODIFICATION TO FIRST IMPLEMENTATION:

    1. save best combo for one less delivery and all other returnVars
    2. save average X/Y for reduced best combo and for outer_delivery
    3. after each distribution, re-distribute and look move orders to DG with better positioning
    4. do step 3 in one iteration, starting with most inconvenient order
