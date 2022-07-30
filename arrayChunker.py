def chunk_array(arr, size):
    """ 
        Returns array 'arr' in mini-arrays of length 'size'.
        
        Sample: 
        For input values, arr = [1, 2, 3, 4, 5] and size = 2, this function would 
        return an array with smaller arrays that each have length of 2 [[1, 2], [2, 3], [4, 5]]
    """
    output_arrays = []
    while len(arr) > size:
        piece = arr[:size]
        output_arrays.append(piece)
        arr = arr[1:]
    output_arrays.append(arr)
    return output_arrays
