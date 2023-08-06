import pandas as pd
import re
import xml.etree.ElementTree as ET
import requests
from pathlib import Path
from typing import NamedTuple, Union
from dataclasses import dataclass
from copy import deepcopy
from enum import Enum

INVALID = '!_INVALID_'

class MapType(Enum):
   OneToOne = 0
   OneToMany = 1
   ManyToOne = 2
   ManyToMany = 3

class SourceField(NamedTuple):
  isRegEx: bool
  value: str   


@dataclass
class Dataflow():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   datastructure: str

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')
      self.datastructure = elem.find('str:Structure', namespaces=SDMXMappingUtility.ns).text

   @property
   def fullid(self):
      return f'{self.agencyID}:{self.id}({self.version})'   

      


@dataclass
class DataStructure():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   dimensions: list

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')

      self.dimensions = [] 
      for dimensions_element in elem.findall('*/str:DimensionList/str:Dimension', namespaces=SDMXMappingUtility.ns):
         dimension = {k: dimensions_element.get(k) for k in ['id', 'position']}
         self.dimensions.append(deepcopy(dimension))
      for dimensions_element in elem.findall('*/str:DimensionList/str:TimeDimension', namespaces=SDMXMappingUtility.ns):
         dimension = {k: dimensions_element.get(k) for k in ['id', 'position']}
         self.dimensions.append(deepcopy(dimension))


   def isdimension(self, dimension) -> bool:
      for d in self.dimensions:
         if d['id'] == dimension:
            return True

      return False       


@dataclass
class StructureMap():
   source: str 
   target: str
   target_type: str = ''
   target_id: str = '' 
   
   def __init__(self, elem: ET.Element) -> None:
      self.source = elem.find('str:Source', namespaces=SDMXMappingUtility.ns).text
      self.target = elem.find('str:Target', namespaces=SDMXMappingUtility.ns).text
      p = re.compile(r'.*datastructure\.(.+)=(.+:.+\([0-9]+\.[0-9]+\))')
      m = p.match(self.target)      
      if m:
         self.target_type, self.target_id = m.groups()

      

@dataclass
class ComponentMap():
   sources: list
   targets: list
   type: MapType
   implicit: bool
   representation: str = ''
  
   def __init__(self, elem: ET.Element) -> None:
      sl = list(elem.findall('str:Source', namespaces=SDMXMappingUtility.ns))
      self.sources = ['_S_'+e.text for e in sl]

      tl = list(elem.findall('str:Target', namespaces=SDMXMappingUtility.ns))
      self.targets = [e.text for e in tl]

      rm = elem.findall('str:RepresentationMap', namespaces=SDMXMappingUtility.ns)
      if rm:
            self.representation = rm[0].text
            self.implicit = False
      else:
            self.implicit = True

      if len(sl)==1:
            if len(tl)==1:
               self.type = MapType.OneToOne
            else:
               self.type = MapType.OneToMany
      else:
         if len(tl)==1:
            self.type = MapType.ManyToOne
         else:
            self.type = MapType.ManyToMany


@dataclass
class FixedValueMap():
   value: str
   target: str
  
   def __init__(self, elem: ET.Element) -> None:
      self.target = elem.find('str:Target', namespaces=SDMXMappingUtility.ns).text
      self.value = elem.find('str:Value', namespaces=SDMXMappingUtility.ns).text


