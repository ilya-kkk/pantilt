// Orthographic z-buffer renderer of actual CAD triangles; no OpenGL required.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <vector>
#include <array>
#include <iostream>
struct V { double x,y,z;V operator-(V b)const{return {x-b.x,y-b.y,z-b.z};} };
double dot(V a,V b){return a.x*b.x+a.y*b.y+a.z*b.z;}
V cross(V a,V b){return {a.y*b.z-a.z*b.y,a.z*b.x-a.x*b.z,a.x*b.y-a.y*b.x};}
V norm(V a){double d=sqrt(dot(a,a));return {a.x/d,a.y/d,a.z/d};}
struct T { float v[12]; };
int main(int argc,char**argv){
    if(argc!=7)return 1;
    std::ifstream f(argv[1],std::ios::binary);uint32_t n;f.read((char*)&n,4);std::vector<T> ts(n);f.read((char*)ts.data(),n*sizeof(T));
    int W=std::stoi(argv[5]),H=std::stoi(argv[6]);double az=std::stod(argv[3])*M_PI/180,el=std::stod(argv[4])*M_PI/180;
    V eye={cos(el)*cos(az),cos(el)*sin(az),sin(el)},right={-sin(az),cos(az),0},up=cross(eye,right),light=norm({-.45,-.7,1.3});
    double xmin=1e9,xmax=-1e9,ymin=1e9,ymax=-1e9;
    for(auto&t:ts)for(int j=0;j<3;j++){V v={t.v[j*3],t.v[j*3+1],t.v[j*3+2]};double x=dot(v,right),y=dot(v,up);xmin=std::min(xmin,x);xmax=std::max(xmax,x);ymin=std::min(ymin,y);ymax=std::max(ymax,y);}
    double scale=std::min(.86*W/(xmax-xmin),.83*H/(ymax-ymin)),cx=(xmin+xmax)/2,cy=(ymin+ymax)/2;
    std::vector<double> depth(W*H,-1e30);std::vector<unsigned char> rgb(W*H*3,248);
    for(auto&t:ts){
        V v[3];double x[3],y[3],z[3];for(int j=0;j<3;j++){v[j]={t.v[j*3],t.v[j*3+1],t.v[j*3+2]};x[j]=W*.5+(dot(v[j],right)-cx)*scale;y[j]=H*.53-(dot(v[j],up)-cy)*scale;z[j]=dot(v[j],eye);}
        V nv=cross(v[1]-v[0],v[2]-v[0]);if(dot(nv,nv)<1e-20)continue;nv=norm(nv);if(dot(nv,eye)<0)nv={-nv.x,-nv.y,-nv.z};
        double shade=.38+.53*std::max(0.,dot(nv,light))+.09*std::max(0.,dot(nv,eye));
        double den=(y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2]);if(fabs(den)<1e-10)continue;
        int x0=std::max(0,(int)floor(std::min({x[0],x[1],x[2]}))),x1=std::min(W-1,(int)ceil(std::max({x[0],x[1],x[2]})));
        int y0=std::max(0,(int)floor(std::min({y[0],y[1],y[2]}))),y1=std::min(H-1,(int)ceil(std::max({y[0],y[1],y[2]})));
        for(int yy=y0;yy<=y1;yy++)for(int xx=x0;xx<=x1;xx++){
            double u=((y[1]-y[2])*(xx+.5-x[2])+(x[2]-x[1])*(yy+.5-y[2]))/den;
            double b=((y[2]-y[0])*(xx+.5-x[2])+(x[0]-x[2])*(yy+.5-y[2]))/den,c=1-u-b;
            if(u<0||b<0||c<0)continue;double zz=u*z[0]+b*z[1]+c*z[2];int i=yy*W+xx;
            if(zz<=depth[i])continue;depth[i]=zz;for(int k=0;k<3;k++)rgb[i*3+k]=(unsigned char)std::clamp(255*(t.v[9+k]*shade+.015),0.,255.);
        }
    }
    auto out=rgb;
    for(int y=3;y<H-3;y++)for(int x=3;x<W-3;x++){int i=y*W+x;if(depth[i]<-1e20)continue;double factor=1;
        for(auto p:std::vector<std::array<int,2>>{{-2,0},{2,0},{0,-2},{0,2}}){double d=depth[(y+p[1])*W+x+p[0]]-depth[i];if(d>.6&&d<18)factor-=.035;}
        for(int k=0;k<3;k++)out[i*3+k]=(unsigned char)(rgb[i*3+k]*factor);
    }
    std::ofstream o(argv[2],std::ios::binary);o<<"P6\n"<<W<<" "<<H<<"\n255\n";o.write((char*)out.data(),out.size());
}
