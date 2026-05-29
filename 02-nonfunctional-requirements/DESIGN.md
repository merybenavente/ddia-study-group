## Assignment Design: dispatch system

Design a ride-sharing dispatch system that matches riders with nearby drivers in real time. Reason through the nonfunctional requirements: what does "fast" mean (percentiles, not averages), what faults do you tolerate, how do you handle demand spikes, and how maintainable is your design two years from now.

- SLOs with real numbers:
    - for reading actions like avb restaurants, menus, etc there SLO should be p99 under 1s
    - for computations like matching riders i see a difference between how long the matching algorithm takes computationally VS how long till there's a match (that relies on external factors like availability)
- choose a matching strategy
    - i think it would have two queues, and just pop/match if they are within the area (area meaning that they are within a range for both pick up and drop off + there's room for everyone) and if not iterate over the list till there's a match. The SLO under no supply constrains should be p99 under 20s.
    - lets say that there's a spike and there are no cars while too much demand. If after the SLO of 3 minutes for matching there's still no driver available within a 5min ETA i would ask the user if they want to leave the queue or stay, and they would be the first to be picked up. Under high demand we can group people in the queue based on similar destination areas so that we better use our existing supplies (to implement this we can first test it internally using data for the past to assess if the extra computation actually brings benefits ie reduced waiting time + optimal usage of the car pool).
    - a matching strategy that i thought about and rejected is  kicking people out to get the queue moving but i think that it's better if we let the user decide and wait to get the service.
- identify faults and your tolerance for each, explain your scaling approach for rainstorm-Friday spikes.
    - A driver's GPS stops updating -> if they are not half way a ride i would kick them out and inform them, till that gets fixed. if they are delivering a service i would let it continue unless there's a reported incedence and just assume that it all went well if no one reports an error, and once the ride finishes dont allow the drive to get back to the system untill the GPS is back.
    - The matching service crashes mid-assignment -> that's a failure, the SLA should be have it back within 30s for example and that could happen if we have a second machine ready to take the work and we start running there. If there's not a machine available i choose to notify the user that the service if temporary unavailable and that they should try in a minute.
    - A database node goes down -> we should have replicas of that DB, we should move our read/writes to another one and we would need to build the lost information from the logs and check if there are any actions pending notifications (if something is not logged is saver to assumed it didnt' happened and renotified, rather than miss it)


Include rejected alternatives with reasoning.
