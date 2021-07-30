"""
Sentiment Analysis Tool - BERT

(Bidirectional Encoder Representations from Transformers)

This is the more advanced model (based on a Neural Network), and it
predicts the sentiment based on the semantic usage of the word. BERT
usually requires extensive training data before use, (for perspective,
training a new model from scratch takes 4+ days of constant GPU usage),
but this library has a pre-trained model (however, it still requires
some shorter "fine-tuning" before use)

Base code source:
    https://towardsdatascience.com/sentiment-analysis-in-10-minutes-with-bert-and-hugging-face-294e8a04b671

Setup:
    pip install --upgrade pip
    pip install pandas
    pip install tensorflow
    pip install transformers
"""
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model.summary()

# This should show the main BERT model, a dropout layer to prevent
# overfitting, and finally a dense layer for classification task


'''
### Get IMDB Dataset for input sequences ###

IMDB Reviews Dataset is a large movie review dataset collected and
prepared by Andrew L. Maas from the popular movie rating service, IMDB.
The IMDB Reviews dataset is used for binary sentiment classification,
whether a review is positive or negative. It contains 25,000 movie reviews
for training and 25,000 for testing. All these 50,000 reviews are labeled
data that may be used for supervised deep learning. Besides, there is an
additional 50,000 unlabeled reviews that we will not use in this case study.
In this case study, we will only use the training dataset.
'''
import tensorflow as tf
import pandas as pd

