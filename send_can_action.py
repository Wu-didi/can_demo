import keyboard
import time
import can

def send_can_messages(angle, angle_speed, enable=1):
    # 创建一个CAN总线接口实例，使用socketcan和can1接口
    bus = can.interface.Bus(channel='can1', bustype='socketcan')

    auto_drive_allowed = False     # 标志位，用于控制是否允许自动驾驶
    manual_triggered = False  # 标志位，表示是否按过's'键

    try:
        while True:
            # 接收CAN消息
            message = bus.recv(timeout=0.1)
            if message is not None and message.arbitration_id == 0x777:
                # 解析数据，假设Auto drive allow位于第一个字节的第0位
                allow_value = message.data[0] & 0x01
                auto_drive_allowed = (allow_value == 1)
                print("VCU允许开启自动驾驶模式" if auto_drive_allowed else "VCU不允许开启自动驾驶模式")

            # 监听键盘输入
            if keyboard.is_pressed('s'):  # 检测按键's'
                manual_triggered = True  # 标记已经按下's'键
                print("收到键盘输入's'，手动请求自动驾驶模式")

            elif keyboard.is_pressed('esc'):  # 检测Esc键
                print("收到Esc键，退出程序")
                auto_drive_allowed = False  # 确保退出时设置auto_drive_allowed为False


            # 只有当VCU允许并且手动触发过才允许进入自动驾驶模式
            if auto_drive_allowed and manual_triggered:
                mode = 1  # 自动驾驶模式
            else:
                mode = 2  # 手动模式

            # 数据缩放和转换
            data1 = int((angle - (-738)) / 0.1)  # 将angle映射到范围
            data1_high = (data1 >> 8) & 0xFF    # data1的高8位
            data1_low = data1 & 0xFF            # data1的低8位

            data2 = int(mode) & 0x03            # 确保mode在0-3范围内
            data3 = int(angle_speed / 10) & 0xFF  # 确保angle_speed在0-255范围内
            data4 = int(enable) & 0x01          # enable保持不变

            # 构建发送数据，确保8字节长度
            data = [data1_high, data1_low, data2, data3, data4, 0, 0, 0]

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
        print("CAN总线已关闭")

if __name__ == "__main__":
    angle = 0    # 输入角度 单位deg
    angle_spd = 100  # 角速度，单位:deg/s
    send_can_messages(angle, angle_spd)
