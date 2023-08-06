#-*-encoding:utf-8-*
"""
作者：菌尘
功能：将秒转换为时、分、秒格式
版本: V001
"""
class s_to_hms:
    """将秒转为时分秒的类"""
    @staticmethod
    def S_HMS(t:float):
        """
        秒转时分秒函数 \n
        举例: \n
            t=23.010 \n
            t1=s_to_hms.S_HMS(t_in) \n
            print(t1) \n
            
        result: 00:00:23.010
        """
        if t < 60:
            t_h='00'
            t_m='00'
            t_s=str(t)
        elif t >= 60 and t < 3600:
            t_h='00'
            t_m=str(int(t / 60))
            t_s=str(t % 60)
        elif t>=3600:
            t_h=str(int(t / 3600))
            t_m=str(t-t_h*3600) / 60
            t_s=str(t % 60)
            
        t_out=(':').join([t_h,t_m,t_s])
        return t_out