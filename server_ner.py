

import sparknlp
 
spark = sparknlp.start() # for GPU training >> sparknlp.start(gpu = True) # for Spark 2.3 =>> sparknlp.start(spark23 = True)
import pyspark.sql.functions as F
from sparknlp.annotator import *
from sparknlp.base import *

from sparknlp.common import *

import sparknlp
from sparknlp.pretrained import PretrainedPipeline
from sparknlp.base import LightPipeline
print("Spark NLP version", sparknlp.version())
 
print("Apache Spark version:", spark.version)



def load_model():

    # You can use any word embeddings you want (Glove, Elmo, Bert, custom etc.)
    document_assembler = DocumentAssembler() \
        .setInputCol('text') \
        .setOutputCol('document')

    sentence = SentenceDetector()\
        .setInputCols(['document'])\
        .setOutputCol('sentence')

    tokenizer = Tokenizer() \
        .setInputCols(['document']) \
        .setOutputCol('token')

    bert = BertEmbeddings.pretrained('bert_base_cased', 'en')\
        .setInputCols(["sentence",'token'])\
        .setOutputCol("bert")\
        .setCaseSensitive(False)

    loaded_ner_model = NerDLModel.load("NER_bert_20200221")\
    .setInputCols(["sentence", "token", "bert"])\
    .setOutputCol("ner")


    ner_converter = NerConverter() \
        .setInputCols(['document', 'token', 'ner']) \
        .setOutputCol('ner_span')

    custom_ner_pipeline = Pipeline(stages=[
        document_assembler, 
        sentence,
        tokenizer,
        bert,
        loaded_ner_model,
        ner_converter
    ])
    return custom_ner_pipeline

def print_labels(text, custom_pipeline):
    prediction_data = spark.createDataFrame([[text]]).toDF("text")
    prediction_model = custom_pipeline.fit(prediction_data)
    light = LightPipeline(prediction_model)
    results = light.annotate(text)
    print(results)
    print(results['ner'])
    for i in results['ner']:
        print(i)
    #for j in results['entities']:
    #    print(j)

loaded_pipeline = load_model()
print_labels("where am I",loaded_pipeline)