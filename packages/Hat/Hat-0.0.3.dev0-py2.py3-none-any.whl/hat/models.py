'''
SUMMARY:  Build Model
AUTHOR:   Qiuqiang Kong
Created:  2016.05.01
Modified: 2016.07.25 Modify fit() to batch version
          2016.07.29 Replace [[]] * n with [ [] for e in self._out_nodes ]
--------------------------------------
'''
import sys
from supports import to_list, BFT, shuffle, memory_usage
from optimizers import *
from globals import reset_id_to_zero
import activations
import objectives as obj
import backend as K
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pickle

class Base( object ):
    def __init__( self, in_layers ):
        # reset global id
        reset_id_to_zero()
        
        # inlayers
        in_layers = to_list( in_layers )
        self._in_layers_ = in_layers
        self._in_nodes_ = [ layer.output_ for layer in self._in_layers_ ]
        
        # find all nodes using BFT
        self._id_list_, self._layer_list_ = BFT( self._in_layers_ )
        
        # get params by traveling all layers
        self._params_ = []
        for layer in self._layer_list_:
            self._params_ += layer.params_
            
        # sum regs by traveling all layers
        self._reg_value_ = 0.
        for layer in self._layer_list_:
            self._reg_value_ += layer.reg_value_
            
        # tr_phase_node
        self._tr_phase_node_ = K.common_tr_phase_node
            
        # time
        self._tr_time_ = 0.
        self._epoch_ = 0
    
    # print progress on screen
    def _print_progress( self, epoch, batch_num, curr_batch_num ):
        #sys.stdout.write("%d-th epoch %d%%   %s %f \r" % ( epoch, float(curr_batch_num)/float(batch_num)*100, 'tr_loss:', loss ) )
        sys.stdout.write("%d-th epoch %d%% \r" % ( epoch, float(curr_batch_num)/float(batch_num)*100 ) )
        sys.stdout.flush()
        
    @property
    def in_layers_( self ):
        return self._in_layers_
        
    
    @property
    def in_nodes_( self ):
        return self._in_nodes_
        
    @property
    def out_nodes_( self ):
        return self._out_nodes_
        
    @property
    def inter_nodes_( self ):
        return self._inter_nodes_
    
    
    @property
    def epoch_( self ):
        return self._epoch_
        
    @property
    def tr_time_( self ):
        return self._tr_time_
        
    @property
    def tr_phase_node_( self ):
        return self._tr_phase_node_
        
    def summary( self ):
        print '---------- summary -----------'
        f = "{0:<20} {1:<20} {2:<20}"
        print f.format( 'layer_name', 'out_shape', 'n_params' )
        for layer in self._layer_list_:
            n_params = self._num_of_params( layer )
            print f.format( layer.name_, str(layer.out_shape_), str(n_params) )
        print 
        
    # search and return layer from name
    def find_layer( self, name ):
        for layer in self._layer_list_:
            if name==layer.name_:
                return layer
        raise Exception("No layer named " + name + "! ")
            
    # get number of params in a layer
    def _num_of_params( self, layer ):
        n_params = 0
        for param in layer.params_:
            n_params += np.prod( K.get_value( param ).shape )
        return n_params
        
    # check if the dim of output is correct
    def _check_data( self, y, loss_func ):
        if loss_func in ['categorical_crossentropy', 'binary_crossentropy', 'kl_divergence']:
            for e in y:
                assert e.ndim!=1, "your y.ndim is 1, try use sparse_to_categorical(y)"
        

    def plot_connection( self ):
        G = nx.DiGraph()
        
        # add node
        for id in self._id_list_:
            G.add_node( id )
        
        # add connection
        for layer in self._layer_list_:
            for next in layer.nexts_:
                G.add_edge( layer.id_, next.id_ )
                
        # pos & labels
        pos = nx.spring_layout(G)
        labels = {}
        for layer in self._layer_list_:
            if hasattr( layer, '_act' ):
                labels[layer.id_] = layer._name_
            else:
                labels[layer.id_] = layer._name_

        # plot
        nx.draw_networkx_nodes( G , pos, node_size=800, node_color='r', node_shape='o' )
        nx.draw_networkx_labels( G, pos, labels=labels )
        nx.draw_networkx_edges( G, pos )
        try:
            plt.show()
        except:
            print "Warning! You do not have graphic interface to plot connection! "

