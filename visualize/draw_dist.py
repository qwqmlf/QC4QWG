"""
入力: グラフ、分布
出力: gif

"""
def make_list(res):
    '''
    make list of the result(from IBMQ backend)
    input example {'00011': 29, '10101': 23, '00101': 38, '10001': 21...}
    output example [[3, 29], [21, 23], [5, 38]....]
    '''
    pairs = []
    for re in res:
        pair = [re, res[re]]
        pairs.append(pair)

    for pair in pairs:
        pair[0] = int(pair[0],2)
    return pairs

def make_alpha_list(pairs,G):
    '''
    make a list for visualize data as alpha nodes
    '''
    alpha_dict = {}
    for pair in pairs:
        alpha = int(pair[1]) / 1000
        alpha_dict[pair[0]] = alpha
    alpha_list = _alpha_dict_to_list(alpha_dict, G)
    return alpha_list

def _alpha_dict_to_list(alpha_dict, G):
    alpha_list = []
    for j in G.nodes():
        alpha_list.append(alpha_dict.get(j, '0'))
    return alpha_list


def make_color(pairs):
    color_pair = []
    for pair in pairs:
        ratio =  int(pair[1]) / 1000
        color = convert_to_color_code(ratio)
        color_pair.append([pair[0],color])
    return color_pair

def convert_to_color_code(a) :
    '''
    from red to white
    '''
    red = 255
    green = round((1-a)*255)
    blue = round((1-a)*255)
    return '#%02x%02x%02x' % (red, green, blue)

def colors(pairs, G):
    color_dict = {}
    for pair in pairs:
        color_dict[pair[0]] = pair[1]
    color_list = color_dict_to_list(color_dict,G)
    return color_list

def color_dict_to_list(color_dict, G):
    color_list = []
    for j in G.nodes():
        color_list.append(color_dict.get(j, '#ffffff'))
    return color_list