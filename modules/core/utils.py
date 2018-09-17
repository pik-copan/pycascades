"""utils module

Provides functions/methods to make life easier.
"""
import matplotlib.pyplot as plt
import networkx as nx

def plot_network(c_data_value):
    net = c_data_value["net"]
    pos=nx.spring_layout(net)
    nx.draw_networkx(net,pos)
    nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
    plt.show()
    
def plot_cascade(c_data_value):
    plt.plot(c_data_value["t_array"],c_data_value["time_series"])
    plt.show()
    
def play_sound(path_to_file):
    try:
        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file(path_to_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except:
        pass