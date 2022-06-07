def is_valid(isbn):
    sum = 0
    isbn = list(isbn.replace("-", ""))

    if len(isbn) != 10:
        return False

    if isbn[-1] == "X":
        isbn[-1] = "10"

    for index in range(len(isbn), 0, -1):
        pointer = isbn[len(isbn)-index]
        if pointer.isdigit():
            sum += index * int(pointer)
        else:
            return False

    return sum % 11 == 0
