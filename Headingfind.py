# Compute heading class Vector3D


class Vector3D


    mArr[]

    def __init__(self,double x, double y, double z):

        self.mArr[0] = x;
        self.mArr[1] = y;
        self.mArr[2] = z;
    

    def dot(self, Vector3D rhs)    
        double out = 0;
        for (int i = 0; i < NUM_DIMENSIONS; ++i)
            out = out + mArr[i] * rhs.mArr[i];
        return out;

    def times ( x):
        Vector3D out;
        for (int i = 0; i < NUM_DIMENSIONS; ++i)
            out.mArr[i] = mArr[i] * x;
        return out;
    

    def sub (  x):
    
        Vector3D out;
        for (int i = 0; i < NUM_DIMENSIONS; ++i)
        
            out.mArr[i] = mArr[i] - x.mArr[i];
        
        return out;
    
    
    def getX(self):
        return mArr[0];
    def getY(self):
        return mArr[1];
    def getZ(self):
        return mArr[2];


    NUM_DIMENSIONS = 3;
    double mArr[NUM_DIMENSIONS];


Vector3D operator* (double x, const Vector3D& y)
{
    return (y * x);
}
