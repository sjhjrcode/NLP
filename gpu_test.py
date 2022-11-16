
import sparknlp
 
spark = sparknlp.start(gpu = True) # for GPU training >> sparknlp.start(gpu = True) # for Spark 2.3 =>> sparknlp.start(spark23 = True)
import pyspark.sql.functions as F
from sparknlp.annotator import *
from sparknlp.base import *

from sparknlp.common import *

import sparknlp
from sparknlp.pretrained import PretrainedPipeline
 
print("Spark NLP version", sparknlp.version())
 
print("Apache Spark version:", spark.version)
