import itertools
from pyeda.inter import ttvars, truthtable, espresso_tts
from parse_espresso_tree import parse_tree


def perms_to_dnf_tree(target_subset_list, n=7):
    # mapping from boolean var index to the actual pair it represents
    pairs = get_variable_pairs(n)
    num_vars = len(pairs)
    
    all_perms = itertools.permutations(range(1, n + 1))
    valid_indices = {permutation_to_index(p, pairs) for p in all_perms}
    target_indices = {permutation_to_index(p, pairs) for p in target_subset_list}
    
    # tt_string[i] is the output value of the i'th row of the truth table if ordered lexicographically (can be 0, 1, or - for 'dont care')
    tt_string = build_truth_table(target_indices, valid_indices, num_vars)

    # this is the step that takes 40s with n=7
    minimized_dnf = minimised_dnf_from_tt(tt_string, num_vars)

    parsed_tree = parse_tree(minimized_dnf.to_ast(), pairs) 
    
    return parsed_tree


def get_variable_pairs(n):
    return [(i, j) for i in range(1, n) for j in range(i + 1, n + 1)]


def permutation_to_index(perm, pairs):
    pos = {val: idx for idx, val in enumerate(perm)}
    index = 0
    for bit_idx, (i, j) in enumerate(pairs):
        if pos[i] < pos[j]:
            index += (1 << bit_idx)
    return index


def build_truth_table(target_indices, valid_indices, num_vars):
    # vast majority of the table (2^(nC2)-n!) is a "don't care" state, corresponding to invalid variable values (e.g. a<b b<c but not a<c)
    tt_array = ['-'] * (2 ** num_vars)
    
    for idx in valid_indices:
        tt_array[idx] = '0'
        
    for idx in target_indices:
        tt_array[idx] = '1'
        
    return "".join(tt_array)


def minimised_dnf_from_tt(tt_string, num_vars):
    X = ttvars('x', num_vars)
    tt = truthtable(X, tt_string)
    minimized_tuple = espresso_tts(tt)
    return minimized_tuple[0]



# test
if __name__ == "__main__":
    n = 6
    
    subset = [
        p for p in itertools.permutations(range(1, n + 1)) 
        if p.index(1) < p.index(2) and p.index(2) < p.index(3)
    ]
    
    print(subset)

    result_tree = perms_to_dnf_tree(subset, n=n)
    
    print(result_tree)