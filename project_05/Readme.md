# Module5:计算机体系结构
## 项目：Memory实现
Memory的实现总体来讲还是比较简单的，看着书上的图来就可以。根据```Memory.hdl```文件前面的注释提示，地址address<0x4000的为RAM16K的部分，地址为0x4000-0x5FFF的为Screen的部分，地址为0x6000的为Keyboard的部分。

所以可以通过输入地址的第14和13位，即address[14]和address[13]来判断：
* 如果address[14]=0，那么一定为RAM输出
* 如果address[14]=1，且address[13]=0，一定为Screen输出
* 如果address[14]=1，且address[13]=1，一定为keyboard输出

搞清楚这个之后后面就比较容易了，把对应的控制地址和判断完的load输入到RAM、screen中，最后通过两个Mux16进行输出的判断就可以了


