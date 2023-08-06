import tensorflow as tf
from tensorflow import keras
import warnings

def transfer(
  num_classes, 
  img_width, 
  img_height, 
  train_ds, 
  val_ds,
  metr,
  opti,
  loss,
  trainingEpochs = 0,
  fineTune = False,
  fineTuneEpochs = 3,
  fineTuneLearningRate = 0.00001,
  baseModelList = ['VGG19', 'Xception', 'ResNet152V2', 'InceptionV3'],
  verbose = True
):
  
  if(not verbose):
    warnings.filterwarnings("ignore")

  modelsList = []
  [modelsList.append([createModel(num_classes, img_width, img_height, baseModel), 0]) for baseModel in baseModelList]

  for model in modelsList:
    print(model[0]._name)
    model[0].compile(
      optimizer = opti, 
      loss = loss, 
      metrics = metr
    )

  print('STARTING TRAINING')
  
  while(len(modelsList) > 1):
    print(len(modelsList), ' models remaining')
    for model in modelsList:

      print('EVALUATING: ', model[0]._name)
      
      hist = model[0].fit(
        train_ds,
        validation_data = val_ds,
        epochs = 1
      )

      model[1] = hist.history['val_accuracy']

    modelsList.sort(key = lambda x: x[1])
    for i in range(0, int(len(modelsList)/2)):
      print('erasing model ', modelsList[0][0]._name, 'with val accuracy ', modelsList[0][1])
      del modelsList[0]
  
  model = modelsList[0][0]
  print('CHOSEN MODEL: ', model._name)

  if(trainingEpochs > 0):
    model.compile(
        optimizer = opti, 
        loss = loss, 
        metrics = metr
      )
    
    hist = model.fit(
      train_ds,
      validation_data = val_ds,
      epochs = trainingEpochs
    )

  if(fineTune):
    print('STARTING FINETUNING')

    model.trainable = True

    opti = tf.keras.optimizers.RMSprop(momentum=0.1,learning_rate=fineTuneLearningRate) 

    model.compile(
      optimizer = opti, 
      loss = loss, 
      metrics = metr
    )

    model.fit(
      train_ds, 
      epochs = fineTuneEpochs, 
      validation_data = val_ds
    )

    model.summary()

  return model

def createModel(
    num_classes, 
    img_width, 
    img_height, 
    application, 
    dropout = 0.2
):
    base_model = None  
    match application:
        case 'VGG16':
            base_model = keras.applications.VGG16(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            ) 
        case 'VGG19':
            base_model = keras.applications.VGG19(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )  
        case 'Xception':
            base_model = keras.applications.Xception(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )  
        case 'ResNet152V2':
            base_model = keras.applications.ResNet152V2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )  
        case 'InceptionV3':
            base_model = keras.applications.InceptionV3(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )  
        case 'ResNet50':
            base_model = keras.applications.ResNet50(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'ResNet50V2':
            base_model = keras.applications.ResNet50V2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'ResNet101':
            base_model = keras.applications.ResNet101(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'ResNet101V2':
            base_model = keras.applications.ResNet101V2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'ResNet152':
            base_model = keras.applications.ResNet152(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'InceptionResNetV2':
            base_model = keras.applications.InceptionResNetV2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'MobileNet':
            base_model = keras.applications.MobileNet(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'MobileNetV2':
            base_model = keras.applications.MobileNetV2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'DenseNet121':
            base_model = keras.applications.DenseNet121(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'DenseNet169':
            base_model = keras.applications.DenseNet169(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'DenseNet201':
            base_model = keras.applications.DenseNet201(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'NASNetMobile':
            base_model = keras.applications.NASNetMobile(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB0':
            base_model = keras.applications.EfficientNetB0(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB1':
            base_model = keras.applications.EfficientNetB1(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB2':
            base_model = keras.applications.EfficientNetB2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB3':
            base_model = keras.applications.EfficientNetB3(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB4':
            base_model = keras.applications.EfficientNetB4(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB5':
            base_model = keras.applications.EfficientNetB5(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB6':
            base_model = keras.applications.EfficientNetB6(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetB7':
            base_model = keras.applications.EfficientNetB7(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2B0':
            base_model = keras.applications.EfficientNetV2B0(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2B1':
            base_model = keras.applications.EfficientNetV2B1(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2B2':
            base_model = keras.applications.EfficientNetV2B2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2B3':
            base_model = keras.applications.EfficientNetV2B3(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2S':
            base_model = keras.applications.EfficientNetV2S(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2M':
            base_model = keras.applications.EfficientNetV2M(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2L':
            base_model = keras.applications.EfficientNetV2L(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )
        case 'EfficientNetV2B2':
            base_model = keras.applications.EfficientNetV2B2(
                weights="imagenet",
                input_shape=(img_width, img_height, 3),
                include_top=False,
            )

    base_model.trainable = False

    scale_layer = keras.layers.Rescaling(scale=1 / 127.5, offset=-1)
    inputs = keras.Input(shape=(img_width, img_height, 3))
    
    x = scale_layer(inputs)
    x = base_model(x)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(dropout)(x)
    outputs = keras.layers.Dense(num_classes)(x)
    model = keras.Model(inputs, outputs)
    model._name = application

    return model