'''
Supervised Model
'''
class Model( Base ):
    def __init__( self, in_layers, out_layers, any_layers=[] ):
        super( Model, self ).__init__( in_layers )

        # out layers
        out_layers = to_list( out_layers )
        self._out_layers_ = out_layers
        self._out_nodes_ = [ layer.output_ for layer in self._out_layers_ ]
        
        # inter layers
        any_layers = to_list( any_layers )
        self._any_layers_ = any_layers
        self._inter_nodes_ = [ layer.output_ for layer in self._any_layers_ ]


    def fit( self, x, y, batch_size=100, n_epochs=10, loss_func='categorical_crossentropy', optimizer=SGD( lr=0.01, rho=0.9 ), clip=None, callbacks=[], memory_mode=0, verbose=1 ):
        x = to_list( x )
        y = to_list( y )
        
        # format
        x = [ K.format_data(e) for e in x ]
        y = [ K.format_data(e) for e in y ]
        
        # shuffle data
        x, y = shuffle( x, y )
        
        # check data
        self._check_data( y, loss_func )
        
        # init gt_nodes
        gt_nodes = [ K.placeholder( e.ndim ) for e in y ]
        
        # memory usage
        #mem_usage = memory_usage( x, y )
        #print 'memory usage:', mem_usage / 8e6, 'Mb'
        
        # default objective
        if type(loss_func) is str:
            assert len(self._out_nodes_)==len(gt_nodes), "If you are using default objectives, " \
                                            + "out_node of out_layers must match ground truth!"
            loss_node = sum( [ obj.get( loss_func )( pred_node, gt_node ) 
                            for pred_node, gt_node in zip( self._out_nodes_, gt_nodes ) ] )
        # user defined objective
        else:
            loss_node = loss_func( self._out_nodes_, self._inter_nodes_, gt_nodes )
         
        # gradient
        gparams = K.grad( loss_node + self._reg_value_, self._params_ )
        
        # todo clip gradient
        if clip is not None:
            gparams = [ K.clip( gparam, -clip, clip ) for gparam in gparams ]
        
        # gradient based opt
        updates = optimizer.get_updates( self._params_, gparams )
        
        # compile for callback
        if callbacks is not None:
            callbacks = to_list( callbacks )
            for callback in callbacks:
                callback.compile( self ) 

        # compile model
        input_nodes = self._in_nodes_ + gt_nodes
        output_nodes = [ loss_node ]
        f = K.function_no_given( input_nodes, self._tr_phase_node_, output_nodes, updates )

        # train
        N = len( x[0] )
        batch_num = int( np.ceil( float(N) / batch_size ) )
        n_abs_epoch = n_epochs + self._epoch_
        while self._epoch_ < n_abs_epoch:
            # callback
            for callback in callbacks:
                if ( self._epoch_ % callback.call_freq == 0 ):
                    callback.call()
                    
            # train
            t1 = time.time()
            loss_list = []
            for i2 in xrange(batch_num):
                batch_x = [ e[i2*batch_size : min( (i2+1)*batch_size, N ) ] for e in x ]
                batch_y = [ e[i2*batch_size : min( (i2+1)*batch_size, N ) ] for e in y ]
                in_list = batch_x + batch_y + [1.]
                loss = f( *in_list )[0]                     # training phase 
                loss_list.append( loss )
                if verbose: self._print_progress( self._epoch_, batch_num, i2 )
            #if verbose: self._print_progress( self._epoch_, batch_num, i2, np.mean(loss_list) )
                
            t2 = time.time()
            self._tr_time_ += (t2 - t1)
            self._epoch_ += 1
            print '\n', '    tr_time: ', "%.2f" % (t2-t1), 's'          # print an empty line

    def predict( self, x, batch_size=100 ):
        # format data
        x = to_list( x )
        x = [ K.format_data(e) for e in x ]
        
        # compile predict model
        if not hasattr( self, '_f_predict' ):
            self._f_predict = K.function_no_given( self._in_nodes_, self._tr_phase_node_, self._out_nodes_ )
        
        # do predict
        # put all data in GPU
        if batch_size is None:
            in_list = x + [0.]
            y_out = self._f_predict( *in_list )
        # put batch data in GPU
        else:
            N = len(x[0])
            batch_num = int( np.ceil( float(N) / batch_size ) )
            n_out_nodes = len( self._out_nodes_ )
            y_out = [ [] for e in self._out_nodes_ ]
            for i1 in xrange( batch_num ):
                in_list = [ e[i1*batch_size : min( (i1+1)*batch_size, N ) ] for e in x ] + [0.]
                batch_y_out = self._f_predict( *in_list )
                for j1 in xrange(n_out_nodes):
                    y_out[j1].append( batch_y_out[j1] )
                    
            # get y_out
            y_out = [ np.concatenate(e, axis=0) for e in y_out ]
        
        if len(y_out)==1:
            return y_out[0]
        else:
            return y_out
        
    
    @property
    def info_( self ):
        dict = { 'epoch': self.epoch_, 
                 'in_ids': [ layer.id_ for layer in self._in_layers_ ], 
                 'out_ids': [ layer.id_ for layer in self._out_layers_ ], 
                 'inter_ids': [layer.id_ for layer in self._any_layers_] }
        return dict
    
    @classmethod
    def load_from_info( cls, in_layers, out_layers, any_layers, info ):
        md = cls( in_layers, out_layers, any_layers )
        md._epoch_ = info['epoch']
        return md


