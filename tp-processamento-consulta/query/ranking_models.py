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
        '''
            Norma é a raiz quadrada do somatório de todos tf*idfs de todos os documentos que contem determinado term_id
        '''
        # O que é necessário:
        # Número de documentos com o termo: <--> Length do dicionário de termos.
        # ID do Termo: <--> Get Term Id:
        # Frequência que o termo aparece: [TermFilePosition]
        
        keysList = [*self.index.dic_index.keys()]
 
        # Número de palavras no arquivo e quais são as palavras

        lista = []
        tf_idf_list = []
        tf_idf_doc = []
        D = {}
        # doc_id como key e norma como value
        self.document_norm = {}
        vectorRank = VectorRankingModel(self.index)
        # cria lista vazia de dcicionarios com os documentos.
        # cada dicionario representa um documento
        for i in range(self.doc_count): 
            lista.append({})
            #tf_idf_list.append()
        

        for key in keysList:
            if self.index.document_count_with_term(key) > 1:
                for doc_num in range(self.index.document_count_with_term(key)): # itera sobre a quantidade de documentos com o termo
                    doc_id_list = self.index.get_occurrence_list(key)
                    doc_pos = (doc_id_list[doc_num].doc_id) - 1
                    # armazena o term_freq na lista de freq de cada termo em um doc
                    lista[doc_pos][self.index.get_term_id(key)] = doc_id_list[doc_num].term_freq
            else:
                # o term_id é a chave de cada dicionario dentro de um documento
                # os valores são o term_freq
                doc_num = self.index.get_occurrence_list(key)[0].doc_id - 1
                # acessa posicão do doc na lista e insere os term freq
                lista[doc_num][self.index.get_term_id(key)] = self.index.get_occurrence_list(key)[0].term_freq
       
        # calcular todos os tf_idf de cada palavra em um doc
        for key in list(self.index.dic_index.keys()):
            lista_ocorrencias = self.index.get_occurrence_list(key)
            num_docs_with_term = len(lista_ocorrencias)
            # acessa a lista de ocorrencias de um termo pra pegar os documentos relacionados
            for term_occur in lista_ocorrencias:
                freq_term = term_occur.term_freq
                doc_count = len(lista) # total de docs
                term_occur.term_freq
                print(term_occur)
                if freq_term != 0 and num_docs_with_term != 0: 
                    tf_idf_term = vectorRank.tf_idf(doc_count, freq_term, num_docs_with_term)
                    print(tf_idf_term)
                    D[key]= tf_idf_term
            tf_idf_list.append(D)
            print('outro')
            '''
            for key,value in lista[doc].items(): # para cada chave term_id no doc, acessar os trens
                # key é o term_id
                print(key)
                num_docs_with_term = len(self.index.get_occurrence_list(key))
                freq_term = lista[doc][key] # os values são a frequencia de cada termo naquele doc
                print(f'freq: {freq_term}')
                print(f'num_docs_with_term: {num_docs_with_term}')
                doc_count = len(lista) # total de docs
                # realiza calculo
                print('calculo')
                if freq_term != 0 and num_docs_with_term != 0: 
                    tf_idf_term = vectorRank.tf_idf(doc_count, freq_term, num_docs_with_term)
                    print(tf_idf_term)
                    D[key]= tf_idf_term
            tf_idf_list.append(D)
        '''
        # cada doc agora tem uma lista de tf_idf
        # acessar para calculo da norma
        for doc in range(len(lista)):
            doc_id = doc + 1
            for key,value in lista[doc].items():
                tf_idf_term = lista[doc][key]
                tf_idf_doc.append(tf_idf_term*tf_idf_term)
            soma = sum(tf_idf_doc)
            tf_idf_doc = []
            # calcula a norma dos tf_idf de cada termo em cada doc
            tf_idf_norma_doc = math.sqrt(soma)
            self.document_norm[doc_id] = tf_idf_norma_doc     
        

        
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
        print(tf*idf, "tf-idf")
        return tf*idf

    def get_ordered_docs(self,query:Mapping[str,TermOccurrence],
                              docs_occur_per_term:Mapping[str,List[TermOccurrence]]) -> (List[int], Mapping[int,float]):
            documents_weight = {}





            #retona a lista de doc ids ordenados de acordo com o TF IDF
            return self.rank_document_ids(documents_weight),documents_weight

