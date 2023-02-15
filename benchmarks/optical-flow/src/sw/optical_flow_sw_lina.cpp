/*===============================================================*/
/*                                                               */
/*                     optical_flow_sw.cpp                       */
/*                                                               */
/*              Software version for optical flow.               */
/*                                                               */
/*===============================================================*/
#define SW
#include "optical_flow_sw.h"
#include <cstdio>
#include <cstdlib>
// compute x, y gradient
void gradient_xy_calc(pixel_t frame[MAX_HEIGHT][MAX_WIDTH],
    pixel_t gradient_x[MAX_HEIGHT][MAX_WIDTH],
    pixel_t gradient_y[MAX_HEIGHT][MAX_WIDTH])
{
  pixel_t x_grad, y_grad;
  gradient_xy_calc_label0:for (int r = 0; r < MAX_HEIGHT + 2; r ++ )
  {
	gradient_xy_calc_label1:for (int c = 0; c < MAX_WIDTH + 2; c ++)
    {
      x_grad = 0;
      y_grad = 0;
      if (r >= 4 && r < MAX_HEIGHT && c >= 4 && c < MAX_WIDTH)
      {
        gradient_xy_calc_label2:for (int i = 0; i < 5; i++)
        {
          x_grad += frame[r-2][c-i] * GRAD_WEIGHTS[4-i];
          y_grad += frame[r-i][c-2] * GRAD_WEIGHTS[4-i];
        }
        gradient_x[r-2][c-2] = x_grad / 12;
        gradient_y[r-2][c-2] = y_grad / 12;
      }
      else if (r >= 2 && c >= 2)
      {
        gradient_x[r-2][c-2] = 0;
        gradient_y[r-2][c-2] = 0;
      }
    }
  }
}

