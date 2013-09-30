#include <iostream>
#include <stdio.h>

#include <iostream>  //keystrokes and cout
#include <sstream>
#include <math.h>	// math
#include <time.h>	// profiling
#include <stdarg.h>
#include <stdlib.h>

#include <array_libraries.h>

void kick(	array2d<double>& own_velocities,
			array2d<double>& own_pos,
			array2d<double>& own_size,
			array2d<double>& pos,
			array2d<double>& velocities,
			array2d<double> size,
			array1d<double>& mass,
			int i,
			int j,
			int vel_idx,
			double bounciness,
			bool dynamic) {

	if (dynamic == true) { // swapping velocities
		double tmp;

		if (own_pos(vel_idx,i) < pos(vel_idx,j)) {
			own_pos(vel_idx,i) = own_pos(vel_idx,i) - 0.1*size(vel_idx,i);
			pos(vel_idx,j) = pos(vel_idx,j) + 0.1*size(vel_idx,j);
		}
		else {
			own_pos(vel_idx,i) = own_pos(vel_idx,i) + 0.1*size(vel_idx,i);
			pos(vel_idx,j) = pos(vel_idx,j) - 0.1*size(vel_idx,j);
		}

		int factor = 1;
		if (own_velocities(vel_idx,i) > 0 && velocities(vel_idx,j) > 0) {
			factor = -1;
		}
		else if (own_velocities(vel_idx,i) < 0 && velocities(vel_idx,j) < 0) {
			factor = -1;
		}
		tmp = own_velocities(vel_idx,i);
		own_velocities(vel_idx,i) = factor*(tmp*(mass(i) - mass(j)) + 2*mass(j)*velocities(vel_idx,j))/(mass(i) + mass(j));
		velocities(vel_idx,j) = (velocities(vel_idx,j)*(mass(j) - mass(i)) + 2*mass(i)*tmp)/(mass(i) + mass(j));
	}
	else {
		if (own_pos(vel_idx,i) < pos(vel_idx,j)) {
			own_pos(vel_idx,i) = own_pos(vel_idx,i) - 0.1*own_size(vel_idx,i);
		}
		else {
			own_pos(vel_idx,i) = own_pos(vel_idx,i) + 0.1*own_size(vel_idx,i);
		}

		own_velocities(vel_idx,i) *= -1*bounciness;
		own_velocities(vel_idx,i) += velocities(vel_idx,j);
	}
}


void collide(	array2d<double>& own_velocities,
				array2d<double>& own_pos,
				array2d<double>& own_size,
				array2d<double>& pos,
				array2d<double>& velocities,
				array2d<double>& size,
				array1d<double>& mass,
				int i,
				int j,
				int vel_idx,
				double bounciness,
				bool dynamic,
				bool static_on_dynamic,
				bool check_touching) {
	if (check_touching == true) {
		kick(own_velocities,own_pos,own_size,pos,velocities,size,mass,i,j,vel_idx,bounciness,dynamic);
		//printf("kick \n");
	}
	else {
		if (dynamic == true) { // swapping velocities
			double tmp;
			tmp = own_velocities(vel_idx,i);
			own_velocities(vel_idx,i) = bounciness*(tmp*(mass(i) - mass(j)) + 2*mass(j)*velocities(vel_idx,j))/(mass(i) + mass(j));
			velocities(vel_idx,j) = bounciness*(velocities(vel_idx,j)*(mass(j) - mass(i)) + 2*mass(i)*tmp)/(mass(i) + mass(j));
		}
		else { // reverse direction and get extra energy from static object if it moves
			if (static_on_dynamic == false) {
				own_velocities(vel_idx,i) *= -1*bounciness;
				own_velocities(0,i) += velocities(0,j);
				own_velocities(1,i) += 0.2*velocities(1,j);
				//printf("static bounce FROM DYN! %i %f %f %f %f \n", vel_idx, velocities(0,j),velocities(1,j),own_velocities(0,i) ,own_velocities(1,i));
			}
			else {
				velocities(vel_idx,j) *= -1*bounciness;
				velocities(0,j) += own_velocities(0,i);
				velocities(1,j) += 0.2*own_velocities(1,i);
				//printf("static bounce ON DYN! \n");
			}

		}
	}
}


