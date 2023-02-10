# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.


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

from flask import Flask
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


use = UniversalSentenceEncoder.pretrained()\
 .setInputCols(["document"])\
 .setOutputCol("sentence_embeddings")
# the classes/labels/categories are in category column
loaded_text_model = ClassifierDLModel.load("Text_Classification")\
  .setInputCols(["sentence_embeddings"])\
  .setOutputCol("class")

load_ner_pipeline = Pipeline(stages=[
      document_assembler,
      tokenizer,
      embeddings,
      loaded_ner_model,
      ner_converter,
      use,
      loaded_text_model
 ])


    
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
@app.route('/NLP/<txt>')
def NLP(txt):

    text = txt
    prediction_data = spark.createDataFrame([[text]]).toDF("text")
    prediction_model = load_ner_pipeline.fit(prediction_data)
    light = LightPipeline(prediction_model)
    results = light.annotate(text)
    #results
    out = ""
    for i in results['ner']:
        out = out+i+" "
    for i in results['class']:
        out = out+":"+i
    return out
@app.route('/text/<txt>')
def text(txt):

    text = txt
    prediction_data = spark.createDataFrame([[text]]).toDF("text")
    prediction_model = load_ner_pipeline.fit(prediction_data)
    light = LightPipeline(prediction_model)
    results = light.annotate(text)
    #results
    out = ""
    for i in results['class']:
        out = out+i+";"
    for i in range(len(results['ner'])):
        store_value_ner=results['ner'].pop()
        store_value_token=results['token'].pop()
        if(store_value_ner!="0"):
            out = out+store_value_ner+":"+store_value_token+" "

    return out

    
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0")
