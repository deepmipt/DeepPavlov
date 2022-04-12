Features
========

.. contents:: :local:

Models
------

NER model :doc:`[docs] </features/models/ner>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Named Entity Recognition task in DeepPavlov is solved with BERT-based model.
The models predict tags (in BIO format) for tokens in input.

BERT-based model is described in  `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
<https://arxiv.org/abs/1810.04805>`__.

+---------------------------------------------------------+-------+--------------------------------------------------------------------------------------------+-------------+
| Dataset                                                 | Lang  | Model                                                                                      |   Test F1   |
+=========================================================+=======+============================================================================================+=============+
| Persons-1000 dataset with additional LOC and ORG markup | Ru    | :config:`ner_rus_bert.json <ner/ner_rus_bert.json>`                                        |    97.9     |
+                                                         +       +--------------------------------------------------------------------------------------------+-------------+
| (Collection 3)                                          |       | :config:`ner_rus_convers_distilrubert_2L.json  <ner/ner_rus_convers_distilrubert_2L.json>` |  88.4 ± 0.5 |
+                                                         +       +--------------------------------------------------------------------------------------------+-------------+
|                                                         |       | :config:`ner_rus_convers_distilrubert_6L.json  <ner/ner_rus_convers_distilrubert_6L.json>` |  93.3 ± 0.3 |
+---------------------------------------------------------+-------+--------------------------------------------------------------------------------------------+-------------+
| Ontonotes                                               | Multi | :config:`ner_ontonotes_bert_mult.json <ner/ner_ontonotes_bert_mult.json>`                  |    88.9     |
+                                                         +-------+--------------------------------------------------------------------------------------------+-------------+
|                                                         | En    | :config:`ner_ontonotes_bert.json <ner/ner_ontonotes_bert.json>`                            |    89.2     |
+---------------------------------------------------------+       +--------------------------------------------------------------------------------------------+-------------+
| ConLL-2003                                              |       | :config:`ner_conll2003_bert.json <ner/ner_conll2003_bert.json>`                            |    91.7     |
+---------------------------------------------------------+-------+--------------------------------------------------------------------------------------------+-------------+

