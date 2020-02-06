def footprint(G, step, backend = 'ibmq_qasm_simulator',initial_state = None, shots = num_shot):
    #ステップ数ごとに作った確率分布を可視化する。 initial_stateを入力して単純な重ね合わせ以外にも対処できると嬉しいのかな
    from qiskit.tools.monitor import job_monitor
    backend = provider.get_backend(backend)
    counts = []
    for i in step:
        job = execute(QC4QWG(G, step), backend, shots = num_shot)
        job_monitor(job_exp, interval = 2)
        result = job.result()
        count =result.get_counts()
        counts.append(count)
    return counts
    # グラフ上の描画はだるいので後回し
    # ノードの座標を固定して大きさとしてnetworkXで描画
    

def QC4QWG(G, step):
    # グラフ上量子ウォーク。グラフを工夫すれば2次元格子なども...
    from qiskit import QuantumCircuit
    from qiskit import QuantumRegister
    from qiskit import ClassicalRegister
    import math
    # 量子レジスタ(グラフに対応した探索空間)を用意
    result_prepare_register = prepare_register(G, step)
    register_list = result_prepare_register[0]
    res_register = result_prepare_register[1] 
    
    # 量子レジスタ(コイン空間)を用意
    degree_set = adj_to_coin(G)
    coin_registers = prepare_coin(deree_set)
    register_list.append(*coin_registers)
    
    # 観測結果を格納するための古典レジスタを用意
    c = ClassicalRegister(数字、 'result')
    
    # 量子回路を用意(レジスタをまとめる)
    qc =  QuantumCircuit(*register_list)
    
    # 量子計算
    ## 初期状態を生成
    initial_distribution(G, qc, t0_register)
    # 遷移の情報ごとにまとめてゲートとして呼び出す
    
    for step in steps:
        for edge in edges:
            コントロール1 遷移前
            コントロール2 コイン
            ターゲット1 
        for gate in gates:
        
    # 観測
    qc.measure(res_register, cr)
    return qc

    
def prepare_register(G, step):
    # ノード数を求め、step数分のレジスタを用意する
    num_nodes = nx.number_of_nodes(G)
    register_size = math.ceil(math.log2(num_nodes))
    register_list = []
    for i in range(step):
        register_name = 't' + str(i) 
        qr = QuantumRegister(register_size, register_name)
        register_list.append(qr)
    res_register = register_list[-1]
    return register_list, res_register  
    
def adj_to_coin(G):
    # 隣接行列を元にコイン用のパラメータ(次数)をリストとして返す
    degree_set = []
    deg_list = list(G.degree)
    for deg in deg_list:
        degree_set.append(deg[1])
    degree_set = set(degree_set)
    return degree_set
    
def prepare_coin(degree_set):
    # コインオペレータ
    for degree in degree_set:
        reg_name = 'coin'  + str(degree)
        # grover coin
        # 偶数ならアダマール、奇数なら...どうすんだっけ
        qr = QuantumRegister()
        
    return coin_registers

def edge_to_transition(edge, initial):
    # 遷移先のノードへの移動に相当するゲートを作る。
    
    基本的には遷移先は初期化されているので反転するビットの情報を作る
    Xゲートの対象を返す
    
    
def

def initial_distribution(G, qc, t0_register):
    # 重ね合わせで初期状態を準備
    qc.h(t0_register[0:-1])