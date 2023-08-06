import os
import time
import torch
import logging
import pandas as pd 
from torchstat import ModelStat

class Prof:
    """Prof the dnn stage time and dnn param、 flops and memrw.

    no returns write the prof to log file.

    """

    """
    eg.
    prof = Prof(10, 30)
    prof.profit(model, (3, 224, 224))
    for step, data in enumerate(trainloader):
        prof.timeit(step, 'data load') #data
        inputs, labels = data[0].cuda(), data[1].cuda(); prof.timeit(step, 'h2d') #h2d
        outputs = model(inputs); prof.timeit(step, 'forward') #forward
        loss = criterion(outputs, labels); prof.timeit(step, 'loss') #loss
        optimizer.zero_grad(); prof.timeit(step, 'zero grad') #zero grad
        loss.backward(); prof.timeit(step, 'backward') #backward
        optimizer.step(); prof.timeit(step, 'optim') #optim

    """
    def __init__(self, start_prof, end_prof, prof_log_path = ''):
        # vaild
        if start_prof > end_prof: # assert start_prof < end_prof
            raise ValueError('start must <= end')
        if (start_prof - 1) < 0: # assert (start_prof - 1) >= 0
            raise ValueError('start - 1 must > 0. because we from start - 1 strat init')

        # prof path
        if prof_log_path != '':
            self.prof_log_path = prof_log_path
        else:
            proc_path = '/proc/self/cgroup'
            uid_path_base = '/k4s/config'
            uid_path_file_name = 'profile.config'
            with open(proc_path, "r", encoding = "utf-8") as file:
                proc_ = file.read()
                proc = proc_.splitlines()[0]
                pod_uid_ = proc.split('/')[-2]
                pod_uid = pod_uid_[3:]
                self.prof_log_path = os.path.join(uid_path_base, pod_uid, uid_path_file_name)

        # logger
        logger= logging.getLogger('prof log')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(self.prof_log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # attribute
        self.logger = logger
        self.log = 'prof log'
        self.last = time.perf_counter()
        self.start_prof = start_prof
        self.end_prof = end_prof
        
    # time
    def timeit(self, step, stage="unnamed"):
        if step >= self.start_prof - 1 and step <= self.end_prof:
            torch.cuda.synchronize()
            now = time.perf_counter()
            interval = now - self.last
            self.last = now
            self.log += f'{stage}:{interval:0.5f}|'
            if stage == 'optim':
                self.logger.info(self.log) if step != self.start_prof - 1 else None
                self.log = ''

    # flops, bytes, memory
    def profit(self, model, input_size):
        # 0. backup call
        _origin_call = dict()
        for module in model.modules():
            if len(list(module.children())) == 0 and module.__class__ not in _origin_call:
                _origin_call[module.__class__] = module.__class__.__call__

        # 1. profile 
        model.cpu()
        ms = ModelStat(model=model, input_size=input_size, query_granularity=1)
        collected_nodes = ms._analyze_model()

        # 2. log
        param, memory, madd, flops, duration, mread, mwrite, memrw = report_format(collected_nodes)
        prof_log = f'param:{param:0.5f}|memory:{memory:0.5f}|madd:{madd:0.5f}|flops:{flops:0.5f}|mread:{mread:0.5f}|mwrite:{mwrite:0.5f}|memrw:{memrw:0.5f}|'
        self.logger.info(prof_log)

        # 3. resume
        # init call
        for module in model.modules():
            if len(list(module.children())) == 0:
                module.__class__.__call__ = _origin_call[module.__class__]
        model.train()
        model.cuda()
        model.apply(register_buffer)

def register_buffer(module):
    assert isinstance(module, torch.nn.Module)

    if len(list(module.children())) > 0:
        return

    del module._buffers["input_shape"]
    del module._buffers["output_shape"]
    del module._buffers["parameter_quantity"]
    del module._buffers["inference_memory"]
    del module._buffers["MAdd"]
    del module._buffers["duration"]
    del module._buffers["Flops"]
    del module._buffers["Memory"]

def report_format(collected_nodes):
    data = list()
    for node in collected_nodes:
        name = node.name
        input_shape = ' '.join(['{:>3d}'] * len(node.input_shape)).format(
            *[e for e in node.input_shape])
        output_shape = ' '.join(['{:>3d}'] * len(node.output_shape)).format(
            *[e for e in node.output_shape])
        parameter_quantity = node.parameter_quantity
        inference_memory = node.inference_memory
        MAdd = node.MAdd
        Flops = node.Flops
        mread, mwrite = [i for i in node.Memory]
        duration = node.duration
        data.append([name, input_shape, output_shape, parameter_quantity,
                     inference_memory, MAdd, duration, Flops, mread,
                     mwrite])
    df = pd.DataFrame(data)
    df.columns = ['module name', 'input shape', 'output shape',
                  'params', 'memory(MB)',
                  'MAdd', 'duration', 'Flops', 'MemRead(B)', 'MemWrite(B)']
    df['duration[%]'] = df['duration'] / (df['duration'].sum() + 1e-7)
    df['MemR+W(B)'] = df['MemRead(B)'] + df['MemWrite(B)']
    total_parameters_quantity = df['params'].sum()
    total_memory = df['memory(MB)'].sum()
    total_operation_quantity = df['MAdd'].sum()
    total_flops = df['Flops'].sum()
    total_duration = df['duration[%]'].sum()
    total_mread = df['MemRead(B)'].sum()
    total_mwrite = df['MemWrite(B)'].sum()
    total_memrw = df['MemR+W(B)'].sum()
    return total_parameters_quantity, total_memory, total_operation_quantity, \
            total_flops, total_duration, total_mread, total_mwrite, total_memrw