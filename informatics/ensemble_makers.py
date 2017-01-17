'''Bla bla

'''
class EnsembleMaker:
    '''Bla bla

    '''
    def join(self, objs):
        '''Bla bla

        '''
        ret = objs[0]
        for obj in objs[1:]:
            ret += obj

        return ret

    def unity(self, objs):
        '''Bla bla

        '''
        return objs

    def __call__(self, summary_obj):
        '''Bla bla

        '''
        return self.operate(summary_obj)
            
    def __init__(self, operation, id_subset):
        '''Bla bla

        '''
        self.id_subset = id_subset
        try:
            self.operate = getattr(self, operation)
        except AttributeError:
            raise AttributeError("No operation named %s " %(operation) + \
                                 "defined for the ensemble maker")

