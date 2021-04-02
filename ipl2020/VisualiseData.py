def get_glove(glove):
    import numpy as np

    glove_dict = glove.dictionary
    glove_vecs = glove.word_vectors
    word_vecs = []
    for item in glove_dict:
        # print(glove_vecs[glove_dict[item]])
        word_vec = []
        word_vec.append(item)
        word_vec.extend(glove_vecs[glove_dict[item]])
        word_vecs.append(word_vec)

    np_array = np.array(word_vecs)  # .reshape(-1, 51)
    np.savetxt('file.txt', np_array, fmt='%s')