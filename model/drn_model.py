import time
import keras
import tensorflow as tf
from keras.layers import Input, Dense, Embedding, Flatten, Concatenate
from keras.models import Model


def drn(n_features, max_id, emb_size_id, max_lu, emb_size_lu, n_nodes=512):
    features_in = Input(shape=(n_features,))
    
    # embedding of the station IDs
    id_in = Input(shape=(1,))
    emb = Embedding(max_id + 1, emb_size_id)(id_in)
    emb = Flatten()(emb)

    # embedding of the land usage
    lu_in = Input(shape=(1,))
    emb_lu = Embedding(max_lu + 1, emb_size_lu)(lu_in)
    emb_lu = Flatten()(emb_lu)

    x = Concatenate()([features_in, emb, emb_lu])
    x = Dense(n_nodes, activation='relu')(x)
    x = Dense(2, activation='linear')(x)

    return Model(inputs=[features_in, id_in, lu_in], outputs=x)


def drn_pp(model, data, loss_fn, early_stopping, lr=0.005, n_epoch=50, bs=4096, VERBOSE=0):  
    train_features = data[0]
    train_IDs = data[1]
    train_lu = data[2]
    train_targets = data[3]
    test_features = data[4]
    test_IDs = data[5]
    test_lu = data[6]
    test_targets = data[7]
    
    tf.compat.v1.reset_default_graph()
    keras.backend.clear_session()
    
    start_train = time.time()
    opt = keras.optimizers.Adam(learning_rate=lr) # or lr=0.002
    model.compile(optimizer=opt, loss=loss_fn)
    model.fit([train_features, train_IDs, train_lu], train_targets, epochs=n_epoch, batch_size=bs, callbacks=[early_stopping], verbose=VERBOSE)
    training_time = time.time() - start_train
    
    start_predict = time.time()
    reprediction = model.predict([train_features, train_IDs, train_lu], batch_size=bs, verbose=VERBOSE)
    prediction = model.predict([test_features, test_IDs, test_lu], batch_size=bs, verbose=VERBOSE)
    predicting_time = time.time() - start_predict
    
    training_score = model.evaluate([train_features, train_IDs, train_lu], train_targets, batch_size=bs, verbose=VERBOSE)
    test_score = model.evaluate([test_features, test_IDs, test_lu], test_targets, batch_size=bs, verbose=VERBOSE)
    
    return training_time, predicting_time, reprediction, prediction, training_score, test_score
    
