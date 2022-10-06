#!wget http://setup.johnsnowlabs.com/colab.sh -O - | bash
import sparknlp
spark = sparknlp.start()

print("Spark NLP version: {}".format(sparknlp.version()))
print("Apache Spark version: {}".format(spark.version))
from sparknlp.pretrained import PretrainedPipeline 
pipeline = PretrainedPipeline('recognize_entities_dl', 'en')
result = pipeline.annotate('President Biden represented Delaware for 36 years in the U.S. Senate before becoming the 47th Vice President of the United States.') 
print(result['ner'])
print(result['entities'])
pipeline = PretrainedPipeline('onto_recognize_entities_bert_tiny', 'en')

result = pipeline.annotate("Johnson first entered politics when elected in 2001 as a member of Parliament. He then served eight years as the mayor of London, from 2008 to 2016, before rejoining Parliament.")

print(result['ner'])
print(result['entities'])
pipeline = PretrainedPipeline('analyze_sentimentdl_glove_imdb', 'en')
result = pipeline.annotate("Harry Potter is a great movie.")
print(result['sentiment'])