@dataclass
class RepresentationMap():
   urn: str
   isexternalreference: bool
   mappings: list 

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')

      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True

      self.mappings = [] 
      for rm in elem.findall('str:RepresentationMapping', namespaces=SDMXMappingUtility.ns):
         rmd = {'sourcevalues': [], 'targetvalues': []}
         for sv in rm.findall('str:SourceValue', namespaces=SDMXMappingUtility.ns):
            if 'isRegEx' in sv.attrib.keys():
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=bool(sv.attrib['isRegEx'])))
            else:   
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=False))   
               
         for tv in rm.findall('str:TargetValue', namespaces=SDMXMappingUtility.ns):
            rmd['targetvalues'].append(tv.text)
         self.mappings.append(deepcopy(rmd))
      
   def _replace_matches(self, matching_groups: tuple, target_list: list[str]) -> list[str]:
      sp = re.compile(r'.*(\\[1-9]).*')
      for idx, val in enumerate(target_list):
         sm = sp.match(val)
         if sm: 
            for x in sm.groups():
               # index correction to allow end-user to use 1 based indexing for matching groups
               target_list[idx] = val.replace(x, matching_groups[int(x[1])-1], 1)
   
      return target_list

   def get_target_values_by_sourcelist(self, sourcelst: list) -> Union[list[str], None]:
      
         for m in self.mappings:
            pairs = zip(m['sourcevalues'], sourcelst)
            matched = True
            target = deepcopy(m['targetvalues'])
            # assumption: only one of the fields in source has RegEx
            for pair in pairs:
               if pair[0].isRegEx:
                  p = re.compile(pair[0].value)
                  matches = p.match(pair[1])
                  if matches:
                     target = self._replace_matches(matches.groups(), deepcopy(target))
                  else: 
                     matched = False
               else:
                  if pair[0].value != pair[1]:
                     matched = False
            if matched:
               return target
         if any([s!='' for s in sourcelst]):
            return [INVALID] * len(self.mappings[0]['targetvalues'])
         else:
            return [''] * len(self.mappings[0]['targetvalues'])   
      


