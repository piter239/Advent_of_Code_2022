# solution to https://adventofcode.com/2022/day/11

class Monkey:
    def __init__(self, id=0, items=(), op='', test='', give_to=(0,0)):
        self.id = id
        self.items = list(items)
        self.op = op
        self.test = test
        self.give_to = list(give_to)
        self.inspected_items = 0

    def __str__(self):
        return f'Monkey {self.id}' + '\n' + \
               f'  holding {self.items}' + '\n' + \
               f'  performing {self.op}' + '\n' + \
               f'  test {self.test}' + '\n' + \
               f'    giving to {self.give_to}' + '\n' + \
               f'  has handled {self.inspected_items} items' + '\n'


#def do_it():
monkeys = []

NOK = 1

with open("11input.txt", "r") as f:
    # read each line of the file
    for line in f:
        line = line.replace(',', '').replace(':','')
        print(line)
        match line.split():
            case ["Monkey", i]:
                monkeys.append(Monkey(id=int(i)))
            case ["Starting", "items", *lst]:
                monkeys[-1].items = list(map(int,lst))
            case ["Operation", _, _, _, op, const]:
                if const == 'old':
                    monkeys[-1].op = '**=2' # handling the case new = old * old
                else:
                    monkeys[-1].op = f'{op}={const}'
            case ["Test", "divisible", "by", const]:
                monkeys[-1].test = f' % {const} == 0'
                NOK *= int(const)
            case ["If", flag, "throw", "to", "monkey", id]:
                monkeys[-1].give_to[flag == 'true'] = int(id)

print("Monkeys", *monkeys)

# Simulate the monkeys' actions for 20 rounds
for round in range(1, 10001):
    # Iterate through each monkey
    for i, monkey in enumerate(monkeys):
        # Iterate through each item the monkey is holding
        while monkey.items:
            item = monkey.items.pop(0)
            # Perform the operation on the item

            exec(f'item{monkey.op}')

            # Divide the item by 3 and round down
            item = item % NOK

            # Using test, decide where to throw the item to
            give_to = monkey.give_to[eval(f'item {monkey.test}')]

            assert (0 <= give_to <= len(monkeys))

            monkeys[give_to].items.append(item)
            monkeys[i].inspected_items += 1
    inspect = [20, 500, 600, 700, 800] + list(range(900,1000,5)) + list(range(1000,10001,1000))
    if round in inspect:
        print(f"=============Round {round} finishes: ==================")
        #print("Monkeys", *monkeys)
        res = []
        for monkey in monkeys:
            print("Monkey", monkey.id, 'inspected', monkey.inspected_items, 'items')
            res.append(monkey.inspected_items)


print(f"Result:")
res = []
for monkey in monkeys:
    print("Monkey", monkey.id, 'inspected', monkey.inspected_items, 'items')
    res.append(monkey.inspected_items)

res.sort()
print(res[-1]*res[-2])
print(res)

# Print the number of items inspected by each monkey
# print(monkeys_inspected_items)


#import cProfile

#cProfile.run('do_it()')

#do_it()
