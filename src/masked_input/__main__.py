from masked_input import masked_input

if __name__ == '__main__':
    password = masked_input(
    prompt='Enter your password: '
    )

    print(f'Your password is: {password}')
