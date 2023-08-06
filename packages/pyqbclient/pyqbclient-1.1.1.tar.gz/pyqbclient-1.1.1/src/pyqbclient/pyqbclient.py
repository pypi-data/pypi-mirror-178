from __future__ import annotations
import json
import numpy as np
import requests
import pandas as pd
from io import StringIO
import requests
import re
from lxml import etree
import logging
from typing import Union, Tuple
import time


logger = logging.getLogger("pyqbclient")


    
class Error(Exception):
    """Base Error
    """
    def __init__(self, code, msg, response=None):
        self.args = (code, msg)
        self.msg = (code, msg)
        self.desc = code
        self.response = response

    def __str__(self):
        return f'{self.msg}: {self.desc}'



class ResponseError(Error):
    pass


class QuickBaseError(Error):
    pass


default_realm_hostname = None
default_user_token = None

def set_default(realm_hostname: str=None, user_token:str =None) -> None:
    '''
    Set default realm hostname and user token for use by the Client
    '''
    global default_realm_hostname
    global default_user_token

    default_realm_hostname = realm_hostname
    default_user_token = user_token

def _slice_list(start_line: int,filter_list: list) -> list:
    '''
    The Quickbase API allows filtering by 100 values, this enables that
    '''
    end_line = start_line + 100
    slice = filter_list[start_line:end_line:]
    return slice  


