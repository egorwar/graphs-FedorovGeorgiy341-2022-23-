from graph import Graph
from graphExceptions import *
import time


def verify(var):
    return var == 'true' or var == 'false'


hlp = "╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\n" \
      "║  >>> help  --  see this text again                                                                           ║\n" \
      "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n" \
      "║  >>> create [unique_graph_name] [filename.txt OR graph_name_to_copy OR nothing] [isDirected] [isWeighted]    ║\n" \
      "║  >>> see [existing_graph_name]  --  print graph attributes                                                   ║\n" \
      "║  >>> del [existing_graph_name]  --  delete existing graph                                                    ║\n" \
      "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n" \
      "║  >>> save [existing_graph_name] [filename.txt]  --  write existing graph to file 'filename.txt'              ║\n" \
      "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n" \
      "║  >>> node add [existing_graph_name] [unique_node_name]                                                       ║\n" \
      "║  >>> node del [existing_graph_name] [existing_node_name]                                                     ║\n" \
      "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n" \
      "║  >>> edge add [existing_graph_name] [origin_node_name] [destination_node_name] [weight]                      ║\n" \
      "║  >>> edge del [existing_graph_name] [origin_node_name] [destination_node_name]                               ║\n" \
      "╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n" \
      "║  >>> exit  --  terminate program                                                                             ║\n" \
      "╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝"

graphs = {}

print(hlp)

