## Keyframe blending

Once we have all the key frames, we need to arrange them (in a chronological order) to form a tapestry. The naive approach is to join the frames. For example:

![Naive approach](https://github.com/melvin15may/interest-frame/blob/develop/public/naive.jpg)

To blend the keyframes further we can remove the most obvious colors like the black top and bottom borders. For example:

![Naive approach2](https://github.com/melvin15may/interest-frame/blob/develop/public/naive2.jpg)

Both the above approaches do not form a tapestry but rather a larger image formed by joining other images (not blending).  We can change this by performing seam carving on this larger image to try and blend them. In seam carving, our goal is to remove unnoticeable pixels
that blend with their surroundings. Hence the energy is calculated by sum the absolute value of the gradient in both x direction and y direction for all three channel (B, G, R). Energy map is a 2D image with the same dimension as input image. We then delete the seam with the lowest energy. The output after seam carving is as follows:

![Seam carving](https://github.com/melvin15may/interest-frame/blob/develop/public/seam.jpg)

In the above seam carved image, you can see that some of the important objects have been distorted. This is because we haven't mentioned explicitly that those objects are important. Furthermore, how do we identify important objects? We define importance of an object based on human eye fixations. To predict human eye fixation in a frame we use a LSTM-based [Saliency Attentive Model](https://github.com/marcellacornia/sam).

![SAM](https://raw.githubusercontent.com/marcellacornia/sam/master/figs/model.jpg)

For example,

**INPUT**

![input](https://github.com/melvin15may/interest-frame/blob/develop/public/sam_input.jpg)

**OUTPUT**

![output](https://github.com/melvin15may/interest-frame/blob/develop/public/sam_output.jpg)

**MASK** created from output after thresholding (Threshold value is 50)

![mask](https://github.com/melvin15may/interest-frame/blob/develop/public/sam_mask.jpg)

This neural network gives us a saliency map which can be used as a mask (after thresholding) in the seam carving process. The energy values in the masked area will be multiplied by a very high constant value so it never has a low energy value and hence that seam won't be selected. The output of seam carving with masking:

![final](https://github.com/melvin15may/interest-frame/blob/develop/public/final.jpg)


