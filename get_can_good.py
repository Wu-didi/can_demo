import can

def read_can_messages():
    # 创建一个CAN总线接口实例，使用socketcan和can0接口
    bus = can.interface.Bus(channel='can0', bustype='socketcan')

    try:
        print("开始监听can0接口的CAN消息...")
        while True:
            # 读取一条CAN消息
            message = bus.recv()
            
            if message is not None:
                # 仅处理 arbitration_id 为 0x504 的消息
                if message.arbitration_id == 0x504:
                    # 直接获取数据字节
                    can_data = message.data
                    print(can_data)
                    print(can_data[0])
                    # 解析前4个字节为纬度
                    INS_Latitude = (can_data[0] << 24) | (can_data[1] << 16) | (can_data[2] << 8) | can_data[3]
                    INS_Latitude = INS_Latitude*0.0000001-180                   # 解析后4个字节为经度
                    INS_Longitude = (can_data[4] << 24) | (can_data[5] << 16) | (can_data[6] << 8) | can_data[7]
                    INS_Longitude= INS_Longitude*0.0000001-180 
                    # 打印经纬度信息
                    print(f"接收到消息 ID=0x{message.arbitration_id:X}, 纬度: {INS_Latitude}, 经度: {INS_Longitude}")
                    
    except KeyboardInterrupt:
        print("\n停止监听CAN消息")

if __name__ == "__main__":
    read_can_messages()
