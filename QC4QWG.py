def QC4QWG(G, step):
    # グラフ上量子ウォーク。グラフを工夫すれば2次元格子なども...
    from qiskit import QuantumCircuit
    from qiskit import QuantumRegister
    from qiskit import ClassicalRegister
    from qiskit import execute
    from CongX.extensions.standard.bmx import BMXGate
    import math
    import copy
    # 量子レジスタ(グラフに対応した探索空間)を用意
    result_prepare_register = prepare_register(G, step)
#     print('result_prepare_register')
#     print(result_prepare_register)
    register_list = result_prepare_register[0]
    state_register_list = copy.copy(register_list)
    initial_register = result_prepare_register[1] 
    res_register = result_prepare_register[2] 
    register_size = result_prepare_register[3] 
    
    # 量子レジスタ(コイン空間)を用意
    degree_set = adj_to_coin(G)
    coins = prepare_coin(degree_set)
    coin_registers = coins[0]
    coin_registers_dict = dict(zip(coins[1],coins[0]))
    for coin_register in coin_registers:
        register_list.append(coin_register)
    
    # 観測結果を格納するための古典レジスタを用意
    cr = ClassicalRegister(register_size, 'result')
    register_list.append(cr)
    # 量子回路を用意(レジスタをまとめる)
    qc =  QuantumCircuit(*register_list)
    for j in coin_registers:
        qc.h(j[0:])
    # 量子計算
    ## 初期状態を生成
    initial_distribution(G, qc, t0 = initial_register)
    # エッジを遷移の情報ごとにまとめてゲートとして呼び出す
    for j in range(step):
        ops = graph_to_gate(G, register_size, degree_set, state_register_list, coin_registers_dict, step_num= step)
        for op in ops:
#             con_bin = op[0]
#             con_regs = op[1]
#             for register in con_regs:
#                 register[0:]
#             tgt_qubits = op[2]
            print('op')
            print(op)
            qc.bmx(*op)
    # 観測
#     qc.measure(res_register, cr)
    return qc

    
def prepare_register(G, step):
    import math
    from qiskit import QuantumRegister
    # ノード数を求め、step数分のレジスタを用意する
    num_nodes = G.number_of_nodes()
    register_size = math.ceil(math.log2(num_nodes))
    register_list = []
    for i in range(step+1):
        register_name = 't' + str(i) 
        qr = QuantumRegister(register_size, register_name)
        register_list.append(qr)
    initial_register = register_list[0]
    res_register = register_list[-1]
    return register_list, initial_register, res_register, register_size  
    
def adj_to_coin(G):
    # 隣接行列を元にコイン用のパラメータ(次数)をリストとして返す
    degree_set = []
    deg_list = list(G.degree)
    for deg in deg_list:
        degree_set.append(deg[1])
    degree_set = set(degree_set)
    return degree_set
    
def prepare_coin(degree_set):
    import math
    coin_registers = []
    num_qubits_list = []
    from qiskit import QuantumRegister
    # コインオペレータ
    for degree in degree_set:
        reg_name = 'coin'  + str(degree)
        # grover coinなどの差し替えを検討
        # 偶数ならアダマール、奇数なら...どうすんだっけ
        num_qubits = math.ceil(math.log2(degree))
        if num_qubits != 0:
            qr = QuantumRegister(num_qubits, reg_name)
            coin_registers.append(qr)
            num_qubits_list.append(degree)
    return coin_registers, num_qubits_list

def initial_distribution(G, qc, t0):
    # 重ね合わせで初期状態を準備
    qc.h(t0[0:])
    

def graph_to_gate(G, register_size, degree_set, state_register_list, coin_registers_dict, step_num):
    import math
    from qiskit import QuantumRegister
    from CongX.extensions.standard.bmx import BMXGate
    edges = G.edges
    ops= []
    # ノードごとにdictとして残りのエッジの本数をとっておく
    deg_dict = dict(G.degree)
    deg_dict2 = dict(G.degree)
    # エッジに番号をふっておく
    for edge in edges:
        nodeA = edge[0]
        nodeB = edge[1]
        # コントロール部前半: 遷移前ノード
        binary_nodeA = bin(nodeA)
        binary_nodeA = binary_nodeA.strip('0b')
        binary_nodeA_zero = binary_nodeA.zfill(register_size)
#         print('binary_nodeA_zero')
#         print(binary_nodeA_zero)
        node_reg_name_c = 't' + str(step_num-1)
        # コントロール部後半: コイン
        # 量子ビット: coin + 'そのノードの次数'
        coin_reg_name = deg_dict[nodeA]  
        coin_size = deg_dict2[nodeA]
        edge_number = bin(deg_dict[nodeA])
#         print('deg_dict')
#         print(deg_dict[nodeA])
        edge_number = edge_number.strip('0b')
        coin_qubit_size = math.ceil(math.log2(deg_dict[nodeA]))
#         print(coin_qubit_size)
        edge_number_zero = edge_number.zfill(coin_qubit_size)
#         print('edge_number_zero')
#         print(edge_number_zero)
        # コントロール部の結合
#         print(coin_registers_dict)
        control_qubits = [state_register_list[step_num-1][0:] + coin_registers_dict[coin_size][0:]]
        binary =  binary_nodeA_zero + edge_number
#         print('control_binary')
#         print(binary)
        # ターゲット部: 反転させる必要がある量子ビット
        binary_nodeB = bin(nodeB)
        binary_nodeB = binary_nodeB.strip('0b')
        binary_nodeB = binary_nodeB.zfill(register_size)
        binary_nodeB = list(binary_nodeB)
         # ノード番号をバイナリに変換、000...0から反転させる必要がある量子ビットを集める
        node_reg_name_t = 't' + str(step_num + 1)
        trues = []
        a = 0
        for bit in binary_nodeB:
            if bit == '1':
                trues.append(a)
                a += 1
            elif bit == '0':
                a += 1
            else:
                print('error')
                
        deg_dict[nodeA] -= 1
        deg_dict[nodeB] -= 1
        target_register = state_register_list[step_num]
        if trues == []:
            print('truesが無')
        else:
            target_qubits = []
            for true in trues:
                if true == 0:
                    number = 0
                else:
                    number = math.ceil(math.log2(true))
                target_qubits.append(target_register[number])
                
                op = [binary,*control_qubits,target_qubits]
                ops.append(op)
    return ops
                
def footprint(G, step, backend = 'ibmq_qasm_simulator',initial_state = None, shots = 1000):
    #ステップ数ごとに作った確率分布を可視化する。 initial_stateを入力して単純な重ね合わせ以外にも対処できると嬉しいのかな
    from qiskit.tools.monitor import job_monitor
    backend = provider.get_backend(backend)
    counts = []
    for i in step:
        job = execute(QC4QWG(G, step), backend, shots = shots)
        job_monitor(job_exp, interval = 2)
        result = job.result()
        count =result.get_counts()
        counts.append(count)
    return counts