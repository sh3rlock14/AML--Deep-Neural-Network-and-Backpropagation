from __future__ import print_function

from builtins import range
from builtins import object
import numpy as np
import matplotlib.pyplot as plt
try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3



class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network. The net has an input dimension of
    N, a hidden layer dimension of H, and performs classification over C classes.
    We train the network with a softmax loss function and L2 regularization on the
    weight matrices. The network uses a ReLU nonlinearity after the first fully
    connected layer.

    In other words, the network has the following architecture:

    input - fully connected layer - ReLU - fully connected layer - softmax

    The outputs of the second fully-connected layer are the scores for each class.
    """



    def __init__(self, input_size, hidden_size, output_size, std=1e-4):
        """
        Initialize the model. Weights are initialized to small random values and
        biases are initialized to zero. Weights and biases are stored in the
        variable self.params, which is a dictionary with the following keys:

        W1: First layer weights; has shape (D, H)
        b1: First layer biases; has shape (H,)
        W2: Second layer weights; has shape (H, C)
        b2: Second layer biases; has shape (C,)

        Inputs:
        - input_size: The dimension D of the input data.
        - hidden_size: The number of neurons H in the hidden layer.
        - output_size: The number of classes C.
        """
        
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)



    def loss(self, X, y=None, reg=0.0):
        """
        Compute the loss and gradients for a two-layer fully connected neural
        network.

        Inputs:
        - X: Input data of shape (N, D). Each X[i] is a training sample.
        - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
          an integer in the range 0 <= y[i] < C. This parameter is optional; if it
          is not passed then we only return scores, and if it is passed then we
          instead return the loss and gradients.
        - reg: Regularization strength.

        Returns:
        If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
        the score for class c on input X[i].

        If y is not None, instead return a tuple of:
        - loss: Loss (data loss and regularization loss) for this batch of training
          samples.
        - grads: Dictionary mapping parameter names to gradients of those parameters
          with respect to the loss function; has the same keys as self.params.
        """
        
        # Unpack variables from the params dictionary

        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N, D = X.shape

        # Compute the forward pass
        scores = 0.
        
        #############################################################################
        # TODO: Perform the forward pass, computing the class probabilities for the #
        # input. Store the result in the scores variable, which should be an array  #
        # of shape (N, C).                                                          #
        #############################################################################
        
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Input and Weights concatenations
        # Input and Weights concatenations
        x0 = np.ones((N, 1))  # dummy variable
        a1 = np.concatenate((x0, X), axis=1)
        b1 = np.reshape(b1, (1, -1))  # prepare for concatenation
        W1 = np.concatenate((b1, W1), axis=0)

        # Define the Activation Functions
        ReLU = lambda x: np.where(x >= 0, x, 0)
        Softmax = lambda x: np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

        # Perform the 1st Linear Operation + Activation
        z2 = np.dot(a1, W1)
        a2 = ReLU(z2)  # np.where(z2>=0, z2, 0)
        x02 = np.ones((a2.shape[0], 1))
        a2 = np.concatenate((x02, a2), axis=1)

        # Perform the 2nd Linear Operation
        W2 = np.concatenate((np.reshape(b2, (1, -1)), W2), axis=0)
        z3 = np.dot(a2, W2)

        # Apply the Softmax
        a3 = Softmax(z3)  # np.exp(z3) / np.sum(np.exp(z3),axis=1, keepdims=True)

        scores = a3

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****


        # If the targets are not given then jump out, we're done
        if y is None:
            return scores


        # Compute the loss
        loss = 0.
        
        #############################################################################
        # TODO: Finish the forward pass, and compute the loss. This should include  #
        # both the data loss and L2 regularization for W1 and W2. Store the result  #
        # in the variable loss, which should be a scalar. Use the Softmax           #
        # classifier loss.                                                          #
        #############################################################################
        
        # Implement the loss for the softmax output layer
        
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        J = -np.log(a3[np.arange(a3.shape[0]), y])  # compute the loss for ALL the input sample in X

        loss_no_reg = np.sum(J) / N  # Average over the whole training set
        loss = loss_no_reg + reg * (np.sum(np.square(W1)) + np.sum(np.square(W2)))  # Add the L2 regularization term

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        # Backward pass: compute gradients
        grads = {}

        ##############################################################################
        # TODO: Implement the backward pass, computing the derivatives of the weights#
        # and biases. Store the results in the grads dictionary. For example,        #
        # grads['W1'] should store the gradient on W1, and be a matrix of same size  #
        ##############################################################################

        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        softmax = a3
        KrenckorDelta = np.zeros((5, 3))

        for dp in range(N):  # For every datapoint, create its class hot-encoding
            KrenckorDelta[dp, y[dp]] = 1

        softmax_grad = (1/N)*(softmax - KrenckorDelta)
        grads['W2'] = (((np.array(a2[:, 1:a2.shape[1]]).transpose()).dot(softmax_grad))) + (2 * reg * W2[1:W2.shape[0], :])
        grads['b2'] = np.sum(softmax_grad, axis=0)

        """ THIS SNIPPET IMPLEMENTS THE DERIVATIONS WE MADE ON "PAPER" JUST TO VERIFY THE CORRECTNESS OF THE IMPLICIT MULTIPLICATION
        c = b2.shape[0]
        dawb = np.zeros((1,c,N,c))
        dbb = np.zeros((1,c,1,c))
        dbb[:,np.arange(3),:,np.arange(3)] = 1
        tmp = (dawb + dbb)
        grads['b2tmp'] = np.einsum("abcd, cd -> ab",tmp,softmax_grad)

        """
        dReLU = lambda x: np.where(x > 0, 1, 0)
        ReLUHadamard = lambda a,x : np.where(a>0, x, 0)
        
        runMattia = True
                              ### CODICE DI MATTIA ###
        if runMattia:
          tmp1 = ReLUHadamard(a2[:,1:], softmax_grad@W2[1:,:].transpose()) # slide 107: invece di calcolare la jacobiana, utilizzo la ReLUHadamard
          tmp3 = X.transpose().dot(tmp1) + (2*reg*W1[1:, :])

          grads["W1"] = tmp3 

          grads["b1"] = np.sum(tmp1, axis=0)
        
        else: 

                                ### CODICE DI ANTONIO ###
          partial1 = softmax_grad.dot(np.array(W2[1:, :]).transpose())
          partial2 = partial1 * dReLU(a2[:,1:])  # this is correct

          grads['W1'] = ((np.array(X).transpose()).dot(partial2)) + (2*reg*W1[1:, :])
          grads['b1'] = np.sum(partial2 / N, axis=0)

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return loss, grads



    def train(self, X, y, X_val, y_val,
              learning_rate=1e-3, learning_rate_decay=0.95,
              reg=5e-6, num_iters=100,
              batch_size=200, verbose=False):
        """
        Train this neural network using stochastic gradient descent.

        Inputs:
        - X: A numpy array of shape (N, D) giving training data.
        - y: A numpy array of shape (N,) giving training labels; y[i] = c means that
          X[i] has label c, where 0 <= c < C.
        - X_val: A numpy array of shape (N_val, D) giving validation data.
        - y_val: A numpy array of shape (N_val,) giving validation labels.
        - learning_rate: Scalar giving learning rate for optimization.
        - learning_rate_decay: Scalar giving factor used to decay the learning rate
          after each epoch.
        - reg: Scalar giving regularization strength.
        - num_iters: Number of steps to take when optimizing.
        - batch_size: Number of training examples to use per step.
        - verbose: boolean; if true print progress during optimization.
        """
        
        num_train = X.shape[0]
        iterations_per_epoch = max( int(num_train // batch_size), 1)


        # Use SGD to optimize the parameters in self.model
        loss_history = []
        train_acc_history = []
        val_acc_history = []

        for it in range(num_iters):
            X_batch = X
            y_batch = y

            #########################################################################
            # TODO: Create a random minibatch of training data and labels, storing  #
            # them in X_batch and y_batch respectively.                             #
            #########################################################################
            
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            
            
            
            pass
        
            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

            # Compute loss and gradients using the current minibatch
            loss, grads = self.loss(X_batch, y=y_batch, reg=reg)
            loss_history.append(loss)

            #########################################################################
            # TODO: Use the gradients in the grads dictionary to update the         #
            # parameters of the network (stored in the dictionary self.params)      #
            # using stochastic gradient descent. You'll need to use the gradients   #
            # stored in the grads dictionary defined above.                         #
            #########################################################################
            
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            
            
            
            pass
        
            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

            if verbose and it % 100 == 0:
                print('iteration %d / %d: loss %f' % (it, num_iters, loss))

            # At every epoch check train and val accuracy and decay learning rate.
            if it % iterations_per_epoch == 0:
                # Check accuracy
                train_acc = (self.predict(X_batch) == y_batch).mean()
                val_acc = (self.predict(X_val) == y_val).mean()
                train_acc_history.append(train_acc)
                val_acc_history.append(val_acc)

                # Decay learning rate
                learning_rate *= learning_rate_decay

        return {
          'loss_history': loss_history,
          'train_acc_history': train_acc_history,
          'val_acc_history': val_acc_history,
        }



    def predict(self, X):
        """
        Use the trained weights of this two-layer network to predict labels for
        data points. For each data point we predict scores for each of the C
        classes, and assign each data point to the class with the highest score.

        Inputs:
        - X: A numpy array of shape (N, D) giving N D-dimensional data points to
          classify.

        Returns:
        - y_pred: A numpy array of shape (N,) giving predicted labels for each of
          the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
          to have class c, where 0 <= c < C.
        """
        y_pred = None

        ###########################################################################
        # TODO: Implement this function; it should be VERY simple!                #
        ###########################################################################
        
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****



        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        return y_pred


