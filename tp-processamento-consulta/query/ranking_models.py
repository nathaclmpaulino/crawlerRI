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
        """
        Inicializa os atributos por meio do indice (idx):
            doc_count: o numero de documentos que o indice possui
            document_norm: A norma por documento (cada termo é presentado pelo seu peso (tfxidf))
        """
        '''
            Norma é a raiz quadrada do somatório de todos tf*idfs de todos os documentos que contem determinado term_id
        '''
        '''
        self.document_norm = {}
        self.doc_count = self.index.document_count
        sum_doc  = dict() 
        term_idf = dict()
        for term in list(self.index.dic_index.keys()):
            occurrence_list = self.index.get_occurrence_list(term)
            for item in occurrence_list:
                tf_idf = VectorRankingModel.tf_idf(self.doc_count,item.term_freq,len(occurrence_list))
                if term not in term_idf.keys():
                    term_idf[term] = list()
                    term_idf[term].append((item.doc_id,tf_idf))
                else:
                    term_idf[term].append((item.doc_id,tf_idf))
        for term in term_idf.keys():
            for occurrence in term_idf[term]:
                if occurrence[0] in sum_doc:
                    sum_doc[occurrence[0]] =  sum_doc[occurrence[0]] + math.pow(occurrence[1],2)
                else: 
                    sum_doc[occurrence[0]] = math.pow(occurrence[1],2)
        for x in self.index.set_documents:
            self.document_norm[x] = round(math.sqrt(sum_doc[x]),2) 
        '''

        vectorRank = VectorRankingModel(self.index)
        # Obtem o total de documentos
        self.doc_count = self.index.document_count
        
        tf_idf_list = {}
        
        documents_id = set()
        '''
          documents_id = self.index.dic_index.keys()#range(1, self.doc_count+1)
        print(documents_id)
                for term in list(self.index.dic_index.keys()):
            occurrence_list = self.index.get_occurrence_list(term)
            for item in occurrence_list:
        '''
        for term in self.index.dic_index.keys():
            occurrence_list = self.index.get_occurrence_list(term)
            for item in occurrence_list:
                documents_id.add(item.doc_id)
    
        # Instanciando um dicionário dentro do dicinário para montar a tabela de tf_idf
        for doc in documents_id:
            tf_idf_list[doc] = {}
        
        # Iterando sobre os termos existêntes
        for term in self.index.dic_index:
            # ni = doc count with term
            ni = self.index.document_count_with_term(term)
            idf = vectorRank.idf(self.doc_count, ni)
            
            #Lista de documentos que ainda não foram lidos por alguma ocorrência
            documents_unread = list(documents_id)
            
            # Iterando sobre as ocorrências de um termo
            for ocurrence in self.index.get_occurrence_list(term):
                #if ocurrence.doc_id in documents_unread: #acrescentei
                documents_unread.remove(ocurrence.doc_id)
                # cria matriz de tf_idf com doc na coluna e o tf_idf de cada termo daquele doc na linha
                tf_idf_list[ocurrence.doc_id][term] = vectorRank.tf_times_idf(vectorRank.tf(ocurrence.term_freq), idf)
            
            # Iterando sobre os documentos que não possuem ocurrence para este termo
            for doc_id in documents_unread:
                tf_idf_list[doc_id][term] = vectorRank.tf_times_idf(vectorRank.tf(0), idf)
        
        # Iterando sobre a tabela de tf_idf para aplicar fórmula de norma
        self.document_norm = {}
        for doc_id in tf_idf_list:
            norma = 0
            for tf_idf in tf_idf_list[doc_id]:
                norma += tf_idf_list[doc_id][tf_idf] ** 2
            # preenche o dic com a key doc_id e value norma    
            self.document_norm[doc_id] = round(math.sqrt(norma), 2) 
                                               
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
        set_ids = []
        lista = []

        for key,value in map_lst_occurrences.items():
            for item in value:
                lista.append(item.doc_id)
        todos = list(dict.fromkeys(lista))
        for i in todos:
            set_ids.append(i)
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
        # 𝑇𝐹=1+𝑙𝑜𝑔2(𝑓𝑖𝑗)
        TF = 0
        if(freq_term != 0):
            TF = 1 + math.log(freq_term,2)
        return TF

    @staticmethod
    def idf(doc_count:int, num_docs_with_term:int )->float:
        # 𝐼𝐷𝐹𝑖=𝑙𝑜𝑔2(𝑁/𝑛𝑖)
        IDF = math.log((doc_count/num_docs_with_term),2)
        return IDF
    
    @staticmethod
    def tf_times_idf(tf:float, idf:float) -> float:
        return tf*idf
    
    @staticmethod
    def tf_idf(doc_count:int, freq_term:int, num_docs_with_term) -> float:
        tf = VectorRankingModel.tf(freq_term)
        idf = VectorRankingModel.idf(doc_count,num_docs_with_term)
        return VectorRankingModel.tf_times_idf(tf, idf)

    def get_ordered_docs(self,query:Mapping[str,TermOccurrence],
                              docs_occur_per_term:Mapping[str,List[TermOccurrence]]) -> (List[int], Mapping[int,float]):
            
            documents_weight = {}
            documents_id = []
            doc_count = self.idx_pre_comp_vals.doc_count
            
            tf_idf_list = {}
            tf_idf_document_list = {}
            
            
            for item in docs_occur_per_term:
                for occurrence in docs_occur_per_term[item]:
                    documents_id.append(occurrence.doc_id)
                        
            # Instanciando um dicionário dentro do dicinário para montar a tabela de tf_idf
            for doc in documents_id:
                tf_idf_document_list[doc] = {}
            
            for term in query:
                documents_unread = list(documents_id)
                
                try:
                    tf_idf = VectorRankingModel.tf_idf(doc_count, query[term].term_freq, len(docs_occur_per_term[term]))
                    tf_idf_list[term] = tf_idf

                    for ocurrence in docs_occur_per_term[term]:
                        documents_unread.remove(ocurrence.doc_id)
                        tf_idf = VectorRankingModel.tf_idf(doc_count, ocurrence.term_freq, len(docs_occur_per_term[term]))
                        tf_idf_document_list[ocurrence.doc_id][term] = tf_idf
                except:
                    tf_idf_list[term] = 0
                    
                # Iterando sobre os documentos que não possuem ocurrence para este termo
                for doc_id in documents_unread:
                    tf_idf_document_list[doc_id][term] = 0
            # peso por doc_id
            for doc_id in tf_idf_document_list: 
                weight = 0
                for term in tf_idf_document_list[doc_id]:
                    wij = tf_idf_document_list[doc_id][term];
                    wiq = tf_idf_list[term]
                    weight += wij * wiq
                if(weight > 0):
                    documents_weight[doc_id] = weight / self.idx_pre_comp_vals.document_norm[doc_id]
            
            #print(self.rank_document_ids(documents_weight))
            #print(documents_weight)
            
            #retona a lista de doc ids ordenados de acordo com o TF IDF
            return self.rank_document_ids(documents_weight),documents_weight
