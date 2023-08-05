import pandas as pd
from pandas import DataFrame
from time import gmtime, strftime
import awswrangler as wr
import json
import boto3
from boto3.session import Session

from aws_feature_store.feature_definition import (
    FeatureDefinition,
    FeatureTypeEnum,
)

from aws_feature_store.inputs import (
    OnlineStoreConfig,
    OnlineStoreSecurityConfig,
    S3StorageConfig,
    OfflineStoreConfig,
    DataCatalogConfig,
    FeatureValue,
    FeatureParameter,
)

from typing import Sequence, List, Dict, Any, Union



class FeatureGroup:
    """FeatureGroup definition.

    This class instantiates a FeatureGroup object that comprises of a name for the FeatureGroup,
    session instance, and a list of feature definition objects i.e., FeatureDefinition.

    Attributes:
        name (str): name of the FeatureGroup instance.
        s3_uri (str): S3 URI of the offline store
        boto3_session (Session): session instance to perform boto calls.
        
    """

    def __init__(
        self,
        name: str,
        s3_uri: str,
        boto3_session: Session):
        
        self.name = name
        self.s3_uri = s3_uri
        self.boto3_session = boto3_session
        
        #==========================================
        
        bucket_name = s3_uri.replace('s3://','').split('/')[0]
        s3_folder = s3_uri.replace(f's3://{bucket_name}/','')
        
        if len(s3_folder)==0:
            raise
        
        if s3_folder[-1]=='/':
            s3_folder = s3_folder[:-1]
        
        self.s3_folder = s3_folder
        self.bucket = boto3_session.resource('s3').Bucket(bucket_name)
        
        json.load_s3 = lambda f: json.load(self.bucket.Object(key=f).get()["Body"])
        json.dump_s3 = lambda obj, f: self.bucket.Object(key=f).put(Body=json.dumps(obj))
        
        #===check bucket existance=================
        folder_exists=False
        for folder_exists in self.bucket.objects.filter(Prefix=f'{s3_folder}/'):
            break
        if not folder_exists:
            logging.error(f'Folder {s3_folder}/ does not exist.')
            raise
                
        for folder in ['data','meta_data']:
            folder_exists=False
            for folder_exists in self.bucket.objects.filter(Prefix=f'{s3_folder}/{folder}/'):
                break
            if not folder_exists:
                logging.warn(f'Folder {s3_folder}/{folder}/ does not exist. Will be created')
                status = self.bucket.put_object(Key=f'{s3_folder}/{folder}/')
                 
        
        #===check if feature_group_exists===========
        if self.exists():
            objs = [o for o in self.bucket.objects.filter(Prefix=f'{s3_folder}/meta_data/{self.name}/')]
            self.create_feature_store_args = json.load_s3(objs[-1].key)
    
    
    def exists(self):
        #===check if feature_group_exists===========
        for folder in ['data','meta_data']:
            feature_group_exists=False
            for feature_group_exists in self.bucket.objects.filter(Prefix=f'{s3_folder}/{folder}/{self.name}/'):
                break
            if not feature_group_exists:
                return False
            
        try:
            objs = [o for o in self.bucket.objects.filter(Prefix=f'{s3_folder}/meta_data/{self.name}/')]
            self.create_feature_store_args = json.load_s3(objs[-1].key)
        except Exception as e:
            logging.war('Failed to read config for {self.name}')
            return False
        
        return True
        

    def create(
        self,
        event_time_feature_name: str,
        record_identifier_name: str = None,
        description: str = None,
        feature_script_repo: str = None,
        data_source: str = None,
        partition_columns: List[str] = None,
        feature_definitions: Sequence[FeatureDefinition] = None,
        tags: List[Dict[str, str]] = None
    ):
        """sumary_line
        
        Keyword arguments:
            description: What is this feature group about
            feature_script_repo: link to the repo with script used to create the feature group
            data_source: description what data are used to create the feature group
            feature_definitions (Sequence[FeatureDefinition]): list of FeatureDefinitions.
            partition_columns: ordered list columns expected in data_frame which will be used for partitioning on S3
        
        Return: return_description
        """
        create_feature_store_args = dict(
            feature_group_name=self.name,
            record_identifier_name=record_identifier_name,
            event_time_feature_name=event_time_feature_name,
            feature_definitions=[
                feature_definition.to_dict() for feature_definition in feature_definitions
            ],
            partition_columns=partition_columns,
            description=description,
            feature_script_repo=feature_script_repo,
            data_source=data_source,
            tags=tags,
        )

        s3_uri = self.s3_uri
        
        #===check feature_group_exists===========
        feature_group_exists=False
        for feature_group_exists in self.bucket.objects.filter(Prefix=f'{self.s3_folder}/data/{self.name}/'):
            break
        if feature_group_exists:
            raise
        #========================================
        
        #===create folder =======================
        status = self.bucket.put_object(Key=f'{self.s3_folder}/data/{self.name}/')
    
        #===create config =======================
        s3_storage_config = S3StorageConfig(s3_uri=s3_uri)
        offline_store_config = OfflineStoreConfig(
            s3_storage_config=s3_storage_config,
            data_catalog_config=None,
        )
        create_feature_store_args.update(
            {"offline_store_config": offline_store_config.to_dict()}
        )
        self.create_feature_store_args = create_feature_store_args
        
        #===record config to meta_data==========
        fg_time = gmtime()
        fg_timestamp = strftime("%Y-%m-%d'T'%H:%M:%SZ", fg_time)
        key = f'{self.s3_folder}/meta_data/{self.name}/{fg_timestamp}.json'
        json.dump_s3(create_feature_store_args, key)
        
        return create_feature_store_args
            
    def describe(
        self,
    ):
        """Describe a FeatureGroup in FeatureStore service.

        Returns:
            Response dict from service.
        """

        return self.create_feature_store_args
    
    def ingest_data_frame(
        self,
        data_frame: DataFrame,
        file_name: str
    ):
        """Ingest the content of a pandas DataFrame to feature store.

        Args:
            data_frame (DataFrame): data_frame to be ingested to feature store splited by biz_id.
            file_name (str): json name of the file to store on s3. (usually timestamp)
            
        Returns:
            Nothing.
        """
        # filter columns
        columns = [f['FeatureName'] for f in self.create_feature_store_args['feature_definitions']]
        
        # add event_time
        event_time_feature_name = self.create_feature_store_args['event_time_feature_name']
        partition_columns = self.create_feature_store_args['partition_columns']
        fg_time = gmtime()
        fg_timestamp = strftime("%Y-%m-%dT%H:%M:%SZ", fg_time)
        
        if partition_columns is not None:
            for ids, g in data_frame.groupby(partition_columns):
                if type(ids)==tuple:
                    ids = [str(x) for x in ids]
                else:
                    ids = [str(ids)]
                    
                ids_key = '/'.join(ids)
                
                key = f'{self.s3_uri}/data/{self.name}/{ids_key}/{fg_time.tm_year}/{fg_time.tm_mon}/{fg_time.tm_mday}/{file_name}.json'#{fg_time.tm_hour}/
                    
                df = g[columns]
                df[event_time_feature_name] = fg_timestamp
                wr.s3.to_json(df=df, path=key, boto3_session=self.boto3_session)
            