void checkCollisionsV2(int amount_of_objects,
							int direction,
							int i,
							double dt,
							array2d<double>& own_vel,
							array2d<double>& own_pos,
							array2d<double>& own_size,
							array2d<double>& pos,
							array2d<double>& vel,
							array2d<double>& size,
							array1d<double>& mass,
							double posx,
							double posy,
							double hw,
							double hh,
							double bounciness,
							double linear_damping,
							bool dynamic_on_static,
							bool static_on_dynamic,
							bool same_type,
							bool check_touching) {
	double cposx,cposy;
	for (int j = 0; j < amount_of_objects; j++) {
		if ((i != j && same_type == true) || same_type == false) {
			if (check_touching == false) {
				// this is where the colliding object will be next dt
				cposx = pos(0,j) + dt*vel(0,j)*(1.0-linear_damping);
				cposy = pos(1,j) + dt*vel(0,j)*(1.0-linear_damping);
				if (abs(cposx-posx) < (hw + 0.5*size(0,j)) && abs(cposy-posy) < (hh + 0.5*size(1,j))) { // if colliding at all
					collide(own_vel,own_pos,own_size,pos,vel,size,mass,i,j,direction,bounciness,dynamic_on_static,static_on_dynamic, check_touching);
					//printf("V2 not check touching %i \n",direction);
				}
			}
			else {
				if (abs(posx-pos(0,j)) < (hw + 0.5*size(0,j)) && abs(posy-pos(1,j)) < (hh + 0.5*size(1,j))) { // if colliding at all
					collide(own_vel,own_pos,own_size,pos,vel,size,mass,i,j,direction,bounciness,dynamic_on_static,static_on_dynamic, check_touching);
					//printf("V2  check touching %i \n",direction);
				}

			}
		}
	}
}

void checkSpecialCollisions(int amount_of_objects,
							array2d<double>& pos,
							array2d<double>& size,
							array1d<int>& hit,
							double posx,
							double posy,
							double hw,
							double hh,
							int index
							) {

	for (int j = 0; j < amount_of_objects; j++) {
		if (abs(posx-pos(0,j)) < (hw + 0.5*size(0,j)) && abs(posy-pos(1,j)) < (hh + 0.5*size(1,j))) { // if colliding at all
			hit(j) = index;
		}
	}
}