Classification model :doc:`[docs] </features/models/classifiers>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model for classification tasks (intents, sentiment, etc) on word-level. Shallow-and-wide CNN, Deep CNN, BiLSTM,
BiLSTM with self-attention and other models are presented. The model also allows multilabel classification of texts.
Several pre-trained models are available and presented in Table below.


+------------------+---------------------+------+----------------------------------------------------------------------------------------------------+-------------+------------------+-----------------+-----------+
| Task             | Dataset             | Lang | Model                                                                                              | Metric      | Valid            | Test            | Downloads |
+==================+=====================+======+====================================================================================================+=============+==================+=================+===========+
| Insult detection | `Insults`_          | En   | :config:`English BERT<classifiers/insults_kaggle_bert.json>`                                       | ROC-AUC     | 0.9327           | 0.8602          |  1.1 Gb   |
+------------------+---------------------+      +----------------------------------------------------------------------------------------------------+-------------+------------------+-----------------+-----------+
| Sentiment        | `SST`_              |      | :config:`5-classes SST on conversational BERT <classifiers/sentiment_sst_conv_bert.json>`          | Accuracy    | 0.6456           | 0.6715          |  400 Mb   |
+------------------+---------------------+------+----------------------------------------------------------------------------------------------------+-------------+------------------+-----------------+-----------+
| Sentiment        | `Twitter mokoron`_  | Ru   | :config:`RuWiki+Lenta emb w/o preprocessing <classifiers/sentiment_twitter.json>`                  |             | 0.9965           | 0.9961          |  6.2 Gb   |
+                  +---------------------+      +----------------------------------------------------------------------------------------------------+-------------+------------------+-----------------+-----------+
|                  | `RuSentiment`_      |      | :config:`Multi-language BERT <classifiers/rusentiment_bert.json>`                                  | F1-weighted | 0.6809           | 0.7193          |  1900 Mb  |
+                  +                     +      +----------------------------------------------------------------------------------------------------+             +------------------+-----------------+-----------+
|                  |                     |      | :config:`Conversational RuBERT <classifiers/rusentiment_convers_bert.json>`                        |             | 0.7548           | 0.7742          |  657 Mb   |
+                  +                     +      +----------------------------------------------------------------------------------------------------+             +------------------+-----------------+-----------+
|                  |                     |      | :config:`Conversational DistilRuBERT-tiny <classifiers/rusentiment_convers_distilrubert_2L.json>`  |             |  0.703 ± 0.0031  | 0.7348 ± 0.0028 |  690 Mb   |
+                  +                     +      +----------------------------------------------------------------------------------------------------+             +------------------+-----------------+-----------+
|                  |                     |      | :config:`Conversational DistilRuBERT-base <classifiers/rusentiment_convers_distilrubert_6L.json>`  |             |  0.7376 ± 0.0045 | 0.7645 ± 0.035  |  1.0 Gb   |
+------------------+---------------------+------+----------------------------------------------------------------------------------------------------+-------------+------------------+-----------------+-----------+

.. _`DSTC 2`: http://camdial.org/~mh521/dstc/
.. _`SNIPS-2017`: https://github.com/snipsco/nlu-benchmark/tree/master/2017-06-custom-intent-engines
.. _`Insults`: https://www.kaggle.com/c/detecting-insults-in-social-commentary
.. _`AG News`: https://www.di.unipi.it/~gulli/AG_corpus_of_news_articles.html
.. _`Twitter mokoron`: http://study.mokoron.com/
.. _`RuSentiment`: http://text-machine.cs.uml.edu/projects/rusentiment/
.. _`Yahoo-L31`: https://webscope.sandbox.yahoo.com/catalog.php?datatype=l
.. _`Yahoo-L6`: https://webscope.sandbox.yahoo.com/catalog.php?datatype=l
.. _`SST`: https://nlp.stanford.edu/sentiment/index.html

As no one had published intent recognition for DSTC-2 data, the
comparison of the presented model is given on **SNIPS** dataset. The
evaluation of model scores was conducted in the same way as in [3]_ to
compare with the results from the report of the authors of the dataset.
The results were achieved with tuning of parameters and embeddings
trained on Reddit dataset.

+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| Model                  | AddToPlaylist   | BookRestaurant   | GetWheather   | PlayMusic    | RateBook     | SearchCreativeWork   | SearchScreeningEvent   |
+========================+=================+==================+===============+==============+==============+======================+========================+
| api.ai                 | 0.9931          | 0.9949           | 0.9935        | 0.9811       | 0.9992       | 0.9659               | 0.9801                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| ibm.watson             | 0.9931          | 0.9950           | 0.9950        | 0.9822       | 0.9996       | 0.9643               | 0.9750                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| microsoft.luis         | 0.9943          | 0.9935           | 0.9925        | 0.9815       | 0.9988       | 0.9620               | 0.9749                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| wit.ai                 | 0.9877          | 0.9913           | 0.9921        | 0.9766       | 0.9977       | 0.9458               | 0.9673                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| snips.ai               | 0.9873          | 0.9921           | 0.9939        | 0.9729       | 0.9985       | 0.9455               | 0.9613                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| recast.ai              | 0.9894          | 0.9943           | 0.9910        | 0.9660       | 0.9981       | 0.9424               | 0.9539                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| amazon.lex             | 0.9930          | 0.9862           | 0.9825        | 0.9709       | 0.9981       | 0.9427               | 0.9581                 |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+
| Shallow-and-wide CNN   | **0.9956**      | **0.9973**       | **0.9968**    | **0.9871**   | **0.9998**   | **0.9752**           | **0.9854**             |
+------------------------+-----------------+------------------+---------------+--------------+--------------+----------------------+------------------------+

.. [3] https://www.slideshare.net/KonstantinSavenkov/nlu-intent-detection-benchmark-by-intento-august-2017


Automatic spelling correction model :doc:`[docs] </features/models/spelling_correction>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipelines that use candidates search in a static dictionary and an ARPA language model to correct spelling errors.

.. note::

    About 4.4 GB on disc required for the Russian language model and about 7 GB for the English one.

Comparison on the `test set <http://www.dialog-21.ru/media/3838/test_sample_testset.txt>`__ for the `SpellRuEval
competition <http://www.dialog-21.ru/en/evaluation/2016/spelling_correction/>`__
on Automatic Spelling Correction for Russian:

+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+
| Correction method                                                                       | Precision | Recall | F-measure | Speed (sentences/s) |
+=========================================================================================+===========+========+===========+=====================+
| Yandex.Speller                                                                          | 83.09     | 59.86  | 69.59     | 5.                  |
+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+
| :config:`Damerau Levenshtein 1 + lm<spelling_correction/levenshtein_corrector_ru.json>` | 53.26     | 53.74  | 53.50     | 29.3                |
+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+
| Hunspell + lm                                                                           | 41.03     | 48.89  | 44.61     | 2.1                 |
+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+
| JamSpell                                                                                | 44.57     | 35.69  | 39.64     | 136.2               |
+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+
| Hunspell                                                                                | 30.30     | 34.02  | 32.06     | 20.3                |
+-----------------------------------------------------------------------------------------+-----------+--------+-----------+---------------------+