while True:
    print('\ngraphs: ' + ('no graphs created' if len(graphs.keys()) == 0 else ' '.join(graphs.keys())))
    print('>>>', sep='', end=' ')
    line = input().split(' ')
    if line[0] == 'help' and len(line) == 1:
        print(hlp)

    elif line[0] == 'create' and len(line) >= 3:
        try:
            graphs[line[1]]
        except KeyError:
            if len(line) == 4:
                dir = str.lower(line[-2])
                wgh = str.lower(line[-1])
                if verify(dir) and verify(wgh):
                    graphs[line[1]] = Graph('', dir == 'true', wgh == 'true')
                else:
                    print(
                        f"Error:when creating an empty graph, last 2 params - '{dir}' and '{wgh}' - must be either 'true' or 'false'")

            elif len(line) == 3:
                try:
                    graphs[line[2]]
                except KeyError:
                    try:
                        graphs[line[1]] = Graph(line[2])
                    except Exception as e:
                        print('Exception while trying to read the graph from file:\n')
                        print(e)
                else:
                    try:
                        graphs[line[1]] = Graph(graphs[line[2]])
                    except Exception as e:
                        print('Copy error:\n')
                        print(e)
            else:
                print(f"Error: too many arguments in: '{str(line)}'")
            print(f">>> Graph '{line[1]}' created successfully")
        else:
            print(f"Error: graph '{line[1]}' already exists")

    elif line[0] == 'see' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Attributes of '{line[1]}':")
            graphs[line[1]]()

    elif line[0] == 'del' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Graph '{line[1]}' deleted successfully")
            graphs.pop(line[1])

    elif line[0] == 'save' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            try:
                graphs[line[1]].save(line[2])
            except Exception as e:
                print(f"Exception while trying to save the graph data into file: '{line[2]}'\n")
                print(e)
            else:
                print(f">>> Graph '{line[1]}' data is saved into file '{line[2]}' successfully")

    elif line[0] == 'node' and len(line) == 4:
        if line[1] == 'add':
            try:
                graphs[line[2]]
            except KeyError:
                print(f"Error: graph '{line[2]}' doesn't exist")
            else:
                try:
                    graphs[line[2]].add_node(line[3])
                except Exception as e:
                    print(f"Exception while trying to add node '{line[3]}' into graph: '{line[2]}'\n")
                    print(e)
                else:
                    print(f">>> Node '{line[3]}' added into graph '{line[2]}' successfully")
        elif line[1] == 'del':
            try:
                graphs[line[2]]
            except KeyError:
                print(f"Error: graph '{line[2]}' doesn't exist")
            else:
                try:
                    graphs[line[2]].del_node(line[3])
                except Exception as e:
                    print(f"Exception while trying to delete node '{line[3]}' from graph: '{line[2]}'\n")
                    print(e)
                else:
                    print(f">>> Node '{line[3]}' deleted from graph '{line[2]}' successfully")

    elif line[0] == 'edge' and 5 <= len(line) <= 6:
        if line[1] == 'add':
            try:
                graphs[line[2]]
            except KeyError:
                print(f"Error: graph '{line[2]}' doesn't exist")
            else:
                if len(line) == 6 and not graphs[line[2]].isWeighted:
                    print(f'Cannot add weighted edge to unweighted graph')
                    continue

                if len(line) == 5:
                    line.append(None)
                try:
                    graphs[line[2]].add_edge(line[3], line[4], line[5])
                except Exception as e:
                    print(
                        f"Exception while trying to add edge ['{line[3]}'-'{line[4]}'] with weight '{line[5]}' into graph: '{line[2]}'\n")
                    print(e)
                else:
                    if graphs[line[2]].isWeighted:
                        print(
                            f">>> Edge ['{line[3]}'-'{line[4]}'] with weight '{line[5]}' added into graph '{line[2]}' successfully")
                    else:
                        print(f">>> Edge ['{line[3]}'-'{line[4]}'] added into graph '{line[2]}' successfully")

        elif line[1] == 'del' and len(line) == 5:
            try:
                graphs[line[2]]
            except KeyError:
                print(f"Error: graph '{line[2]}' doesn't exist")
            else:
                try:
                    graphs[line[2]].del_edge(line[3], line[4])
                except Exception as e:
                    print(f"Exception while trying to delete edge ['{line[3]}'-'{line[4]}'] from graph: '{line[2]}'\n")
                    print(e)
                else:
                    print(f">>> Edge ['{line[3]}'-'{line[4]}'] deleted from graph '{line[2]}' successfully")
        else:
            print("Error: incorrect syntax. Type 'help' for help")

    elif line[0] == 'task1' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if not graphs[line[1]].isDirected:
                print("Error: graph is not directed!")
                continue
            print(f">>> Result for graph '{line[1]}' and node '{line[2]}':")
            try:
                graphs[line[1]].lesser_income_then(line[2])
            except GraphError as e:
                print(e)

    elif line[0] == 'task2' and len(line) == 4:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Result for graph '{line[1]}' and nodes '{line[2]}' and '{line[3]}':")
            try:
                print(graphs[line[1]].find_between(line[2], line[3]))
            except Exception as e:
                print(e)

    elif line[0] == 'task3' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if not graphs[line[1]].isDirected:
                print("Error: graph is not directed!")
                continue
            try:
                graphs[line[2]]
            except KeyError:
                try:
                    undir_dict = graphs[line[1]].undirect()
                    graphs[line[2]] = Graph((graphs[line[1]].isWeighted, undir_dict))
                except GraphError as e:
                    print(e)
                else:
                    print(f">>> Graph '{line[2]}' created as an undirected version of graph '{line[1]}':")

            else:
                print(f"Error: graph '{line[2]}' already exists")

    elif line[0] == 'task4' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if not graphs[line[1]].isDirected:
                print("Error: graph is not directed!")
                continue
            print(f">>> Result for graph '{line[1]}':")
            try:
                res = graphs[line[1]].check_tree()
                if res != '':
                    print(f"Tree with root ['{res[1]}'] after removing node ['{res[0]}']")
            except GraphError as e:
                print(e)

    elif line[0] == 'task5' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> For graph '{line[1]}':")
            try:
                res = graphs[line[1]].radius()
                print(f"Radius is: {res[0][0]}\nRadius nodes are: ")
                for el in res:
                    print(el[1], sep='', end=' ')
            except Exception as e:
                print(e)

    elif line[0] == 'task6' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if graphs[line[1]].isDirected or not graphs[line[1]].isWeighted:
                print("Error: graph must be weighted and not directed!")
                continue
            print(f">>> Result for graph '{line[1]}':")
            try:
                res = graphs[line[1]].kruskal()
                print(res)
            except GraphError as e:
                print(e)

    elif line[0] == 'negloop' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if not graphs[line[1]].isWeighted:
                print("Error: graph must be weighted!")
                continue
            print(f">>> Result for graph '{line[1]}':")
            try:
                res = graphs[line[1]].negloop()
                print(res)
            except GraphError as e:
                print(e)

    elif line[0] == 'kpaths' and len(line) == 5:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Result for graph '{line[1]}' and nodes '{line[2]}' and '{line[3]}':")
            ans = graphs[line[1]].kpaths(line[2], line[3], line[4])
            for length, path in ans:
                print(f'Path {"-".join(path)} of length {length}')


    elif line[0] == 'draw' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if len(graphs[line[1]].nodes) > 19:
                print("Error: graph with more than 19 nodes would be too cumbersome to understand")
                continue
            print(f">>> Drawn graph '{line[1]}':")
            try:
                res = graphs[line[1]].draw()
                for line in res:
                    for char in line:
                        print(char, end='')
                    print()
            except GraphError as e:
                print(e)

    elif line[0] == 'animate' and len(line) == 2:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if len(graphs[line[1]].nodes) > 19:
                print("Error: graph with more than 19 nodes would be too cumbersome to understand")
                continue
            print(f">>> Drawn graph '{line[1]}':")
            try:
                res = graphs[line[1]].draw(True, None)
                for frame in res:
                    for line in frame:
                        for char in line:
                            print(char, end='')
                        print()
                    time.sleep(1)
            except GraphError as e:
                print(e)

    elif line[0] == 'dfsanim' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            if len(graphs[line[1]].nodes) > 19:
                print("Error: graph with more than 19 nodes would be too cumbersome to understand")
                continue
            print(f">>> Drawn graph '{line[1]}':")
            try:
                res = graphs[line[1]].draw(True, line[2])
                for frame in res:
                    for line in frame:
                        for char in line:
                            print(char, end='')
                        print()
                    time.sleep(1)
            except GraphError as e:
                print(e)

    elif line[0] == 'dfs' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Nodes for graph '{line[1]}' by depth-first search, starting from node '{line[2]}':")
            try:
                res = graphs[line[1]].dfs(line[2])
                try:
                    res[-1]
                except KeyError:
                    for node, val in res.items():
                        print(node, val)
                else:
                    print("Not a tree")
            except Exception as e:
                print(e)

    elif line[0] == 'dfs1' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Nodes for graph '{line[1]}' by depth-first search, starting from node '{line[2]}':")
            try:
                res = graphs[line[1]].dfs1(line[2])
                for parent, node in res:
                    print(parent, node)
            except Exception as e:
                print(e)

    elif line[0] == 'bfs' and len(line) == 3:
        try:
            graphs[line[1]]
        except KeyError:
            print(f"Error: graph '{line[1]}' doesn't exist")
        else:
            print(f">>> Nodes for graph '{line[1]}' by breadth-first search, starting from node '{line[2]}':")
            try:
                res = graphs[line[1]].bfs(line[2])
                for node, val in res.items():
                    print(node, val)
            except Exception as e:
                print(e)

    elif line[0] == 'exit' and len(line) == 1:
        break

    else:
        print("Error: incorrect syntax. Type 'help' for help")