extern "C" {
void collision_detection(int amount_of_dynamic_objects,
							int amount_of_static_objects,
							int amount_of_special_objects,
							double* dynamic_positions,
							double* dynamic_velocities,
							double* dynamic_sizes,
							double* static_positions,
							double* static_velocities,
							double* static_sizes,
							double* special_positions,
							double* special_sizes,
							int* special_hit,
							double bounciness,
							double linear_damping,
							double dt,
							int substeps
							) {
		int dimensions = 2;

		double effective_dt = dt/substeps;

		array2d<double> dpos	(dimensions,amount_of_dynamic_objects,dynamic_positions);
		array2d<double> dvel	(dimensions,amount_of_dynamic_objects,dynamic_velocities);
		array2d<double> dsize	(dimensions,amount_of_dynamic_objects,dynamic_sizes);
		array1d<double> dmass	(amount_of_dynamic_objects);

		array2d<double> spos	(dimensions,amount_of_static_objects,static_positions);
		array2d<double> svel	(dimensions,amount_of_static_objects,static_velocities);
		array2d<double> ssize	(dimensions,amount_of_static_objects,static_sizes);
		array1d<double> smass	(amount_of_static_objects); smass.setTo(1);

		array2d<double> sp_pos	(dimensions,amount_of_special_objects,special_positions);
		array2d<double> sp_size	(dimensions,amount_of_special_objects,special_sizes);
		array1d<int> 	sp_hit	(amount_of_special_objects,special_hit);

		for (int i = 0; i < amount_of_dynamic_objects; i++)
			dmass(i) = dsize(0,i)*dsize(1,i);


		double posx,posy,hw,hh;

		for (int j = 0; j < substeps; j++) {
			// static objects intersecting with dynamic objects (only for moving static objects)
			for (int i = 0; i < amount_of_static_objects; i++) {
				if (svel(0,i) != 0 || svel(1,i) != 0) {
					hw = 0.5*ssize(0,i);
					hh = 0.5*ssize(1,i);
					posx = spos(0,i) + effective_dt*svel(0,i)*(1.0-linear_damping);
					posy = spos(1,i);

					// check X direction
					checkCollisionsV2(amount_of_dynamic_objects,0, i, effective_dt, svel, spos, ssize, dpos, dvel, dsize, dmass, posx, posy, hw, hh, bounciness, linear_damping, false,true,false,false);

					// check Y direction
					posy = spos(1,i) + effective_dt*svel(1,i)*(1.0-linear_damping);
					checkCollisionsV2(amount_of_dynamic_objects,1, i, effective_dt, svel, spos, ssize, dpos, dvel, dsize, dmass, posx, posy, hw, hh, bounciness, linear_damping, false,true,false,false);

					spos(0,i) = posx;
					spos(1,i) = posy;
				}
			}

			for (int i = 0; i < amount_of_dynamic_objects; i++) {
				hw = 0.5*dsize(0,i);
				hh = 0.5*dsize(1,i);

				// is there an active intersection?
				posx = dpos(0,i);
				posy = dpos(1,i);
				// dynamic collisions
				checkCollisionsV2(amount_of_dynamic_objects,0,i, effective_dt, dvel, dpos, dsize, dpos, dvel, dsize, dmass, posx, posy, hw, hh, bounciness, linear_damping, true,false,true,true);
				// static collisions
				checkCollisionsV2(amount_of_static_objects,0, i, effective_dt, dvel, dpos, dsize, spos, svel, ssize, smass, posx, posy, hw, hh, bounciness, linear_damping, false,false,false,true);



				// try a step in the x direction
				posx = dpos(0,i) + effective_dt*dvel(0,i)*(1.0-linear_damping);
				posy = dpos(1,i);
				// dynamic collisions
				checkCollisionsV2(amount_of_dynamic_objects,0,i, effective_dt, dvel, dpos, dsize, dpos, dvel, dsize, dmass, posx, posy, hw, hh, bounciness, linear_damping, true,false,true,false);
				// static collisions
				checkCollisionsV2(amount_of_static_objects,0,	i, effective_dt, dvel, dpos, dsize, spos, svel, ssize, smass, posx, posy, hw, hh, bounciness, linear_damping, false,false,false,false);
				// move a small step in the x direction
				dpos(0,i) = dpos(0,i) + effective_dt*dvel(0,i)*(1.0-linear_damping);


				// try a step in the y direction
				posx = dpos(0,i);
				posy = dpos(1,i) + effective_dt*dvel(1,i)*(1.0-linear_damping);

				// dynamic collisions
				checkCollisionsV2(amount_of_dynamic_objects,1,i, effective_dt, dvel, dpos, dsize, dpos, dvel, dsize, dmass, posx, posy, hw, hh, bounciness, linear_damping, true,false,true,false);
				// static collisions
				checkCollisionsV2(amount_of_static_objects,1,	i, effective_dt, dvel, dpos, dsize, spos, svel, ssize, smass, posx, posy, hw, hh, bounciness, linear_damping, false,false,false,false);
				// move a small step in the y direction
				dpos(1,i) = dpos(1,i) + effective_dt*dvel(1,i)*(1.0-linear_damping);


				// finally we check if a special object has been hit
				checkSpecialCollisions(amount_of_special_objects,
										sp_pos,
										sp_size,
										sp_hit,
										posx,
										posy,
										hw,
										hh,
										i
										);
			}
		}
		for (int i = 0; i < amount_of_static_objects; i++) {
			svel(0,i) = 0.0;
			svel(1,i) = 0.0;
		}
	}
}