Ranking model :doc:`[docs] </features/models/neural_ranking>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Available pre-trained models for paraphrase identification:

.. table::
   :widths: auto

   +------------------------+------------------------------------------------------------------------------------------------------+----------------+-----------------+------------+------------+----------------+-----------------+-----------+
   |    Dataset             | Model config                                                                                         | Val (accuracy) | Test (accuracy) | Val (F1)   | Test (F1)  | Val (log_loss) | Test (log_loss) | Downloads |
   +========================+======================================================================================================+================+=================+============+============+================+=================+===========+
   | `paraphraser.ru`_      | :config:`paraphrase_bert_multilingual <classifiers/paraphraser_bert.json>`                           |   87.4         |   79.3          |   90.2     |  83.4      |   --           |   --            | 1330M     |
   +------------------------+------------------------------------------------------------------------------------------------------+----------------+-----------------+------------+------------+----------------+-----------------+-----------+
   | `paraphraser.ru`_      | :config:`paraphrase_rubert <classifiers/paraphraser_rubert.json>`                                    |   90.2         |   84.9          |   92.3     |  87.9      |   --           |   --            | 1325M     |
   +------------------------+------------------------------------------------------------------------------------------------------+----------------+-----------------+------------+------------+----------------+-----------------+-----------+
   | `paraphraser.ru`_      | :config:`paraphraser_convers_distilrubert_2L <classifiers/paraphraser_convers_distilrubert_2L.json>` |  76.1 ± 0.2    |  64.5 ± 0.5     | 81.8 ± 0.2 | 73.9 ± 0.8 |   --           |   --            | 618M      |
   +------------------------+------------------------------------------------------------------------------------------------------+----------------+-----------------+------------+------------+----------------+-----------------+-----------+
   | `paraphraser.ru`_      | :config:`paraphraser_convers_distilrubert_6L <classifiers/paraphraser_convers_distilrubert_6L.json>` |  86.5 ± 0.5    |  78.9 ± 0.4     | 89.6 ± 0.3 | 83.2 ± 0.5 |   --           |   --            | 930M      |
   +------------------------+------------------------------------------------------------------------------------------------------+----------------+-----------------+------------+------------+----------------+-----------------+-----------+

.. _`paraphraser.ru`: https://paraphraser.ru/


References:

* Yu Wu, Wei Wu, Ming Zhou, and Zhoujun Li. 2017. Sequential match network: A new architecture for multi-turn response selection in retrieval-based chatbots. In ACL, pages 372–381. https://www.aclweb.org/anthology/P17-1046

* Xiangyang Zhou, Lu Li, Daxiang Dong, Yi Liu, Ying Chen, Wayne Xin Zhao, Dianhai Yu and Hua Wu. 2018. Multi-Turn Response Selection for Chatbots with Deep Attention Matching Network. Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1118-1127, ACL. http://aclweb.org/anthology/P18-1103

* Chongyang Tao, Wei Wu, Can Xu, Wenpeng Hu, Dongyan Zhao, and Rui Yan. Multi-Representation Fusion Network for Multi-turn Response Selection in Retrieval-based Chatbots. In WSDM'19. https://dl.acm.org/citation.cfm?id=3290985

* Gu, Jia-Chen & Ling, Zhen-Hua & Liu, Quan. (2019). Interactive Matching Network for Multi-Turn Response Selection in Retrieval-Based Chatbots. https://arxiv.org/abs/1901.01824



TF-IDF Ranker model :doc:`[docs] </features/models/tfidf_ranking>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on `Reading Wikipedia to Answer Open-Domain Questions <https://github.com/facebookresearch/DrQA/>`__. The model solves the task of document retrieval for a given query.

+---------------+-------------------------------------------------------------------+----------------------+-----------------+-----------+
| Dataset       | Model                                                             |  Wiki dump           |  Recall@5       | Downloads |
+===============+========================================================+==========+======================+=================+===========+
| `SQuAD-v1.1`_ | :config:`doc_retrieval <doc_retrieval/en_ranker_tfidf_wiki.json>` |  enwiki (2018-02-11) |   75.6          | 33 GB     |
+---------------+-------------------------------------------------+-----------------+----------------------+-----------------+-----------+


