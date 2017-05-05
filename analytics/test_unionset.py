user_merged = [
    set([1,2,3]),
    set([2]),
    set([4]),
    set([5]),
    set([4,5,6]),
    set([6]),
    set([7,8,9]),
    set([3,4])
]

##########################
# Danning Algo
##########################

user_n = len(user_merged)

visited = [0] * user_n # init all sets' states as 'not visited'
# visited state:
# 0: not visited set
# 1: visited, fully checked sets
# 2: visited, deleted set
# 3: temporary state, need to be compared again
i = 0
while( i < user_n ): # the first set i
    if visited[i] == 0: # if this set i hasn't been visited, then visit
        for j in range(i + 1, user_n): # all other following sets j
            if visited[j] == 0: # if this set j hasn't been visited, then visit
                if (user_merged[i] & user_merged[j]): # if there are intersected, then union them
                    user_merged[i] = user_merged[i] | user_merged[j] # union set j's elements into the first set i
                    visited[j] = 2 # delete this set j
                    visited[i] = 3 # re-check this set later
                    break
                #else: if there are not intersected then continue the loop

            #else: if the set j is deleted or  then go on to the next set j+1

        # inner loop finished, meaning that the set i's comparison is fully checked, no other sets have common elements with it, then mark it as 1
    if visited[i] == 3: # if this set is merged, compare it with all the other sets again
        visited[i] = 0 # initiate its state, stay on this loop
    elif visited[i] ==2: # if this set is deleted, go to next loop
        i +=1
    else:           # if this set is fully checked and not merged, it won't have any intersection anymore.
        visited[i] = 1 # mark it as finished and go to next loop.
        i += 1

    #else: the set i is deleted, we don't need to do anything, just go on with the loop.

# we only need those expanded sets whose state is marked as 1
user_list = []
for i in range(user_n):
    if (visited[i] == 1):
        user_list.append(list(user_merged[i])) # here in the list are all the user clusters


#######
print user_list