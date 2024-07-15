#include "phylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


//Function to makle new still ball
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{
    phylib_object *newStillBall = malloc(sizeof(phylib_object));

    if (newStillBall == NULL)
    {
        return NULL;
    }

    newStillBall->type = PHYLIB_STILL_BALL;

    newStillBall->obj.still_ball.number = number;
    newStillBall->obj.still_ball.pos = *pos;

    return newStillBall;

}


//Function to make new rolling ball
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos,phylib_coord *vel, phylib_coord *acc)
{
    phylib_object * newRollingBall = malloc(sizeof(phylib_object));

    if(newRollingBall == NULL)
    {
        return NULL;
    }

    newRollingBall->type = PHYLIB_ROLLING_BALL;

    newRollingBall->obj.rolling_ball.number = number;
    newRollingBall->obj.rolling_ball.pos = *pos;
    newRollingBall->obj.rolling_ball.vel = *vel;
    newRollingBall->obj.rolling_ball.acc = *acc;


    return newRollingBall;

}


//Function to make new hole
phylib_object *phylib_new_hole(phylib_coord *pos)
{
    phylib_object *newHoleObject = malloc(sizeof(phylib_object));

    if(newHoleObject == NULL)
    {
        return NULL;
    }

    newHoleObject->type = PHYLIB_HOLE;

    newHoleObject->obj.hole.pos = *pos;

    return newHoleObject;

}


//Function to make new hcushion
phylib_object *phylib_new_hcushion(double y)
{
    phylib_object *newhCushionObject = malloc(sizeof(phylib_object));

    if(newhCushionObject == NULL)
    {
        return NULL;
    }

    newhCushionObject->type = PHYLIB_HCUSHION;

    newhCushionObject->obj.hcushion.y = y;

    return newhCushionObject;

}


//Function to make new vcushion
phylib_object *phylib_new_vcushion(double x)
{
    phylib_object *newvCushionObject = malloc(sizeof(phylib_object));

    if(newvCushionObject == NULL)
    {
        return NULL;
    }

    newvCushionObject->type = PHYLIB_VCUSHION;

    newvCushionObject->obj.vcushion.x = x;

    return newvCushionObject;
}

//Function to make new table
phylib_table *phylib_new_table(void)
{
    phylib_table *newTableStructure = malloc(sizeof(phylib_table));

    if(newTableStructure == NULL)
    {
        return NULL;
    }

    //Assign values to the table
    newTableStructure->time = 0.0;
    newTableStructure->object[0] = phylib_new_hcushion(0.0);
    newTableStructure->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTableStructure->object[2] = phylib_new_vcushion(0.0);
    newTableStructure->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    phylib_coord hole1 = {0.0, 0.0};
    newTableStructure->object[4] = phylib_new_hole(&hole1);

    phylib_coord hole2 = {0.0, PHYLIB_TABLE_WIDTH};
    newTableStructure->object[5] = phylib_new_hole(&hole2);

    phylib_coord hole3 = {0.0, PHYLIB_TABLE_LENGTH};
    newTableStructure->object[6] = phylib_new_hole(&hole3);

    phylib_coord hole4 = {PHYLIB_TABLE_WIDTH, 0.0};
    newTableStructure->object[7] = phylib_new_hole(&hole4);


    phylib_coord hole5 = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH};
    newTableStructure->object[8] = phylib_new_hole(&hole5);


    phylib_coord hole6 = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
    newTableStructure->object[9] = phylib_new_hole(&hole6);

    //Make rest of table NULL
    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {
        newTableStructure->object[i] = NULL;
    }

    return newTableStructure;

}




void phylib_copy_object( phylib_object **dest, phylib_object **src )
{
    if(*src == NULL)
    {
        *dest = NULL;
    }
    
    *dest = malloc(sizeof(phylib_object));


    if(*dest != NULL)
    {
        memcpy(*dest, *src, sizeof(phylib_object));
    }
    else
    {
        *dest = NULL;
    }

}




phylib_table *phylib_copy_table( phylib_table *table )
{

    if(table == NULL)
    {
        return NULL;
    }

    phylib_table *newTable = malloc(sizeof(phylib_table));
    
    if (newTable == NULL)
    {
        return NULL;
    }

    newTable->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            phylib_copy_object(&newTable->object[i], &table->object[i]);
        } 
        else 
        {
            newTable->object[i] = NULL;
        }
    }

    return newTable;

}



