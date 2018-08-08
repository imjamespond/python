from keras.models import load_model

# from test_lstm import decode_sequence

model = load_model('./lstm_seq2seq/s2s.h5')
# print(model.get_weights())
# print(model.layers)
# print(model.inputs)
# print(model.outputs)
model.summary()

def keys(f):
    return [key for key in f.keys()]

# import h5py
# with h5py.File('./lstm_seq2seq/s2s.h5', 'r') as f:
#   fkeys = keys(f)
#   print(fkeys)
#   print(keys(f['model_weights']))
#   print(keys(f['optimizer_weights']))