from typing import Union
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download
from gensim.models import KeyedVectors
import gensim.downloader as api
from sentence_transformers import SentenceTransformer, util, InputExample, losses, models
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer
from scipy.spatial.distance import cdist

def preprocess(sentence: str, remove_punct: bool, remove_stop_words: bool, stemm: bool, lang: str='en') -> str: 
    if lang.lower() == 'en':
        ps = PorterStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('english')
            return ' '.join([ps.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([ps.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    elif lang.lower() == 'ar':
        st = ISRIStemmer()
        # remove punctuations
        if not remove_punct:
            sentence = sentence.translate(str.maketrans('', '', punctuation))
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('arabic')
            return ' '.join([st.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([st.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    else:
        raise Exception('non recognized language please specify either en|ar')
        
        
class sentence_tranformer():
    def __init__(
        self, 
        source: Union[list[str], pd.DataFrame], 
        target: Union[list[str], pd.DataFrame], 
        target_group: Union[list[str], pd.DataFrame]=None,
        source_col: str=None, 
        target_col: str=None, 
        model: SentenceTransformer=None, 
        lang: str='en', 
        only_include: list[str]=None
    ):

        if isinstance(source, pd.DataFrame) and not isinstance(source, pd.DataFrame):
            raise TypeError('if source is a dataframe target must also be a dataframe')

        if isinstance(source, list) and not isinstance(source, list):
            raise TypeError('if source is a list target must also be a list')

        if isinstance(source, pd.DataFrame):
            self.use_frames = True
    
            if source_col not in source.columns:
                raise KeyError('source_col not found in source DataFrame cloumns')
            if target_col not in target.columns:
                raise KeyError('target_col not found in target DataFrame cloumns')

            if target_group is not None:
                if isinstance(target_group, str):
                    if target_group not in target.columns:
                        raise KeyError('target_group not found in target DataFrame cloumns')
                    self.group_ids = target[target_group].tolist()
                else:
                    self.group_ids = target_group
            else:
                self.group_ids = None
                
            if only_include is not None:
                for col_name in only_include:
                    if col_name not in target.columns:       
                        raise KeyError(f'only_include value:({col_name}) not found not found in target DataFrame cloumns')    
                only_include.insert(0, target_col)
                
                target = target.loc[:, only_include]

            self.source_df = source
            self.target_df = target
            self.source_names = source[source_col]
            self.target_names = target[target_col]
        else:
            if isinstance(target_group, list):
                self.group_ids = target_group
            else:
                self.group_ids = None
            if not source:
                raise TypeError('Inputs are empty')
        
            if not target:
                raise TypeError('Targets are empty') 
            self.use_frames = False
            self.source_names = source
            self.target_names = target

        if pd.isnull(self.source_names).any():
            raise ValueError('Inputs contain null values')
        
        if pd.isnull(self.target_names).any():
            raise ValueError('Targets contain null values')

        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model...')
            if lang.lower() == 'en':
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                print('done...')
            else:
                self.model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
                print('done...')


    def match(self, topn: int=1, return_match_idx: bool=False, threshold: float=0.5) -> pd.DataFrame:
        '''
        Main match function. return only the top candidate for every source string.
        '''    
        self.encoded_targets = self.model.encode(self.target_names) # encode the targets
        self.encoded_inputs = self.model.encode(self.source_names) # encode the inputs
        
        self.topn = topn
        self.return_match_idx = return_match_idx
        self.threshold = threshold

        self.top_cosine_sim()

        match_output = self._make_matchdf()

        return match_output

    def clean_data(self, remove_punct: bool=True, remove_stop_words: bool=True, stemm: bool=False, lang: str='en') -> None: 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def top_cosine_sim(self) -> None:
        # results = np.array([self.max_cosine_sim(self.model.encode(input)) if not (pd.isnull(input)) else (None, None) for input in self.source_names], dtype=object)
        self.targets, self.top_cosine, self.match_idxs = self.max_cosine_sim()
        self.match_idxs_trans = self.match_idxs.T
        self.top_cosine_trans = self.top_cosine.T

    def max_cosine_sim(self):
        # cosine_results = util.cos_sim(input, self.encoded_targets)
        distances = util.cos_sim(self.encoded_inputs, self.encoded_targets).numpy()
        sorted = -np.sort(-distances)

        targets = np.full((len(self.source_names), self.topn), None)
        max_cosines = np.full((len(self.source_names), self.topn), None)
        match_idxs = np.full((len(self.source_names), self.topn), None)
        # loop over top results to extract the index, target, and score for each match
        if self.group_ids is not None:
            for i, row in enumerate(sorted):
                column_id = 0
                previous_group_id = float('inf')
                for highest_score in row:
                    if column_id >= self.topn or highest_score < self.threshold:
                        break
                    for score_index in (np.where(distances[i] == highest_score)[0]):
                        if self.group_ids[score_index] == previous_group_id:
                            continue
                        match_idxs[i, column_id] = score_index
                        targets[i, column_id] = self.target_names[score_index]
                        max_cosines[i, column_id] = float(highest_score)
                        
                        column_id += 1
                        previous_group_id = self.group_ids[score_index]
                        if column_id >= self.topn:
                            break
        else:
            for i, row in enumerate(sorted):
                column_id = 0
                for highest_score in row:
                    if column_id >= self.topn or highest_score < self.threshold:
                        break
                    for score_index in (np.where(distances[i] == highest_score)[0]):
                        match_idxs[i, column_id] = score_index
                        targets[i, column_id] = self.target_names[score_index]
                        max_cosines[i, column_id] = float(highest_score)
                        
                        column_id += 1
                        if column_id >= self.topn:
                            break

        return targets, max_cosines, match_idxs



    def _make_matchdf(self)-> pd.DataFrame:
        ''' Build dataframe for result return '''
        if self.use_frames:
            arr_temp = np.full((len(self.source_names), len(self.target_df.columns)+1), None)
            for i, (match_idx, score) in enumerate(zip(self.match_idxs_trans[0], self.top_cosine_trans[0])):
                if match_idx in self.target_df.index:
                     temp = self.target_df.iloc[match_idx].tolist()
                     temp.insert(0, score)
                     arr_temp[i, :] = temp
            cols = self.target_df.columns.tolist() 
            cols.insert(0, 'score_1')
            match_df= pd.DataFrame(arr_temp, columns=cols)
            # concat targets matches into one dataframe
            for match_num in range(1, len(self.match_idxs_trans)):
                arr_temp = np.full((len(self.source_names), len(self.target_df.columns)+1), None)
                for i, (match_idx, score) in enumerate(zip(self.match_idxs_trans[match_num], self.top_cosine_trans[match_num])):
                    if match_idx in self.target_df.index:
                        temp = self.target_df.iloc[match_idx].tolist()
                        temp.insert(0, score)
                        arr_temp[i, :] = temp
                cols = self.target_df.columns.tolist() 
                cols.insert(0, f'score_{match_num+1}')
                df_temp= pd.DataFrame(arr_temp, columns=cols)
                match_df = match_df.merge(df_temp, left_index=True, right_index=True, suffixes=(f'_{match_num}', f'_{match_num+1}'))
            # merge matches with source
            match_df = self.source_df.reset_index(drop=True).merge(match_df, left_index=True, right_index=True, suffixes=(f'_source', f'_target'))
        elif not self.return_match_idx:
            match_list = []
            for source, top_scores, targets in zip(self.source_names, self.top_cosine, self.targets):
                row = []
                row.append(source)
                # loop over results of multi matches
                for top_score, target in zip(top_scores, targets):
                    row.append(top_score)
                    row.append(target)
                     
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'score', 'prediction']
            
            for i in range(2, self.topn+1):
                colnames.append(f'score_{i}')
                colnames.append(f'prediction_{i}')
                
            match_df = pd.DataFrame(match_list, columns=colnames)
        else:
            match_list = []
            for source, top_scores, targets, match_idxs in zip(self.source_names, self.top_cosine, self.targets, self.match_idxs):
                row = []
                row.append(source)
                # loop over results of multi matches
                for top_score, target, match_idx in zip(top_scores, targets, match_idxs):
                    row.append(top_score) 
                    row.append(target)
                    row.append(match_idx)
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'score', 'prediction', 'match_idx']
            
            for i in range(2, self.topn+1):
                colnames.append(f'score_{i}')
                colnames.append(f'prediction_{i}')
                colnames.append(f'match_idx_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)  

        return match_df


class word_mover_distance():
    def __init__(self, source_names, target_names, model):
        if not source_names:
            raise Exception('Inputs are empty')
        
        if not target_names:
            raise Exception('Targets are empty') 
               
        if pd.isnull(source_names).any():
            raise Exception('Inputs contain null values')
        
        if pd.isnull(target_names).any():
            raise Exception('Targets contain null values')
        
        self.source_names = source_names
        self.target_names = target_names
        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model (English model)...')
            self.model = api.load('glove-wiki-gigaword-300')

    def match(self, topn=1, return_match_idx=False):
        '''
        Main match function. return only the top candidate for every source string.
        '''
        self.topn = topn
        self.return_match_idx = return_match_idx
        
        self.top_wmd_distance()

        match_output = self._make_matchdf()

        return match_output


    def clean_data(self, remove_punct=True, remove_stop_words=True, stemm=False, lang='en'): 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def min_wmd_distance(self, input):
        wmd_results = np.array([self.model.wmdistance(input, target) for target in self.target_names])
        
        # get topn results
        wmd_sorted = np.sort(np.unique(wmd_results))
        scores = []
        indexes = []
        for x in wmd_sorted:
            if len(indexes) == self.topn:
                break
            for y in np.where(wmd_results == x)[0]:
                scores.append(float(1 - x)) # convert distance to score
                indexes.append(y)
                if len(indexes) == self.topn:
                    break    
        targets = [self.target_names[idx] for idx in indexes]
        
        # fill empty topn results 
        while len(targets) < self.topn:
            indexes.append(None)
            targets.append(None)
            scores.append(None)
        return targets, scores, indexes
    

    def top_wmd_distance(self):
        results = np.array([self.min_wmd_distance(input) for input in self.source_names])
        self.targets = results[:, 0]
        self.top_scores = results[:, 1]
        self.match_idxs = results[:, 2]


    def _make_matchdf(self):
        ''' Build dataframe for result return '''
        if not self.return_match_idx:
            match_list = []
            for source, targets, top_scores in zip(self.source_names, self.targets, self.top_scores):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score in zip(targets, top_scores):
                        row.append(target)
                        row.append(top_score) 
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)
        else:
            match_list = []
            for source, targets, top_scores, match_idxs in zip(self.source_names, self.targets, self.top_scores, self.match_idxs):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score, match_idx in zip(targets, top_scores, match_idxs):
                        row.append(target)
                        row.append(top_score) 
                        row.append(match_idx)
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score', 'match_idx']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')
                colnames.append(f'match_idx_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)  
        
        return match_df