from tkinter import *
from numpy import array as ar

root =Tk()

canvas = Canvas(root,width=600,height = 600,bg="black")

list_nodes =[]
temp_edge=["a","b"]
first_click = False
graph_dict = dict()
graph = []


def front_end():

    def export(event):
        global main_return
        graph_matrix = [[0 for x in range(len(list_nodes))]for x in range(len(list_nodes))]
        for pair in graph:
            x = pair[0]-1
            y = pair[1]-1
            graph_matrix[x][y]=graph_matrix[y][x]=1
        root.destroy()
        main_return = graph_matrix

    def motion(event):
        global first_click,temp_edge
        if first_click:
            global parent_point,canvas,temp
            x,y = event.x,event.y
            temp = canvas.create_line(parent_point[0],parent_point[1],x,y,fill="white",width=2)
            temp_edge.append(temp)
            canvas.delete(temp_edge[-2])
            temp_edge.remove(temp_edge[-2])

    def draw_node(canvas,x,y):
        global first_click
        global list_nodes,graph_dict
        list_nodes.append((x,y))
        canvas.create_oval(x-10,y-10,x+10,y+10,fill="white")
        canvas.create_text(x,y,text= str(len(list_nodes)))
        graph_dict[(x,y)]=len(list_nodes)


    canvas.grid()

    def leftClick(event):
        global list_nodes,first_click,child_point,parent_point,temp_edge,graph_dict,graph
        child_point = None
        if not first_click:
            flag =True
            x,y = event.x,event.y
            for tup in list_nodes:
                if tup[0]-15<x<tup[0]+30 and tup[1]-15<y<tup[1]+30:
                    first_click = True
                    parent_point = tup
                    flag = False
                    break
            if flag:
                draw_node(canvas,x,y)
        else:
            first_click = False
            x,y = event.x,event.y
            for tup in list_nodes:
                if tup[0]-15<x<tup[0]+15 and tup[1]-15<y<tup[1]+15:
                    child_point = tup
                    if child_point!=parent_point:
                        canvas.delete(temp_edge[-1])
                        temp_edge=["a","b"]
                        temp = canvas.create_line(parent_point[0],parent_point[1],child_point[0],child_point[1],fill="white",width=2)
                        canvas.lower(temp)
                        graph.append((graph_dict[child_point],graph_dict[parent_point]))
                        break
            else:
                canvas.delete(temp_edge[-1])
                temp_edge=["a","b"]
                

    canvas.bind("<Button-1>", leftClick)
    canvas.bind("<Button-3>", export)
    canvas.bind("<Motion>",motion)

    root.mainloop()

    return main_return

if __name__ == "__main__":
    print(ar(front_end()))