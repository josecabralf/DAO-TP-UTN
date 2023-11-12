from boundaries.PantallaSecundaria import PantallaSecundaria
from tkinter import Frame, Label, Entry, Scrollbar
from tkinter import ttk
from tkinter import StringVar, PhotoImage
from tkinter import messagebox
from tkinter import LEFT, RIGHT, X, Y, BOTH, CENTER
from tkinter.ttk import Treeview
from config import png_search, png_refresh, png_extravios, png_found, png_create
from entities.fabricacionPura.Observer import IObserver

class PantallaExtravios(PantallaSecundaria, IObserver):
    def __init__(self, gestor, backToMain):
        super().__init__(gestor, backToMain)
        self.ventana.title("Libros Extraviados")
        self.librosExtraviados = []
        self.fila_seleccionada = None
        self.createWidgets()

    def actualizar(self, message): 
        self.refresh()
    
    def bloquear(self):
        for c in self.frameBotones.winfo_children(): c.config(state="disabled")
        for c in self.frameBtnVolver.winfo_children(): c.config(state="disabled")
        
    def desbloquear(self):
        for c in self.frameBotones.winfo_children(): c.config(state="normal")
        for c in self.frameBtnVolver.winfo_children(): c.config(state="normal")
    
    def showErrorMessage(self, message): messagebox.showerror(message=message)
    def showInfo(self, message): messagebox.showinfo(message=message)
    
    def createWidgets(self):
      super().createWidgets()
      self.widgets.append(self.createBarraBusqueda())
      self.widgets.append(self.createLblLibrosExtraviados())
      self.widgets.append(self.createGrillaLibros())
      self.widgets.append(self.createBotonesAccion())

    def validateInput(self, *args):
      entrada_actual = self.varBusqueda.get()
      if entrada_actual.isdigit(): return True
      self.varBusqueda.set(self.varBusqueda.get()[:-1])
      return False
      
    def search(self):
      id = self.varBusqueda.get() if self.varBusqueda.get() != "" else -1
      self.gestor.search(id)
            
    def refresh(self):
      self.varBusqueda.set("")
      self.gestor.search(-1)
    
    def setLibros(self, libros):
      self.librosExtraviados = libros
      self.loadTable()
      
    def loadTable(self):
        self.treeview.delete(*self.treeview.get_children())  # Limpiar la grilla
        for libro in self.librosExtraviados:
            self.treeview.insert("", "end", values=libro)

    def getRowValues(self, event):
        seleccion = self.treeview.selection()
        if seleccion: self.fila_seleccionada = self.treeview.item(seleccion[0], "values")

    def validarFilaSeleccionada(self):
        if self.fila_seleccionada == None:
            messagebox.showwarning("Advertencia", "Debe seleccionar un libro")
            return False
        return True
    
    def encontrar(self):
      if self.validarFilaSeleccionada(): self.gestor.openEncontrarWindow(self.fila_seleccionada)

    def buscarNuevosExtravios(self):
        self.gestor.buscarNuevosExtravios()
        
    def createBotonesAccion(self):
        self.frameBotones = Frame(self.ventana, bg="#4c061d")
        self.frameBotones.grid(row=4, column=0, pady=(0, 10))
        
        self.imgEncontrados = PhotoImage(file=png_found).subsample(15)
        self.imgExtravios = PhotoImage(file=png_extravios).subsample(15)
        self.imgNuevoExtravio = PhotoImage(file=png_create).subsample(15)
        
        btnEncontrado = ttk.Button(self.frameBotones, text="Encontrado", command=self.encontrar, 
                              style="Botones.TButton", image=self.imgEncontrados, compound="left")
        btnNuevoExtravio = ttk.Button(self.frameBotones, text="Nuevo Extravio", 
                                      command=self.gestor.openNuevoExtravioWindow,
                                      style="Botones.TButton", image=self.imgNuevoExtravio, compound="left")
        btnActualizar = ttk.Button(self.frameBotones, text="Actualizar", command=self.buscarNuevosExtravios, 
                                  style="Botones.TButton", image=self.imgExtravios, compound="left")
        
        btnActualizar.pack(side=LEFT, padx=5)
        btnEncontrado.pack(side=LEFT, padx=5)
        btnNuevoExtravio.pack(side=LEFT, padx=5)
        return self.frameBotones

    def createBarraBusqueda(self):
        self.frameBusqueda = Frame(self.ventana, bg="#4c061d")
        self.frameBusqueda.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        lblBuscar = Label(self.frameBusqueda, text="Buscar por ID:", font=("Helvetica", 12), bg="#4c061d", fg="white")
        lblBuscar.pack(side=LEFT, padx=5)
        
        frameBarraBoton = Frame(self.frameBusqueda, bg="#4c061d")
        frameBarraBoton.pack(side=LEFT, fill=X, expand=True)
        
        self.varBusqueda = StringVar()
        self.varBusqueda.trace_add("write", self.validateInput)
        entryBusqueda = Entry(frameBarraBoton, textvariable=self.varBusqueda, font=("Helvetica", 12))
        entryBusqueda.pack(side=LEFT, fill=X, expand=True)
        
        estilo_nuevo = ttk.Style()
        estilo_nuevo.configure("Busqueda.TButton", width=10)
        self.imgSearch = PhotoImage(file=png_search).subsample(30)
        btnBuscar = ttk.Button(frameBarraBoton, command=self.search, image=self.imgSearch, compound="left", style="Busqueda.TButton")
        btnBuscar.pack(side=LEFT, padx=5)
        self.imgRefresh = PhotoImage(file=png_refresh).subsample(120)
        btnBuscar = ttk.Button(frameBarraBoton, command=self.refresh, image=self.imgRefresh, compound="left", style="Busqueda.TButton")
        btnBuscar.pack(side=LEFT, padx=5)
        
        return self.frameBusqueda

    def createLblLibrosExtraviados(self):
        lblLibrosRegistrados = Label(self.ventana, text="Libros Extraviados", font=("Helvetica", 16, "bold"), bg="#4c061d", fg="white")
        lblLibrosRegistrados.grid(row=2, column=0, pady=10)
        return lblLibrosRegistrados

    def createGrillaLibros(self):
        self.frame_grilla = Frame(self.ventana, bg="#4c061d")
        self.frame_grilla.grid(row=3, column=0, padx=10, pady=(0, 10), sticky='nsew')
        columns = ("Codigo", "Titulo", "Precio", "Estado")
        self.treeview = Treeview(self.frame_grilla, columns=columns, show="headings", selectmode="browse")

        column_widths = {"Codigo": 50, "Titulo": 300, "Precio": 50, "Estado": 150}

        for col in columns:
            self.treeview.heading(col, text=col)
            width = column_widths.get(col, 100)
            self.treeview.column(col, width=width, anchor=CENTER)

        scrollbar = Scrollbar(self.frame_grilla, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.treeview.config(yscrollcommand=scrollbar.set)
        self.treeview.pack(fill=BOTH, expand=True)
        self.treeview.bind("<ButtonRelease-1>", self.getRowValues)
        return self.frame_grilla