void phylib_add_object( phylib_table *table, phylib_object *object )
{

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if(table->object[i] == NULL)
        {
            table->object[i] = object;
            break;
        }
    }
}


void phylib_free_table( phylib_table *table )
{
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if(table->object[i] != NULL)
        {
            free(table->object[i]);
        }
    }

    free(table);
}



phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{

    phylib_coord diff;

    diff.x= c1.x - c2.x;
    diff.y = c1.y - c2.y;

    return diff;
}


double phylib_length(phylib_coord c)
{
    double length = (c.x * c.x) + (c.y * c.y);
    length = sqrt(length);

    return length;
}



double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    double dotProd = (a.x * b.x) + (a.y * b.y);

    return dotProd;

}


double phylib_distance( phylib_object *obj1, phylib_object *obj2 )
{
    
    //obj1 must be a rolling ball
    if(obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }


    phylib_coord rollingBallCenter = obj1->obj.rolling_ball.pos;

    phylib_coord subtract;


    //Calculate distance between 2 balls
    if(obj2->type == PHYLIB_STILL_BALL || obj2->type == PHYLIB_ROLLING_BALL)
    {

        if(obj2->type == PHYLIB_STILL_BALL)
        {
            subtract = phylib_sub(rollingBallCenter, obj2->obj.still_ball.pos); // Center of ball 1 - center of ball 2
        }
        else
        {
            subtract = phylib_sub(rollingBallCenter, obj2->obj.rolling_ball.pos); //Center of ball 1 - center of ball 2
        }

        return phylib_length(subtract) - PHYLIB_BALL_DIAMETER; 

    }

    if(obj2->type == PHYLIB_HOLE)
    {
        subtract = phylib_sub(rollingBallCenter, obj2->obj.hole.pos);
        
        return phylib_length(subtract) - PHYLIB_HOLE_RADIUS;
    }

    if(obj2->type == PHYLIB_HCUSHION)
    {
        return fabs(rollingBallCenter.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
    }

    if(obj2->type == PHYLIB_VCUSHION)
    {
        return fabs(rollingBallCenter.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
    }

    else
    {
        return -1.0;
    }


}



void phylib_roll( phylib_object *new, phylib_object *old, double time )
{


    if(new->type == PHYLIB_ROLLING_BALL || old->type == PHYLIB_ROLLING_BALL)
    {
        // x position
        new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * (time * time));

        //y position
        new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * (time * time));


        // x velocity
        new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);

        // y velocity
        new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);


        // Change x velocity to 0 if sign changes
        if(new->obj.rolling_ball.vel.x >= 0 && old->obj.rolling_ball.vel.x <= 0)
        {
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }
        if(new->obj.rolling_ball.vel.x <= 0 && old->obj.rolling_ball.vel.x >= 0)
        {
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }



        // Change y velocity to 0 if sign changes
        if(new->obj.rolling_ball.vel.y >= 0 && old->obj.rolling_ball.vel.y <= 0)
        {
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }
        if(new->obj.rolling_ball.vel.y <= 0 && old->obj.rolling_ball.vel.y >= 0)
        {
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }

    }

}


unsigned char phylib_stopped( phylib_object *object )
{

    //If absolute velocity is less than epsilon than rolling ball is converted to still ball
    if(fabs(object->obj.rolling_ball.vel.x) < PHYLIB_VEL_EPSILON && fabs(object->obj.rolling_ball.vel.y) < PHYLIB_VEL_EPSILON)
    {
        *object = *phylib_new_still_ball(object->obj.rolling_ball.number, &object->obj.rolling_ball.pos);
        return 1;
    }

    return 0;   

}


