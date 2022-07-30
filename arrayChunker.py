def chunk_array(arr, size):
    output_arrays = []
    while len(arr) > size:
        piece = arr[:size]
        output_arrays.append(piece)
        arr = arr[1:]
    output_arrays.append(arr)
    return output_arrays
