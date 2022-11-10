import sparknlp
 
spark = sparknlp.start() # for GPU training >> sparknlp.start(gpu = True) # for Spark 2.3 =>> sparknlp.start(spark23 = True)
import pyspark.sql.functions as F
from sparknlp.annotator import *
from sparknlp.base import *

from sparknlp.common import *

import sparknlp
from sparknlp.pretrained import PretrainedPipeline
 
print("Spark NLP version", sparknlp.version())
 
print("Apache Spark version:", spark.version)

from sparknlp.base import LightPipeline

document_assembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document')

tokenizer = Tokenizer() \
    .setInputCols(['document']) \
    .setOutputCol('token')

embeddings = WordEmbeddingsModel.pretrained('glove_100d')\
          .setInputCols(["document", "token"])\
          .setOutputCol("embeddings")

loaded_ner_model = NerDLModel.load("outputs/ner_wiki_glove100d_en")\
   .setInputCols(["sentence", "token", "embeddings"])\
   .setOutputCol("ner")

ner_converter = NerConverter() \
    .setInputCols(['document', 'token', 'ner']) \
    .setOutputCol('ner_chunk')

load_ner_pipeline = Pipeline(stages=[
      document_assembler,
      tokenizer,
      embeddings,
      loaded_ner_model,
      ner_converter
 ])




text = input("Enter Testing Text\n")
prediction_data = spark.createDataFrame([[text]]).toDF("text")
prediction_model = load_ner_pipeline.fit(prediction_data)
light = LightPipeline(prediction_model)
while(text != "exit"):
    results = light.annotate(text)
    print(results['ner'])
    text = input("Enter New Text\n")