'''
class Model( Base ):
    def __init__( self, in_layers, out_layers, any_layers=[] ):
        super( Model, self ).__init__( in_layers )

        # out layers
        out_layers = to_list( out_layers )
        self._out_layers_ = out_layers
        self._out_nodes_ = [ layer.output_ for layer in self._out_layers_ ]
        
        # inter layers
        any_layers = to_list( any_layers )
        self._any_layers_ = any_layers
        self._inter_nodes_ = [ layer.output_ for layer in self._any_layers_ ]


    def fit( self, x, y, batch_size=100, n_epochs=10, loss_func='categorical_crossentropy', optimizer=SGD( lr=0.01, rho=0.9 ), clip=None, callbacks=[], memory_mode=0, verbose=1 ):
        x = to_list( x )
        y = to_list( y )
        
        # format
        x = [ K.format_data(e) for e in x ]
        y = [ K.format_data(e) for e in y ]
        
        # shuffle data
        x, y = shuffle( x, y )
        
        # check data
        self._check_data( y, loss_func )
        
        # init gt_nodes
        gt_nodes = [ K.placeholder( e.ndim ) for e in y ]
        
        # memory usage
        #mem_usage = memory_usage( x, y )
        #print 'memory usage:', mem_usage / 8e6, 'Mb'
        
        # default objective
        

        if type(loss_func) is str:
            assert len(self._out_nodes_)==len(gt_nodes), "If you are using default objectives, " \
                                            + "out_node of out_layers must match ground truth!"
            loss_node = sum( [ obj.get( loss_func )( pred_node, gt_node ) 
                            for pred_node, gt_node in zip( self._out_nodes_, gt_nodes ) ] )
        # user defined objective
        else:
            loss_node = loss_func( self._out_nodes_, self._inter_nodes_, gt_nodes )
         
        # gradient
        gparams = K.grad( loss_node + self._reg_value_, self._params_ )
        
        # todo clip gradient
        if clip is not None:
            gparams = [ K.clip( gparam, -clip, clip ) for gparam in gparams ]
        
        # gradient based opt
        updates = optimizer.get_updates( self._params_, gparams )
        
        # compile for callback
        if callbacks is not None:
            callbacks = to_list( callbacks )
            for callback in callbacks:
                callback.compile( self ) 

        from numpy import linalg
        import theano
        

        # compile model
        input_nodes = self._in_nodes_ + gt_nodes
        output_nodes = [ loss_node ]
        f = K.function_no_given( input_nodes, self._tr_phase_node_, output_nodes, updates)

        a1_out_node = self.find_layer('a1').output_
        f_debug = K.function_no_given( self._in_nodes_, self._tr_phase_node_, a1_out_node )
        
        g_a1_node = K.grad( loss_node+self._reg_value_, [a1_out_node] )
        f_debug2 = K.function_no_given( input_nodes, self._tr_phase_node_, g_a1_node )
        
        
        g_a1_H =  K.grad( loss_node+self._reg_value_, [self.find_layer('a1')._H_] )
        f_debug3 = K.function_no_given( input_nodes, self._tr_phase_node_, g_a1_H )

        

        # train
        N = len( x[0] )
        batch_num = int( np.ceil( float(N) / batch_size ) )
        n_abs_epoch = n_epochs + self._epoch_
        while self._epoch_ < n_abs_epoch:
            # callback
            for callback in callbacks:
                if ( self._epoch_ % callback.call_freq == 0 ):
                    callback.call()
                    
            # train
            t1 = time.time()
            loss_list = []
            for i2 in xrange(batch_num):
                batch_x = [ e[i2*batch_size : min( (i2+1)*batch_size, N ) ] for e in x ]
                batch_y = [ e[i2*batch_size : min( (i2+1)*batch_size, N ) ] for e in y ]
                in_list = batch_x + batch_y + [1.]
                
                in_list2 = batch_x + [0.]
                
                
                
                #np.set_printoptions(threshold=np.nan, linewidth=1000, precision=2, suppress=True)
                print self._epoch_
                print 'is_nan_H^11:', np.sum(np.isnan(linalg.matrix_power( self.find_layer('a1').H_, 11 )))
                print 'is_nan_reluWx:', np.sum(np.isnan(activations.relu( np.dot(batch_x, self.find_layer('a1').W_) )))
                print np.sum(self.find_layer('a1').W_), np.sum(self.find_layer('a1').H_), np.sum(self.find_layer('a1').b_)
                print np.sum(self.find_layer('a3').W_), np.sum(self.find_layer('a3').b_)
                print 'a1_out:', f_debug( *in_list2 )
                print 'a1_grad_node:', f_debug2( *in_list )
                print 'a1_grad_H:', f_debug3( *in_list )
                
                
                loss = f( *in_list )[0]  
                loss_list.append( loss ) 
                #print self._epoch_, loss
                print  loss 
                #if verbose: self._print_progress( self._epoch_, batch_num, i2 )
            #if verbose: self._print_progress( self._epoch_, batch_num, i2, np.mean(loss_list) )
                
            t2 = time.time()
            self._tr_time_ += (t2 - t1)
            self._epoch_ += 1
            print '\n', '    tr_time: ', "%.2f" % (t2-t1), 's'          # print an empty line

    def predict( self, x, batch_size=100 ):
        # format data
        x = to_list( x )
        x = [ K.format_data(e) for e in x ]
        
        # compile predict model
        if not hasattr( self, '_f_predict' ):
            self._f_predict = K.function_no_given( self._in_nodes_, self._tr_phase_node_, self._out_nodes_ )
        
        # do predict
        # put all data in GPU
        if batch_size is None:
            in_list = x + [0.]
            y_out = self._f_predict( *in_list )
        # put batch data in GPU
        else:
            N = len(x[0])
            batch_num = int( np.ceil( float(N) / batch_size ) )
            n_out_nodes = len( self._out_nodes_ )
            y_out = [ [] for e in self._out_nodes_ ]
            for i1 in xrange( batch_num ):
                in_list = [ e[i1*batch_size : min( (i1+1)*batch_size, N ) ] for e in x ] + [0.]
                batch_y_out = self._f_predict( *in_list )
                for j1 in xrange(n_out_nodes):
                    y_out[j1].append( batch_y_out[j1] )
                    
            # get y_out
            y_out = [ np.concatenate(e, axis=0) for e in y_out ]
        
        if len(y_out)==1:
            return y_out[0]
        else:
            return y_out
        
    
    @property
    def info_( self ):
        dict = { 'epoch': self.epoch_, 
                 'in_ids': [ layer.id_ for layer in self._in_layers_ ], 
                 'out_ids': [ layer.id_ for layer in self._out_layers_ ], 
                 'inter_ids': [layer.id_ for layer in self._any_layers_] }
        return dict
    
    @classmethod
    def load_from_info( cls, in_layers, out_layers, any_layers, info ):
        md = cls( in_layers, out_layers, any_layers )
        md._epoch_ = info['epoch']
        return md
'''
        
class Sequential( Model ):
    def __init__( self ):
        self._layer_seq_ = []
        
    def add( self, layer ):
        self._layer_seq_.append( layer )
        if len( self._layer_seq_ ) > 1:
            self._layer_seq_[-1].__call__( self._layer_seq_[-2] )

    def combine( self ):
        # regenerate model when add a new layer
        md = Model( [ self._layer_seq_[0] ], [ self._layer_seq_[-1] ] )
        return md
    
class Pretrain():
    pass