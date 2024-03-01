from helpers import chunks


def test_chunks():
    # create a sample input list containing integers from 0 to 49
    input_list = [i for i in range(50)]

    # define the size of each chunk
    chunk_size = 5

    # call the 'chunks' function to split the input list into chunks of the specified size
    result_chunks = list(chunks(input_list, chunk_size))

    # generate the expected chunks manually based on the input list and chunk size
    expected_chunks = [
        input_list[i : i + chunk_size] for i in range(0, len(input_list), chunk_size)
    ]

    # assert that the actual result from the 'chunks' function matches the expected chunks
    assert result_chunks == expected_chunks
