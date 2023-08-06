import math
from collections.abc import Iterable
from dataclasses import astuple, dataclass

import numpy as np


class ValidDataset:
    pass

@dataclass
class DataSet:
    x: np.array
    y: np.array
    numClasses: int = None
    transformToCategorical = False
    catMatrix = None
    
    def __len__(self):
        return len(self.x)


    @classmethod
    def toCategorical(cls, numClasses, distinct=True):
        if cls.catMatrix is None:
            if distinct == False:
                size = 2**numClasses
                cls.catMatrix = np.full((size + 1, numClasses), 0)
                for i in range(size):
                    cls.catMatrix[i] = (((2 ** np.arange(numClasses)) & i) > 0) * 1
                cls.catMatrix[0][0] = 1  # first entry is implicit "None"

            else:
                cls.catMatrix = np.eye(cls.numClasses)
                # append a zero line on the end so that -1 will map to all zeros
                cls.catMatrix = np.concatenate((cls.catMatrix, np.eye(1, numClasses, -1))).astype(cls.y.dtype)

        return np.squeeze(cls.catMatrix[cls.y.astype(np.int32)])
    
    def toCategorical(self, distinct=True):
        if self.catMatrix is None:
            if distinct == False:
                size = 2**self.numClasses
                self.catMatrix = np.full((size + 1, self.numClasses), 0)
                for i in range(size):
                    self.catMatrix[i] = (((2 ** np.arange(self.numClasses)) & i) > 0) * 1
                self.catMatrix[0][0] = 1  # first entry is implicit "None"

            else:
                self.catMatrix = np.eye(self.numClasses)
                # append a zero line on the end so that -1 will map to all zeros
                self.catMatrix = np.concatenate((self.catMatrix, np.eye(1, self.numClasses, -1))).astype(self.y.dtype)

        self.y = np.squeeze(self.catMatrix[self.y.astype(np.int32)])

    @staticmethod
    def fromTuple(data, numClasses=None):
        x, y = data
        return DataSet(x, y, numClasses)
    
    def asTuple(self):
        return astuple(self)

class DataSetContinous(ValidDataset):
    def __len__(self):
        return self.recordCount if self.recordWise else self.batchCount

    def __init__(self, batchFunction, batchCount=None, recordCount=None, numClasses=None, getSingleRecord=None) -> None:
        self.batchFunction = batchFunction
        self.batchCount = batchCount
        self.recordCount = recordCount
        self.numClasses = numClasses
        self.transformToCategorical = False
        self.continous = True
        self.index = 0
        self.recordWise = False
        self.getSingleRecord = getSingleRecord
        self.augmentation = True
        self.function = None
        self.distinct = True
        if self.recordWise and self.recordCount is None:
            self.recordCount = len(batchFunction)
        if not self.recordWise and self.batchCount is None:
            self.batchCount = len(batchFunction)

    def getFunction(self):
        if self.function is None:
            self.function = self.batchFunction(recordWise=self.recordWise, augmentation=self.augmentation)
        return self.function

    def toCategorical(self):
        self.transformToCategorical = True

    def nonContinous(self):
        self.continous = False

    def __next__(self):
        if not self.continous and self.index == len(self):
            raise StopIteration

        dataTuple = self.getFunction().__next__()
        batch = DataSet.fromTuple(dataTuple, numClasses=self.numClasses)
        if self.transformToCategorical:
            batch.toCategorical(self.distinct)
        self.index += 1
        return batch

    def __iter__(self):
        self.function = None
        self.getFunction().__iter__()
        self.index = 0
        return self

    def generator(self, wrapper=None):

        while True:
            ret = self.__next__()
            wrapper = (lambda x: x) if wrapper is None else wrapper
            yield wrapper(ret)

    def __getitem__(self, index):
        dataTuple = self.getSingleRecord(index)
        batch = DataSet.fromTuple(dataTuple, numClasses=self.numClasses)
        if self.transformToCategorical:
            batch.toCategorical()
        return batch


class TrainingSet:
    def __init__(
        self,
        trainingData=None,
        validationData=None,
        transformToCategorical=False,
        numClasses=None,
        useContinous=True,
        distinct=True,
    ) -> None:

        self.trainingData: DataSet = None
        self.validationData: DataSet = None
        self.transformToCategorical = transformToCategorical
        self.transformChannelLast = False

        if isinstance(trainingData, ValidDataset):
            self.trainingData = trainingData
        elif isinstance(trainingData, Iterable) and useContinous:
            self.trainingData = DataSetContinous(trainingData)
        else:
            self.trainingData = DataSet.fromTuple(trainingData, len(trainingData))

        if isinstance(validationData, ValidDataset):
            self.validationData = validationData
        elif isinstance(validationData, Iterable) and useContinous:
            self.validationData = DataSetContinous(validationData, len(validationData))
        else:
            self.validationData = DataSet.fromTuple(validationData)

        self.trainingData.transformToCategorical = transformToCategorical
        self.validationData.transformToCategorical = transformToCategorical
        self.trainingData.distinct = distinct
        self.validationData.distinct = distinct

        self.trainingData.numClasses = numClasses
        self.validationData.numClasses = numClasses

    def toCategorical(self):
        self.trainingData.toCategorical()
        self.validationData.toCategorical()

    def getNextTrainingBatch(self):
        dataTuple = self.trainingData.__next__()
        batch = DataSet.fromTuple(dataTuple)
        if self.transformToCategorical:
            batch.toCategorical()
        return batch


class DatasetWrap(DataSetContinous):

    def __getitem__(self, index):
        return self.dataset[index]


    def __len__(self):
        return len(self.dataset)

    def __init__(self, dataset) -> None:
        self.dataset = dataset
        
    def toCategorical(self):
        self.transformToCategorical = True

    def nonContinous(self):
        self.continous = False

    def __next__(self):
        return self.dataset.__next__()

    def __iter__(self):
        return self.dataset.__iter__()
    
    def asTuple(self):
        return self
    

class DatasetWrapXY(ValidDataset):    
    
    def __init__(self, dataset, batchSize=1) -> None:
        self.x, self.y = dataset
        self.batchSize = batchSize
        self.length = math.ceil(len(self.x)/self.batchSize)

    def __getitem__(self, index):
        if index > self.length:
            raise IndexError
        s = slice(index*self.batchSize, (index+1)*self.batchSize)
        return self.x[s], self.y[s]

    def __len__(self):
        return self.length 

    def nonContinous(self):
        self.continous = False

    def generator(self, wrapper=None):
        while True:
            for d in self:
                wrapper = (lambda x: x) if wrapper is None else wrapper
                yield wrapper(DataSet.fromTuple(d))