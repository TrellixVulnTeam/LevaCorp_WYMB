#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import os.path
import pprint
import rdflib
from rdflib import *
from rdflib import Literal
from rdflib.namespace import RDF
import shutil
import sys
import time
from rdflib import URIRef
sys.path.append('./AuxiliaresPck')
import AuxiliaresPck.AppUtil
import logging

## En esta clase se procesan las consultas a la ontologia y se insertan los datos
class Ontologia:
#    def __init__(self, mac, idUsuario):
#        logging.basicConfig()
#        try:           
#            os.stat(AppUtil.pathOWL)
#        except:
#            os.mkdir(AppUtil.pathOWL, 0777)
#        self.path = AppUtil.pathOWL+mac + "&" + idUsuario + ".owl"
#        
#        self.g = rdflib.Graph()
#        if os.path.exists(self.path):
#            self.g.parse(self.path)
#        else:
#            self.g.parse(AppUtil.ontologiaPU)
#            self.g.serialize(destination = self.path, format='xml')
        
    def __init__(self,path):
        logging.basicConfig()
        try:           
            os.stat(AuxiliaresPck.AppUtil.pathOWL)
            self.path = path
            self.g = rdflib.Graph()
            if os.path.exists(path):
                self.g.parse(path)
        except:
            print("Errrroooooooooooooooooooor en init de ontologia")
            print("Desde Ontologia. El path es incorrecto")
            pass
        
###################### Grafo #####################################################   

    def crearNuevaOntologia(self, path):
        try:           
            os.stat(AuxiliaresPck.AppUtil.pathOWL)
        except:
            os.mkdir(AuxiliaresPck.AppUtil.pathOWL, 0x0777)
        self.path = path
        if not os.path.exists(path):
            self.g.parse(AuxiliaresPck.AppUtil.ontologiaPU)
            self.g.serialize(destination = path, format='xml')
        
        
    def cargarOntologia(self, dirOntologia):
        self.g = rdflib.Graph()
        self.g.parse(dirOntologia)
         
    def guardarGrafoOntologia(self ):
        self.g.serialize(destination = self.path, format='xml')
    
    def guardarGrafoOntologiaPath(self, path ):
        self.g.serialize(destination = path, format='xml')
        
        
###################### Consultas #####################################################
    def consultaInstancias(self, query):
##        self.cargarGrafoNuevo()
        resultado = []
        qrest = self.g.query(query)
        for row in qrest:
                resultado.append(row[0].split("#")[1].replace("()",("")))
        return resultado
    
    ##retorna una lista con los resultados [[],[]]
    def consultaDataProperty(self, query):
        ##self.cargarGrafoNuevo()
        resultado = []
        qrest = self.g.query(query) 
        for row in qrest:
            aux = []
            for subrow in row:
                if not subrow == None:
                    aux.append(subrow.encode('utf-8'))
                else:
                    aux.append("")
            resultado.append(aux)
        return resultado
    
    ##retorna un boolean yes/no Questions
    def consultasASK(self, query):
##        self.cargarGrafoNuevo()
        qrest = self.g.query(query)         
        return qrest
    
###################### Insertar #####################################################
    def insertarIndividuo(self, uriNuevo, uriClase):
        
        nodoNuevo = URIRef(uriNuevo)
        clase = URIRef(uriClase)
        self.g.add((nodoNuevo,RDF.type, clase))
        self.guardarGrafoOntologia()

    def insertarListaIndividuos(self,lista):
        for i in lista:
            nodoNuevo = URIRef(i[0])
            clase = URIRef(i[1])
            self.g.add((nodoNuevo,RDF.type, clase))
        self.guardarGrafoOntologia()

    def insertarDataProperty(self, uriIndividuo, uriData, valor):
        individuo = URIRef(uriIndividuo)
        dataProperty = URIRef(uriData)
        self.g.add ((individuo, dataProperty, valor))
        self.guardarGrafoOntologia()
        
    def insertarListaDataProperty(self,lista):
        for i in lista:
            individuo=URIRef(i[0])
            dataProperty = URIRef(i[1])
            self.g.add ((individuo, dataProperty, i[2]))
        self.guardarGrafoOntologia()
       
    def insertarObjectProperty(self, uriIndividuo, uriObjectProperty, uriIndividuo2):
        #print "Desde ontologia"
        #print "   ind 1 " + uriIndividuo
        #print "   ind 2 " + uriIndividuo2
        individuo1 = URIRef(uriIndividuo)
        individuo2 = URIRef(uriIndividuo2)
        objectProperty = URIRef(uriObjectProperty)
        self.g.add ((individuo1, objectProperty, individuo2))
        self.guardarGrafoOntologia()

    def insertarListaObjectProperty(self,lista):
        for i in lista:
            individuo1 = URIRef(i[0])
            objectProperty = URIRef(i[1])
            individuo2= URIRef(i[2])
            self.g.add ((individuo1, objectProperty, individuo2))
        self.guardarGrafoOntologia()

