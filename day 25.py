def reverse_modulo(key, subject_message, salt):
    while key % subject_message != 0:
        key += salt
    return key

def crack(key, subject_message, salt):
    loop_counter = 1
    while key != subject_message:
        loop_counter += 1
        key = reverse_modulo(key, subject_message, salt)
        key //= subject_message
    return loop_counter

def transform(loops, subject_message, salt):
    value = 1
    for _ in range(loops):
        value *= subject_message
        value %= salt
    return value

with open('25input1.txt', 'r') as f:
    door_key, card_key = [int(l) for l in f.read().split('\n')]
    door_loop_cycle = crack(door_key, 7, 20201227)
    card_loop_cycle = crack(card_key, 7, 20201227)

    print(transform(door_loop_cycle, card_key, 20201227))
    print(transform(card_loop_cycle, door_key, 20201227))