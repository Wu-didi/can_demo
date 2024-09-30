import time
import can

def send_can_messages():
    # 创建一个CAN总线接口实例，使用socketcan和can0接口
    bus = can.interface.Bus(channel='can1', bustype='socketcan')

    try:
        while True:
            # 将数据90和2转换为字节格式
            data = [90, 2]
            
            # 创建CAN消息，ID设置为0x123（可以根据需求修改）
            msg = can.Message(arbitration_id=0x666, data=data, is_extended_id=False)
            
            # 发送CAN消息
            bus.send(msg)
            print(f"发送消息: ID={msg.arbitration_id}, 数据={data}")

            # 等待0.5秒
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n停止发送消息")

if __name__ == "__main__":
    send_can_messages()

