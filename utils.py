import cupy as cp

def create_state(psi, phi, theta):
    phase = cp.exp(psi*1.j)

    cos = cp.cos(theta / 2)
    sin = cp.sin(theta / 2)

    active_phase = cp.exp(phi*1.j)

    return phase * cp.array([cos, active_phase * sin])

def tensor_product_vector_list(vector_list):
    if len(vector_list) > 1:
        tmp = (vector_list[0][:, None] * vector_list[1][None, :]).reshape(4,)

        for i in range(2, len(vector_list)):
            tmp = (tmp[:, None] * vector_list[i][None, :]).reshape(2 ** (i + 1),)
    else:
        tmp = vector_list[0]
    
    return tmp 

def tensor_product_matrix_list(matrix_list):
    if len(matrix_list) == 1:
        tmp = matrix_list[0]
    else:
        tmp = cp.kron(matrix_list[0], matrix_list[1])

        for i in range(2, len(matrix_list)):
                tmp = cp.kron(tmp, matrix_list[i])
    
    return tmp

def reorder_gate(G, new_control, new_target, circuit_length):
    perm = [-1] * circuit_length

    perm[new_control] = 0
    perm[new_target] = 1

    counter = 2
    for _ in range(circuit_length):
        if perm[_] == -1:
            perm[_] = counter
            counter += 1

    # reorder both input and output dimensions
    perm2 = perm + [circuit_length + i for i in perm]
    
    return cp.reshape(cp.transpose(cp.reshape(G, 2*circuit_length*[2]), perm2), (2**circuit_length, 2**circuit_length))

def reorder_gate_three(G, new_one, new_two, new_three, circuit_length):
    perm = [-1] * circuit_length

    perm[new_one] = 0
    perm[new_two] = 1
    perm[new_three] = 2

    counter = 2
    for _ in range(circuit_length):
        if perm[_] == -1:
            perm[_] = counter
            counter += 1

    # reorder both input and output dimensions
    perm2 = perm + [circuit_length + i for i in perm]
    
    return cp.reshape(cp.transpose(cp.reshape(G, 2*circuit_length*[2]), perm2), (2**circuit_length, 2**circuit_length))