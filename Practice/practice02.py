import random as rd

def helper(member_list, team_list):
    # print(best_friend)
    best_friend = "TK"
    score = [ rd.randint(1, 100) for ele in member_list ]
    score.sort(reverse=True)
    print(score)

    def is_team_member(who):
        if who in team_list:
            return (0, who)
        return (1, who)

    def judge():
        print(score)
        output = []
        for m, s in zip(member_list, score):
            if s - rd.randint(1, 10) > 60:
                output.append(m)
        return output

    def update_best(choose_function):
        # global best_friend
        # nonlocal best_friend
        new_best = choose_function()
        if new_best:
            print(new_best)
            best_friend = new_best[0]

    # member_list.sort()
    member_list.sort(key=is_team_member)
    update_best(judge)
    
    print(score)
    print(member_list)
    return best_friend

# best_friend = "Cris"
# members = ["Ashelly", "Ben", "Simon", "Jimmy", "Bruce", "Vicky", "Terisa"]
# teams = ["Ashelly", "Ben", "Simon", "Jimmy"]
# choose = helper(members, teams)

# print(choose)
# print(best_friend)

def calculate():
    try:
        r = 100
        # b = a -- 1
    except Exception as e:
        raise ValueError("Input valid") from e
    else:
        # b = a -- 2
        r = 200
        return r

def handle():
    try:
        r = calculate()
    except ValueError as e:
        print("Calculate Error")
        r = 200
    except Exception as e:
        print("Exception")
        return
    else:
        r += 10
    print(r)

def outer(index):
    flag = True
    def inner():
        flag = False
        print(index)
        print(a)
    a = 10
    inner()
    print(flag)
a = 1
outer(5)
