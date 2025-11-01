from treelib import Node, Tree
class DatosNodo(object): 
        def __init__(self, simbolo, lexema): 
            self.simbologramatical = simbolo
            self.lexema = lexema

def exportar_arbol(arbol):
    with open("arbol.txt", "w") as f:
        for node in arbol.all_nodes_itr():
            f.write(f"ID: {node.identifier}, TAG: {node.tag}, PID: {node.predecessor(arbol.identifier)}, SIMB: {node.data.simbologramatical}, LEX: {node.data.lexema}\n")
# print(hojas)
# def exportar_arbol(arbol):
#     with open("arbol.txt", "w") as f:
#         for node in arbol.all_nodes_():
#             pid = arbol.predecessor(node.identifier)
#             simb = getattr(node.data, "simbologramatical", None)
#             lex = getattr(node.data, "lexema", None)
#             f.write(f"ID: {node.identifier}, TAG: {node.tag}, PID: {pid}, SIMB: {simb}, LEX: {lex}\n")
