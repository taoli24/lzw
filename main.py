def lzw_encoder(input_data, bits = 6, binary = True):
    table = {}
    res = []

    max_key = sum(2**i for i in range(bits))

    # creating default compression table - ASCII
    if not binary:
        for i in range(0, 255):
            table[chr(i + 1)] = i + 1
        next = 255
    else:
        for i in range(2):
            table[str(i)] = i
        next = 2

    idx = 0
    while idx < len(input_data):
        current = input_data[idx]
        current_idx = idx

        while current in table:
            current_idx = current_idx + 1 if current_idx < len(input_data) - 1 else None
            idx += 1

            if current_idx:
                current = current + input_data[current_idx]
            else:
                current += chr(10000)

        if current[-1] != chr(10000) and next <= max_key:
            table[current] = next
            next += 1

        current = current[:-1]
        res.append(table[current])

    return res, bits ,{v:k for k,v in table.items()}



def lzw_decode(lzw_encoding, bits = 6, binary=True):
    table = {}
    res = ""

    max_key = sum(2**i for i in range(bits))

    # creating default compression table - ASCII
    if not binary:
        for i in range(0, 255):
            table[i + 1] = chr(i + 1)
        next_ind = 255
    else:
        for i in range(2):
            table[i] = str(i)
        next_ind = 2

    for x in range(len(lzw_encoding)):
        encoding = lzw_encoding[x]

        if x == len(lzw_encoding) - 1:
            if encoding in table.keys():
                res += table[encoding]
            else:
                print("last encoding not in table")
            break
        else:
            if encoding in table.keys():
                current = table[encoding]
                res += current

                if next_ind <= max_key:
                    table[next_ind] = current + table.get(lzw_encoding[x+1], current)[0]
                    next_ind += 1

    return res