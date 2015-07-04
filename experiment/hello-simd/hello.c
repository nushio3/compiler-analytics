#include <stdio.h>

int main () {
  double a[4],b[4],c[4];

  for (int i=0;i<4;++i) {
    double x=1.0+i;
    a[i]=x; b[i]=1/x/x; c[i]=x*x*x;
  }

  asm volatile("#central loop begin");
  for (int t=0;t<1<<30;++t) {
    for (int i=0;i<4;++i) {
      a[i]=a[i]*b[i]+c[i];
    }
  }
  asm volatile("#central loop end");

  for (int i=0;i<4;++i) {
    printf("%lf ",a[i]);
  }
  
}
