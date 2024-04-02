#ifndef MOTION_H
#define MOTION_H

static void decode_motion_vector
(int *pred, int r_size, int motion_code,
	      int motion_residualesidual, int full_pel_vector);

void motion_vector(int *PMV, int *dmvector, int h_r_size, int v_r_size, int dmv,
	      int mvscale, int full_pel_vector);

void
motion_vectors (int PMV[2][2][2], int dmvector[2], int motion_vertical_field_select[2][2], int s,
		int motion_vector_count, int mv_format, int h_r_size, int v_r_size, int dmv,
		int mvscale);

#endif
