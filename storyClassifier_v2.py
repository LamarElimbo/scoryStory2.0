import pickle, os

def v2_classifyStory(story):

    pickleDir = os.getcwd()
    pickleFilePath = pickleDir +'/v2_savedNBClassifier.pkl'
    savedClassifier = open(pickleFilePath, 'rb')
    classer = pickle.load(savedClassifier)
    vectorer = pickle.load(savedClassifier)
    savedClassifier.close()

    storyList = ['this is the buffer']
    storyList.append(story)
    storyFeatures = vectorer.transform(storyList)
    classification = classer.predict(storyFeatures)
    return classification[-1]