Question Answering model :doc:`[docs] </features/models/squad>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models in this section solve the task of looking for an answer on a
question in a given context (`SQuAD <https://rajpurkar.github.io/SQuAD-explorer/>`__ task format).
There are two models for this task in DeepPavlov: BERT-based and R-Net. Both models predict answer start and end
position in a given context.

BERT-based model is described in  `BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
<https://arxiv.org/abs/1810.04805>`__.

R-Net model is based on `R-NET: Machine Reading Comprehension with Self-matching Networks
<https://www.microsoft.com/en-us/research/publication/mcr/>`__.

+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
|    Dataset     | Model config                                                                                | lang  |    EM (dev)    |    F-1 (dev)    |    Downloads    |
+================+=============================================================================================+=======+================+=================+=================+
| `SQuAD-v1.1`_  | :config:`DeepPavlov BERT <squad/squad_bert.json>`                                           |  en   |     80.88      |     88.49       |     806Mb       |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SQuAD-v1.1`_  | :config:`DeepPavlov BERT on PyTorch <squad/squad_torch_bert.json>`                          |  en   |    80.79       |     88.30       |     1.1 Gb      |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SQuAD-v1.1`_  | :config:`DeepPavlov R-Net <squad/squad.json>`                                               |  en   |     71.49      |     80.34       |     ~2.5Gb      |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SDSJ Task B`_ | :config:`DeepPavlov RuBERT <squad/squad_ru_rubert_infer.json>`                              |  ru   |  66.30 ± 0.24  |   84.60 ± 0.11  |     1325Mb      |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SDSJ Task B`_ | :config:`DeepPavlov multilingual BERT <squad/squad_ru_bert_infer.json>`                     |  ru   |     66.24      |     84.71       |     1.6 Gb      |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SDSJ Task B`_ | :config:`DeepPavlov R-Net <squad/squad_ru.json>`                                            |  ru   |     60.62      |     80.04       |     ~5Gb        |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SDSJ Task B`_ | :config:`DeepPavlov DistilRuBERT-tiny <squad/squad_ru_convers_distilrubert_2L_infer.json>`  |  ru   |  44.2 ± 0.46   |  65.1 ± 0.36    |     867Mb       |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+
| `SDSJ Task B`_ | :config:`DeepPavlov DistilRuBERT-base <squad/squad_ru_convers_distilrubert_6L_infer.json>`  |  ru   |  61.23 ± 0.42  |  80.36 ± 0.28   |     1.18Gb      |
+----------------+---------------------------------------------------------------------------------------------+-------+----------------+-----------------+-----------------+

In the case when answer is not necessary present in given context we have :config:`squad_noans <squad/multi_squad_noans.json>`
model. This model outputs empty string in case if there is no answer in context.


Morphological tagging model :doc:`[docs] </features/models/morphotagger>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a BERT-based model for Russian language.
Model takes as input tokenized sentences and outputs the corresponding
sequence of morphological labels in `UD format <http://universaldependencies.org/format.html>`__.

.. table::
    :widths: auto

    +----------------------+--------------------------------------------------------------------------------------------------------------+---------------+----------------+--------------------+
    |    Dataset           | Model                                                                                                        | Word accuracy | Sent. accuracy | Download size (MB) |
    +======================+==============================================================================================================+===============+================+====================+
    | `UD2.3`_ (Russian)   | `UD Pipe 2.3`_ (Straka et al., 2017)                                                                         |    93.5       |                |                    |
    |                      +--------------------------------------------------------------------------------------------------------------+---------------+----------------+--------------------+
    |                      | `UD Pipe Future`_ (Straka et al., 2018)                                                                      |    96.90      |                |                    |
    |                      +--------------------------------------------------------------------------------------------------------------+---------------+----------------+--------------------+
    |                      | :config:`BERT-based model <morpho_tagger/BERT/morpho_ru_syntagrus_bert.json>`                                |    97.83      |     72.02      |       661          |
    +----------------------+--------------------------------------------------------------------------------------------------------------+---------------+----------------+--------------------+

.. _`UD2.3`: http://hdl.handle.net/11234/1-2895
.. _`UD Pipe 2.3`: http://ufal.mff.cuni.cz/udpipe
.. _`UD Pipe Future`: https://github.com/CoNLL-UD-2018/UDPipe-Future

