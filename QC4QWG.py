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
    from qiskit import execute
    from CongX.extensions.standard.bmx import BMXGate
    import math
    # 量子レジスタ(グラフに対応した探索空間)を用意
    result_prepare_register = prepare_register(G, step)
    register_list = result_prepare_register[0]
    res_register = result_prepare_register[1] 
    register_size = result_prepare_register[2] 
    
    # 量子レジスタ(コイン空間)を用意
    degree_set = adj_to_coin(G)
    coin_registers = prepare_coin(deree_set)
    register_list.append(*coin_registers)
    
    # 観測結果を格納するための古典レジスタを用意
    cr = ClassicalRegister(register_size, 'result')
    
    # 量子回路を用意(レジスタをまとめる)
    qc =  QuantumCircuit(*register_list)
    
    # 量子計算
    ## 初期状態を生成
    initial_distribution(G, qc, t0_register)
    # エッジを遷移の情報ごとにまとめてゲートとして呼び出す
    gates = graph_to_gate(G, register_size, degree_set)
    gates = sort_gate(gates)
    for j in range(step):
        call_gate(gates)
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
    return register_list, res_register, register_size  
    
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

def initial_distribution(G, qc, t0_register):
    # 重ね合わせで初期状態を準備
    qc.h(t0_register[0:-1])
    

def graph_to_gate(G, register_size, degree_set):
    # エッジのリスト
    edge_list = list(G.edges)
    # エッジに対応した用いるコインのリスト
    degrees = list(G.degree)
    
    
    # エッジがノードにとって何番めのエッジか(どのコイン状態を用いるのか)
    edge_number_list = [0,1,2,0,1,...みたいな]
    # エッジごとにゲートに整形する
    for edges in edge_list:
        nodeA = edge[0]
        nodeB = edge[1]
        control = bin(int(nodeA))
        ゼロパディング
        
    
    
def sort_gate():
    # あとあとコンパイルしやすいようにターゲットゲートごとに同じものを揃える

    
def call_gate(edge, coin_info)
