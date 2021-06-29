# This is a sample Python script.
from random import randrange
from tkinter import *
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from networkx import shortest_path, dijkstra_path, floyd_warshall_predecessor_and_distance, reconstruct_path

G = nx.Graph()
start = ""
stop = ""

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def generer_graphe():
    global G
    G = nx.Graph()
    nodes = []
    for i in range(1, randrange(3, 16)):
        nodes.append(i)
    G.add_nodes_from(nodes)

    for node in G.nodes:
        others = list(G.nodes)
        others.remove(node)
        edges = list(G.edges(node))
        for i in range(randrange(5)-len(edges)+1):
            partner = others[randrange(len(others))]
            if (node, partner) not in edges and (partner, node) not in edges:
                G.add_edge(node, partner, weight=randrange(1,10))

def display_graphe():
    global G
    options = {
        "font_size": 17,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 3,
        "width": 3,
    }
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, **options)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

    # f = plt.Figure(figsize=(5, 5), dpi=100)
    # canvas = FigureCanvasTkAgg(f, frame)
    # canvas.get_tk_widget().grid(row=5, column=5)
    # frame.pack()

def nouveau_graphe():
    generer_graphe()
    display_graphe()

def onChangeSS(start_stop_sv, error_label_sv):
    global G
    global start
    global stop
    ssSv = start_stop_sv.get()
    try:
        ssList = ssSv.split(":")
        if G.has_node(int(ssList[0])) and G.has_node(int(ssList[1])):
            start = int(ssList[0])
            stop = int(ssList[1])
            error_label_sv.set("Valid arguments")
        else:
            error_label_sv.set("Invalid arguments!!!")
    except IndexError as error:
        error_label_sv.set("Invalid arguments!!!")
    except ValueError as error:
        error_label_sv.set("Invalid arguments!!!")

def djikstra_cb(error_label_sv, res_sv):
    global G
    global start
    global stop

    if error_label_sv.get != "Valid arguments":
        res_sv.set(str(dijkstra_path(G, start, stop, weight='weight')))
    else:
        res_sv.set("Invalid arguments, please try again")

def floyd_marshall_cb(error_label_sv, res_sv):
    global G
    global start
    global stop

    if error_label_sv.get != "Valid arguments":
        predecessors, _  = floyd_warshall_predecessor_and_distance(G, weight='weight')
        res_sv.set(str(reconstruct_path(start, stop, predecessors)))
    else:
        res_sv.set("Invalid arguments, please try again")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    tk = Tk()
    tk.title("Routage")
    tk.geometry("1280x720")

    pw = PanedWindow(tk, orient=HORIZONTAL, sashrelief=RAISED, sashwidth=4)
    pw.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

    menu = Frame(pw)
    graphe = Frame(pw)
    pw.add(menu, minsize="160", width="320")
    pw.add(graphe, minsize="777")

    pw.pack()

    ouvrir = Button(menu, text="Ouvrir graph (txt)")
    generer = Button(menu, text="Générer graph", command=nouveau_graphe)

    start_stop_label = Label(menu, text=" Enter start & stop this way: [Start]:[Stop]")

    error_label_sv = StringVar(value="Invalid arguments")
    error_label = Label(menu, textvariable=error_label_sv)

    start_stop_sv = StringVar();
    start_stop_sv.trace("w", lambda name, index, mode, sv=start_stop_sv: onChangeSS(start_stop_sv, error_label_sv))

    start_stop_entry = Entry(menu, textvariable=start_stop_sv)

    res_sv = StringVar()
    res_label = Label(menu, textvariable=res_sv)
    res_length_sv = StringVar()
    res_length_label = Label(menu, textvariable=res_length_sv)

    djikstra = Button(menu, text="Djikstra", command=lambda: djikstra_cb(error_label_sv, res_sv))
    floyd_marshall = Button(menu, text="Floyd-Warshall", command=lambda: floyd_marshall_cb(error_label_sv, res_sv))

    #ouvrir.pack()
    generer.pack()
    start_stop_label.pack()
    error_label.pack()
    start_stop_entry.pack()
    djikstra.pack()
    floyd_marshall.pack()
    res_label.pack()
    res_length_label.pack()

    nouveau_graphe()

    tk.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