Syntactic parsing model :doc:`[docs] </features/models/syntaxparser>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a biaffine model for syntactic parsing based on RuBERT.
It achieves the highest known labeled attachments score of 93.7%
on ``ru_syntagrus`` Russian corpus (version UD 2.3).

.. table::
    :widths: auto

    +-------------------------+-------------------------------------------------------------------------------------------+---------+----------+
    |   Dataset               |  Model                                                                                    | UAS     | LAS      |
    +=========================+===========================================================================================+=========+==========+
    | `UD2.3`_ (Russian)      | `UD Pipe 2.3`_ (Straka et al., 2017)                                                      | 90.3    | 89.0     |
    |                         +-------------------------------------------------------------------------------------------+---------+----------+
    |                         | `UD Pipe Future`_ (Straka, 2018)                                                          | 93.0    | 91.5     |
    |                         +-------------------------------------------------------------------------------------------+---------+----------+
    |                         | `UDify (multilingual BERT)`_ (Kondratyuk, 2018)                                           | 94.8    | 93.1     |
    |                         +-------------------------------------------------------------------------------------------+---------+----------+
    |                         | :config:`our BERT model <syntax/syntax_ru_syntagrus_bert.json>`                           | 95.2    | 93.7     |
    +-------------------------+-------------------------------------------------------------------------------------------+---------+----------+

.. _`UD2.3`: http://hdl.handle.net/11234/1-2895
.. _`UD Pipe 2.3`: http://ufal.mff.cuni.cz/udpipe
.. _`UD Pipe Future`: https://github.com/CoNLL-UD-2018/UDPipe-Future
.. _`UDify (multilingual BERT)`: https://github.com/hyperparticle/udify

Frequently Asked Questions (FAQ) model :doc:`[docs] </features/skills/faq>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of pipelines for FAQ task: classifying incoming question into set of known questions and return prepared answer.
You can build different pipelines based on: tf-idf, weighted fasttext, cosine similarity, logistic regression.


Skills
------

Goal-oriented bot :doc:`[docs] </features/skills/go_bot>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on Hybrid Code Networks (HCNs) architecture from `Jason D. Williams, Kavosh Asadi,
Geoffrey Zweig, Hybrid Code Networks: practical and efficient end-to-end dialog control
with supervised and reinforcement learning – 2017 <https://arxiv.org/abs/1702.03274>`__.
It allows to predict responses in a goal-oriented dialog. The model is
customizable: embeddings, slot filler and intent classifier can be switched on and off on demand.

ODQA :doc:`[docs] </features/skills/odqa>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An open domain question answering skill. The skill accepts free-form questions about the world and outputs an answer
based on its Wikipedia knowledge.


+----------------+--------------------------------------------------------------------+-----------------------+--------+-----------+
| Dataset        | Model config                                                       |  Wiki dump            |   F1   | Downloads |
+================+====================================================================+=======================+========+===========+
| `SQuAD-v1.1`_  | :config:`ODQA <odqa/en_odqa_infer_wiki.json>`                      | enwiki (2018-02-11)   |  35.89 | 9.7Gb     |
+----------------+--------------------------------------------------------------------+-----------------------+--------+-----------+
| `SDSJ Task B`_ | :config:`ODQA <odqa/ru_odqa_infer_wiki.json>`                      | ruwiki (2018-04-01)   |  28.56 | 7.7Gb     |
+----------------+--------------------------------------------------------------------+-----------------------+--------+-----------+
| `SDSJ Task B`_ | :config:`ODQA with RuBERT <odqa/ru_odqa_infer_wiki_rubert.json>`   | ruwiki (2018-04-01)   |  37.83 | 4.3Gb     |
+----------------+--------------------------------------------------------------------+-----------------------+--------+-----------+


AutoML
--------------------

Hyperparameters optimization :doc:`[docs] </features/hypersearch>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hyperparameters optimization by cross-validation for DeepPavlov models
that requires only some small changes in a config file.


Embeddings
----------

Pre-trained embeddings :doc:`[docs] </features/pretrained_vectors>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Word vectors for the Russian language trained on joint `Russian Wikipedia <https://ru.wikipedia.org/>`__ and `Lenta.ru
<https://lenta.ru/>`__ corpora.


Examples of some models
---------------------------

-  Run insults detection model with console interface:

   .. code-block:: bash

      python -m deeppavlov interact insults_kaggle_bert -d

-  Run insults detection model with REST API:

   .. code-block:: bash

      python -m deeppavlov riseapi insults_kaggle_bert -d

-  Predict whether it is an insult on every line in a file:

   .. code-block:: bash

      python -m deeppavlov predict insults_kaggle_bert -d --batch-size 15 < /data/in.txt > /data/out.txt


.. _`SQuAD-v1.1`: https://arxiv.org/abs/1606.05250
.. _`SDSJ Task B`: https://arxiv.org/abs/1912.09723
