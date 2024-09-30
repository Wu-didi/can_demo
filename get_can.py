import can
import json
import os
import math
def read_can_messages():
    # 创建一个CAN总线接口实例，使用socketcan和can0接口
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    
    # 定义JSON文件的名称
    json_file = 'latitude_longitude.json'
    
    # 如果文件不存在，则创建一个空列表以存储数据
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump([], f)

    try:
        print("开始监听can0接口的CAN消息...")
        while True:
            # 读取一条CAN消息
            message = bus.recv()
            new_entry = []
            if message is not None:
                # 仅处理 arbitration_id 为 0x504 的消息
                if message.arbitration_id == 0x504:
                    # 直接获取数据字节
                    can_data = message.data
                    
                    # 解析前4个字节为纬度
                    INS_Latitude = (can_data[0] << 24) | (can_data[1] << 16) | (can_data[2] << 8) | can_data[3]
                    INS_Latitude = INS_Latitude * 0.0000001 - 180
                   
                    # 解析后4个字节为经度
                    INS_Longitude = (can_data[4] << 24) | (can_data[5] << 16) | (can_data[6] << 8) | can_data[7]
                    INS_Longitude = INS_Longitude * 0.0000001 - 180 
                    
                    # 打印经纬度信息
                    # print(f"接收到消息 ID=0x{message.arbitration_id:X}, 纬度: {INS_Latitude}, 经度: {INS_Longitude}")
                    
                    # # 将经纬度信息以 [x, y] 形式存储到JSON文件中
                    # new_entry = [INS_Latitude, INS_Longitude]
                    #                 # 读取现有数据
                    # with open(json_file, 'r') as f:
                    #     data = json.load(f)
                        
                    # # 添加新的经纬度数据
                    # data.append(new_entry)
                    
                    # # 将数据写回到JSON文件
                    # with open(json_file, 'w') as f:
                    #     json.dump(data, f, indent=4)
                        
                if message.arbitration_id == 0x505:
                    speed_data = message.data
                    
                    # 北向速度
                    INS_NorthSpd =  (speed_data[0] << 8) | speed_data[1]
                    INS_NorthSpd =   INS_NorthSpd*0.0030517-100    # m/s
                    INS_NorthSpd *= 3.6
                    # 东向速度
                    INS_EastSpd =  (speed_data[2] << 8) | speed_data[3]
                    INS_EastSpd =   INS_EastSpd*0.0030517-100    # m/s
                    INS_EastSpd *= 3.6
                    # 地向速度
                    INS_ToGroundSpd =  (speed_data[4] << 8) | speed_data[5]
                    INS_ToGroundSpd =   INS_ToGroundSpd*0.0030517-100    # m/s
                    INS_ToGroundSpd *= 3.6
                    
                    speed =  math.sqrt(INS_EastSpd**2+INS_NorthSpd**2+INS_ToGroundSpd**2)
                    
                    # 计算航向角（单位：度）
                    angle = math.degrees(math.atan2(INS_NorthSpd, INS_EastSpd))
                    print("====================================",angle)
                    # print("===============speed=============:",speed)
                    # print(f"INS_NorthSpd: {INS_NorthSpd*3.6}, INS_EastSpd: {INS_EastSpd*3.6}, INS_ToGroundSpd: {INS_ToGroundSpd*3.6}")
                if message.arbitration_id == 0x500:
                    acc_data = message.data
                    # 北向速度
                    ACC_X =  (acc_data[0] << 8) | acc_data[1]
                    ACC_X =   (ACC_X*0.0001220703125-4)*9.8   # g
                    # print("=============================ACC_X:", ACC_X)
                    

                    

                    
    except KeyboardInterrupt:
        print("\n停止监听CAN消息")

if __name__ == "__main__":
    read_can_messages()
