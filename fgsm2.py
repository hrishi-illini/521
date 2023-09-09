import torch
import torch.nn as nn


# fix seed so that random initialization always performs the same 
torch.manual_seed(1)


# create the model N as described in the question
N = nn.Sequential(nn.Linear(10, 10, bias=False),
                  nn.ReLU(),
                  nn.Linear(10, 10, bias=False),
                  nn.ReLU(),
                  nn.Linear(10, 3, bias=False))

# random input
x = torch.rand((1,10)) # the first dimension is the batch size; the following dimensions the actual dimension of the data
x.requires_grad_() # this is required so we can compute the gradient w.r.t x

t = 0 # target class

# The network N classfies x as belonging to class 2
original_class = N(x).argmax(dim=1).item()  # TO LEARN: make sure you understand this expression
print("Original Class: ", original_class)
assert(original_class == 2)

# compute gradient
# note that CrossEntropyLoss() combines the cross-entropy loss and an implicit softmax function
L = nn.CrossEntropyLoss()
loss = L(N(x), torch.tensor([t], dtype=torch.long)) # TO LEARN: make sure you understand this line
loss.backward()

# your code here
# adv_x should be computed from x according to the fgsm-style perturbation such that the new class of xBar is the target class t above
# hint: you can compute the gradient of the loss w.r.t to x as x.grad

# adv_x = x - eps*torch.sign((x.grad))
# This finds a close enough adv_x that is classified as 1 instead of 2. We wish to target 0 instead. 
# Iterative FGSM:
epsReal = 0.2 #depending on your data this might be large or small
eps = epsReal - 1e-7 # small constant to offset floating-point erros
adv_x = x
adv_x.retain_grad()
clip_range = 0.5
clip_min = x - clip_range
clip_max = x + clip_range
for i in range(9):
    adv_x = torch.clamp( adv_x - eps*torch.sign(adv_x.grad), min = clip_min, max = clip_max)
    loss = L(N(adv_x), torch.tensor([t], dtype=torch.long)) # TO LEARN: make sure you understand this line
    adv_x.retain_grad()
    loss.backward(retain_graph=True)
    new_class = N(adv_x).argmax(dim=1).item()
    if new_class == t:
        # print(i)
        break

print("New Class: ", new_class)
# new_class = N(adv_x).argmax(dim=1).item()
assert(new_class == t)
# it is not enough that adv_x is classified as t. We also need to make sure it is 'close' to the original x.
assert( torch.norm((x-adv_x), p=float('inf')) <= clip_range)