# Partial key mapping utility working with SDMX 3.0 structure-set and representation mapping objects
class SDMXMappingUtility():

   ns = {"xsi": "http://www.w3.org/2001/XMLSchema-instance",
         "message": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/message",
         "str": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/structure",
         "com": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/common"
         }

   def __init__(self, mapping_tree: ET.ElementTree , source_file: Path):
         self.source_file = source_file
         self.mapping_tree = mapping_tree
         self._read_mapping()
         self._read_source()
      
   @classmethod
   def initialise_with_registry(cls, registry_url: str, source_file: Path):
      try:
         headers = {
            'accept': 'application/vnd.sdmx.structure+xml;version=3.0'
         }
         # TODO check if SSL verification can be switched on - needs https for the registry
         response = requests.get(registry_url, verify=False, headers=headers)

      except Exception as err:
         return 'ERROR: ' + str(err)
      else:
         if response.status_code != 200:
            return 'UNEXPECTED: ' + response.text 
         else:
            return cls(ET.ElementTree(ET.fromstring(response.content)), source_file)

   @classmethod
   def initialise_with_file(cls, mapping_file: Path, source_file: Path):
      return cls(ET.parse(mapping_file), source_file)         
               

   def _read_mapping(self):
      print('reading mapping objects...')
      try:
         root = self.mapping_tree.getroot()

         dataflow_elements = root.findall('*/str:Dataflows/str:Dataflow', namespaces=SDMXMappingUtility.ns)
         dataflows = [Dataflow(e) for e in dataflow_elements]
         self.dataflows = dataflows

         datastructure_elements = root.findall('*/str:DataStructures/str:DataStructure', namespaces=SDMXMappingUtility.ns)
         datastructures = [DataStructure(e) for e in datastructure_elements]
         self.datastructures = datastructures

         struct_map = root.find('*/str:StructureMaps/str:StructureMap', namespaces=SDMXMappingUtility.ns)
         self.structure_map = StructureMap(struct_map)

         component_maps = list(struct_map.findall('str:ComponentMap', namespaces=SDMXMappingUtility.ns))
         cms = [ComponentMap(e) for e in component_maps]
         self.component_maps = cms

         fixedvalue_maps = list(struct_map.findall('str:FixedValueMap', namespaces=SDMXMappingUtility.ns))
         fvms = [FixedValueMap(e) for e in fixedvalue_maps]
         self.fixedvalue_maps = fvms

         representations = root.findall('*/str:RepresentationMaps/str:RepresentationMap', namespaces=SDMXMappingUtility.ns)
         reps = [RepresentationMap(e) for e in representations]
         self.representation_maps = reps
      except Exception as err:
         print(str(err))

   def _read_source(self):
      print('reading source file...')
      try:
         df = pd.read_csv(self.source_file, dtype=str, na_filter=False)
         df.rename(columns = {cn: '_S_'+cn for cn in df.columns}, inplace = True)
         # Add missing columns
         for cm in self.component_maps:
            for source in cm.sources:
               if source not in df.columns:
                  df[source] = pd.Series(dtype='str')

         self.df_source_partial_keys = df 
      except Exception as err:
         print(str(err))

   def get_representation_by_urn(self, urn: str) -> Union[RepresentationMap, None]:
      for x in self.representation_maps:
         if x.urn == urn:
            return x
      return None

   # the urn to lookup could be that of a Dataflow or the DSD itself 
   def get_dsd_by_urn(self, urn: str) -> DataStructure:
      for df in self.dataflows:
         if df.urn == urn:
            for ds in self.datastructures:
               if ds.urn == df.datastructure:
                  return ds

      for dsd in self.datastructures:
         if dsd.urn == urn:
            return dsd

      return None                   

   # Generate mappings partial keys
   # includeSourceColumns: if true: both keys (from source and from target) will be in the dataframe
   #          false: only keys from target dataflow will be in the dataframe
   # includeAttributesMeasures: if true: all dimensions, attributes, and measures of the target dataflow will be in the dataframe
   #          false: only dimensions from target dataflow will be in the dataframe
   # nulledFixedTargets: if true: the targets with fixed representation will not be inserted (the expected behaviour when partial keys are mapped 
   #          for attribute and referential metadata attachment), false: for full data mappings
   # writeTargetStructInfo: if true: SDMX csv 3.0 style structural and action information will be writtern into the first columns of the generated file
   # dropInvalid: if true: non-mapped and source records containing invalid members will be dropped (in cases when the mapping acts as a filter)
   # TODO correct the order of columns and produce SID - a partial-key for metadata attachments

   def generate_mappings_partial_keys(self, includeSourceColumns=False, includeAttributesMeasures=False, nulledFixedTargets=False, writeTargetStructInfo=False, dropInvalid=False):
      
         df = self.df_source_partial_keys
         
         # TODO revise the structure components to write (is source needed?, controlling the Action - with an Enum?, Generate SID?)
         if writeTargetStructInfo:
            al = ['STRUCTURE', 'STRUCTURE_ID', 'ACTION']
            df[al] = df.apply(lambda row: [self.structure_map.target_type.lower(), self.structure_map.target_id, 'A'], axis=1, result_type='expand')

         # ComponentMaps
         for cm in self.component_maps:
            if cm.type in [MapType.OneToOne] and cm.implicit:
               # copy identical with target component-name
               print(f'copying source to target {cm.sources} -> {cm.targets}')
               df[cm.targets[0]] = df[cm.sources[0]]
            else:
               # only those cases can be mapped safely where there are valid inputs in all source columns
               print(f'applying representation map {cm.sources} -> {cm.targets}')
               rm = self.get_representation_by_urn(cm.representation)
               df[cm.targets] = df.apply(lambda x: rm.get_target_values_by_sourcelist([x[c] for c in cm.sources]), axis=1, result_type='expand')

         # Add target missing columns mapped as fixed value
         for fvm in self.fixedvalue_maps:
            if not nulledFixedTargets:
               df[fvm.target] = fvm.value
            else:
               df[fvm.target] = ''

         # Remove source columns, which are in the mappings       
         if not includeSourceColumns:
            # Get mapped source columns 
            source_columns = [] 
            for cm in self.component_maps:
               source_columns += cm.sources
               
            df.drop(source_columns, axis=1, inplace=True)

         # Remove columns, which are not in the dimension list of the target dataflow
         # such as attributes and measures
         if not includeAttributesMeasures:
            dsd = self.get_dsd_by_urn(self.structure_map.target)
            columns_to_drop = [column for column in df.columns if (not dsd.isdimension(column) and not column.startswith("_S_"))]
            df.drop(columns_to_drop, axis=1, inplace=True)

         if dropInvalid:
            df = df[df.ne(INVALID).all(axis=1)]   

         return deepcopy(df)


# ---------------The code from here is used for illustration of the class and could be translated into test cases----------------
if __name__ == "__main__":      
   mf = Path('tests/Structures-withRegEx2.xml')
   sf = Path('tests/SourcePartialKeys.csv')
   mu = SDMXMappingUtility.initialise_with_file(mf, sf)
   df = mu.generate_mappings_partial_keys(includeSourceColumns=False, includeAttributesMeasures=False, nulledFixedTargets=True, writeTargetStructInfo=False, dropInvalid=False)
   df.to_csv(Path('tests/TargetPartialKeys.csv'), index=False)