//obj a is assumed to be a rolling ball
void phylib_bounce( phylib_object **a, phylib_object **b )
{

    //Velocities are negated to account for the ball going in the opposite direction after the bounce
    if((*b)->type == PHYLIB_HCUSHION)
    {
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
    }

    //Velocities are negated to account for the ball going in the opposite direction after the bounce
    if((*b)->type == PHYLIB_VCUSHION)
    {
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
    }

    //Ball is free'd when it goes in a whole
    if((*b)->type == PHYLIB_HOLE)
    {
        if(*a != NULL)
        {
            free(*a);
            *a = NULL;
        }

    }

    //Initilaize values to 0 to make a new rolling ball
    phylib_coord stillVel;
    stillVel.x = 0;
    stillVel.y = 0;
    phylib_coord stillAcc;
    stillAcc.x = 0;
    stillAcc.y = 0;

    //Convert still ball to rolling ball
    if((*b)->type == PHYLIB_STILL_BALL)
    {

        phylib_object *oldB; 
        oldB = *b;

        (*b) = phylib_new_rolling_ball((*b)->obj.still_ball.number,&(*b)->obj.still_ball.pos, &stillVel, &stillAcc);

        free(oldB);

    }


    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    double v_rel_n;

    if((*b)->type == PHYLIB_ROLLING_BALL)
    {
        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);

        v_rel_n = phylib_dot_product(v_rel, n);

        //Update ball a velocities
        (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
        (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

        //Update ball b velocities
        (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x);
        (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

        double aSpeed = phylib_length((*a)->obj.rolling_ball.vel);
        double bSpeed = phylib_length((*b)->obj.rolling_ball.vel);


        if(aSpeed > PHYLIB_VEL_EPSILON)
        {
            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / aSpeed * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / aSpeed * PHYLIB_DRAG;

        }

        if(bSpeed > PHYLIB_VEL_EPSILON)
        {
            (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / bSpeed * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / bSpeed * PHYLIB_DRAG;

        }

    }


}


//Count number of rolling balls on the table
unsigned char phylib_rolling( phylib_table *t )
{

    int rollingBalls = 0;

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if(t->object[i] != NULL)
        {
            if(t->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                rollingBalls++;
            }
        }
        
    }

    return rollingBalls;
}



phylib_table *phylib_segment( phylib_table *table )
{

    int rollingBalls = phylib_rolling(table);

    if (rollingBalls == 0)
    {
        return NULL;
    }

    phylib_table *newTable = phylib_copy_table(table);

    double time = PHYLIB_SIM_RATE;

    //Loop over time
    while(time < PHYLIB_MAX_TIME)
    {

        
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            //Roll a rolling ball evreytime a rolling ball is detected and check if it stopped
            if (newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL)
            {

                phylib_roll(newTable->object[i], table->object[i], time);

                if(phylib_stopped(newTable->object[i]) == 1)
                {
                    newTable->time += time;
                    return newTable;
                }


            }

        }   



        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                {   
                    //If the distance between 2 opbject is 0 then 2 object will bounce
                    if(i != j && newTable->object[j] != NULL && phylib_distance(newTable->object[i], newTable->object[j]) < 0.0)
                    {
                        phylib_bounce(&newTable->object[i], &newTable->object[j]);
                        newTable->time += time;
                        return newTable;

                    }
                }
            }
        }

    
        time += PHYLIB_SIM_RATE; //Increment by sim rate

    }


    phylib_free_table(newTable);

    return NULL;

}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
    snprintf( string, 80, "NULL;" );
    return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
    snprintf( string, 80,
    "STILL_BALL (%d,%6.1lf,%6.1lf)",
    object->obj.still_ball.number,
    object->obj.still_ball.pos.x,
    object->obj.still_ball.pos.y );
    break;
    case PHYLIB_ROLLING_BALL:
    snprintf( string, 80,
    "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
    object->obj.rolling_ball.number,
    object->obj.rolling_ball.pos.x,
    object->obj.rolling_ball.pos.y,
    object->obj.rolling_ball.vel.x,
    object->obj.rolling_ball.vel.y,
    object->obj.rolling_ball.acc.x,
    object->obj.rolling_ball.acc.y );
    break;
    case PHYLIB_HOLE:
    snprintf( string, 80,
    "HOLE (%6.1lf,%6.1lf)",
    object->obj.hole.pos.x,
    object->obj.hole.pos.y );
    break;
    case PHYLIB_HCUSHION:
    snprintf( string, 80,
    "HCUSHION (%6.1lf)",
    object->obj.hcushion.y );
    break;
    case PHYLIB_VCUSHION:
    snprintf( string, 80,
    "VCUSHION (%6.1lf)",
    object->obj.vcushion.x );
    break;
    }
    return string;
}



