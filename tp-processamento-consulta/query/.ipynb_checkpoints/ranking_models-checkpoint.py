from typing import List
from abc import abstractmethod
from typing import List, Set,Mapping
from index.structure import TermOccurrence
import math
from enum import Enum
from collections import Counter

class IndexPreComputedVals():
    def __init__(self,index):
        self.index = index
        self.precompute_vals()

    def precompute_vals(self):
        self.doc_count = self.index.document_count
        
        """
        Inicializa os atributos por meio do indice (idx):
            doc_count: o numero de documentos que o indice possui
            document_norm: A norma por documento (cada termo é presentado pelo seu peso (tfxidf))
        """
        '''No modelo vetorial temos que calcular a norma de cada documento 𝑑𝑗. Esse calculo não pode ser feito durante o preprocessamento da consulta. Assim, na classe IndexPreComputedVals possui o atributo document_norm que é um dicionário que mapeia cada documnto 𝑗 à sua norma. Esse calculo é feito apenas uma vez ao iniciar o programa.
Desta forma, você deverá terminar de implementar o método precompute_vals que percorre todo o índice e armazena a norma de cada documento.
        '''
        '''
            Norma é a raiz quadrada do somatório de todos tf*idfs de todos os documentos que contem determinado term_id
        '''
        # O que é necessário:
        # Número de documentos com o termo: <--> Length do dicionário de termos.
        # ID do Termo: <--> Get Term Id:
        # Frequência que o termo aparece: [TermFilePosition]
        
        keysList = [*self.index.dic_index.keys()]
 
        # Número de palavras no arquivo e quais são as palavras
        # 
        '''     
        lista = []
        for i,key in zip(range(self.doc_count),keysList):
            lista.append([])
            print(self.index.get_occurrence_list(key).doc_count_with_term)
            if self.index.get_occurrence_list(key) == i:
                lista[i].append(self.index.get_occurrence_list(key).term_id)
        
        print(lista)
        ''' 
        lista = []
        
        vectorRank = VectorRankingModel(self.index)
        
        for i in range(self.doc_count):
            lista.append({})
        
        print(lista)
        for key in keysList:
            print('Term id: ' + key)
            if self.index.document_count_with_term(key) > 1:
                for j in range(self.index.document_count_with_term(key)):
                    print('Inserir: ' + str(j))
                    lista[j][self.index.get_term_id(key)] = self.index.get_occurrence_list(key)[j].term_freq
            else:
                j = self.index.get_occurrence_list(key)[0].doc_id - 1
                lista[j][self.index.get_term_id(key)] = self.index.get_occurrence_list(key)[0].term_freq
       
        for i in range(lista):
            tf_idf = 0
            for key in keysList:
                
            
        print(lista)
        print(self.index.get_occurrence_list(key))
        
        print(self.index.dic_index)
        
        '''
                        for doc in range(1:self.doc_count):
                if self.index.get_occurence_list(key).doc_id == doc:
                    self.index.get_occurence_list
            for i in range (self.index.get_occurence_list(key).doc_id):
                term_freq = term_freq + self.index.get_occurrence_list(key).term_freq
            # Chama cálculo do TF * IDF

            '''
        '''
        for doc in range(self.doc_count):
            self.index
            raiz = math.sqrt(num)
        
        key = 0
        for doc in range(self.doc_count):
            key = key + 1
            self.document_norm[key] =  
        '''
        self.document_norm = {}
        
class RankingModel():
    @abstractmethod
    def get_ordered_docs(self,query:Mapping[str,TermOccurrence],
                              docs_occur_per_term:Mapping[str,List[TermOccurrence]]) -> (List[int], Mapping[int,float]):
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")

    def rank_document_ids(self,documents_weight):
        doc_ids = list(documents_weight.keys())
        doc_ids.sort(key= lambda x:-documents_weight[x])
        return doc_ids

class OPERATOR(Enum):
  AND = 1
  OR = 2
    
#Atividade 1
class BooleanRankingModel(RankingModel):
    def __init__(self,operator:OPERATOR):
        self.operator = operator

    def intersection_all(self,map_lst_occurrences:Mapping[str,List[TermOccurrence]]) -> List[int]:
        print(map_lst_occurrences)
        set_ids = set()
        lista = []
        for key,value in map_lst_occurrences.items():
            for item in value:
                lista.append(item.doc_id)
        
        comum = [key for key, count in Counter(lista).items() if count >= len(map_lst_occurrences)]
        for i in comum:
            set_ids.add(i)
        return set_ids


    def union_all(self,map_lst_occurrences:Mapping[str,List[TermOccurrence]]) -> List[int]:
        set_ids = set()
        lista = []
        print(map_lst_occurrences)
        for key,value in map_lst_occurrences.items():
            for item in value:
                lista.append(item.doc_id)
        todos = list(dict.fromkeys(lista))
        for i in todos:
            set_ids.add(i)
        return set_ids

    def get_ordered_docs(self,query:Mapping[str,TermOccurrence],
                              map_lst_occurrences:Mapping[str,List[TermOccurrence]]) -> (List[int], Mapping[int,float]):
        """Considere que map_lst_occurrences possui as ocorrencias apenas dos termos que existem na consulta"""
        if self.operator == OPERATOR.AND:
            return self.intersection_all(map_lst_occurrences),None
        else:
            return self.union_all(map_lst_occurrences),None

#Atividade 2
class VectorRankingModel(RankingModel):

    def __init__(self,idx_pre_comp_vals:IndexPreComputedVals):
        self.idx_pre_comp_vals = idx_pre_comp_vals

    @staticmethod
    def tf(freq_term:int) -> float:
        #𝑇𝐹=1+𝑙𝑜𝑔2(𝑓𝑖𝑗)
        TF = 1 + math.log(freq_term,2)
        return TF

    @staticmethod
    def idf(doc_count:int, num_docs_with_term:int )->float:
        #𝐼𝐷𝐹𝑖=𝑙𝑜𝑔2(𝑁/𝑛𝑖)
        IDF = math.log((doc_count/num_docs_with_term),2)
        return round(IDF,3)

    @staticmethod
    def tf_idf(doc_count:int, freq_term:int, num_docs_with_term) -> float:
        tf = VectorRankingModel.tf(freq_term)
        idf = VectorRankingModel.idf(doc_count,num_docs_with_term)
        #print(f"TF:{tf} IDF:{idf} n_i: {num_docs_with_term} N: {doc_count}")
        return tf*idf

    def get_ordered_docs(self,query:Mapping[str,TermOccurrence],
                              docs_occur_per_term:Mapping[str,List[TermOccurrence]]) -> (List[int], Mapping[int,float]):
            documents_weight = {}





            #retona a lista de doc ids ordenados de acordo com o TF IDF
            return self.rank_document_ids(documents_weight),documents_weight

