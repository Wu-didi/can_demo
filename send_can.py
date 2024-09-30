import time
import can

def send_can_messages(angle, mod, angle_speed, Enable):
    # 创建一个CAN总线接口实例，使用socketcan和can0接口
    bus = can.interface.Bus(channel='can1', bustype='socketcan')

    try:
        while True:
            # 验证输入参数类型和范围
            if not isinstance(angle, (int, float)):
                print(f"Invalid angle value: {angle}")
                return
            
            # 数据缩放和转换
            data1 = int((angle - (-738)) / 0.1)  # 确保data1根据传入angle正确计算
            data1_high = (data1 >> 8) & 0xFF    # data1的高8位
            data1_low = data1 & 0xFF            # data1的低8位

            data2 = int(mod) & 0x03           # data2缩放到2位范围，0-3
            data3 = int(angle_speed / 10) & 0xFF      # data3缩放到8位范围，0-255
            data4 = int(Enable) & 0x01           # data4缩放到1位范围，0或1
            
            # 打印调试信息，检查缩放和转换过程
            # print(f"Original angle: {angle}, Scaled data1: {data1}, data1_high: {data1_high}, data1_low: {data1_low}")
            # print(f"Original data2: {data2}, data3: {data3}, data4: {data4}")

            # 构建发送数据，确保8字节长度
            data = [data1_high, data1_low, data2, data3, data4, 0, 0, 0]
            # print(f"Constructed data frame: {data}")

            # 创建CAN消息，ID设置为0x0AE
            msg = can.Message(arbitration_id=0x0AE, data=data, is_extended_id=False)

            # 发送CAN消息
            bus.send(msg)
            print(f"发送消息: ID={msg.arbitration_id}, 数据={data}")

            # 限制发送频率
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n停止发送消息")
    finally:
        bus.shutdown()

if __name__ == "__main__":
    angle = 0   # 输入角度 单位deg 
    mode = 1     #  模式：可选0:待机；1:手动； 2:自动驾驶； 3:手动接入恢复
    angle_spd = 100  # 8个bit  角速度，单位:deg/s   
    Enable = 1   # 1位          0:disable; 1:Enable
    send_can_messages(angle, mode, angle_spd, Enable)
