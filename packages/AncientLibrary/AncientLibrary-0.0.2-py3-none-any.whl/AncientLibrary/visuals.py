import sys
import time
import numpy as np
import matplotlib.pyplot as plt 

class VisualTraining:
    
    def __init__(self, **kwargs):
        self.epoch = 0
        self.max_iter = 100
        self.display = 5
        self.should_graph = True
        self.bar_size = 40
        self.loss_names = None
        self.round = 3
        self.start_time = time.time()
        self.time_type = 'min'
        self.time_den = 60
        
        if 'title' in kwargs:
            self.title = kwargs['title']
        else:
            self.title = 'Training Loss'
        
        if 'loss_names' in kwargs:
            self.loss_names = kwargs['loss_names']
            
        if 'round' in kwargs:
            self.round = kwargs['round']
            
        if 'display' in kwargs:
            self.display = int(kwargs['display'])
            
        if 'time_type' in kwargs:
            if kwargs['time_type'] == 'hrs':
                self.time_type = 'hrs'
                self.time_den = 3600
                
        if 'max_iter' in kwargs:
            self.max_iter = int(kwargs['max_iter'])
            
        if 'bar_size' in kwargs:
            self.bar_size = int(kwargs['bar_size'])

        if 'graph' in kwargs:
            if not kwargs['graph']:
                self.should_graph = False
                
        print(f'Initializing Model ...')
                
    def __call__(self, losses):
        
        if self.epoch < self.max_iter:
            if self.epoch == 0:
                if self.loss_names is None:
                    self.loss_names = [f'Loss_{i+1}' for i in range(len(losses))]
                self.loss_arrays = {name: [loss] for (name, loss) in zip(self.loss_names, losses)}    
                
            for i, (name, val) in enumerate(zip(self.loss_names, losses)):
                self.loss_arrays[name].append(val)

            if self.epoch % self.display == 0:
                curr_time = (time.time()-self.start_time)/self.time_den
                eta = ((time.time() - self.start_time)/self.time_den) / ((self.epoch + 1)/self.max_iter) - curr_time
                s1 = f'Epoch: {self.epoch:{len(str(self.max_iter))}}  '
                s2 = "".join([f'{name}: {val:.{self.round}f} ' for (name, val) in zip(self.loss_names, losses)])
                s3 = f' Runtime/ETA: {curr_time:.2f} - {eta:.2f} {self.time_type}'
                print(s1 + s2 + s3)

            self.epoch += 1    
            self.display_bar()
            if self.epoch == self.max_iter:
                self.display_bar(True)
                print(f'\nModel Finished in {(time.time()-self.start_time)/self.time_den:.2f} {self.time_type}')
                if self.should_graph:
                    self.graph_loss()
            else:
                self.display_bar()
            
    def display_bar(self, finished=False):
        pct = int(self.bar_size * ((self.epoch)/self.max_iter))
        bar = [f'Epoch: {self.epoch:{len(str(self.max_iter))}}/{self.max_iter} [']
        if finished:
            bar += ['$' for _ in range(self.bar_size)]
        else:
            bar += [u"█" for _ in range(pct)]
            bar += [' ' for _ in range(self.bar_size-pct)]
        bar += [f'] {self.epoch/self.max_iter:.2%}']
        progressbar = "".join(bar)
        sys.stdout.write(progressbar)
        sys.stdout.flush()
        if not finished:
            sys.stdout.write('\r')

    def graph_loss(self):
        colors = ['dodgerblue', 'limegreen', 'coral', 'magenta']
        counter = 0
        plt.figure(figsize=(16, 4))
        for name, val in self.loss_arrays.items():
            if counter < len(self.loss_names):
                plt.plot(val, color=colors[counter])
            else:
                plt.plot(val, color=colors[counter])
            counter += 1
            
        plt.title(self.title)
        plt.legend(self.loss_names)
        plt.axhline(y=0, color='grey', alpha = .1)
        plt.xlabel('Epoch')
        plt.show()
        
    @staticmethod
    def info():
        print('* Visualize Model Training Ancient Library *\n')
        print('Class kwargs init parameters:')
        print('display: 5, max_iter: 100, graph: True, time_type: min, bar_size: 40, loss_names, title, round: 3')
        print('\nClass call:')
        print('[losses as list]')
        