// compute z gradient
void gradient_z_calc(pixel_t frame0[MAX_HEIGHT][MAX_WIDTH], 
                     pixel_t frame1[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame2[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame3[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame4[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t gradient_z[MAX_HEIGHT][MAX_WIDTH])
{
  gradient_z_calc_label3:for (int r = 0; r < MAX_HEIGHT; r ++)
  {
    gradient_z_calc_label4:for (int c = 0; c < MAX_WIDTH; c ++)
    {
      gradient_z[r][c] = 0.0f;
      gradient_z[r][c] += frame0[r][c] * GRAD_WEIGHTS[0]; 
      gradient_z[r][c] += frame1[r][c] * GRAD_WEIGHTS[1]; 
      gradient_z[r][c] += frame2[r][c] * GRAD_WEIGHTS[2]; 
      gradient_z[r][c] += frame3[r][c] * GRAD_WEIGHTS[3]; 
      gradient_z[r][c] += frame4[r][c] * GRAD_WEIGHTS[4]; 
      gradient_z[r][c] /= 12.0f;
    }
  }
}

// compute y weight
void gradient_weight_y(pixel_t gradient_x[MAX_HEIGHT][MAX_WIDTH],
                       pixel_t gradient_y[MAX_HEIGHT][MAX_WIDTH],
                       pixel_t gradient_z[MAX_HEIGHT][MAX_WIDTH],
                       gradient_t filt_grad[MAX_HEIGHT][MAX_WIDTH])
{
  gradient_weight_y_label5:for (int r = 0; r < MAX_HEIGHT + 3; r ++)
  {
    gradient_weight_y_label6:for (int c = 0; c < MAX_WIDTH; c ++)
    {
      gradient_t acc;
      acc.x = 0;
      acc.y = 0;
      acc.z = 0;
      if (r >= 6 && r < MAX_HEIGHT)
      { 
        gradient_weight_y_label7:for (int i = 0; i < 7; i ++)
        {
          acc.x += gradient_x[r-i][c] * GRAD_FILTER[i];
          acc.y += gradient_y[r-i][c] * GRAD_FILTER[i];
          acc.z += gradient_z[r-i][c] * GRAD_FILTER[i];
        }
        filt_grad[r-3][c] = acc;            
      }
      else if (r >= 3)
      {
        filt_grad[r-3][c] = acc;
      }
    }
  }
}

// compute x weight
void gradient_weight_x(gradient_t y_filt[MAX_HEIGHT][MAX_WIDTH],
                       gradient_t filt_grad[MAX_HEIGHT][MAX_WIDTH])
{
  gradient_weight_x_label8:for (int r = 0; r < MAX_HEIGHT; r ++)
  {
    gradient_weight_x_label9:for (int c = 0; c < MAX_WIDTH + 3; c ++)
    {
      gradient_t acc;
      acc.x = 0;
      acc.y = 0;
      acc.z = 0;
      if (c >= 6 && c < MAX_WIDTH)
      {
        gradient_weight_x_label10:for (int i = 0; i < 7; i ++)
        {
          acc.x += y_filt[r][c-i].x * GRAD_FILTER[i];
          acc.y += y_filt[r][c-i].y * GRAD_FILTER[i];
          acc.z += y_filt[r][c-i].z * GRAD_FILTER[i];
        }
        filt_grad[r][c-3] = acc;
      }
      else if (c >= 3)
      {
        filt_grad[r][c-3] = acc;
      }
    }
  }
}
 
// outer product
void outer_product(gradient_t gradient[MAX_HEIGHT][MAX_WIDTH],
                   outer_t outer_product[MAX_HEIGHT][MAX_WIDTH])
{ 
  outer_product_label11:for (int r = 0; r < MAX_HEIGHT; r ++)
  {
    outer_product_label12:for (int c = 0; c < MAX_WIDTH; c ++)
    {
      gradient_t grad = gradient[r][c];
      outer_t out;
      out.val[0] = grad.x * grad.x;
      out.val[1] = grad.y * grad.y;
      out.val[2] = grad.z * grad.z;
      out.val[3] = grad.x * grad.y;
      out.val[4] = grad.x * grad.z;
      out.val[5] = grad.y * grad.z;
      outer_product[r][c] = out;
    }
  }
}

// tensor weight y
void tensor_weight_y(outer_t outer[MAX_HEIGHT][MAX_WIDTH],
                     tensor_t tensor_y[MAX_HEIGHT][MAX_WIDTH])
{
  tensor_weight_y_label13:for (int r = 0; r < MAX_HEIGHT + 1; r ++)
  {
    tensor_weight_y_label14:for(int c = 0; c < MAX_WIDTH; c ++)
    {
      tensor_t acc;
      tensor_weight_y_label15:for (int k = 0; k < 6; k ++)
      {
        acc.val[k] = 0;
      }

      if (r >= 2 && r < MAX_HEIGHT) 
      {
        tensor_weight_y_label16:for (int i = 0; i < 3; i ++)
        {
          tensor_weight_y_label17:for(int component = 0; component < 6; component ++)
          {
            acc.val[component] += outer[r-i][c].val[component] * TENSOR_FILTER[i];
          }
        }
      }
      if (r >= 1)
      { 
        tensor_y[r-1][c] = acc;            
      }
    }
  }
}

// tensor weight x
void tensor_weight_x(tensor_t tensor_y[MAX_HEIGHT][MAX_WIDTH],
                     tensor_t tensor[MAX_HEIGHT][MAX_WIDTH])
{
  tensor_weight_x_label18:for (int r = 0; r < MAX_HEIGHT; r ++)
  {
    tensor_weight_x_label19:for (int c = 0; c < MAX_WIDTH + 1; c ++)
    {
      tensor_t acc;
      tensor_weight_x_label20:for(int k = 0; k < 6; k++)
      {
        acc.val[k] = 0;
      }
      if (c >= 2 && c < MAX_WIDTH) 
      {
        tensor_weight_x_label21:for (int i = 0; i < 3; i ++)
        {
          tensor_weight_x_label22:for (int component = 0; component < 6; component ++)
          {
            acc.val[component] += tensor_y[r][c-i].val[component] * TENSOR_FILTER[i];
          }
        }
      }
      if (c >= 1)
      {
        tensor[r][c-1] = acc;
      }
    }
  }
}

// compute flow
void flow_calc(tensor_t tensors[MAX_HEIGHT][MAX_WIDTH],
               velocity_t output[MAX_HEIGHT][MAX_WIDTH])
{
  flow_calc_label23:for(int r = 0; r < MAX_HEIGHT; r ++)
  {
    flow_calc_label24:for(int c = 0; c < MAX_WIDTH; c ++)
    {
      if (r >= 2 && r < MAX_HEIGHT - 2 && c >= 2 && c < MAX_WIDTH - 2)
      {
        pixel_t denom = tensors[r][c].val[0] * tensors[r][c].val[1] -
                        tensors[r][c].val[3] * tensors[r][c].val[3];
        output[r][c].x = (tensors[r][c].val[5] * tensors[r][c].val[3] -
                          tensors[r][c].val[4] * tensors[r][c].val[1]) / denom;
        output[r][c].y = (tensors[r][c].val[4] * tensors[r][c].val[3] -
                          tensors[r][c].val[5] * tensors[r][c].val[0]) / denom;
      }
      else
      {
        output[r][c].x = 0;
        output[r][c].y = 0;
      }
    }
  }
}

// top-level sw function
void optical_flow_sw(pixel_t frame0[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame1[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame2[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame3[MAX_HEIGHT][MAX_WIDTH],
                     pixel_t frame4[MAX_HEIGHT][MAX_WIDTH],
                     velocity_t outputs[MAX_HEIGHT][MAX_WIDTH])
{
  // intermediate arrays
  static pixel_t gradient_x[MAX_HEIGHT][MAX_WIDTH];
  static pixel_t gradient_y[MAX_HEIGHT][MAX_WIDTH];
  static pixel_t gradient_z[MAX_HEIGHT][MAX_WIDTH];
  static gradient_t y_filtered[MAX_HEIGHT][MAX_WIDTH];
  static gradient_t filtered_gradient[MAX_HEIGHT][MAX_WIDTH];
  static outer_t out_product[MAX_HEIGHT][MAX_WIDTH];
  static tensor_t tensor_y[MAX_HEIGHT][MAX_WIDTH];
  static tensor_t tensor[MAX_HEIGHT][MAX_WIDTH];

  // compute
  //gradient_xy_calc(frame2, gradient_x, gradient_y);
  {
    pixel_t x_grad, y_grad;
    gradient_xy_calc_label0:for (int r = 0; r < MAX_HEIGHT + 2; r ++ )
    {
    gradient_xy_calc_label1:for (int c = 0; c < MAX_WIDTH + 2; c ++)
      {
        x_grad = 0;
        y_grad = 0;
        if (r >= 4 && r < MAX_HEIGHT && c >= 4 && c < MAX_WIDTH)
        {
          gradient_xy_calc_label2:for (int i = 0; i < 5; i++)
          {
            x_grad += frame2[r-2][c-i] * GRAD_WEIGHTS[4-i];
            y_grad += frame2[r-i][c-2] * GRAD_WEIGHTS[4-i];
          }
          gradient_x[r-2][c-2] = x_grad / 12;
          gradient_y[r-2][c-2] = y_grad / 12;
        }
        else if (r >= 2 && c >= 2)
        {
          gradient_x[r-2][c-2] = 0;
          gradient_y[r-2][c-2] = 0;
        }
      }
    }
  }
  //gradient_z_calc(frame0, frame1, frame2, frame3, frame4, gradient_z);
  {
    gradient_z_calc_label3:for (int r = 0; r < MAX_HEIGHT; r ++)
    {
      gradient_z_calc_label4:for (int c = 0; c < MAX_WIDTH; c ++)
      {
        gradient_z[r][c] = 0.0f;
        gradient_z[r][c] += frame0[r][c] * GRAD_WEIGHTS[0]; 
        gradient_z[r][c] += frame1[r][c] * GRAD_WEIGHTS[1]; 
        gradient_z[r][c] += frame2[r][c] * GRAD_WEIGHTS[2]; 
        gradient_z[r][c] += frame3[r][c] * GRAD_WEIGHTS[3]; 
        gradient_z[r][c] += frame4[r][c] * GRAD_WEIGHTS[4]; 
        gradient_z[r][c] /= 12.0f;
      }
    }
  } 
  //gradient_weight_y(gradient_x, gradient_y, gradient_z, y_filtered);
  {
    gradient_weight_y_label5:for (int r = 0; r < MAX_HEIGHT + 3; r ++)
    {
      gradient_weight_y_label6:for (int c = 0; c < MAX_WIDTH; c ++)
      {
        gradient_t acc;
        acc.x = 0;
        acc.y = 0;
        acc.z = 0;
        if (r >= 6 && r < MAX_HEIGHT)
        { 
          gradient_weight_y_label7:for (int i = 0; i < 7; i ++)
          {
            acc.x += gradient_x[r-i][c] * GRAD_FILTER[i];
            acc.y += gradient_y[r-i][c] * GRAD_FILTER[i];
            acc.z += gradient_z[r-i][c] * GRAD_FILTER[i];
          }
          y_filtered[r-3][c] = acc;            
        }
        else if (r >= 3)
        {
          y_filtered[r-3][c] = acc;
        }
      }
    }
  }
  //gradient_weight_x(y_filtered, filtered_gradient);
  {
    gradient_weight_x_label8:for (int r = 0; r < MAX_HEIGHT; r ++)
    {
      gradient_weight_x_label9:for (int c = 0; c < MAX_WIDTH + 3; c ++)
      {
        gradient_t acc;
        acc.x = 0;
        acc.y = 0;
        acc.z = 0;
        if (c >= 6 && c < MAX_WIDTH)
        {
          gradient_weight_x_label10:for (int i = 0; i < 7; i ++)
          {
            acc.x += y_filtered[r][c-i].x * GRAD_FILTER[i];
            acc.y += y_filtered[r][c-i].y * GRAD_FILTER[i];
            acc.z += y_filtered[r][c-i].z * GRAD_FILTER[i];
          }
          filtered_gradient[r][c-3] = acc;
        }
        else if (c >= 3)
        {
          filtered_gradient[r][c-3] = acc;
        }
      }
    }
  }
  //outer_product(filtered_gradient, out_product);
  { 
    outer_product_label11:for (int r = 0; r < MAX_HEIGHT; r ++)
    {
      outer_product_label12:for (int c = 0; c < MAX_WIDTH; c ++)
      {
        gradient_t grad = filtered_gradient[r][c];
        outer_t out;
        out.val[0] = grad.x * grad.x;
        out.val[1] = grad.y * grad.y;
        out.val[2] = grad.z * grad.z;
        out.val[3] = grad.x * grad.y;
        out.val[4] = grad.x * grad.z;
        out.val[5] = grad.y * grad.z;
        out_product[r][c] = out;
      }
    }
  }
  //tensor_weight_y(out_product, tensor_y);
  {
    tensor_weight_y_label13:for (int r = 0; r < MAX_HEIGHT + 1; r ++)
    {
      tensor_weight_y_label14:for(int c = 0; c < MAX_WIDTH; c ++)
      {
        tensor_t acc;
        tensor_weight_y_label15:for (int k = 0; k < 6; k ++)
        {
          acc.val[k] = 0;
        }

        if (r >= 2 && r < MAX_HEIGHT) 
        {
          tensor_weight_y_label16:for (int i = 0; i < 3; i ++)
          {
            tensor_weight_y_label17:for(int component = 0; component < 6; component ++)
            {
              acc.val[component] += out_product[r-i][c].val[component] * TENSOR_FILTER[i];
            }
          }
        }
        if (r >= 1)
        { 
          tensor_y[r-1][c] = acc;            
        }
      }
    }
  }
  //tensor_weight_x(tensor_y, tensor);
  {
    tensor_weight_x_label18:for (int r = 0; r < MAX_HEIGHT; r ++)
    {
      tensor_weight_x_label19:for (int c = 0; c < MAX_WIDTH + 1; c ++)
      {
        tensor_t acc;
        tensor_weight_x_label20:for(int k = 0; k < 6; k++)
        {
          acc.val[k] = 0;
        }
        if (c >= 2 && c < MAX_WIDTH) 
        {
          tensor_weight_x_label21:for (int i = 0; i < 3; i ++)
          {
            tensor_weight_x_label22:for (int component = 0; component < 6; component ++)
            {
              acc.val[component] += tensor_y[r][c-i].val[component] * TENSOR_FILTER[i];
            }
          }
        }
        if (c >= 1)
        {
          tensor[r][c-1] = acc;
        }
      }
    }
  }
  //flow_calc(tensor, outputs);
  {
    flow_calc_label23:for(int r = 0; r < MAX_HEIGHT; r ++)
    {
      flow_calc_label24:for(int c = 0; c < MAX_WIDTH; c ++)
      {
        if (r >= 2 && r < MAX_HEIGHT - 2 && c >= 2 && c < MAX_WIDTH - 2)
        {
          pixel_t denom = tensor[r][c].val[0] * tensor[r][c].val[1] -
                          tensor[r][c].val[3] * tensor[r][c].val[3];
          outputs[r][c].x = (tensor[r][c].val[5] * tensor[r][c].val[3] -
                            tensor[r][c].val[4] * tensor[r][c].val[1]) / denom;
          outputs[r][c].y = (tensor[r][c].val[4] * tensor[r][c].val[3] -
                            tensor[r][c].val[5] * tensor[r][c].val[0]) / denom;
        }
        else
        {
          outputs[r][c].x = 0;
          outputs[r][c].y = 0;
        }
      }
    }
  }
}
int main(){
  pixel_t frame0[MAX_HEIGHT][MAX_WIDTH];
  pixel_t frame1[MAX_HEIGHT][MAX_WIDTH];
  pixel_t frame2[MAX_HEIGHT][MAX_WIDTH];
  pixel_t frame3[MAX_HEIGHT][MAX_WIDTH];
  pixel_t frame4[MAX_HEIGHT][MAX_WIDTH];
  velocity_t outputs[MAX_HEIGHT][MAX_WIDTH];
  for(int i = 0; i<MAX_HEIGHT; i++)
	for(int j = 0; i<MAX_WIDTH; j++){
  	frame0[i][j] = i%MAX_HEIGHT + (rand()%100) ;
  	frame1[i][j] = j%MAX_HEIGHT + (rand()%100);
  	frame2[i][j] = (i+j)%MAX_HEIGHT + (rand()%100);
  	frame3[i][j] = (i+i)%MAX_HEIGHT + (rand()%100);
  	frame4[i][j] = (j+j)%MAX_HEIGHT + (rand()%100);
  	outputs[i][j].x = (rand()%150) ;
  	outputs[i][j].y = (rand()%100);
	}
  optical_flow_sw(frame0,frame1,frame2,frame3,frame4,outputs);
  return 0;
}