class Client(object):
    '''
    A client object for interacting with a Quickbase Table
    '''

    def _check_defaults(self, realm_hostname: str, user_token: str) -> None:
        '''
        Function that checks for default host and user token, raises an 
        Exception if there has not been either a default set or a value 
        provided on Client instantiation
        '''

        if default_realm_hostname == None:
            if realm_hostname == None:
                raise ValueError('Must provide a realm hostname')
            self.realm_hostname = realm_hostname
        else:
            if realm_hostname != None:
                self.realm_hostname = realm_hostname
            else:
                self.realm_hostname = default_realm_hostname
        
        if default_user_token == None:
            if user_token == None:
                raise ValueError('Must provide a user token')
            self.user_token = f'QB-USER-TOKEN {user_token}'
        else:
            if user_token != None:
                self.user_token = f'QB-USER-TOKEN {user_token}'
            else:
                self.user_token = f'QB-USER-TOKEN {default_user_token}'

    def _set_retries(self, retries: int) -> None:
        '''
        Sets the amount of times any given transaction will be re-attempted
        '''
        if retries < 0:
            raise ValueError('Retries must be 0 or greater')
        self.retries = retries
    
    def _json_request(self, body: str, request_type: str,
    api_type: str, return_type: str, sub_url: str=None, load_as_json: bool = True) -> Union[requests.Response,
    pd.DataFrame, dict, Tuple[pd.DataFrame,dict]]:
        '''
        Make a JSON request to the JSON API
        '''

        url =f'https://api.quickbase.com/v1/{api_type}'
        if  not isinstance(sub_url,type(None)):
            url += f'/{sub_url}'
        


        for attempt in range(self.retries + 1):
            try:
                if request_type == 'post':
                    with requests.Session() as s:
                        r = s.post(
                        url, 
                        params = self.base_params, 
                        headers = self.headers, 
                        json = body
                        )


                elif request_type == 'delete':
                    with requests.Session() as s:
                        r = s.delete(
                        url, 
                        params = self.base_params, 
                        headers = self.headers, 
                        json = body
                        )

                
                elif request_type == 'get':
                    with requests.Session() as s:
                        r = s.get(
                        url, 
                        params = self.base_params, 
                        headers = self.headers
                        )
                    
                if load_as_json:
                    response = json.loads(r.text)
                else:
                    response = r.text
                

                if request_type != 'get': 
                    if "message" in response.keys():
                        raise QuickBaseError(
                         response['message'],
                         response['description']
                       ,
                        response=response
                        )
                    if "errors" in response.keys():
                        raise QuickBaseError(
                        'Request returned error(s):',
                        f'{", ".join(response["errors"])}',response=response
                        )
                if r.status_code not in [200,207]:
                        r.raise_for_status()
             

            except QuickBaseError:
                logger.critical('Quickbase Error')
                raise
            except Exception as e:    
                if attempt < self.retries:
                    logger.error(e)
                    logger.info(f'Retrying  - Attempt {attempt +1}')
                    time.sleep(10)
                    continue
                else:
                    logger.critical(e)
                    raise
            break

        if return_type == 'response':
            return response
        elif return_type == 'dataframe':
            df = pd.json_normalize(response['data'])
            metadata = response['metadata']
            return df, metadata
        elif return_type == 'properties':

            json_data = pd.read_json(StringIO(r.text))
            properties = json_data.join(
            pd.json_normalize(
            json_data.pop('properties')
            ))
            return properties
        
        elif return_type == 'unparsed':
            return r
        

    
    def _get_fields(self) -> dict:
        '''
        Function to get available fields from the table you are instantiating 
        the Client for
        '''

        params = self.base_params
        params['includeFieldPerms'] = 'false'
        return self._json_request(None,'get','fields','properties') 

    def _get_reports(self) -> dict:
        '''
        Function to get available reports from the table you are instantiating 
        the Client for
        '''
        
        return self._json_request(
        None,
        'get',
        'reports',
        'properties'
        )  

    def _get_valid_reports(self) -> list:
        '''
        Parse the available reports for table type reports
        '''
        return     self.reports.loc[
        self.reports['type'].eq('table'),'name'].to_list()

    def _get_column_dict(self) -> dict:
        '''
        Get a dictionary of field labels to field ids
        '''
        pared_fields = self.field_data.loc[:,['id','label',]].copy()
        pared_fields.loc[:,'id'] = pared_fields.loc[:,'id']
        column_dict  = pared_fields.set_index('label').to_dict()['id']
        
        return column_dict 

    def _get_label_dict(self) -> dict:
        '''
        Get a dictionary of field ids to field labels
        '''
        pared_fields = self.field_data.loc[:,['id','label',]].copy()
        pared_fields.loc[:,'id'] = pared_fields.loc[:,'id'].astype(str) + '.value'
        label_dict = pared_fields.set_index('id').to_dict()['label']
        
        return label_dict 

    def _get_rename_dict(self) -> dict:
        '''
        Returns dictionary  for renaming query results using field labels, 
        handling sub fields
        '''
        labels =list(self.label_dict.keys())
        values = list(self.label_dict.values())
        rename_dict = self.label_dict.copy()
        sub_values = [
            'name', 'id', 'email', 'userName', 'url','versions'
        ]
 
        for i  in range(0,len(labels)):
            rename_dict[
            int(f"{labels[i].replace('.value','')}")
            ] = values[i]
            rename_dict[
            f"'{labels[i].replace('.value','')}'"
            ] = int(f"{labels[i].replace('.value','')}")
            for j in range(0,len(sub_values)):
                rename_dict[
                f'{labels[i]}.{sub_values[j]}'
                ] = f'{values[i]} - {sub_values[j]}'
          
        return rename_dict

    def _get_inv_label_dict(self) -> dict:
        '''
        Returns dictionary  for renaming query field labels as field ids 
        for use in querying 
        '''
        inv_label_dict = {
        v: str(k).replace('.value','') for k, v in self.label_dict.items()
        }
        return inv_label_dict
    
        


    def _get_base_xml_request(self) -> None:
        '''
        Sets base XML request parameters for the Client
        '''
        request = {}
        request['encoding'] = 'UTF-8'
        request['msInUTC'] = 1
        request['realmhost'] = self.realm_hostname
        request['apptoken'] = self.user_token
        self.base_xml_request = request

    def _get_base_xml_headers(self) -> None:
        '''
        Sets base XML headers for the Client
        '''
        self.base_xml_headers = {
        'User-Agent': '{User-Agent}',
        'Authorization': self.user_token,
        'Content-Type': 'application/xml'
        }
    
    def _get_xml_url(self):
        '''
        Sets XML URL for the Client
        '''
        self.xml_url = f'https://{self.realm_hostname}/db/{self.table_id}'

    def _build_request(self,**request_fields) -> str:
        r"""Build QuickBase request XML with given fields. Fields can be straight
        key=value, or if value is a 2-tuple it represents (attr_dict, value), or if
        value is a list of values or 2-tuples the output will contain multiple entries.
        >>> Client._build_request(a=1, b=({}, 'c'), d=({'f': 1}, 'e'))
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><a>1</a><b>c</b><d f="1">e</d></qdbapi>'
        >>> Client._build_request(f=['a', 'b'])
        "<?xml version='1.0' encoding='UTF-8'?>\n<qdbapi><f>a</f><f>b</f></qdbapi>"
        >>> Client._build_request(f=[({'n': 1}, 't1'), ({'n': 2}, 't2')])
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><f n="1">t1</f><f n="2">t2</f></qdbapi>'
        """
        request = etree.Element('qdbapi')
        doc = etree.ElementTree(request)

        def add_sub_element(field, value):
            if isinstance(value, tuple):
                attrib, value = value
                attrib = dict((k, str(v)) for k, v in attrib.items())
            else:
                attrib = {}
            sub_element = etree.SubElement(request, field, **attrib)
            if not isinstance(value, str):
                value = str(value)
            sub_element.text = value

        for field, values in request_fields.items():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                add_sub_element(field, value)

        return etree.tostring(doc, xml_declaration=True, encoding="utf-8")




    def _xml_request(self, action: str, data: str, 
    stream: bool=True) -> etree.Element:
        '''
        Function to make XML requests against the XML API. Included because 
        the JSON API did not provide a convenient method to get the table name 
        knowing only the table id nor a method to upload files that I could figure out.
        '''


        headers = self.base_xml_headers
        headers['QUICKBASE-ACTION'] = action

        response = ""
        for attempt in range(self.retries + 1):
            try:

                response = requests.post(
                self.xml_url, data, headers=headers, stream=stream
                )
                if response.status_code != 200:
                        response.raise_for_status()
            except Exception as e:

                if attempt < self.retries:
                    logger.error(e)
                    logger.info(f'Retrying  - Attempt {attempt +1}')
                    continue
                else:
                    raise
            break

        parsed = etree.fromstring(
        response.text.encode('ascii',errors='replace')
        ) 
        error_code = parsed.findtext('errcode')
        if error_code is None:
            raise ResponseError(
            -4, '"errcode" not in response', response=response
            )
        if error_code != '0':
            error_text = parsed.find('errtext')
            error_text = error_text.text if error_text is not\
            None else '[no error text]'
            raise ResponseError(error_code, error_text, response=response)


        return parsed



    def _get_table_name(self) -> str:
        """Performs get schema on XML API to extract table name"""
        request = self.base_xml_request
        data = self._build_request(**request)
        response = self._xml_request('API_GetSchema', data)
        return response.xpath('//table/name')[0].text
    
    def _fetch_field_info(self) -> None:
        """ Updates field information and dictionaries for translation"""
        self.field_data = self._get_fields()
        self.column_dict = self._get_column_dict()
        self.label_dict = self._get_label_dict()
        self.rename_dict = self._get_rename_dict()
        self.inv_label_dict = self._get_inv_label_dict()

    def __init__(self, table_id: str, realm_hostname: str=None,
    user_token: str=None, retries: int=3, 
    dataframe: pd.DataFrame=pd.DataFrame()) -> None:
        self.table_id = table_id
        self.base_params = {
            'tableId': self.table_id
        }
        self.base_json_url = 'https://api.quickbase.com/v1/'

        self._check_defaults(realm_hostname,user_token)
        self._set_retries(retries)
        self.dataframe = dataframe
        self.headers = {
            'QB-Realm-Hostname': self.realm_hostname,

            'User-Agent': '{User-Agent}',
            'Authorization': self.user_token
        }
        self._get_base_xml_request()
        self._get_base_xml_headers()
        self._get_xml_url()
        self.table_name = self._get_table_name()
        self._fetch_field_info()
        self.reports = self._get_reports()
        self.valid_reports = self._get_valid_reports()
        self.merge_dicts = {}
        logger.info(f'Created Client for table "{self.table_name}"')
        
    

    

    def _get_filter(self,filter_criteria,record=False):
        """
        Substitutes ids for labels using the quickbase query language.
        I found using field ids to be cumbersome, this translates labels
        in to field ids.

        Example: {My_Field_Label.EX.'My Value'} might become {6.EX.'My Value'}
        
        """
        error_list = []
        pattern = re.compile(r'{(.*?)[.]')
        filter_list = []
        for m in re.finditer(pattern, filter_criteria):
            if str(m.group()).replace(
                '{',''
                ).replace('.','') not in filter_list:
                filter_list.append(str(m.group()).replace(
                '{','').replace('.','')
                )
        if record ==False:
            for k in filter_list:
                if k in filter_criteria:
                    try:
                        filter_criteria = filter_criteria.replace(
                        k,str(self.inv_label_dict[k])
                        )
                    except KeyError:
                        error_list.append(k)
            if len(error_list) > 0:
                raise ValueError(f'''Invalid field label(s) "{'", "'.join(error_list)}" '''
                                 f'''found in filter for {self.table_name}''')

        else:
            for k in filter_list:
                if k in filter_criteria:
                    filter_criteria = filter_criteria.replace(
                    k,str(self.rename_dict[k])
                    )
        
        return filter_criteria


    def _gen_filter_from_list(self, filter_list: list, 
    filter_list_label: str) -> str:
        '''
        Translates filters with labels to filters with ids
        '''
        where_str = f'{{{filter_list_label}.EX."' 
        join_str = f'"}}OR{{{filter_list_label}.EX."'
        return f'{where_str}{join_str.join(filter_list)}"}}'
         


    def get_data(self, report: str=None, columns: list=None, 
    all_columns: bool=False, overwrite_df: bool=True, return_copy: bool=True,
    filter_list_dict: dict=None, where: str=None, **kwargs) -> pd.DataFrame:
        '''
        Queries data from a quickbase table and returns a DataFrame. Primarily 
        because I wanted to upload files I gave the Client itself a DataFrame, 
        which in hindsight was perhaps not the best idea. 
        
        '''

        valid_kwargs = [
        'sortBy',
        'groupBy'
        ]
        body = {"from":self.table_id}
        # Without a default sort order does not behave as expected
        body['sortBy'] = [{'fieldId': 2, 'order': 'DESC'}]
        if report:
            if any([filter_list_dict,columns,all_columns,where,kwargs]):
                raise ValueError(
                'Columns,filters and kwargs can not be specified with a report'
                )
            if report not in self.valid_reports:
                raise ValueError(
                f'"{report}" is not a valid table type report for'
                f' {self.table_name}'
                )

            for k, v in self.reports.loc[
            self.reports['name'].eq(report),'query'
            ].to_dict().items():
                
                body['select'] = v['fields']
                body['where'] = self._get_filter(v['filter'],record=True)
                if len(v['sortBy']) > 0:
                    body['sortBy'] = v['sortBy']
                if len(v['groupBy']) > 0:
                    body['groupBy'] = v['groupBy']



        if columns:
            try:
                body['select'] = [self.column_dict[c] for c in columns]
            except KeyError as e:
                raise ValueError(
                f'Invalid Column {e} provided.'
                )
        if all_columns:
            body['select'] = list(self.label_dict.keys())
        if where:
            if not isinstance(filter_list_dict, type(None)):
                raise ValueError('Can not specify where with a filter list')
            if not isinstance(report, type(None)):
                raise ValueError('Can not specify where with a report')
            body['where']  = self._get_filter(where)

  
        invalid_kwargs = []
        for kw in kwargs:
            if kw  in valid_kwargs:
                body[kw] = kwargs[kw]
            else:
                invalid_kwargs.append(kw)

        if len(invalid_kwargs)>0:
            raise ValueError(f'Invalid Kwargs {", ".join(invalid_kwargs)}')

        if isinstance(filter_list_dict, dict):
            df_list = []
            retrieved = 0 

            for k,v in filter_list_dict.items():

                list_length = len(v)
                iter_np = np.arange(0, list_length, 100)
                iter = list(iter_np)
                for i in iter:
                    slice = _slice_list(i,v)
                    body['where'] = self._get_filter(self._gen_filter_from_list(
                    slice,
                    k)
                    )
                    df, metadata = self._json_request(
                    body,
                    'post',
                    'records',
                    'dataframe',
                    'query'
                    )
                    df_list.append(df)
                    retrieved += metadata['numRecords']

            
        else:
            df_list = []
            retrieved = 0 
            df, metadata = self._json_request(
            body,
            'post',
            'records',
            'dataframe',
            'query'
            )
            df_list.append(df)
            retrieved = metadata['numRecords']
            if metadata['totalRecords'] > metadata['numRecords']:
                body['options'] = {"skip": retrieved}
                remaining = metadata['totalRecords'] -  metadata['numRecords']
                while remaining > 0:
                    df, metadata = self._json_request(
                    body,
                    'post',
                    'records',
                    'dataframe',
                    'query'
                    )
                    retrieved += metadata['numRecords']
                    remaining = metadata['totalRecords'] - retrieved
                    body['options'] = {"skip": retrieved}
                    df_list.append(df)
                   



        result = pd.concat(df_list)
        logger.info(f'Retrieved {retrieved} records from {self.table_name}')
        result.columns = result.columns.to_series().map(self.rename_dict)

        if overwrite_df  == True:
            self.dataframe = result
        if return_copy == True:
            return result.copy()
        else:
            return result

    def get_files(self, file_field: str, where: str= None, 
    filter_list_dict: dict = None ) -> dict:
        '''
        Returns a dictionary with Field id 3 values as keys 
        and base64 encoded files as values 
        '''
        body = {"from":self.table_id}
        # Without a default sort order does not behave as expected
        body['sortBy'] = [{'fieldId': 2, 'order': 'DESC'}]

        record_label = self.field_data.loc[
        self.field_data['id']==3,
        'label'
        ].to_string(index=False)

        columns = [record_label, file_field ]
        try:
            body['select'] = [self.column_dict[c] for c in columns]
        except KeyError as e:
            raise ValueError(
            f'Invalid Column {e} provided.'
            )

        if where:
            if not isinstance(filter_list_dict, type(None)):
                raise ValueError('Can not specify where with a filter list')
            body['where']  = self._get_filter(where)

        if isinstance(filter_list_dict, dict):
            df_list = []
            retrieved = 0 
            try:
                body['select'] += [self.column_dict[col] for col in filter_list_dict.keys()]
            except KeyError as e:
                raise ValueError(
                f'Invalid Column {e} provided.'
                )
            

            for k,v in filter_list_dict.items():

                list_length = len(v)
                iter_np = np.arange(0, list_length, 100)
                iter = list(iter_np)
                for i in iter:
                    slice = _slice_list(i,v)
                    body['where'] = self._get_filter(self._gen_filter_from_list(
                    slice,
                    k)
                    )
                    
                    df, metadata = self._json_request(
                    body,
                    'post',
                    'records',
                    'dataframe',
                    'query'
                    )
                    df_list.append(df)
                    retrieved += metadata['numRecords']

        else:
            df_list = []
            retrieved = 0 
            df, metadata = self._json_request(
            body,
            'post',
            'records',
            'dataframe',
            'query'
            )
            df_list.append(df)
            retrieved = metadata['numRecords']
            if metadata['totalRecords'] > metadata['numRecords']:
                body['options'] = {"skip": retrieved}
                remaining = metadata['totalRecords'] -  metadata['numRecords']
                while remaining > 0:
                    df, metadata = self._json_request(
                    body,
                    'post',
                    'records',
                    'dataframe',
                    'query'
                    )
                    retrieved += metadata['numRecords']
                    remaining = metadata['totalRecords'] - retrieved
                    body['options'] = {"skip": retrieved}
                    df_list.append(df)
                   
        result = pd.concat(df_list)
        
        return_dict = {}
        if retrieved == 0:
            logger.info(f'Found {retrieved} records from '
                        f'{self.table_name} matching the filter criteria')
            return return_dict
        result.columns = result.columns.to_series().map(self.rename_dict)

        url_column = f'{file_field} - url'

        has_files = result.loc[result[url_column] != ''].copy()

        has_file_count = len(has_files.index)
        logger.info(f'Found {has_file_count} records from '
                    f'{self.table_name} with files in the {file_field} field')
        if has_file_count == 0:
            return return_dict


        record_list = has_files[record_label].tolist()
        file_urls = has_files[url_column].tolist()
        for index, url  in enumerate(file_urls):
            url = url[1:]
            file_str = self._json_request(None,
                                          'get',
                                          url,
                                          'response',
                                          load_as_json=False
                                          )
            return_dict[record_list[index]] = file_str

        return return_dict


    def create_fields(self, field_dict: Union[dict,list]=None, 
    external_df: pd.DataFrame=None, ignore_errors: bool=False, 
    appearsByDefault: bool=True) -> list[dict]:
        """
        Creates fields on a quickbase table. Can create based on columns 
        in a DataFrame or based on a field_dict of desired attributes.
        
        Note that my DataFrame implementation depends on my having mapped a 
        pandas Data Type to an equivalent Quickbase Data type and the mapping 
        I have done is nowhere near exhaustive. If you want to be sure that a 
        field gets created when uploading a DataFrame, create it explicitly 
        prior to uploading the DataFrame using a field_dict. Returns a list of 
        created field dictionaries
        """

        type_dict = {
        'float64': 'numeric',
        'int64': 'numeric',
        'datetime64[ns]': 'datetime',
        'object': 'text',
        'bool': 'checkbox',
        'int32': 'numeric',
        'UInt32': 'numeric',
        'Int32': 'numeric'
        }

        logger.info('Preparing to create fields')


        return_list = []
        if field_dict:
            if isinstance(field_dict, dict):
                field_dict = [field_dict]
            
            for fd in field_dict:
                body = fd
                if appearsByDefault == False:
                    body['appearsByDefault'] = False
                response = self._json_request(
                body,'post','fields','response'
                )
                logger.info(f'''Added field "{response['label']}"'''
                f' to {self.table_name}'
                )
                return_list.append(response)
                
            self._fetch_field_info()    
            return return_list
             
        if external_df is not None:
            self.dataframe = external_df.copy()
       
        body = {}

        unknown_columns = [
            col for col in self.dataframe.columns \
            if col not in self.rename_dict.values()
        ]

        
        if len(unknown_columns) > 0:
            
            dtypes_dict = self.dataframe.dtypes.to_dict()
            unknown_dict = {
            str(k): str(v) for k, v in dtypes_dict.items(
            ) if k in unknown_columns
            }

            counter = 0
            counter_dict = {}
            for k,v in unknown_dict.items():
                counter += 1
                if v not in type_dict.keys():
                    
                    counter_dict[k] =v

            if len(counter_dict) > 0 and len(counter_dict) < len(unknown_dict):
                if ignore_errors==False and len(counter_dict) > 0:
                    error_string = ''
                    for k,v in counter_dict.items():
                        error_string += f'Column: {k} datatype: {v}\n'
                    logger.error(
                    f'Unknown Pandas datatypes:\n'
                    f'{error_string}'   
                    )
                    raise ValueError(f'Unknown Pandas datatypes:\n'
                    f'{error_string}'
                    )
                else:
                    
                    for k,v in counter_dict.items():
                        logger.warn(
                            f'Unknown Pandas datatype {v} for column {k},'
                            f' field not created'
                        )
                        unknown_dict.pop(k)
                        
                    for k,v in unknown_dict.items():
  
                        if appearsByDefault == False:
                            body['appearsByDefault'] = False

                        body['label'] = k
                        body['fieldType']=type_dict[v]
                        response = self._json_request(
                        body,'post','fields','response'
                        )
                        return_list.append(response)
                        logger.info(
                        f'''Added field "{response['label']}"'''
                        f' to {self.table_name}'
                        )
                        
                    self._fetch_field_info()    
                    return return_list
             


            elif len(counter_dict) == len(unknown_dict):
                for k,v in counter_dict.items():
                    logger.warn(
                    f'Unknown Pandas datatype {v} for column {k},'
                    f' field not created'
                    )
                return return_list
            else:
                
                for k,v in unknown_dict.items():

                    if appearsByDefault == False:
                        body['appearsByDefault'] = False

                    body['label'] = k
                    body['fieldType']=type_dict[v]
                    response = self._json_request(
                    body,'post','fields','response'
                    )
                    return_list.append(response)
                    logger.info(
                    f'''Added field "{response['label']}"'''
                    f' to {self.table_name}'
                    )
                self._fetch_field_info()
                return return_list   
        else:
            
            logger.info('No unknown fields found')
            return return_list

    def update_field(self, field_label: str, field_dict: dict=None,
    **kwargs) -> dict:
        '''
        Update field attributes using field_dict or using key word arguments.
        Returns dict with field characteristics
        '''


        valid_args = [
        "label", "noWrap", "bold", "required", "appearsByDefault",
        "findEnabled", "unique", "fieldHelp", "addToForms", "properties"
        ]
        if  not any([kwargs,field_dict]):
            raise ValueError(
            'Must provide a field dict or a key word argument'
            )
        if kwargs:
            if not all([i in valid_args  for i in kwargs]):
                inv_args = [
                '"' + str(i) + '"' for i in kwargs if i not in valid_args
                ]
                raise ValueError(
                f'Invalid argument(s) {", ".join(inv_args)}.'
                )
        if field_dict:
            if type(field_dict) != dict:
                raise TypeError("'field_dict' must be a dictionary.")
            if not all([i in valid_args  for i in field_dict]):
                inv_args = [
                '"' + i + '"' for i in field_dict if i not in valid_args
                ]
                raise ValueError(f'Invalid argument(s) {", ".join(inv_args)}.')
        
        
        if type(field_label) != str:
            raise TypeError("'label' must be a string")
        if field_label not in self.inv_label_dict.keys():
            raise ValueError(
            f'{field_label} is not a valid label for table {self.table_id}'
            )
        body = {}
        if field_dict:
            body.update(field_dict)
        body.update(kwargs)
        

        response = self._json_request(
        body,
        'post',
        'fields',
        'response',
        sub_url=f'{self.inv_label_dict[field_label]}'
        )
        
        
        logger.info(
            f'Updated field {self.inv_label_dict[field_label]} with'
            f' { {k: v for k, v in response.items() if k in body.keys()} }'
        )
        self._fetch_field_info()
        return response

    def delete_fields(self, field_labels: list) -> list:
        '''
        Delete a list of fields. Takes in field labels. Returns list of deleted field ids
        '''

        if not isinstance(field_labels,list):
            raise ValueError('Must supply a list of field labels to delete')

        invalid_labels = [
        l for l in field_labels if l not in list(self.inv_label_dict.keys())
        ]
        if len(invalid_labels)>0:
            raise ValueError(
            f'''Invalid fieldlabel(s) "{'", "'.join(invalid_labels)}".'''
            )
        
        

        body = {}
        body['fieldIds'] = [int(self.inv_label_dict[f]) for f in field_labels]
        built_ins = [_ for _ in range(1,6)]

        entered_built_ins = [
            self.rename_dict[i] for i in body['fieldIds'] if i in built_ins
        ]
        if len(entered_built_ins) > 0:
            err_str = ", ".join([f'"{b}"' for b in entered_built_ins])
            raise ValueError(f'Built in field(s) {err_str} can not be deleted')

        response = self._json_request(body,'delete','fields','response')
        deleted_field_ids = []
        for k, v in response.items():
            if k == 'deletedFieldIds':
                deleted_field_ids = v
                deleted_field_labels = [
                self.rename_dict[d] for d in v
                ]
                logger.info(f'''Deleted field(s) "{'", "'.join(deleted_field_labels)}"'''
                f' from {self.table_name}')

        self._fetch_field_info() 
        return deleted_field_ids
        

    def _slice_df(self, start_line: int,step: int=5000) -> pd.DataFrame:
        '''
        Return a slice of the Client's DataFrame to facilitate uploads
        '''

        end_line = start_line + step
        slice = self.dataframe.iloc[start_line:end_line,:]
        return slice

    def post_data(self, external_df: pd.DataFrame=None, step: int=5000, 
    merge: str=None, create_if_missing: bool=False, 
    exclude_columns: list=None, subset: list=None) -> dict:
        """
        Upload a DataFrame to a quickbase table. Returns a dict with records processed,
        created record ids, updated record ids and unchanged record ids
        """

        if  isinstance(external_df, pd.DataFrame):
            self.dataframe = external_df.copy()
        if exclude_columns:
            self.dataframe.drop(labels=exclude_columns, 
                                axis=1, 
                                inplace=True)
        if subset:
            self.dataframe.drop(
            labels=[
            col for col in self.dataframe.columns
            if col not in subset and not merge],
            axis=1, 
            inplace=True
            )

        if create_if_missing ==True:
            self.create_fields(ignore_errors=True)

        self.dataframe = self.dataframe.rename(
        columns=self.inv_label_dict
        )
        if merge:
            if merge not in self.field_data.loc[
            self.field_data['unique']==True,'label'
            ].to_list():
                raise ValueError(
                'Merge columns must be unique, check Quickbase field settings'
                )

        unknown_columns = [
        col for col in self.dataframe.columns if col
        not in self.inv_label_dict.values()
        ]

        if len(unknown_columns) >= 1:
            logger.warn(f'Discovered unknown column(s) '
            f'''"{'", "'.join(unknown_columns)}".'''
            ' Unknown columns were dropped'
            )
            self.dataframe.drop(labels=unknown_columns, axis=1, inplace=True)
        
        

        dflength = len(self.dataframe.index)
        iter_np = np.arange(0, dflength, step)
        iter = list(iter_np)
        
        
        req_total = int(np.ceil(dflength / step))
        req_nr = 1
        processed=0
        created = 0
        unchanged = 0
        updated = 0
        failed = 0

        id_lists = [
            'createdRecordIds',
            'unchangedRecordIds',
            'updatedRecordIds'
        ]
        response_dict = {}

        for id_list in id_lists:
            response_dict[id_list] = []


        for i in iter :
            slice = self._slice_df(i,step=step)
            logger.info(
            f'Sending Insert/ Update Records API request {req_nr} '
            f'out of {req_total}')
            df_json = slice.to_json(orient='records')
            df_json = json.loads(df_json)
            for l in df_json:
                for k,v in l.items():
                    v = str(v).replace('None','Null')
            df_json = [{key: {"value": value} for key, value in item.items(
            ) if value is not None} for item in df_json]
            data = {"to": self.table_id, "data": df_json}
            if merge:
                data["mergeFieldId"] = int(self.inv_label_dict[merge])
            
            
            response = self._json_request(
            data,
            'post',
            'records',
            'unparsed'
            )
            metadata = json.loads(response.text)['metadata']
            processed  += metadata['totalNumberOfRecordsProcessed']
            created += len(metadata['createdRecordIds'])
            unchanged += len(metadata['unchangedRecordIds'])
            updated += len(metadata['updatedRecordIds'])

            for id_list in id_lists:
                response_dict[id_list] += metadata[id_list]
      
            if response.status_code == 200:
                logger.debug(f'Request {req_nr}: 0 no error')
            elif response.status_code == 207:
                count_dict={}
                for k,v in metadata["lineErrors"].items():
                    for item in v:
                        if item not in count_dict.keys():
                            count_dict[item] = 0;
                        count_dict[item] +=1
                for k,v in count_dict.items():
                    logger.error(f'Failed to insert {v} record(s) due to {k}')
                    failed +=v

                logger.debug(
                f'Request {req_nr}: {response}'
                f' {json.dumps(response.json())} \n'
                )
            else:
                logger.error(f'Failed to insert request {req_nr}. '
                 'Check debug logs for reason if enabled')

                logger.debug(f'Request {req_nr}: {response}' 
                f'{json.dumps(response.json())["description"]} \n')
            req_nr += 1
        
        response_dict['totalNumberOfRecordsProcessed'] = processed
        

        logger.info(f'Uploaded {processed} records to {self.table_name}, '
        f'created: {created}, unchanged: {unchanged}, updated: {updated}, '
        f'failed: {failed}'
        )

        return response_dict

    def delete_records(self, where: str=None, all_records: bool=False) -> dict:
        '''
        Delete records from a Quickbase table. Returns dict with number of records deleted
        '''

        if where == None:
            if all_records == False:
                raise ValueError(
                'Must specify records to delete'
                )
        if all_records == True:
             body = {
            "from": self.table_id,
            "where": '{3.GT.0}'
            }
        elif where:
            body ={
            "from": self.table_id,
            "where":  f"{self._get_filter(where)}"
            }
                
            

        response = self._json_request(
        body,
        'delete',
        'records',
        'response'
        )
        
        

        logger.info(
        f'Deleted {response["numberDeleted"]} records from {self.table_name}'
        )

        return response

        





    def _get_merge_dict(self, merge_field: str, try_internal: bool) -> None:
        """
        Creates a dictionary for use in uploading files
        """


        record_label = self.field_data.loc[
        self.field_data['id']==3,
        'label'
        ].to_string(index=False)
        if merge_field == record_label:
            if record_label in self.dataframe.columns:
                self.merge_dicts[merge_field]  = dict(zip(
                self.dataframe[record_label].to_list(),
                self.dataframe[record_label].to_list()
                ))
                logger.debug(
                f'Created merge dict for {merge_field}'
                )
                return
            else:
                logger.info(
                'Downloading required fields to upload files'
                )
                merge_df = self.get_data(
                columns=[record_label],
                overwrite_df=False,
                return_copy=True
                )
                self.merge_dicts[merge_field]  = dict(zip(
                merge_df[record_label].to_list(),merge_df[record_label].to_list()
                ))
                logger.debug(
                f'Created merge dict for {merge_field}'
                )
                return
        


        if try_internal:
            if merge_field and record_label in self.dataframe.columns:
                self.merge_dicts[merge_field]  = dict(zip(
                self.dataframe[merge_field].to_list(),
                self.dataframe[record_label].to_list()
                ))
                logger.debug(
                f'Created merge dict for {merge_field}'
                )
                return
        logger.info(
        'Downloading required fields to upload files'
        )
        merge_df = self.get_data(
        columns=[merge_field,record_label],
        overwrite_df=False,
        return_copy=True
        )
        self.merge_dicts[merge_field]  = dict(zip(
        merge_df[merge_field].to_list(),merge_df[record_label].to_list()
        ))
        logger.debug(
        f'Created merge dict for {merge_field}'
        )
        
 


            
    def upload_files(self, field_label: str, file_dict: dict,
    merge_field: str, try_internal: bool=True) -> list[dict[str,str]]:
        """
        Upload files to existing records, merging on a value in a unique field.
        file_dict is a dictionary  setup like so :
        {'*Filename with extension*':
         {
            'merge_value': '*The value you are merging on*',
            'file_str': '*Base64 encoded string of your file*'
         }
        }
        The merge field is provided separately as the label of the field.
        Returns a list of dicts with record ids and update ids
        """
    
        request = self.base_xml_request
        if merge_field not in self.field_data.loc[
        self.field_data['unique']==True,'label'
        ].to_list():
                raise ValueError(
                'Invalid merge field. Merge field must exist in the table'
                ' and be unique, check Quickbase field settings'
                )
       
        if merge_field not in self.merge_dicts.keys():
            self._get_merge_dict(merge_field,try_internal)
        
        uploaded_files = 0

        return_list = []

        for k, v in file_dict.items():
            try:
                request['rid'] = self.merge_dicts[merge_field][v['merge_value']]
            except KeyError:
                raise ValueError(
                f'"{v["merge_value"]}" not a valid value in {merge_field}'
                )
            request_field = (
            {'fid': self.inv_label_dict[field_label],
                'filename': k}, v['file_str'])
            request['field'] = [request_field]

            data = self._build_request(**request)
            response = self._xml_request('API_EditRecord',data)
            rid = response.xpath('//qdbapi/rid')[0].text
            update_id = response.xpath('//qdbapi/update_id')[0].text

            return_list.append({'rid': rid,
                                'update_id': update_id,
                                }
                            )
            uploaded_files +=1
        
        logger.info(f'Uploaded {uploaded_files} files to {self.table_name}')
        return return_list