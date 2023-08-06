import numpy as np


class DataIterator(object):
    def __init__(self, *data, **params):
        self.data = data
        self.batchsize = params['batchsize']

    def __iter__(self):
        self.first = 0
        return self

    def __len__(self):
        return len(self.data[0])

    def __getitem__(self, key):
        outs = []
        for val in self.data:
            outs.append(val[key])
        return self.__class__(*outs, batchsize=self.batchsize)


class SequentialIterator(DataIterator):
    '''
    batchsize = 3
    [0, 1, 2], [3, 4, 5], [6, 7, 8]
    '''
    def next(self):
        if self.first >= len(self):
            raise StopIteration()
        outs = []
        for val in self.data:
            outs.append(val[self.first:self.first+self.batchsize])
        self.first += self.batchsize
        return outs


class StepIterator(DataIterator):
    '''
    batchsize = 3
    step = 1
    [0, 1, 2], [1, 2, 3], [2, 3, 4]
    '''
    def __init__(self, *data, **params):
        super(self, StepIterator).__init__(self, *data, **params)
        self.step = params['step']

    def next(self):
        if self.first >= len(self):
            raise StopIteration()
        outs = []
        for val in self.data:
            outs.append(val[self.first:self.first+self.batchsize])
        self.first += self.step
        return outs


def np_load_func(path):
    with open(path) as fin:
        arr = np.load(fin)
    return arr


class DataBlocks(object):

    def __init__(self, data_paths, batchsize=32, load_func=np_load_func, allow_preload=False):
        """
        DESCRIPTION:
            This is class for processing blocks of data, whereby dataset is loaded
            and unloaded into memory one block at a time.
        PARAM:
            data_paths (list or list of list): contains list of paths for data loading,
                            example:
                                [f1a.npy, f1b.npy, f1c.npy]  or
                                [(f1a.npy, f1b.npy, f1c.npy), (f2a.npy, f2b.npy, f2c.npy)]
            load_func (function): function for loading the data_paths, default to
                            numpy file loader
            allow_preload (bool): by allowing preload, it will preload the next data block
                            while training at the same time on the current datablock,
                            this will reduce time but will also cost more memory.
        """

        assert isinstance(data_paths, (list)), "data_paths is not a list"
        self.data_paths = data_paths
        self.batchsize = batchsize
        self.load_func = load_func
        self.allow_preload = allow_preload
        self.q = Queue()


    def __iter__(self):
        self.files = iter(self.data_paths)
        if self.allow_preload:
            self.lastblock = False
            bufile = next(self.files)
            self.load_file(bufile, self.q)
        return self


    def next(self):
        if self.allow_preload:
            if self.lastblock:
                raise StopIteration

            try:
                arr = self.q.get(block=True, timeout=None)
                self.iterator = SequentialIterator(*arr, batchsize=self.batchsize)
                bufile = next(self.files)
                p = Process(target=self.load_file, args=(bufile, self.q))
                p.start()
            except:
                self.lastblock = True
        else:
            fpath = next(self.files)
            arr = self.load_func(fpath)
            self.iterator = SequentialIterator(*arr, batchsize=self.batchsize)

        return self.iterator


    def load_file(self, paths, queue):
        '''
        paths (list or str): []
        '''
        data = []
        if isinstance(paths, (list, tuple)):
            for path in paths:
                data.append(self.load_func(path))
        else:
            data.append(self.load_func(paths))
        queue.put(data)


    @property
    def nblocks(self):
        return len(self.data_paths)
