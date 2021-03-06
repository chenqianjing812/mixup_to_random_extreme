import numpy as np
import torch


def mixup_data(x, y, alpha=1.0, use_cuda=True):
    '''Returns mixed inputs, pairs of targets, and lambda'''
    # print("x_size",x.size())   #x_size torch.Size([128, 3, 32, 32])
    if alpha > 0:
        lam = np.random.beta(alpha, alpha,x.size()[1]*x.size()[2]*x.size()[3])
    else:
        lam = 1
    lam_average = np.mean(lam)
    lam = lam.reshape((x.size()[1],x.size()[2],x.size()[3]))  #把lam resize 成图片的大小
    lam_ = 1 - lam
    

    batch_size = x.size()[0]
    if use_cuda:
        index = torch.randperm(batch_size).cuda()
        lam_ = torch.from_numpy(lam_).cuda()
        lam = torch.from_numpy(lam).cuda()
    else:
        index = torch.randperm(batch_size)
        lam_ = torch.from_numpy(lam_)
        lam = torch.from_numpy(lam)
    # mixed_x = lam * x + (1 - lam) * x[index, :]
    mixed_x = x.mul(lam) +  x[index, :].mul(lam_)
    y_a, y_b = y, y[index]
    return mixed_x, y_a, y_b, lam_average


def mixup_criterion(criterion, pred, y_a, y_b, lam):
    return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)