###################### Modificar #####################################################
    ##Este metodo modifica un valor en la ontologia
    ##Tiene el inconveniente que agrega muchas más líneas a la ontología
    ##por eso se creo el metodo ActualizarDataProperty
#    def setDataProperty(self, uriIndividuo, uriDataProperty, valorNuevo):
#        individuo = URIRef(uriIndividuo)
#        valor = valorNuevo
#        dataProperty = URIRef(uriDataProperty)
#        self.g.set ((individuo, dataProperty, Literal(valor)))         
#        self.guardarGrafoOntologia()
        
    def actualizarDataProperty(self,uriIndividuo,uriDataProperty, valorNuevo):
        ##Primero se elimina de la ontologia y luego se inserta
       # print "Inicia a actualizar dataproperty " + time.ctime()
        individuo = URIRef(uriIndividuo)
        dataProperty = URIRef(uriDataProperty)
        self.g.remove ((individuo, dataProperty, None))
        self.g.add((individuo, dataProperty, Literal(valorNuevo)))
        self.g.serialize(destination = self.path, format='xml')
        self.guardarGrafoOntologia()
        #print "Fin actualizar dataproperty " + time.ctime()

    def actualizarListaDataProperty(self,listaIndividuos): ##[[uriind, uridata,valornuevo]]
        ##Primero se elimina de la ontologia y luego se inserta
        for item in listaIndividuos:
            individuo = URIRef(item[0])
            dataProperty = URIRef(item[1])
            valorNuevo = item[2]
            self.g.remove ((individuo, dataProperty, None))
            self.g.add((individuo, dataProperty, Literal(valorNuevo)))
        self.g.serialize(destination = self.path, format='xml')
        self.guardarGrafoOntologia()
        
###################### Eliminar #####################################################
    def eliminarTodoIndividuo(self, uriIndividuo):
        ontologiaInst =self.path
        g = rdflib.Graph()
        g.parse(ontologiaInst)
        individuo = URIRef(uriIndividuo)
        g.remove ((individuo, None, None))
        g.serialize(destination = ontologiaInst, format='xml')
        self.guardarGrafoOntologia()

    def eliminarListaTodoIndividuo(self, ListauriIndividuo):
        ontologiaInst =self.path
        g = rdflib.Graph()
        g.parse(ontologiaInst)
        for uriIndividuo in ListauriIndividuo:
            individuo = URIRef(uriIndividuo)
            g.remove ((individuo, None, None))
        g.serialize(destination = ontologiaInst, format='xml')
        self.guardarGrafoOntologia()

    def eliminarDataProperty(self, uriIndividuo,uriDatapropertyP):
        ontologiaInst =self.path
        g = rdflib.Graph()
        g.parse(ontologiaInst)
        individuo = URIRef(uriIndividuo)
        dataProperty = URIRef(uriDatapropertyP)
        g.remove ((individuo, dataProperty, None))
        g.serialize(destination = ontologiaInst, format='xml')
        self.guardarGrafoOntologia()
   
##    def eliminarObjectProperty(self, uriIndividuo):
###################### Operaciones entre ontologias #####################################################
    def restarOntologias(self, pathOntologiaMinuendo, pathOntologiaSustraendo, pathOntologiaResultado):
        minuendo = rdflib.Graph()
        sustraendo = rdflib.Graph()
        r = rdflib.Graph()
        sustraendo.parse(pathOntologiaSustraendo)
        minuendo.parse(pathOntologiaMinuendo)
        r = minuendo-sustraendo
        r.serialize(destination = pathOntologiaResultado,format='xml')
        return pathOntologiaResultado