"""
### Start by Getting Data from the Stanford Repo ###
URL = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"

dataset = tf.keras.utils.get_file(fname="aclImdb_v1.tar.gz", 
                                  origin=URL,
                                  untar=True,
                                  cache_dir='.',
                                  cache_subdir='')


### Remove Unlabeled Reviews ###

# To remove the unlabeled reviews, we need the following operations.
# The comments below explain each operation:

import os
import shutil # offers many high-level operations on files and collections of files.

# Create main directory path ("/aclImdb")
main_dir = os.path.join(os.path.dirname(dataset), 'aclImdb')

# Create sub directory path ("/aclImdb/train")
train_dir = os.path.join(main_dir, 'train')

# Remove unsup folder since this is a supervised learning task
remove_dir = os.path.join(train_dir, 'unsup')
shutil.rmtree(remove_dir)

# View the final train folder
print(os.listdir(train_dir))


### Train and Test Split ###

# Now that we have our data cleaned and prepared, we can create
# text_dataset_from_directory with the following lines. The author
# selected a very large batch size, because they wanted to process
# the entire data in a single batch (like I do)
train_dir = os.path.join(main_dir, 'train')
# Remove unsup folder since this is a supervised learning task

# We create a training dataset and a validation 
# dataset from our "aclImdb/train" directory with a 80/20 split.
train = tf.keras.preprocessing.text_dataset_from_directory(
    'aclImdb/train', batch_size=30000, validation_split=0.2, 
    subset='training', seed=123)

test = tf.keras.preprocessing.text_dataset_from_directory(
    'aclImdb/train', batch_size=30000, validation_split=0.2, 
    subset='validation', seed=123)


### Convert to Pandas to View and Process ###

# Now we have our basic train and test datasets, and will prepare
# them for our BERT model. To make it more comprehensible, we're
# creating a pandas dataframe from our TensorFlow dataset object.
# The following code converts our train Dataset object to train
# pandas dataframe:
for i in train.take(1):
    train_feat = i[0].numpy()
    train_lab = i[1].numpy()

train = pd.DataFrame([train_feat, train_lab]).T
train.columns = ['DATA_COLUMN', 'LABEL_COLUMN']
train['DATA_COLUMN'] = train['DATA_COLUMN'].str.decode("utf-8")
train.head()

# Same thing here
for j in test.take(1):
    test_feat = j[0].numpy()
    test_lab = j[1].numpy()

test = pd.DataFrame([test_feat, test_lab]).T
test.columns = ['DATA_COLUMN', 'LABEL_COLUMN']
test['DATA_COLUMN'] = test['DATA_COLUMN'].str.decode("utf-8")
test.head()


### Creating Input Sequences ###

# We have two pandas Dataframe objects waiting for us to
# convert them into suitable objects for the BERT model. We will
# take advantage of the InputExample function that helps us to
# create sequences from our dataset. The InputExample function
# can be called as follows:
InputExample(guid=None,
             text_a = "Hello, world",
             text_b = None,
             label = 1)


# Now we will create two main functions: #

# 1. convert_data_to_examples:
#       This will accept our train and test datasets and convert
#       each row into an InputExample object.

# 2. convert_examples_to_tf_dataset:
#       This function will tokenize the InputExample objects,
#       then create the required input format with the tokenized
#       objects, finally, create an input dataset that we can
#       feed to the model.

def convert_data_to_examples(train, test, DATA_COLUMN, LABEL_COLUMN): 
    train_InputExamples = train.apply(lambda x: InputExample(guid=None, # Globally unique ID for bookkeeping, unused in this case
                                                            text_a = x[DATA_COLUMN], text_b = None,
                                                            label = x[LABEL_COLUMN]),
                                        axis = 1)
    #
    validation_InputExamples = test.apply(lambda x: InputExample(guid=None, # Globally unique ID for bookkeeping, unused in this case
                                                                text_a = x[DATA_COLUMN], text_b = None,
                                                                label = x[LABEL_COLUMN]),
                                        axis = 1)
    #
    return train_InputExamples, validation_InputExamples
    #
    train_InputExamples, validation_InputExamples = convert_data_to_examples(train, 
                                                                            test, 
                                                                           'DATA_COLUMN', 
                                                                           'LABEL_COLUMN')
# End of Function

def convert_examples_to_tf_dataset(examples, tokenizer, max_length=128):
    features = [] # -> will hold InputFeatures to be converted later

    for e in examples:
        # Documentation is really strong for this method, so please take a look at it
        input_dict = tokenizer.encode_plus(
            e.text_a,
            add_special_tokens=True,
            max_length=max_length, # truncates if len(s) > max_length
            return_token_type_ids=True,
            return_attention_mask=True,
            pad_to_max_length=True, # pads to the right by default # CHECK THIS for pad_to_max_length
            truncation=True
        )
        
        input_ids, token_type_ids, attention_mask = (input_dict["input_ids"],
            input_dict["token_type_ids"], input_dict['attention_mask'])
        
        features.append(
            InputFeatures(
                input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, label=e.label
            )
        )
    # end of loop
    
    def gen():
        for f in features:
            yield (
                {
                    "input_ids": f.input_ids,
                    "attention_mask": f.attention_mask,
                    "token_type_ids": f.token_type_ids,
                },
                f.label,
            )
    # end of subfunction
    
    return tf.data.Dataset.from_generator(
        gen,
        ({"input_ids": tf.int32, "attention_mask": tf.int32, "token_type_ids": tf.int32}, tf.int64),
        (
            {
                "input_ids": tf.TensorShape([None]),
                "attention_mask": tf.TensorShape([None]),
                "token_type_ids": tf.TensorShape([None]),
            },
            tf.TensorShape([]),
        ),
    )
# End of Function

DATA_COLUMN = 'DATA_COLUMN'
LABEL_COLUMN = 'LABEL_COLUMN'

# We can call the functions we created above with the following lines:
train_InputExamples, validation_InputExamples = convert_data_to_examples(train, test, DATA_COLUMN, LABEL_COLUMN)

train_data = convert_examples_to_tf_dataset(list(train_InputExamples), tokenizer)
train_data = train_data.shuffle(100).batch(32).repeat(2)

validation_data = convert_examples_to_tf_dataset(list(validation_InputExamples), tokenizer)
validation_data = validation_data.batch(32)

# Our dataset containing processed input sequences are ready to
# be fed to the model.


### Configuring the BERT model and Fine-tuning ###

# We will use Adam as our optimizer, CategoricalCrossentropy as our
# loss function, and SparseCategoricalAccuracy as our accuracy metric.
# Fine-tuning the model for 2 epochs will give us around 95% accuracy,
# which is great.
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0), 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])

model.fit(train_data, epochs=2, validation_data=validation_data)


# Training the model might take a while, so ensure you enabled the
# GPU acceleration from the Notebook Settings. After our training
# is completed, we can move onto making sentiment predictions.


### Making Predictions ###

# I created a list of two reviews I created. The first one is a
# positive review, while the second one is clearly negative.
pred_sentences = ['This was an awesome movie. I watch it twice my time watching this beautiful movie if I have known it was this good',
                  'One of the worst movies of all time. I cannot believe I wasted two hours of my life for this movie']

# We need to tokenize our reviews with our pre-trained BERT tokenizer.
# We will then feed these tokenized sequences to our model and run a
# final softmax layer to get the predictions. We can then use the
# argmax function to determine whether our sentiment prediction for
# the review is positive or negative. Finally, we will print out the
# results with a simple for loop. The following lines do all of these
# said operations:

tf_batch = tokenizer(pred_sentences, max_length=128, padding=True, truncation=True, return_tensors='tf')
tf_outputs = model(tf_batch)
tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
labels = ['Negative','Positive']
label = tf.argmax(tf_predictions, axis=1)
label = label.numpy()
for i in range(len(pred_sentences)):
    print(pred_sentences[i], ": \n", labels[label[i]])

# Also, with the code above, you can predict as many reviews as possible.


### Congratulations ###

# You have successfully built a transformers network with a pre-trained
# BERT model and achieved ~95% accuracy on the sentiment analysis of the
# IMDB reviews dataset! If you are curious about saving your model, I
# would like to direct you to the Keras Documentation. After all, to
# efficiently use an API, one must learn how to read and use the
# documentation.
"""
