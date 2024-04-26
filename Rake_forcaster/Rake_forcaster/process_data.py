# import sklearn
import pandas as pd
import numpy as np
import joblib
import xml.etree.ElementTree as ET
from pathlib import Path


def preprocess(df):
  df = df[['SttnFrom', 'SttnTo', 'LoadName', 'LoadID', 'RakeID', 'LoadType', 'TotalUnit', 'LEFlag', 'Cmdt', 'Cnsr', 'Cnsg',
          'DeptTime', 'TransitTime', 'ExpdArvlTime']]

  df.rename(columns={'TotalUnit': 'ActlUnits',
                     'Cmdt': 'Cmdt_2',
                     'LEFlag': 'LEFlag.1'}, inplace=True)

  df[['Wagons', 'Engine']] = df['ActlUnits'].str.split('+', expand=True)
  df['Engine'] = df.Engine.astype('int')
  df['Wagons'] = df.Wagons.astype('int')
  df.drop('ActlUnits', axis=1, inplace=True)
  df.dropna(subset=['DeptTime'], inplace=True)
  df['DeptTime']= pd.to_datetime(df['DeptTime'], dayfirst=True)
  df['ExpdArvlTime'] = pd.to_datetime(df['ExpdArvlTime'], dayfirst=True)

  time_hold = df[['DeptTime', 'ExpdArvlTime', 'TransitTime']]

  df['DepMonth']= df['DeptTime'].dt.month
  df['DepDayk'] = df.DeptTime.dt.day
  df['DepDayOfYear'] = df.DeptTime.dt.day_of_year
  df['DepYear'] = df.DeptTime.dt.year
  df['DepDayOfWeek'] = df.DeptTime.dt.day_of_week
  df.drop(['DeptTime', 'ExpdArvlTime', 'TransitTime'], axis=1, inplace=True)
  df['SailUnitFrom'] = ''

  for label, content in df.items():
    if(pd.api.types.is_string_dtype(content)):
      df[label] = content.astype('category').cat.as_ordered()

  for label, content in df.items():
    if(not pd.api.types.is_numeric_dtype(content)):
        df[label + "_is_missing"] = pd.isnull(content)
        df[label] = pd.Categorical(content).codes + 1

  return df, time_hold



def process():
  print("hello00000000ooooooooooo")
  file_dir = str(Path(__file__).resolve().parent.parent) + '/uploads/uploaded_file.xml'
  # print(file_dir)
  tree = ET.parse(file_dir)
  root = tree.getroot()

  columns = ['ZoneCode', 'CrntDvsn', 'Sttn', 'LoadStts', 'SttsChngTime', 'SttnFrom', 'SttnTo', 'LineNo', 'CC',
           'LoadName', 'LoadID', 'RakeID', 'LoadType', 'TotalUnit', 'EW', 'LEFlag', 'Cmdt', 'Cnsr', 'Cnsg',
           'LdngDate', 'DeptTime', 'TransitTime', 'LocoNumb', 'LocoType', 'ExpdArvlTime']

  data_rows = []
  for row in root.findall('.//Row'):
    data = {}
    for col in columns:
        data[col] = row.find(col).text
    data_rows.append(data)

  df = pd.DataFrame(data_rows, columns=columns)
  tmp, time_hold = preprocess(df)
  # print(tmp.head())

  mod_dir = str(Path(__file__).resolve().parent.parent) + '/estimator/GS_Model.joblib'
  model = joblib.load(mod_dir)
  tmp = tmp.reindex(columns=model.feature_names_in_)
  y_pred = model.predict(tmp)
  y_pred = np.floor(y_pred)
  # print(y_pred)
  final_df = df[['RakeID', 'LoadType', 'SttnFrom', 'SttnTo',  'LEFlag', 'Cmdt', 'Cnsr',
          'DeptTime', 'LoadStts']]
  final_df['DeptTime'] = pd.to_datetime(final_df['DeptTime'])
  final_df.dropna(subset=['DeptTime'], inplace=True)
  final_df['ETA'] = (final_df['DeptTime'] + pd.to_timedelta(y_pred, unit='m'))
  final_df['DeptTime'] = final_df['DeptTime'].dt.strftime('%d/%m/%Y %H:%M:%S')
  final_df['ETA'] = final_df['ETA'].dt.strftime('%d/%m/%Y %H:%M:%S')
  # print(len(final_df['DeptTime']))
  # print(y_pred.shape)
  # print(final_df)
  return final_df

# process()