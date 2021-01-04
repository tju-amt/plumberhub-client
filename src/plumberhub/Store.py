class SampleStore:

    _sampleList = []

    def __init__(self):
        pass

    def append(self, sample):
        self._sampleList.append()

    def map(self, iterator):
        list = []

        for index in range(len(self._sampleList)):
            list[index] = iterator(self._sampleList[index], index)
        
        return list

    def clear(self):
        self._sampleList.clear()