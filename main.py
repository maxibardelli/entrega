from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re
#############################################################################
def crear_base():
    my_base= sqlite3.connect('my_base.sqlite3')
    return my_base
def crear_tabla():
    my_base=crear_base()
    cursor = my_base.cursor()
    sql = "CREATE TABLE producto(id integer PRIMARY KEY autoincrement, producto text, precio integer, stock integer)"
    cursor.execute(sql)
    my_base.commit()
try:
    crear_base()
    crear_tabla()
    showinfo(title="BASE DE DATO", message="Crear Base de Datos")
except:
    showinfo(title="BASE DE DATO", message="Conectar a my_base.sqlite3")
###############################################################################################
def vaciar():
    vaciar=("")
    producto.set(vaciar)
    precio.set(vaciar)
    stock.set(vaciar)
def alta(producto,precio,tree,stock):
    cadena_producto = producto
    patron_producto="^[A-Za-záéíóú1-9ñÑ0.,\s\*]*$" #USAR LA "x" COMO SIMBOLO DE MULTIPICAR
    vacio=("")
    if producto!=vacio:    
        if(re.match(patron_producto, cadena_producto)):
            if askyesno( "ALTA",f"decea dar de alta: {producto} ${precio}"):
                my_base=crear_base()
                cursor=my_base.cursor()
                data=(producto,precio,stock)
                sql="INSERT INTO producto(producto, precio, stock) VALUES(?,?,?)"
                cursor.execute(sql,data)
                my_base.commit()
                actualizar_treeview(tree)
                showinfo(title="ALTA",message="Alta Exitosa")
            else:
                showinfo(title="ALTA",message="Alta Cancelada")    
            vaciar()
        else:
            showerror(title="ERROR AL VALIDAR", message="ERROR EN EL CAMPO DESCIPCION")
    else:
        showerror(title="ERROR", message="NO SE PUEDEN DAR DE ALTA CAMPOS VACIOS")
def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    sql = "SELECT * FROM producto ORDER BY id ASC"
    my_base=crear_base()
    cursor=my_base.cursor()
    datos=cursor.execute(sql)
    resultado = datos.fetchall()
    for fila in resultado:
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2],fila[3]))
def baja(tree):    
    if askyesno("BAJA",f"decea dar de baja: {producto.get()} $ {precio.get()}"):
        select=tree.selection()
        select_item=tree.item(select)
        id=select_item['text']
        my_base=crear_base()
        cursor=my_base.cursor()
        data=(id,)
        sql= "DELETE FROM producto WHERE id = ?;"
        cursor.execute(sql,data)
        my_base.commit()
        tree.delete(select)
        showinfo(title="BAJA",message="Baja Exitosa")
    else:
        showinfo(title="BAJA",message="Baja Cancelada")
    boton_borrar.configure(state=DISABLED)
    boton_alta.configure(state=NORMAL)
    boton_modificar.configure(state=DISABLED)
    vaciar()
def modificar(tree,producto,precio,stock):
    cadena = producto
    patron="^[A-Za-záéíóú1-9ñÑ0.,\s\*]*$"     #USAR LA "x" COMO SIMBOLO DE MULTIPICAR    
    if(re.match(patron,cadena)):
        if askyesno("MODIFICAR",f"decea modificar: {producto} ${precio} {stock}"):
            select=tree.selection()
            select_item=tree.item(select)
            id_item=select_item["text"]
            id_item=str(id_item)
            my_base=crear_base()
            cursor=my_base.cursor()
            sql="UPDATE producto SET (producto,precio,stock)=(?,?,?) WHERE id=?;"
            data=(producto,precio,stock,id_item)
            cursor.execute(sql,data)
            my_base.commit()
            actualizar_treeview(tree)
            showinfo(title="MODIFICAR",message="Modificacion Exitosa")
        else:
            showinfo(title="MODIFICAR",message="Modificacion Cancelada")
    else:
        showerror(title="ERROR AL VALIDAR", message="ERROR EN EL CAMPO DESCIPCION")
    boton_modificar.configure(state=DISABLED)
    boton_alta.configure(state=NORMAL)
    boton_borrar.configure(state=DISABLED)
    vaciar()
def muestra(tree):
    select=tree.selection()
    select_item=tree.item(select)
    i=select_item["values"]
    producto.set(i[0])
    precio.set(i[1])
    stock.set(i[2])
    boton_modificar.configure(state=NORMAL)
    boton_alta.configure(state=DISABLED)
    boton_borrar.configure(state=NORMAL)
##########################################################################################
master=Tk()
master.geometry("500x400")
master.title("programa de alta y venta")
producto,stock,precio=StringVar(),DoubleVar(),DoubleVar()
label_descripcion=Label(master,text="descripcion")
label_descripcion.place(x=125)
label_precio=Label(master,text="precio")
label_precio.place(x=300)
label_sotck=Label(master,text="stok")
label_sotck.place(x=350)
entry_descripcion=Entry(master, textvariable=producto)
entry_descripcion.place(x=0,width=300,y=25)
entry_precio=Entry(master,textvariable=precio)
entry_precio.place(x=300,width=100,y=25)
entry_stock=Entry(master,textvariable=stock)
entry_stock.place(x=350,width=100,y=25)
###########################################################################################
tree=ttk.Treeview(master)
tree["column"]=("col1","col2","col3")
tree.column("#0",width=15)
tree.column("col1", width=50)
tree.column("col2", width=15)
tree.column("col3", width=15)
tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="precio")
tree.heading("col3", text="stock")
tree.place(x=0,width=450,y=95) 
###########################################################################################
boton_alta=Button(master, text="alta", command=lambda:alta(producto.get(),precio.get(),tree,stock.get()))
boton_alta.place(x=0,width=100,y=55)
boton_borrar=Button(master, text="borrar",command=lambda:baja(tree),state=DISABLED)
boton_borrar.place(x=101,width=100,y=55)
boton_modificar=Button(master, text="modificar", command=lambda:modificar(tree,producto.get(),precio.get(),stock.get()),state=DISABLED)
boton_modificar.place(x=201,width=100,y=55)
boton_consulta=Button(master, text="cargar DB", command=lambda:actualizar_treeview(tree))
boton_consulta.place(x=301,width=100,y=55)
boton_select=Button(master, text="seleccionar", command=lambda:muestra(tree))
boton_select.place(x=401,width=100,y=55)
##########################################################################################
menubar=Menu(master,tearoff=0)
menubar.add_command(label="salir",command=master.quit)
master.config(menu=menubar)
##########################################################################################
master.mainloop()
