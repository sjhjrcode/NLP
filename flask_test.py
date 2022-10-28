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
    prediction_model = custom_ner_pipeline.fit(prediction_data)
    light = LightPipeline(prediction_model)
    results = light.annotate(text)
    #results
    out = ""
    for i in results['ner']:
        out = out+i+" "
    return out

    
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0")
