import os

# Define paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MUSHROOM_DATA_FILE = os.path.join(PROJECT_DIR, "mushroom", "agaricus-lepiota.data")
PARAMS_FILE = os.path.join(PROJECT_DIR, "parameters.pkl")
COLUMN_NAMES = [ 'poisonous','cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 
                           'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
                           'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
                           'stalk-surface-below-ring', 'stalk-color-above-ring',
                           'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
                           'ring-type','spore-print-color', 'population', 'habitat']
    
POSSIBLE_VALUES=[['e','p'],
    ['b','c','x','f','k','s'],
    ['f','g','y','s'],
    ['n','b','c','g','r'],
    ['t','f'],
    ['a','l','c','y','f','m','n','p','s'],
    ['a','d','f','n'],
    ['c','w','d'],
    ['b','n'],
    ['k','n','b','h','g','r','o','p','u','e','w','y'],
    ['e','t'],
    ['b','c','u','e','z','r','?'],
    ['s','f','k','y'],
    ['s','f','k','y'],
    ['n','b','c','g','o','p','e','w','y'],
    ['n','b','c','g','o','p','e','w','y'],
    ['p','u'],
    ['n','o','y','w'],
    ['n','o','t'],
    ['c','e','f','l','n','p','s','z'],
    ['k','n','b','h','r','o','u','w','y'],
    ['a','c','n','s','v','y'],
    ['g','l','m','p','u','w','d']]

MEANINGS=['e=edible,p=poisonous','bell=b,conical=c,convex=x,flat=f, knobbed=k,sunken=s',
 'fibrous=f,grooves=g,scaly=y,smooth=s',
 'brown=n,buff=b,cinnamon=c,gray=g,green=r,pink=p,purple=u,red=e,white=w,yellow=y',
 'no=f,yes=t',
 'almond=a,anise=l,creosote=c,fishy=y,foul=f,musty=m,none=n,pungent=p,spicy=s',
 'attached=a,descending=d,free=f,notched=n',
 'close=c,crowded=w,distant=d',
 'broad=b,narrow=n',
 'black=k,brown=n,buff=b,chocolate=h,gray=g,green=r,orange=o,pink=p,purple=u,red=e,white=w,yellow=y',
 'enlarging=e,tapering=t',
 'bulbous=b,club=c,cup=u,equal=e,rhizomorphs=z,rooted=r,missing=?',
 'fibrous=f,scaly=k,silky=y,smooth=s',
 'fibrous=f,scaly=k,silky=y,smooth=s',
 'brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y',
 'brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y',
 'partial=p,universal=u',
 'brown=n,orange=o,white=w,yellow=y',
 'none=n,one=o,two=t',
 'cobwebby=c,evanescent=e,flarging=f,large=l,none=n,pendant=p,sheating=s,zone=z',
 'black=k,brown=n,buff=b,chocolate=h,gray=g,green=r,orange=o,pink=p,purple=u,red=e,white=w,yellow=y',
 'abundant=a,clustered=c,numerous=n,scattered=s,several=v,solitary=y', 
 'grasses=g,leaves=l,meadows=m,paths=p,urban=u,waste=w,woods=d']

# to use only for debug
def display_loaded_data_info(x, y, parameters):
    print("=" * 60)
    print("LOADED DATA INFORMATION")
    print("=" * 60)
    
    # Features (X) information
    print("\n📊 FEATURES (X):")
    print(f"  Shape: {x.shape}")
    print(f"  Columns: {list(x.columns)}")
    print(f"  Data types:\n{x.dtypes}")
    print(f"\n  First few rows:\n{x.head()}")
    print(f"\n  Statistical summary:\n{x.describe()}")
    
    # Target (y) information
    print("\n" + "=" * 60)
    print("🎯 TARGET (y):")
    print(f"  Shape: {y.shape}")
    print(f"  Column name: {y.name}")
    print(f"  Data type: {y.dtype}")
    print(f"  Unique values: {y.nunique()}")
    print(f"  Value counts:\n{y.value_counts()}")
    print(f"\n  First few values:\n{y.head()}")
    
    # Parameters information
    if parameters:
        print("\n" + "=" * 60)
        print("⚙️ PARAMETERS:")
        print(f"  Number of parameter groups: {len(parameters)}")
        print(f"  Parameter keys: {list(parameters.keys())}")
        for key, value in parameters.items():
            print(f"\n  {key}:")
            if isinstance(value, (list, tuple)):
                print(f"    Type: {type(value).__name__}")
                print(f"    Length: {len(value)}")
                print(f"    Content: {value[:5]}..." if len(value) > 5 else f"    Content: {value}")
            elif isinstance(value, dict):
                print(f"    Type: dict")
                print(f"    Keys: {list(value.keys())}")
            elif hasattr(value, 'shape'):
                print(f"    Type: {type(value).__name__}")
                print(f"    Shape: {value.shape}")
            else:
                print(f"    Type: {type(value).__name__}")
                print(f"    Value: {value}")
    
    print("\n" + "=" * 60)