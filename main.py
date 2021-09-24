import serial
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
bot = Bot(token='***')
dp = Dispatcher(bot)


ser = serial.Serial('/dev/ttyS0', 9600)
time.sleep(2)
chat_id = "****"


async def make_image(numder):
    start = time.time()
    print("Thread [" + str(numder) + "]")
    cap = cv2.VideoCapture(numder)
    for i in range(50):
        cap.read()
    ret, frame = cap.read()
    image_name = 'image' + str(numder-1) + '.png'
    cv2.imwrite(image_name, frame)
    
    photo = open(image_name, "rb")
    await bot.send_photo(chat_id=chat_id, photo=photo)
	
    cap.release()
    end = time.time()
    print("Thread" + str(numder) + "'s speed = " + str(end - start))


def run_threads():
    thread1 = Thread(target=make_image(1))
    #thread2 = Thread(target=make_image(2))
    thread1.start()
    #thread2.start()
    thread1.join()
    #thread2.join()


async def get_data():
    ser.write(b'1')
    response1 = ser.readline().decode('UTF-8')
    print(response1)
    response2 = ser.readline().decode('UTF-8')
    print(response2)
    s1 = response1.replace("Temp: ", "")
    s1 = s1.replace("\n", "")
    s1 = s1.replace("\n", "")
    s2 = response2.replace("Gas %: ", "")
    s2 = "temp_data:" + s2
    await bot.send_message(chat_id=chat_id, photo=photo)
    


def main():
    try:
        while 1:
            response = ser.readline()
            print(response)
            if response == b'make photo\r\n':
                get_data()
                run_threads()
    except KeyboardInterrupt:
        ser.close()

if __name__ == '__main__':
    main()

