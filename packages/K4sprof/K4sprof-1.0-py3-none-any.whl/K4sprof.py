import os
import time
import torch
import logging
from torchstat import ModelStat
from util import report_format

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
    def timeit(self, step, stage):
        if step >= self.start_prof - 1 and step <= self.end_prof:
            torch.cuda.synchronize()
            now = time.perf_counter()
            interval = now - self.last
            self.last = now
            self.log += f'{stage}:{interval:0.5f}|'
            if stage == 'optim':
                self.logger.info(self.log) if step != self.start_prof - 1 else None
                self.log = f'{step + 1} ==> '

    # flops, bytes, memory
    def profit(self, model, input_size):
        model.cpu()
        ms = ModelStat(model=model, input_size=input_size, query_granularity=1)
        collected_nodes = ms._analyze_model()
        param, memory, madd, flops, duration, mread, mwrite, memrw = report_format(collected_nodes)
        prof_log = f'param:{param:0.5f}|memory:{memory:0.5f}|madd:{madd:0.5f}|flops:{flops:0.5f}|mread:{mread:0.5f}|mwrite:{mwrite:0.5f}|memrw:{memrw:0.5f}|'
        self.logger.info(prof_log)
