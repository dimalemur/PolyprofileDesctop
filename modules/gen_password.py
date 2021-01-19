import random

# Доступные символы для генерации пароля
chars = '@!№#%^,.;:)(/]['
chars_numbers = '1234567890'
chars_lc = 'abcdefghijklnopqrstuvwxyz'
chars_uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
all_chars = chars + chars_numbers + chars_lc + chars_uc


def gen_password():
    lc = 0
    uc = 0
    numbers = 0
    ch = 0
    pass_count = 0
    password = ''
    count = random.randint(6, 12)
    for i in range(count):
        if lc < 1:
            password += random.choice(chars_lc)
            pass_count += 1
            lc += 1
        if uc < 1:
            password += random.choice(chars_uc)
            pass_count += 1
            uc += 1
        if numbers < 1:
            password += random.choice(chars_numbers)
            pass_count += 1
            numbers += 1
        if ch < 1:
            password += random.choice(chars)
            pass_count += 1
            ch += 1

    if pass_count < count:
        for pass_count in range(count):
            password += random.choice(all_chars)

    password = ''.join(random.sample(password, len(password)))

    return password