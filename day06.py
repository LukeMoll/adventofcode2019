import aoc
from typing import List, Dict, Tuple, FrozenSet
from collections import namedtuple
from operator import itemgetter

def main():
    aoc.header("Universal Orbit Map")
    aoc.run_tests()

    orbits = aoc.get_input().readlines()
    output = aoc.output(1, part1, args=[orbits], post=itemgetter(0))
    aoc.output(2, part2_graph, args=[orbits, *output[1:]], comment="Dijstra's algorithm")
    aoc.output(2, part2_ancestor, args=[orbits, *output[1:]], comment="Common ancestor")

def test():
    # part 1
    p1_input = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L"
    ]
    (children, parents) = connect_nodes(p1_input)
    for child in children.keys():
        if child != "COM":
            assert ischildof(child, "COM", children, parents), f"{child} not connected to COM!"

    values = annotate_nodes_depth(children)
    assert values["COM"] == 0
    assert values["D"]   == 3
    assert values["L"]   == 7

    assert sum(values.values()) == 42

    # part 2 (graph)
    p1_input.extend(["K)YOU","I)SAN"])
    (children,parents) = connect_nodes(p1_input)
    graph = tree_to_graph(children, parents)
    start = parents["YOU"]
    end = next(filter(lambda t: "SAN" in t[1],children.items()))[0]
    transfers = dijkstra(graph, start=start, end=end)
    assert transfers == 4

    assert part2_ancestor(p1_input, children, parents, annotate_nodes_depth(children)) == 4

def part1(orbits : List[str]):
    children, parents = connect_nodes(orbits)
    values = annotate_nodes_depth(children)
    return (sum(values.values()), children, parents, values)

def part2_graph(orbits : List[str], children, parents, values):
    # children, parents = connect_nodes(orbits) # Could reuse this from p1, would save at most 1% time
    graph = tree_to_graph(children, parents)
    start = parents["YOU"]
    end = next(filter(lambda t: "SAN" in t[1],children.items()))[0]
    transfers = dijkstra(graph, start=start, end=end)
    return transfers

def part2_ancestor(orbits : List[str], children, parents, values):
    # children, parents = connect_nodes(orbits)
    # values = annotate_nodes_depth(children)

    start = parents["YOU"]
    end = next(filter(lambda t: "SAN" in t[1],children.items()))[0]

    common_ancestors = set(ancestors(start, parents)).intersection(ancestors(end, parents))
    closest_common = max(
        map(
            lambda n:(n, values[n]),
            common_ancestors
        ), 
        key=itemgetter(1)
    )
    return values[start] - closest_common[1] + values[end] - closest_common[1]

def connect_nodes(orbits : List[str]) -> Tuple[Dict[str,List[str]], Dict[str,str]]:
    children = {}
    parents = {}

    for orbit in orbits:
        (parent, child) = orbit.strip().split(")")
        parents[child] = parent
        if parent in children:
            children[parent].append(child)
        else:
            children[parent] = [child]

    return (children, parents)

def ischildof(child : str, parent : str, children : Dict[str,List[str]], parents : Dict[str,str]):
    if child in parents:
        if parents[child] == parent: return True         # Immediate child
        else: return ischildof(parents[child], parent, children, parents)   # Might be a grandchild
    else:
        # orphan - either not connected or COM
        return False

def annotate_nodes_depth(children : Dict[str,List[str]], start_node="COM", values=None) -> Dict[str,int]:
    if values == None:
        values = {start_node: 0}
    for child in children.get(start_node, []):
        values[child] = values[start_node] + 1
        values = annotate_nodes_depth(children, start_node=child, values=values)
    return values

def tree_to_graph(children : Dict[str,List[str]], parents : Dict[str,str]) -> Dict[str,FrozenSet[str]]:
    graph = {}
    for node, parent in parents.items():
        if node in children.keys():
            graph[node] = frozenset([parent, *children[node]])
        else:
            graph[node] = frozenset([parent])

    return graph

def dijkstra(graph : Dict[str,FrozenSet[str]], start : str, end : str):
   # basically a translation of https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
   # 1.
    unvisited = set(graph.keys())
   # 2.
    distances = dict((n, len(graph)**10) if n != start else (start, 0) for n in graph.keys())
    # A distance is tentative if the node is unvisited
    current = start

    while True:
   # 3.
        for neighbour in graph[current].intersection(unvisited):
            tentative = distances[current] + 1
            if distances[neighbour] > tentative:
                distances[neighbour] = tentative
   # 4.
        unvisited.remove(current)
   # 5.
        if end not in unvisited:
            return distances[end]
   # 6.
        current = min(map(lambda n:(n,distances[n]), unvisited), key=itemgetter(1))[0]

def ancestors(node : str, parents : Dict[str,str]):
    while node in parents.keys():
        node = parents[node]
        yield node

if __name__ == "__main__":
    main()
