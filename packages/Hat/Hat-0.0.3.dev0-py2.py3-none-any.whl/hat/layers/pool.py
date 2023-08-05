'''
SUMMARY:  Pooling Layers
AUTHOR:   Qiuqiang Kong
Created:  2016.05.22
Modified: 2016.05.27 Add MaxPool1D
--------------------------------------
'''
from core import Layer, Lambda
from ..globals import new_id
from .. import backend as K
from .. import initializations
from .. import activations
from ..supports import to_list, to_tuple, get_mask
import numpy as np
# from theano.tensor.signal.downsample import max_pool_2d


# todo
def _max_pool_1d( input, in_shape, **kwargs ):
    assert len(in_shape)==3, "shape.ndim should be 3, shape:(batch_size, n_time, n_in), yours is " + str(in_shape)
    
    # init kwargs
    [batch_size, n_time, n_in] = in_shape
    len_pool = kwargs['len_pool']
    
    # downsample
    pool_size = (len_pool, 1)
    
    # size(output): (batch_size, n_outfmaps, n_time, 1)
    output = downsample.max_pool_2d( input.dimshuffle(0,2,1,'x'), pool_size, ignore_border=True )
    
    # size(output): (batch_size, n_time, n_outfmaps)
    output = output.dimshuffle(0,2,1,3).flatten(3)
    out_shape = ( None, n_time//len_pool, n_in )
    
    return output, out_shape
    
class MaxPool1D( Lambda ):
    def __init__( self, name=None, **kwargs ):
        assert 'len_pool' in kwargs, "You must specifiy len_pool kwarg in MaxPool1D!"
        super( MaxPool1D, self ).__init__( _max_pool_1d, name, **kwargs )



'''
Max Pooling 2D
'''
# for cnn
def _max_pool_2d( input, in_shape, **kwargs ):
    assert len(in_shape)==4, "shape.ndim should be 4, shape:(batch_size, n_infmaps, height, width), yours is " + str(in_shape)
    
    # init kwargs
    [batch_size, n_infmaps, height, width] = in_shape
    pool_size = kwargs['pool_size']
    
    # downsample
    output = K.pool2d( input, pool_size, ignore_border=True )
    out_shape = ( None, n_infmaps, int(height/pool_size[0]), int(width/pool_size[1]) )
    return output, out_shape
    
class MaxPool2D( Lambda ):
    def __init__( self, name=None, **kwargs ):
        assert 'pool_size' in kwargs, "You must specifiy pool_size kwarg in MaxPool2D!"
        super( MaxPool2D, self ).__init__( _max_pool_2d, name, **kwargs )
    
    # model's info & params
    @property
    def info_( self ):
        dict = { 'class_name': self.__class__.__name__, 
                 'id': self._id_, 
                 'kwargs': self._kwargs_, 
                 'name': self._name_, }
        return dict
        
    # load layer from info
    @classmethod
    def load_from_info( cls, info ):
        layer = cls( info['name'], **info['kwargs'] )
        return layer
    
    
# todo
'''
'''
def _pool_2d( input, in_shape, **kwargs ):
    assert len(in_shape)==4, "shape.ndim should be 4, shape:(batch_size, n_infmaps, height, width), yours is " + str(in_shape)
    
    # init kwargs
    [batch_size, n_infmaps, height, width] = in_shape
    pool_size = kwargs['pool_size']
    pool_mode = kwargs['pool_mode']
    
    # downsample
    output = K.pool2d( input, ds=pool_size, mode=pool_mode )
    out_shape = ( None, n_infmaps, int(height/pool_size[0]), int(width/pool_size[1]) )
    return output, out_shape
    
# kwargs: 'max' | 'avg'
class Pool2D( Lambda ):
    def __init__( self, name=None, **kwargs ):
        assert 'pool_size' in kwargs, "You must specifiy pool_size kwarg!"
        assert 'pool_mode' in kwargs, "You must specifiy pool_mode kwarg! eg. 'max', 'avg'"
        super( Pool2D, self ).__init__( _pool_2d, name, **kwargs )


# todo
'''
Mean along time axis in RNN. 
'''
def _global_mean_time_pool( input, in_shape, **kwargs ):
    assert len(in_shape)==3, "Input dimension must be 3, (batch_size, n_time, n_freq)"
    masking = kwargs['masking']
    
    if masking is True:
        output = K.sum( input, axis=1 )
        mask = get_mask( input )
        batch_nums = K.sum( mask, axis=1 )
        output /= batch_nums[:, None]
    else:
        output = K.mean( input, axis=1 )
        
    out_shape = ( in_shape[0], in_shape[2] )
    return output, out_shape
    
    
# todo
class GlobalMeanTimePool( Lambda ):
    def __init__( self, name=None, **kwargs ):
        assert 'masking' in kwargs, "You must specifiy masking kwarg in GlobalMeanTimePool!"
        super( GlobalMeanTimePool, self ).__init__( _global_mean_time_pool, name, **kwargs )
        
    # model's info & params
    @property
    def info_( self ):
        dict = { 'class_name': self.__class__.__name__, 
                 'id': self._id_, 
                 'kwargs': self._kwargs_, 
                 'name': self._name_, }
        return dict
        
    # load layer from info
    @classmethod
    def load_from_info( cls, info ):
        layer = cls( info['name'], **info['kwargs'] )
        return layer


# todo
'''
max pool along axis
'''
def _global_max_pool( input, in_shape, **kwargs ):
    axis = kwargs['axis']
    output = K.max( input, axis )
    out_shape = in_shape[0:axis] + in_shape[axis+1:]
    return output, out_shape
    
class GlobalMaxPool( Lambda ):
    def __init__( self, name=None, **kwargs ):
        assert 'axis' in kwargs, "You must specifiy axis kwarg in GlobalMaxPool!"
        super( GlobalMaxPool, self ).__init__( _global_max_pool, name, **kwargs )
